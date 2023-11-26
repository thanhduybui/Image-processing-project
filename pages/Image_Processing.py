import streamlit as st
import cv2
import numpy as np
from algorithm import Chapter03 as c3
from algorithm import Chapter04 as c4
from algorithm import Chapter05 as c5
from algorithm import Chapter09 as c9
# Streamlit code


def main():
    st.title("Machine Vision")

    uploaded_file = st.file_uploader(
        "Choose an image...", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        file_bytes = np.asarray(
            bytearray(uploaded_file.read()), dtype=np.uint8)
        imgin = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

        st.image(imgin, channels="BGR", caption='Uploaded Image')

        option = st.selectbox("Choose an operation", ("Negative", "Logarit", "Power", "PiecewiseLinear", "Histogram", "HistEqual", "HistEqualColor",
                              "LocalHist", "BoxFilter", "Threshold", "MedianFilter", "Sharpen", "Gradient"))

        if st.button("Apply"):
            if option == "Negative":
                imgout = c3.Negative(imgin)
                st.image(imgout, channels="BGR", caption='Negative Image')
            elif option == "Logarit":
                imgout = c3.Logarit(imgin)
                st.image(imgout, channels="BGR", caption='Logarit Image')
            elif option == "Power":
                imgout = c3.Power(imgin)
                st.image(imgout, channels="BGR",
                         caption='Power Image')
            elif option == "PiecewiseLinear":
                gray_image = cv2.cvtColor(imgin, cv2.COLOR_BGR2GRAY)
                imgout = c3.PiecewiseLinear(gray_image)
                st.image(imgout,
                         caption='PiecewiseLinear Image')
            elif option == "Histogram":
                imgout = c3.Histogram(imgin)
                st.image(imgout, caption='Grayscale Histogram')
            elif option == "HistEqual":
                gray_image = cv2.cvtColor(imgin, cv2.COLOR_BGR2GRAY)
                imgout = c3.HistEqual(gray_image)
                st.image(imgout, caption='HistEqual Image')
            elif option == "HistEqualColor":
                imgout = c3.HistEqualColor(imgin)
                st.image(imgout, channels="BGR",
                         caption='HistEqualColor Image')
            elif option == "LocalHist":
                gray_image = cv2.cvtColor(imgin, cv2.COLOR_BGR2GRAY)
                imgout = c3.LocalHist(gray_image)
                st.image(imgout, caption='LocalHist Image')
            elif option == "HistStat":
                gray_image = cv2.cvtColor(imgin, cv2.COLOR_BGR2GRAY)
                imgout = c3.HistStat(gray_image)
                st.image(imgout, caption='HistStat Image')
            elif option == "BoxFilter":
                gray_image = cv2.cvtColor(imgin, cv2.COLOR_BGR2GRAY)
                imgout = c3.BoxFilter(gray_image)
                st.image(imgout, caption='BoxFilter Image')
            elif option == "Threshold":
                gray_image = cv2.cvtColor(imgin, cv2.COLOR_BGR2GRAY)
                imgout = c3.Threshold(gray_image)
                st.image(imgout,  caption='Threshold Image')
            elif option == "MedianFilter":
                gray_image = cv2.cvtColor(imgin, cv2.COLOR_BGR2GRAY)
                imgout = c3.MedianFilter(gray_image)
                st.image(imgout, caption='MedianFilter Image')
            elif option == "Sharpen":
                imgout = c3.Sharpen(imgin)
                st.image(imgout, channels="BGR", caption='Sharpen Image')
            elif option == "Gradient":
                imgout = c3.Gradient(imgin)
                st.image(imgout, channels="BGR", caption='Gradient Image')


if __name__ == "__main__":
    main()
