import face_recognition
import cv2
import os
import numpy as np
import pickle
from datetime import datetime
import pandas as pd


def save_encodings(training_dir='training_images', encodings_file='encodeFile.p'):
    images = []
    names = []

    for name in os.listdir(training_dir):
        person_dir = os.path.join(training_dir, name)
        if not os.path.isdir(person_dir):
            continue
        for file in os.listdir(person_dir):
            img_path = os.path.join(person_dir, file)
            img = cv2.imread(img_path)
            if img is None:
                print(f"[!] Warning: Couldn't read image {name}/{file}")
                continue
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            face_locations = face_recognition.face_locations(img)
            if len(face_locations) != 1:
                continue
            encoding = face_recognition.face_encodings(img)[0]
            images.append(encoding)
            names.append(name)

    print("[✓] Face encodings saved to", encodings_file)
    with open(encodings_file, 'wb') as f:
        pickle.dump((images, names), f)


def run_face_recognition(image_path):
    with open('encodeFile.p', 'rb') as f:
        encode_list_known, student_ids = pickle.load(f)

    img = cv2.imread(image_path)
    img_small = cv2.resize(img, (0, 0), fx=0.25, fy=0.25)
    img_small_rgb = cv2.cvtColor(img_small, cv2.COLOR_BGR2RGB)

    faces_cur_frame = face_recognition.face_locations(img_small_rgb)
    encodes_cur_frame = face_recognition.face_encodings(img_small_rgb, faces_cur_frame)

    recognized = []
    for encode_face, face_loc in zip(encodes_cur_frame, faces_cur_frame):
        distances = face_recognition.face_distance(encode_list_known, encode_face)
        if len(distances) == 0:
            continue
        match_index = np.argmin(distances)

        if distances[match_index] < 0.6:
            name = student_ids[match_index]
            recognized.append(name)

            y1, x2, y2, x1 = face_loc
            y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(img, name, (x1 + 6, y2 - 6),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    # Save image
    os.makedirs('static/output', exist_ok=True)
    output_img_path = 'static/output/output_image.jpg'
    cv2.imwrite(output_img_path, img)

    # Save Excel
    recognized = list(set(recognized))
    df = pd.DataFrame({'Recognized Students': recognized})
    excel_path = 'static/output/attendance.xlsx'
    df.to_excel(excel_path, index=False)

    return recognized, output_img_path
