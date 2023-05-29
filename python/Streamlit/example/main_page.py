import streamlit as st


def reset_value():
    if "value" in st.session_state:
        st.session_state["value"] = 0


start = st.button("reset", on_click=reset_value)
