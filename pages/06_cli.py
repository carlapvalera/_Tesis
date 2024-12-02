import streamlit as st
import subprocess

from lib.utils import Chatbot

bot = Chatbot("mistral-small-latest")


st.set_page_config(page_title="The Hackerbot", page_icon="🖥️", layout="wide")
st.sidebar.page_link("demo.py", label="Go back to home", icon="🏠")

bot_input = st.container()
left, right = st.columns([2, 1])

terminal = left.container()
bot_output = right.container()


@bot.tool(code="A one-liner bash code to run")
def run_bash(code: str):
    """
    Use this method to run a one-line bash code to answer the user query.

    Returns the output of the bash code.

    Examples:

    1) List all my files
       code: "ls -lh"

    2) What is my git status
       code: "git status"

    3) Compress the folder
       code: "zip -f data.zip ."
    """

    with terminal:
        st.code("$ " + code, language="bash")

        if code.startswith("sudo"):
            st.error("Attempted sudo call has been restricted.")
            return "You cannot run sudo here."

        with st.spinner("Running code"):
            if not st.secrets.allow_code_execution:
                st.error("Code execution is disallowed in this instance. Run it locally.")
                return "You cannot run codes in this instance for security reasons."

            response = subprocess.run(
                code,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                shell=True,
            ).stdout

        if response:
            st.code(response)
        else:
            st.warning("No output.")

    if len(response) > 1024:
        return "Response too long."

    return response or "No output"


query = bot_input.chat_input("Ask anything about your system")

if query:
    with bot_output.chat_message("user"):
        st.write(query)

    with bot_output.chat_message("assistant"):
        st.write(bot.submit(query, stream=False, force_tools=True))
