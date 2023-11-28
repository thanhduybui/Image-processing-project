import streamlit as st

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

# Introduction text
st.write("Xin chào thầy Trần Tiến Đức! 👋")
st.write("Đây là project cuối kì môn học Xử lý ảnh số được giảng dạy và hướng dẫn bởi thầy Trần Tiến Đức giảng viên khoa CNTT trường ĐH Sư phạm Kỹ thuật TP.HCM.")

# Grouped section with highlighted color
with st.expander('Thông tin dự án', expanded=True):
    with st.container():
        st.markdown("""
            Thực hiện bởi nhóm sinh viên: 
            Bùi Thanh Duy               20110623
            Văn Thị Mười Ngọc           21110561
        """)

        st.markdown("""
            Website được xây dựng dựa trên Streamlit - mã nguồn mở hỗ trợ phổ biến cho các dự án Machine Learning. Với các nội dung:
            1. Giải phương trình bậc 2
            2. Nhận diện khuôn mặt sử dụng opencv-python 
            3. Nhận diện các loại trái cây sử dụng opencv-python
            4. Nhận diện vật thể sử dụng yolo5
            5. Nhận dạng cử chỉ tay sử dụng PointHistoryClassifier và KeyPointClassifier
            6. Nhận dạng hành động con người sử dụng tensorflow
            7. Nhận dạng chữ số viết tay sử dụng NMIST
            8. Xử lí ảnh - thay đổi các thuộc tính của ảnh
        """)

# Function to handle contact form submission
def take_information_from_contact(email, text):
    with open(f'contacts/{email}.txt', 'wb') as file:
        file.write(text)

# Contact form
with st.expander('Liên hệ với chúng tôi'):
    with st.form(key='contact', clear_on_submit=True):
        email = st.text_input('Email liên hệ của bạn')
        text = st.text_area('Nội dung', '').encode('utf-8')
        submit_button = st.form_submit_button(label='Gửi thông tin')

        if submit_button:
            take_information_from_contact(email, text)