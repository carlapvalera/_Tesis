import streamlit as st
from itertools import cycle

st.set_page_config(
    page_title="How to Train your Chatbot", page_icon="🤖", layout="wide"
)

st.title("🤖 How to Train your Chatbot")

st.subheader(
    "A practical handbook on using LLMs to build all sorts of cool stuff", divider=True
)

left, right = st.columns([3,1])

with left:
    st.write(
    """
    Welcome to the demo application gallery for _How to Train your Chatbot_.
    Please consider supporting this project.
    As a special token of appreciation, the following link contains a coupon for a 50% discount.
    Click on any of the following links to see the corresponding demo application.
    """
    )

with right:
    st.page_link("https://store.apiad.net/l/chatbots/fiftyoff", label="Get How to Train your Chatbot - 50% off", icon="🎁")

st.write("---")

cols = iter(st.columns(5))

with next(cols):
    st.page_link("pages/01_chatbot.py", label="**The Chatbot**", icon="🤖")
    st.write("A basic chatbot, with conversation history and custom system prompt.")

with next(cols):
    st.page_link("pages/02_pdfbot.py", label="**The PDF Bot**", icon="📚")
    st.write("A bot that can answer questions from an arbitrary PDF file.")

with next(cols):
    st.page_link("pages/03_search.py", label="**The Answer Engine**", icon="❓")
    st.write("A search engine that synthetizes answers with references.")

with next(cols):
    st.page_link("pages/04_shopping.py", label="**The Salesbot**", icon="🛒")
    st.write("A sales chatbot that can search products and manage the cart.")

with next(cols):
    st.page_link("pages/05_analyst.py", label="**The Analyst**", icon="📊")
    st.write("A data analyst bot that can run pandas code and draw graphs.")

st.write("---")

cols = iter(st.columns(5))

with next(cols):
    st.page_link("pages/06_cli.py", label="**The Hackerbot**", icon="🖥️")
    st.write("A chatbot that access your terminal and works like a hacker.")

with next(cols):
    st.page_link("pages/07_writer.py", label="**The Writer**", icon="🖋️")
    st.write("A writing assistant that can create long-form content interactively.")

with next(cols):
    st.page_link("pages/08_coder.py", label="**The Coder**", icon="⌨️")
    st.write("A coding assistant that can write, modify, and explain code.")

with next(cols):
    st.page_link("pages/09_planner.py", label="**The Planner**", icon="🗓️")
    st.write("A planner bot that can create tasks and update your calendar.")

with next(cols):
    st.page_link("pages/10_feeder.py", label="**The News Reader**", icon="📰")
    st.write("An RSS feed summarizer and analyzer that helps you stay on the news.")

st.write("---")

cols = iter(st.columns(5))

with next(cols):
    st.page_link("pages/11_journal.py", label="**The Journal**", icon="📓")
    st.write("A journaling app with automatic summarization and goal tracking.")

with next(cols):
    st.page_link("pages/12_graph.py", label="**The Conceptualizer**", icon="💡")
    st.write("A knowledge extraction and consolidation engine.")

with next(cols):
    st.page_link("pages/13_research.py", label="**The Researcher**", icon="⚗️")
    st.write("A reseaching and state of the art creation tool.")

with next(cols):
    st.page_link("pages/14_dnd.py", label="**The Dungeon Master**", icon="🧙")
    st.write("A text-based history-driven role playing game with AI characters")

with next(cols):
    st.page_link("pages/15_storyteller.py", label="**The Storyteller**", icon="📖")
    st.write("A storytelling machine with smart character- and world-building.")

st.write("---")

st.write("And that's all! Feel free to "
         "[subscribe to my Substack](https://blog.apiad.net)"
         " for free to stay up to date with all updates.")