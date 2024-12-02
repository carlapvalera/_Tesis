import streamlit as st
from code_editor import code_editor
from lib.utils import Chatbot


st.set_page_config(page_title="The Coder", page_icon="⌨️", layout="wide")
st.sidebar.page_link("demo.py", label="Go back to home", icon="🏠")


lang = st.sidebar.selectbox(
    "Programming Language", ["python", "csharp", "cpp", "c", "java", "javascript"]
)

bot = Chatbot(
    "mistral-small-latest",
    system_prompt=f"""
    Your task is to answer questions about code,
    and generate code in the {lang} programming language.
    For every user input, you either reply with a natural language
    comment, or exclusively with a fragment of source code,
    enclosed in <code></code>.
    """,
)


EXPLAIN_CODE_PROMPT = """
Here is the current source code:

<code>
{code}
</code>

Given the previous code,
answer the following user question in natural language.

Instruction: {input}
"""


GENERATE_CODE_PROMPT = """
Here is the current source code:

<code>
{code}
</code>

Given the previous code and the following user instruction,
generate a new code that fullfils the user request.

Instruction: {input}

Reply only with the new source code, enclosed in <code></code> tags.
"""


MODIFY_CODE_PROMPT = """
Here is the current source code:

<code>
{code}
</code>

Given the previous code and the following user instruction,
generate a modified version of this code that fullfils the user request.

Instruction: {input}

Reply only with the modified source code, enclosed in <code></code> tags.
"""


@bot.tool(question="The verbatim user question")
def query(question: str):
    """
    Use this function when the user asks a question about
    the code, such as explanations, commentaries, etc.,
    that doesn't involve generating new code.

    Examples:
    - What does this method do
    - How does this function work
    - Explain this code
    """
    response = bot.submit(question, user_prompt=EXPLAIN_CODE_PROMPT, code=selected)
    st.write(response)
    return False


def generate_code(prompt, instruction, code):
    response = bot.submit(instruction, user_prompt=prompt, code=code, store=False, stream=False)

    open_format = f"<code>"
    start = response.find(open_format)
    end = response.find("</code>")
    return response[start + len(open_format) : end].strip()


@bot.tool(instruction="The user instruction")
def generate(instruction: str):
    """
    Use this function when the user asks to generate
    new code.

    Examples:
    - Add a unit test for this method
    - Generate a new method for task X
    - Continue the code
    """
    response = generate_code(GENERATE_CODE_PROMPT, instruction, code=selected)

    st.session_state.code += "\n\n" + response
    st.rerun()


@bot.tool(instruction="The user instruction")
def modify(instruction: str):
    """
    Use this function when the user asks to modify
    existing code.

    Examples:
    - Change this method to remove recursion
    - Remove all calls to function `find`
    - Add comments
    """
    response = generate_code(MODIFY_CODE_PROMPT, instruction, code=selected)

    st.session_state.code = st.session_state.code.replace(selected, response)
    st.rerun()


if "code" not in st.session_state:
    st.session_state.code = ""


editor_result = code_editor(st.session_state.code, lang, height=[20, 300])


if editor_result["id"]:
    code = editor_result["text"]
    selected = editor_result["selected"] or code
    st.session_state.code = code
else:
    code = st.session_state.code
    selected = ""


with st.sidebar.popover("Chat with Coder"):
    instruction = st.chat_input("Instruction or question")

    if instruction:
        bot.submit(instruction, stream=False, force_tools=True)