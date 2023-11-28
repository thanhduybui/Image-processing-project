"""
    Use Index & Thumb finger tips' movement to control the volume of the system
    Made with cv2, pycaw & numpy library
"""

import cv2
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import streamlit as st
import mediapipe as mp
import numpy as np
import threading
import tensorflow as tf
import argparse

# access system's volume control
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
# volume.GetMute()
# volume.GetMasterVolumeLevel()
volRange = volume.GetVolumeRange()
volMin = volRange[0]
volMax = volRange[1]
st.set_page_config(page_title="Nhận dạng hành vi con người", page_icon="🌐")
page_bg_img = """
<style>
[data-testid="stAppViewContainer"] {
    background-image: url("");
    background-size: 100% 100%;
}
[data-testid="stHeader"]{
    background: rgba(0,0,0,0);
}
[data-testid="stToolbar"]{
    right:2rem;
}
[data-testid="stSidebar"] > div:first-child {
    background-image: url("https://i.pinimg.com/564x/bc/43/27/bc43279827af63b3fdba3c93514c69a8.jpg");
    background-position: center;
}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)
st.markdown("# Nhận dạng hành vi con người ")
FRAME_WINDOW = st.image([])
def get_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("--device", type=int, default=0)
    parser.add_argument("--width", help='cap width', type=int, default=960)
    parser.add_argument("--height", help='cap height', type=int, default=540)

    parser.add_argument('--use_static_image_mode', action='store_true')
    parser.add_argument("--min_detection_confidence",
                        help='min_detection_confidence',
                        type=float,
                        default=0.7)
    parser.add_argument("--min_tracking_confidence",
                        help='min_tracking_confidence',
                        type=int,
                        default=0.5)

    args = parser.parse_args()

    return args
def main():
    pythoncom.CoInitialize()
    label = "Warmup...."
    n_time_steps = 10
    lm_list = []
    mpPose = mp.solutions.pose
    pose = mpPose.Pose()
    mpDraw = mp.solutions.drawing_utils

    model = tf.keras.models.load_model("./models/behavior_detect/model.h5")

    video = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    def make_landmark_timestep(results):
        c_lm = []
        for id, lm in enumerate(results.pose_landmarks.landmark):
            c_lm.append(lm.x)
            c_lm.append(lm.y)
            c_lm.append(lm.z)
            c_lm.append(lm.visibility)
        return c_lm


    def draw_landmark_on_image(mpDraw, results, img):
        mpDraw.draw_landmarks(img, results.pose_landmarks, mpPose.POSE_CONNECTIONS)
        for id, lm in enumerate(results.pose_landmarks.landmark):
            h, w, c = img.shape
            print(id, lm)
            cx, cy = int(lm.x * w), int(lm.y * h)
            cv2.circle(img, (cx, cy), 5, (255, 0, 0), cv2.FILLED)
        return img


    def draw_class_on_image(label, img):
        font = cv2.FONT_HERSHEY_SIMPLEX
        bottomLeftCornerOfText = (10, 30)
        fontScale = 1
        fontColor = (0, 255, 0)
        thickness = 2
        lineType = 2
        cv2.putText(img, label,
                    bottomLeftCornerOfText,
                    font,
                    fontScale,
                    fontColor,
                    thickness,
                    lineType)
        return img


    def detect(model, lm_list):
        global label
        lm_list = np.array(lm_list)
        lm_list = np.expand_dims(lm_list, axis=0)
        print(lm_list.shape)
        results = model.predict(lm_list)
        print(results)
        if results[0][0] > 0.5:
            label = "SWING BODY"
        else:
            label = "SWING HAND"
        return label


    i = 0
    warmup_frames = 60

    while True:

        success, img = video.read()
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = pose.process(imgRGB)
        i = i + 1
        if i > warmup_frames:
            print("Start detect....")

            if results.pose_landmarks:
                c_lm = make_landmark_timestep(results)

                lm_list.append(c_lm)
                if len(lm_list) == n_time_steps:
                    # predict
                    t1 = threading.Thread(target=detect, args=(model, lm_list,))
                    t1.start()
                    lm_list = []

                img = draw_landmark_on_image(mpDraw, results, img)

        img = draw_class_on_image(label, img)
        cv2.imshow("Image", img)
        if cv2.waitKey(1) == ord('q'):
            break
        FRAME_WINDOW.image(img, channels='BGR')

if __name__ == "__main__":
    main()
