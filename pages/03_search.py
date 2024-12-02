from dataclasses import dataclass
import streamlit as st
import json
import googlesearch
import bs4
import requests

from lib.utils import VectorStore, Chatbot

st.set_page_config(page_title="The Answer Engine", page_icon="❓", layout="wide")
st.sidebar.page_link("demo.py", label="Go back to home", icon="🏠")

USER_PROMPT = """
Here is an extract of relevant context from different web pages:

---
{chunks}
---

Given the provided search context, please answer the following user query.
For every substantive claim extracted from the context, please
provide between square brackets the corresponding chunk ID number,
such as [1], [2], etc.

Query: {input}
"""

bot = Chatbot("mistral-small-latest", user_prompt=USER_PROMPT)
num_queries = st.sidebar.number_input("Number of different queries", 1, 10, 3)
num_results = st.sidebar.number_input("Top K results to crawl", 1, 10, 3)
num_chunks = st.sidebar.number_input("Number of context chunks", 1, 10, 3)
chunk_size = st.sidebar.number_input("Chunk size (tokens)", 128, 2048, 256)
retries = st.sidebar.number_input("Retries", 0, 10, 3)


with st.container():
    query = st.chat_input("Search anything...")

    if not query:
        st.stop()

    query = query.strip()
    progress = st.progress(0)


left, right = st.columns([3, 2])

with left:
    st.info(f"Query: **{query}**")


QUERY_PROMPT = """
Given the following question, provide a set of {num_queries}
of relevant Google queries that would answer the question.
For that, first think about the user query and provide your own interpretation.
Then generate the relevant queries.

Question: {question}

Answer only with a JSON object containing a list of the relevant queries,
in the following format:

{{
    "interpretation": "...",
    "queries": [ ... ] # list of relevant queries
}}
"""


@dataclass
class Response:
    interpretation: str
    queries: list


with right:
    urls = set()
    texts = []
    url_by_text = {}

    with st.status("Understanding question..."):
        queries: Response = bot.json(
            QUERY_PROMPT.format(question=query, num_queries=num_queries),
            model=Response,
            retries=retries,
        )
        st.write(queries.interpretation)
        st.write(queries.queries)

    with st.status("Searching online..."):

        for query in queries.queries:
            st.write(f"Querying Google: `{query}`")
            search_results = list(
                googlesearch.search(
                    query,
                    num_results=num_results,
                    advanced=True,
                )
            )

            for i, result in enumerate(search_results):
                urls.add(result.url)

        st.json(list(urls), expanded=False)

        for i, url in enumerate(urls):
            try:
                st.write(f"Crawling {url}")
                html = requests.get(url, timeout=3).text

                if "<!DOCTYPE html>" not in html:
                    st.write(f"Skipped {url}")
                    continue

                text = bs4.BeautifulSoup(html, "lxml").get_text()
                text = text.split()

                if len(text) < 50:
                    st.write(f"Skipped {url}")
                    continue

                for j in range(0, len(text), chunk_size):
                    chunk = " ".join(text[j : j + chunk_size])
                    texts.append(chunk)
                    url_by_text[chunk] = url
            except:
                pass

            progress.progress((i + 1) / len(urls))

    with st.status("Extracting relevant context..."):
        store = VectorStore()

        st.write("Indexing batches...")
        store.add(texts)

        chunks = [
            dict(id=i + 1, url=url_by_text[c], text=c)
            for i, c in enumerate(store.search(query, k=num_chunks))
        ]

        for c in chunks:
            st.write(c)


with left:
    st.write_stream(bot.submit(query, chunks=json.dumps(chunks, indent=2)))

    st.write("**References:**")

    for c in chunks:
        st.write(c["id"], c["url"])
