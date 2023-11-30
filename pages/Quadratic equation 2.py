import streamlit as st
import math
# Set page configuration
st.set_page_config(
    page_title='Project',
    layout='wide',
    initial_sidebar_state='collapsed',
    page_icon='./images/icon_1.png'
)

# Set custom CSS styles
st.markdown(
    """
    <style>
    body {
        background-color: #F0F2F6;
        color: #333333;
    }
    .stButton {
        background-color: #4CAF50 !important;
        color: white !important;
    }
    .stTextInput {
        border: 1px solid #4CAF50 !important;
    }
    .highlight {
        background-color: #EAF7FF;
        padding: 12px;
        margin-bottom: 12px;
        border-radius: 5px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Display banner image
st.image('./images/banner.png')

# Display page title
st.title('ĐỒ ÁN MÔN XỬ LÝ ẢNH NĂM HỌC 2023')
def gptb2(a, b, c):
    if a == 0:
        if b == 0:
            if c == 0:
                ket_qua = 'PTB1 có vô số nghiệm'
            else:
                ket_qua = 'PTB1 vô nghiệm'
        else:
            x = -c/b
            ket_qua = 'PTB1 có nghiệm %.2f' % x
    else:
        delta = b**2 - 4*a*c
        if delta < 0:
            ket_qua = 'PTB2 vô nghiệm'
        else:
            x1 = (-b + math.sqrt(delta))/(2*a)
            x2 = (-b - math.sqrt(delta))/(2*a)
            ket_qua = 'PTB2 có nghiệm x1 = %.2f và x2 = %.2f' % (x1, x2)
    return ket_qua

def clear_input():
    st.session_state["nhap_a"] = 0.0
    st.session_state["nhap_b"] = 0.0
    st.session_state["nhap_c"] = 0.0

st.title('Giải phương trình bậc 2')
with st.form(key='columns_in_form', clear_on_submit=False):
    col1, col2, col3 = st.columns(3)
    
    with col1:
        a = st.number_input('Nhập a', key='nhap_a')
    
    with col2:
        b = st.number_input('Nhập b', key='nhap_b')
    
    with col3:
        c = st.number_input('Nhập c', key='nhap_c')
    
    col4, col5 = st.columns(2)
    
    with col4:
        btn_giai = st.form_submit_button('Giải')
    
    with col5:
        btn_xoa = st.form_submit_button('Xóa', on_click=clear_input)
    
    if btn_giai:
        s = gptb2(a, b, c)
        st.subheader('Kết quả:')
        st.write(s)