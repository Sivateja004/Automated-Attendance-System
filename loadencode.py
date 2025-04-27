import os
import cv2
import face_recognition
import pickle

def find_image(folder_path):
    for file in os.listdir(folder_path):
        if file.lower().endswith(('.jpg', '.jpeg', '.png')):
            return os.path.join(folder_path, file)
    return None

def load_known_faces(training_dir):
    encodeList = []
    student_ids = []

    for student_folder in os.listdir(training_dir):
        student_path = os.path.join(training_dir, student_folder)
        if not os.path.isdir(student_path):
            continue

        image_path = find_image(student_path)
        if image_path is None:
            print(f"[!] Warning: No valid image found in {student_folder}")
            continue

        img = cv2.imread(image_path)
        if img is None:
            print(f"[!] Warning: Couldn't read image {student_folder}")
            continue

        rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        faces = face_recognition.face_encodings(rgb_img)

        if len(faces) == 0:
            print(f"[!] Warning: No face found in {student_folder}")
            continue

        encodeList.append(faces[0])
        student_ids.append(student_folder)

    # Save encodings
    with open("encodeFile.p", "wb") as f:
        pickle.dump((encodeList, student_ids), f)

    print("[✓] Face encodings saved to encodeFile.p")

if __name__ == "__main__":
    training_path = "training_images"
    load_known_faces(training_path)
