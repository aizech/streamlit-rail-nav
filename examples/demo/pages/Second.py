import streamlit as st

from streamlit_rail_nav import render

st.set_page_config(page_title="Second", layout="wide")

render(
    {
        "items": [
            {
                "kind": "link",
                "label": "Home",
                "icon": "home",
                "page": "demo_app.py",
            },
            {
                "kind": "badge_link",
                "label": "Second page",
                "icon": "table",
                "page": "pages/Second.py",
                "badge": "New",
            },
            {
                "kind": "link",
                "label": "Third page",
                "icon": "science",
                "page": "pages/Third.py",
            },
        ],
    },
    footer="streamlit-rail-nav demo",
)

st.title("Second page")
st.write("The rail nav state carries over across pages.")
