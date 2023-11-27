import streamlit as st


st.set_page_config(
    page_title='Project',
    layout='wide',
    initial_sidebar_state='collapsed',
    page_icon='./images/logo.jpg'
)


st.image('./images/banner.png')


st.title('ĐỒ ÁN MÔN XỬ LÝ ẢNH NĂM HỌC 2023')

st.write("Xin chào thầy Trần Tiến Đức! 👋")


def take_information_from_contact(email, text):
    with open(f'contacts/{email}.txt', 'wb') as file:
        file.write(text)


with st.expander('Liên hệ với chúng tôi'):
    with st.form(key='contact', clear_on_submit=True):
        email = st.text_input('Email liên hệ của bạn')
        text = st.text_area('Nội dung', '').encode('utf-8')
        submit_button = st.form_submit_button(label='Send Information')

        if submit_button:
            take_information_from_contact(email, text)
