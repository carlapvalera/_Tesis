import streamlit as st
from lib.utils import Chatbot

st.set_page_config(page_title="The Writer", page_icon="🖋️", layout="wide")
st.sidebar.page_link("demo.py", label="Go back to home", icon="🏠")

bot = Chatbot("mistral-small-latest", user_prompt="""
The following is a user-generated text.
Please continue it using the same style and format.

{input}
""")

raw, md = st.tabs(["📝 Raw text", "👁️ Markdown preview"])

with raw:
    text = st.text_area("Text", height=300, key="text")

with md:
    st.markdown(text)

def continue_text():
    response = bot.submit(text, stream=False)
    st.session_state.text += response

st.sidebar.button("Continue text", on_click=continue_text)
