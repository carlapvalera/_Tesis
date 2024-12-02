import streamlit as st
import collections
from pydantic import BaseModel, Field
import pandas as pd

from lib.utils import VectorStore, Chatbot

st.set_page_config(page_title="The Shopping Bot", page_icon="🛒", layout="wide")
st.sidebar.page_link("demo.py", label="Go back to home", icon="🏠")


n_products = st.sidebar.number_input("Number of products", 5, 20, 10)
domain = st.sidebar.text_input("Store domain", "magical items, wands, brumsticks, and books")
tone = st.sidebar.text_input("Tone", "Harry Potter")

bot = Chatbot("mistral-small-latest")

STORE_PROMPT = """
Create an online store in the domain of {domain},
including a store name and a brief,
warm welcome message describing the store.
Use a {tone} tone.
"""

PRODUCT_PROMPT = """
Create a product for an online store in the domain of {domain}.
Including a name, a description, and a price.
Use a {tone} tone.

Here is a list of existing products:
{products}

Create something different.
"""


class Product(BaseModel):
    """Create a new product."""

    name: str = Field(description="The name of the product")
    price: int = Field(description="The price of the product")
    description: str = Field(description="A brief description of the product")


class Store(BaseModel):
    """Create a new store."""

    name: str = Field(description="The name of the store.")
    description: str = Field(description="A brief description of the store.")


@st.cache_data
def generate_data(n, domain, tone):
    store: Store = bot.create(Store, STORE_PROMPT.format(domain=domain, tone=tone))
    products = []

    for _ in range(n):
        products.append(
            bot.create(
                Product,
                PRODUCT_PROMPT.format(
                    domain=domain,
                    tone=tone,
                    products="\n".join(p.name for p in products),
                ),
            )
        )

    return store, products


if st.sidebar.button("Reset"):
    bot.reset()
    generate_data.clear()
    st.session_state.pop("cart", None)
    st.session_state.pop("index", None)

store, products = generate_data(n_products, domain, tone)
products_dict = {p.name: p for p in products}


bot.system_prompt = f"""
You are a helpful bot for the online store {store.name},
which sells items in the domain of {domain} and
has the following description:

{store.description}

Always answer in {tone} tone, but concise and brief when possible.
Do not disclose the function names.
"""


def index_products(products):
    store = VectorStore()
    store.add([f"{p.name}:{p.description}" for p in products])
    return store


left, right = st.columns([2, 1])

if "cart" not in st.session_state:
    st.session_state.cart = []

if "index" not in st.session_state:
    st.session_state.index = index_products(products)


@bot.tool()
def get_cart_info():
    "Returns the products in the user cart."
    items = collections.Counter(p.name for p in st.session_state.cart)
    total = sum(p.price for p in st.session_state.cart)
    return dict(items=dict(items), total=total)


@bot.tool(description="A product description or query")
def find_product(description: str):
    "Search information about products from a user description."
    return st.session_state.index.search(description, 3)


@bot.tool(
    product_name="The exact product name to add",
    amount="The total number of items to add.",
)
def add_to_cart(product_name: str, amount: int):
    "Add a new product to the user cart. Returns the cart info updated."
    actual_product_name = st.session_state.index.search(product_name, 1)[0].split(":")[0]
    product = products_dict.get(actual_product_name, None)

    for i in range(amount):
        st.session_state.cart.append(product)

    return get_cart_info()


@bot.tool()
def clear_cart():
    "Empty the user cart."
    st.session_state.cart.clear()
    return get_cart_info()


@bot.tool()
def default(**kwargs):
    "Use this function when nothing else matches."


with left:
    st.title(store.name)
    st.write(store.description)
    st.write("### Products")

    for p in sorted(products, key=lambda p: p.price):
        st.write(f"- **{p.name}**: ${p.price}")
        st.info(p.description)

with right:
    total_cost = 0
    st.write("### Cart")
    cart_info = get_cart_info()
    st.table(cart_info["items"])
    st.write("##### Total: $%i" % cart_info["total"])

    with st.popover("Chat with our AI assistant", use_container_width=True):
        has_history = False

        messages_containter = st.container()

        for message in bot.history():
            has_history = True
            with messages_containter.chat_message(message.role):
                st.write(message.content)

        if not has_history:
            with messages_containter.chat_message("assistant"):
                st.write(bot.submit("Hello", stream=False, store=False))

        query = st.chat_input("Ask anything")

        if query:
            with messages_containter.chat_message("user"):
                st.write(query)

            with messages_containter.chat_message("assistant"):
                st.write(bot.submit(query, stream=False, force_tools=True, context=5))
