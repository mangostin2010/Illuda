import streamlit as st

st.markdown('<style>' + open('./style.css').read() + '</style>', unsafe_allow_html=True)
#st.set_page_config(page_title='AI Tools', page_icon='🤖', initial_sidebar_state="expanded")
st.markdown("<style> ul {display: none;} </style>", unsafe_allow_html=True)


st.set_page_config(
    page_title="일루다가 뭐임?",
    page_icon="👧",
)

st.title("일루다를 소개합니다!")
