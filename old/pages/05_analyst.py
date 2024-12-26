import streamlit as st
from altair import Chart
import altair as alt
import pandas as pd
from lib.utils import Chatbot


st.set_page_config(page_title="The Data Analyst", page_icon="📊")
st.sidebar.page_link("demo.py", label="Go back to home", icon="🏠")

data = st.sidebar.file_uploader("Upload a CSV file.", type={"csv"})

if not data:
    st.warning("Please upload the CSV file.")
    st.stop()

df = pd.read_csv(data)

system_prompt = f"""
You are a data analysis chatbot. I will provide you with a
dataset and ask you questions about it.

Here is an brief excerpt of the dataset that you can use
to understand its structure and composition, but the whole
data is much longer.

{df.head().to_markdown()}

The dataset has the following columns.

{df.columns}

The dataset has {len(df)} rows.
"""

bot = Chatbot('mistral-small-latest', system_prompt=system_prompt)

@bot.tool(question="The user question")
def default(question:str):
    """Use this function when the question can be answered directly,
    without executing any code.
    """
    pass

@bot.tool(code="A pandas expression on the variable df.")
def run_code(code:str):
    """Use this function to run a pandas code on the dataset for,
    e.g., filtering, grouping, counting, etc.

    Returns the result of the operation.

    Remarks: Make sure the `code` expression uses `df` as variable name,
    and that it is a single Python expression.

    Examples:

    1) Find the maximum value of a column
       code: `df['column_name'].max()`

    2) Count the different values on some column
       code: `df.groupby('column_name').count()
    """
    with st.status("Executing pandas code."):
        st.code(code)

        try:
            result = eval(code)
            st.code(repr(result))
        except Exception as e:
            result = dict(error=repr(e))
            st.error(repr(e))

    return dict(result=repr(result))

@bot.tool(code="An altair expression to generate a chart.")
def make_chart(code:str):
    """Use this function to generate an Altair chart.

    This function already prints the chart to the user,
    you don't need to show it afterwards.

    Returns True if everything worked, and exception otherwise.

    Remarks: Make sure the `code` expression
    is a single Altair expression that starts with `alt.Chart`
    and uses `df` as the dataset.

    Examples

    1) Plot the total amount per column
       code: `alt.Chart(df).mark_bar().encode(...)`

    2) Show the distribution of some values
       code: `alt.Chart(df).mark_line().encode(...)
    """
    with st.status("Executing altair code."):
        st.code(code)

    try:
        chart: Chart = eval(code)

        if not isinstance(chart, Chart):
            raise ValueError(f"{repr(chart)} is not a chart instance.")

        st.altair_chart(chart)
        result = True
    except Exception as e:
        result = dict(error=repr(e))
        st.error(repr(e))

    return dict(result=result)

if st.sidebar.button("Reset conversation"):
    bot.reset()

has_history = False
for message in bot.history():
    has_history = True

    with st.chat_message(message.role):
        st.write(message.content)

if not has_history:
    with st.chat_message("assistant"):
        st.write(bot.submit("What is this dataset about", stream=False, store=False, force_tools=True))

msg = st.chat_input()

if not msg:
    st.stop()

with st.chat_message("user"):
    st.write(msg)

with st.chat_message("assistant"):
    st.write(bot.submit(msg, context=5, stream=False, force_tools=True))
