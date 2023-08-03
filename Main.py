import streamlit as st
import streamlit_authenticator as stauth
from dependancies import sign_up, fetch_users
import socket # socket 모듈을 import합니다.
from pathlib import Path
import time

st.set_page_config(
    page_title="일루다랑 채팅",
    page_icon="👧",
)

st.markdown('<style>' + open('./style.css').read() + '</style>', unsafe_allow_html=True)
#st.set_page_config(page_title='AI Tools', page_icon='🤖', initial_sidebar_state="expanded")
st.markdown("<style> ul {display: none;} </style>", unsafe_allow_html=True)

try:
    users = fetch_users()
    emails = []
    usernames = []
    passwords = []

    for user in users:
        emails.append(user['key'])
        usernames.append(user['username'])
        passwords.append(user['password'])

    credentials = {'usernames': {}}
    for index in range(len(emails)):
        credentials['usernames'][usernames[index]] = {'name': emails[index], 'password': passwords[index]}

    Authenticator = stauth.Authenticate(credentials, cookie_name='Streamlit', key='abcdef', cookie_expiry_days=20)

    email, authentication_status, username = Authenticator.login(':green[Login]', 'main')

    info, info1 = st.columns(2)

    if not authentication_status:
        if username:
            if username in usernames:
                with info:
                    st.error('Incorrect Password or username')
            else:
                st.error("유효하지 않은 계정입니다. 계정을 만들어 주세요.")
                sign_up()
        else:
            sign_up()

    else:
        # let User see app
       # st.sidebar.subheader(f'Welcome {username}')
        st.markdown("<style> ul {display: block;} </style>", unsafe_allow_html=True)
        
        import openai
        import streamlit as st
        import random
        from streamlit_extras.add_vertical_space import add_vertical_space

        st.markdown('<style>' + open('./style.css').read() + '</style>', unsafe_allow_html=True)

        #st.title("ChatGPT-like clone")
        Title = st.markdown("<h1 style='text-align: center; color: white;'>일루다</h1>", unsafe_allow_html=True)

        add_vertical_space(4)


        openai.api_key = "sk-ERbEZ6g35cYPM7DcMylctYXpg92zF60UaaVGMZWfPU1x7dpX"
        openai.api_base = "https://api.chatanywhere.com.cn/v1"


        if "messages" not in st.session_state:
            st.session_state.messages = []

        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])



        system = open('system.txt',mode='r', encoding='UTF8')

        #모든 텍스트를 가져온다.
        system = system.read()

        messages=[
            {"role": "system", "content": f"{system} And the name of the user is {username}"},
        ]

        with st.sidebar:
            st.write(f"Logged with {username}")
            Authenticator.logout(":red[Log Out]", 'main')

        prompt = st.chat_input("일루다에게 보내기")

        def apply_user():
            with st.chat_message("user"):
                st.markdown(prompt)
            st.session_state.messages.append({"role": "user", "content": f"{prompt}"})
            item =  {"role": "user", "content": prompt}
            messages.append(item)

        def apply_bot():
           # with st.chat_message("assistant"):

                def create_resp():
                    message_placeholder = st.empty()
                    full_response = ""
                    for response in openai.ChatCompletion.create(
                        model="gpt-3.5-turbo",
                        messages=messages,
                        stream=True     ):
                            
                            message_placeholder.markdown(full_response + "▌")
                            full_response += response.choices[0].delta.get("content", "")
                            time.sleep(0.1)
                    message_placeholder.markdown(full_response)
                    messages.append(full_response)
                    st.session_state.messages.append({"role": "assistant", "content": full_response})
                create_resp()

        if prompt:
            apply_user()
            apply_bot()

            
except FileNotFoundError:
    st.success('이 페이지를 새로고침 해주세요.')
