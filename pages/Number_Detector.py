import streamlit as st
import numpy as np
from tensorflow import keras
from keras.models import model_from_json
from keras.optimizers import SGD
from PIL import Image

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
model_architecture = "models/MNIST/digit_config.json"
model_weights = "models/MNIST/digit_weight.h5"
model = model_from_json(open(model_architecture).read())
model.load_weights(model_weights)

optim = SGD()
model.compile(loss="categorical_crossentropyn",
              optimizer=optim, metrics=["accuracy"])

mnist = keras.datasets.mnist
(X_train, Y_train), (X_test, Y_test) = mnist.load_data()
X_test_image = X_test

RESHAPED = 784

X_test = X_test.reshape(10000, RESHAPED)
X_test = X_test.astype('float32')

# normalize in [0,1]
X_test /= 255


def create_image():
    index = np.random.randint(0, 9999, 150)
    digit_random = np.zeros((10 * 28, 15 * 28), dtype=np.uint8)
    for i in range(0, 150):
        m = i // 15
        n = i % 15
        digit_random[m * 28:(m + 1) * 28, n * 28:(n + 1)
                     * 28] = X_test_image[index[i]]
    Image.fromarray(digit_random).save('models/MNIST/digit_random.jpg')
    return digit_random, index


def predict(digits):
    X_test_sample = np.zeros((150, 784), dtype=np.float32)
    for i in range(0, 150):
        X_test_sample[i] = X_test[digits[i]]
    prediction = model.predict(X_test_sample)
    results = np.argmax(prediction, axis=1).reshape((10, 15))
    return results


def app():
    st.subheader('Nhận dạng chữ số viết tay')
    digit_random, index = create_image()
    image = Image.fromarray(digit_random)
    image_placeholder = st.empty()
    image_placeholder.image(image, use_column_width=True)

    if st.button('Tạo ảnh mới'):
        digit_random, index = create_image()
        image = Image.fromarray(digit_random)
        image_placeholder.image(image, use_column_width=True)

    if st.button('Nhận dạng'):
        results = predict(index)
        st.write('Kết quả:')
        st.write(results)


if __name__ == "__main__":
    app()
