from PIL import Image
import streamlit as st
import cv2 as cv
import numpy as np
import os


def detect_object(frame):
    cfg_path = os.path.abspath('models/yolo/yolov4.cfg')
    weights_path = os.path.abspath('models/yolo/yolov4.weights')
    names_path = os.path.abspath(
        'models/yolo/object_detection_classes_yolov4.txt')

    # Load Yolo
    net = cv.dnn_DetectionModel(cfg_path, weights_path)
    net.setInputSize(704, 704)
    net.setInputScale(1.0 / 255)
    net.setInputSwapRB(True)

    # Resize the image
    frame = cv.resize(frame, dsize=(704, 704), interpolation=cv.INTER_AREA)

    with open(names_path, 'rt') as f:
        names = f.read().rstrip('\n').split('\n')

    classes, confidences, boxes = net.detect(
        frame, confThreshold=0.1, nmsThreshold=0.4)

    for classId, confidence, box in zip(classes.flatten(), confidences.flatten(), boxes):
        label = '%.2f' % confidence
        label = '%s: %s' % (names[classId], label)
        labelSize, baseLine = cv.getTextSize(
            label, cv.FONT_HERSHEY_SIMPLEX, 0.5, 1)
        left, top, width, height = box
        top = max(top, labelSize[1])
        cv.rectangle(frame, box, color=(0, 255, 0), thickness=3)
        cv.rectangle(frame, (left, top - labelSize[1]), (left + labelSize[0], top + baseLine),
                     (255, 255, 255), cv.FILLED)
        cv.putText(frame, label, (left, top),
                   cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0))

    return frame  # Return the modified image


def main():
    st.title("Object detection with YOLOv4")
    img_array = upload_image_ui()

    if isinstance(img_array, np.ndarray):
        modified_image = detect_object(img_array)
        st.image(modified_image, channels="BGR",
                 caption="Object Detection Result", use_column_width=True)


def upload_image_ui():
    uploaded_image = st.file_uploader(
        "Please choose an image file", type=["png", "jpg", "jpeg"])
    if uploaded_image is not None:
        try:
            image = Image.open(uploaded_image)
        except Exception:
            st.error("Error: Invalid image")
        else:
            img_array = np.array(image)
            return img_array


if __name__ == '__main__':
    main()
