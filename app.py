import streamlit as st

st.set_page_config(
    page_title="首頁",
    page_icon="👋"
)

st.sidebar.header("首頁")

st.write("# 歡迎來到統資系系展覽館 👋")
st.sidebar.success("選擇一個模擬方法的程式。")
st.sidebar.write(f"{st.secrets.dummy.s1} jump over the {st.secrets.dummy.s2}.")

st.markdown(
"""
    歡迎來到應用統計與資料科學學系的系展覽館網頁，這裡有許多關於模擬方法的程式。
"""
)
