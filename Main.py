import streamlit as st
import openai
import time

st.set_page_config(page_title="일루다랑 채팅", page_icon="👧",)

# 일루다 이름 대문작만하게 박아놓기
Title = st.markdown("<h1 style='text-align: center; color: white;'>일루다</h1>", unsafe_allow_html=True)

with st.chat_message("user"):
    st.markdown("안녕")
with st.chat_message("assistant"):
    st.markdown("안녕 새끼야! 뭐하냐?")

st.markdown('<style>' + open('./style.css').read() + '</style>', unsafe_allow_html=True)

openai.api_key = "sk-ERbEZ6g35cYPM7DcMylctYXpg92zF60UaaVGMZWfPU1x7dpX"
openai.api_base = "https://api.chatanywhere.cn"

Chat_Model = "gpt-3.5-turbo"

system = open('prompt.txt',mode='r', encoding='UTF8')

#모든 텍스트를 가져온다.
system = system.read()

#일루다에게 보낼 메시지 관리
messages=[
    {"role": "system", "content": system},
]

#streamlit 세션관리
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

#사용자의 인풋을 받아오는 chat_input
User_Message = st.chat_input("일루다에게 보내기")


#만약 사용자가 메시지를 보냈다면,
if User_Message:
    #유저 메시지 세션에 저장
    def Write_UserMessage():
        Chat_User = st.chat_message("user")
        if Chat_User.markdown(User_Message):
            item =  {"role": "user", "content": User_Message}
            messages.append(item)
            st.session_state.messages.append({"role": "user", "content": User_Message})
    #챗봇 메시지를 실시간으로 생성하고 그걸 챗봇 메시지 세션에 저장
    def Write_BotMessage():
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            for response in openai.ChatCompletion.create(model=Chat_Model, messages=messages,
                stream=True,
            ):
                full_response += response.choices[0].delta.get("content", "")
                message_placeholder.markdown(full_response + "▌")
                time.sleep(0.1)
            message_placeholder.markdown(full_response)
            messages.append(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})

    Write_UserMessage()
    Write_BotMessage()
