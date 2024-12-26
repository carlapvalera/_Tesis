import streamlit as st
from lib.utils import Chatbot, VectorStore
from pypdf import PdfReader

st.set_page_config(page_title="The PDF Bot", page_icon="📚")
st.sidebar.page_link("demo.py", label="Go back to home", icon="🏠")

fp = st.sidebar.file_uploader("Upload a PDF file", "pdf")

if not fp:
    st.warning("Please upload your PDF")
    st.stop()


@st.cache_data(show_spinner="Indexing PDF...")
def get_store(pdf):
    store = VectorStore()
    texts = [page.extract_text() for page in PdfReader(pdf).pages]
    store.add(texts)
    return store


store = get_store(fp)
st.sidebar.write(f"Index size: {len(store)} pages.")

USER_PROMPT = """
The following is a relevant extract of a PDF document
from which I will ask you a question.

## Extract

{extract}

## Query

Given the previous extract, answer the following query:
{input}
"""

bot = Chatbot("open-mixtral-8x7b", user_prompt=USER_PROMPT)

if st.sidebar.button("Reset conversation"):
    bot.reset()

for message in bot.history():
    with st.chat_message(message.role):
        st.write(message.content)

msg = st.chat_input()

if not msg:
    st.stop()

with st.chat_message("user"):
    st.write(msg)

extract = store.search(msg, 3)

with st.chat_message("assistant"):
    with st.expander("Context", False):
        st.write(extract)

    st.write_stream(bot.submit(msg, context=2, extract="\n\n".join(extract)))
