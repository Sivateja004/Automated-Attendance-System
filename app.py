import os
import face_recognition
import numpy as np
import pandas as pd
from flask import Flask, render_template, request, redirect, url_for, send_from_directory, session
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Folders
UPLOAD_FOLDER = 'static/uploads'
TRAIN_FOLDER = 'static/train'

# Ensure folders exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(TRAIN_FOLDER, exist_ok=True)

# ---------- Login Page ----------
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'admin' and password == 'basha':
            session['logged_in'] = True
            return redirect(url_for('upload_page'))
        else:
            return render_template('login.html', error='Invalid credentials')
    return render_template('login.html')


# ---------- Upload Page ----------
@app.route('/upload-page', methods=['GET'])
def upload_page():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template('upload.html')


# ---------- Upload and Process ----------
@app.route('/upload', methods=['POST'])
def upload():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    if 'image' not in request.files:
        return "No file part"

    file = request.files['image']
    if file.filename == '':
        return "No selected file"

    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    known_encodings = []
    known_names = []

    # Load all student training images
    for student_folder in os.listdir(TRAIN_FOLDER):
        student_path = os.path.join(TRAIN_FOLDER, student_folder)
        if os.path.isdir(student_path):
            for image_file in os.listdir(student_path):
                image_path = os.path.join(student_path, image_file)
                if image_file.lower().endswith(('.png', '.jpg', '.jpeg')):
                    try:
                        image = face_recognition.load_image_file(image_path)
                        encodings = face_recognition.face_encodings(image)
                        if encodings:
                            known_encodings.append(encodings[0])
                            known_names.append(student_folder)
                    except Exception as e:
                        print(f"Error with {image_path}: {e}")

    # Process uploaded image
    image = face_recognition.load_image_file(filepath)
    face_locations = face_recognition.face_locations(image)
    face_encodings = face_recognition.face_encodings(image, face_locations)

    names = []
    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        matches = face_recognition.compare_faces(known_encodings, face_encoding)
        name = "Unknown"
        face_distances = face_recognition.face_distance(known_encodings, face_encoding)
        if len(face_distances) > 0:
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_names[best_match_index]
        names.append(name)

    # Draw rectangles and names on image
    from PIL import Image, ImageDraw
    pil_image = Image.fromarray(image)
    draw = ImageDraw.Draw(pil_image)
    for (top, right, bottom, left), name in zip(face_locations, names):
        draw.rectangle(((left, top), (right, bottom)), outline=(0, 255, 0), width=2)
        draw.text((left, bottom + 5), name, fill=(255, 255, 255))
    output_image_filename = f"output_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.jpg"
    output_image_path = os.path.join(UPLOAD_FOLDER, output_image_filename)
    pil_image.save(output_image_path)

    # Save to Excel
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    df = pd.DataFrame({"Name": names, "DateTime": now})
    output_excel_filename = f"attendance_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.xlsx"
    output_excel_path = os.path.join(UPLOAD_FOLDER, output_excel_filename)
    df.to_excel(output_excel_path, index=False)

    return render_template(
        'result.html',
        image_filename=output_image_filename,
        excel_filename=output_excel_filename
    )


# ---------- Download Route ----------
@app.route('/download/<filename>')
def download(filename):
    return send_from_directory(UPLOAD_FOLDER, filename, as_attachment=True)


# ---------- Logout ----------
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


# ---------- Run Server ----------
if __name__ == '__main__':
    app.run(debug=True)