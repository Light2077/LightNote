import streamlit as st
import time


with st.empty():
    if "value" not in st.session_state:
        st.session_state["value"] = 0

    while st.session_state["value"] < 60:
        st.session_state["value"] += 1
        # 如果不这么写，st.write之前写的东西会被保留
        st.write(f'⏳ {st.session_state["value"]} have passed')
        time.sleep(0.1)
    st.write("✔️ over!")
