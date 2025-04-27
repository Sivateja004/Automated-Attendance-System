# Automated Attendance System

## Overview
This project is an **Automated Attendance System** that uses deep learning techniques for face recognition to mark attendance. It leverages the `face_recognition` library to identify individuals in images and records their attendance in an Excel file. The system includes a web interface built with Flask for user interaction, allowing users to upload images, process them for face recognition, and download attendance records.

## Features
- **Face Recognition**: Identifies individuals in uploaded images using pre-trained face encodings.
- **Web Interface**: A Flask-based web application with login, image upload, and result display functionalities.
- **Attendance Logging**: Saves recognized individuals' names and timestamps in an Excel file.
- **Image Annotation**: Draws rectangles and names on recognized faces in the output image.
- **Pre-processing Scripts**: Includes scripts to prepare and encode face images for training.

## Project Structure
```
├── app.py                  # Main Flask application
├── loadencode.py           # Script to generate face encodings from training images
├── main.py                 # Script for face recognition and attendance processing
├── test.py                 # Script to rename training images for consistency
├── Procfile                # Configuration for deployment (e.g., Heroku)
├── runtime.txt             # Specifies Python runtime version
├── requirements.txt        # List of Python dependencies
├── static/
│   ├── uploads/           # Stores uploaded and output images
│   ├── train/             # Stores training images
│   ├── output/            # Stores processed output images and Excel files
├── templates/
│   ├── login.html         # Login page template
│   ├── upload.html        # Image upload page template
│   ├── result.html        # Results display page template
└── training_images/       # Directory for training images (organized by student names)
```

## Prerequisites
- Python 3.12.1
- A webcam or image source for capturing attendance images
- Training images organized in the `training_images` directory, with subfolders named after each individual (e.g., `training_images/John_Doe/`)

## Installation
1. **Clone the Repository**:
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Set Up a Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Prepare Training Images**:
   - Place training images in the `training_images` directory, with one subfolder per person (e.g., `training_images/John_Doe/image1.jpg`).
   - Run the `test.py` script to ensure image filenames match the folder names:
     ```bash
     python test.py
     ```

5. **Generate Face Encodings**:
   - Run the `loadencode.py` script to create face encodings from training images:
     ```bash
     python loadencode.py
     ```
   - This generates an `encodeFile.p` file containing face encodings and corresponding names.

## Usage
1. **Run the Flask Application**:
   ```bash
   python app.py
   ```
   - The application will start at `http://127.0.0.1:5000`.

2. **Log In**:
   - Navigate to `http://127.0.0.1:5000` in your browser.
   - Use the credentials:
     - Username: `admin`
     - Password: `basha`

3. **Upload an Image**:
   - On the upload page, select an image containing faces to process.
   - The system will:
     - Identify faces and match them against known encodings.
     - Annotate the image with names and rectangles around faces.
     - Save the annotated image and an Excel file with attendance details in the `static/uploads` directory.

4. **View and Download Results**:
   - The results page displays the annotated image and provides a link to download the attendance Excel file.
   - Use the `/download/<filename>` route to download files.

5. **Log Out**:
   - Click the logout button to clear the session and return to the login page.

## Alternative Usage (Standalone Script)
- Use `main.py` for standalone face recognition without the web interface:
  ```bash
  python main.py
  ```
- This script processes a specified image, saves the annotated output to `static/output/output_image.jpg`, and generates an attendance Excel file at `static/output/attendance.xlsx`.

## Deployment
- The project is configured for deployment on platforms like Heroku.
- Ensure the `Procfile` and `runtime.txt` are correctly set up.
- Install `gunicorn` for production:
  ```bash
  pip install gunicorn
  ```
- Deploy using:
  ```bash
  heroku create
  git push heroku main
  ```

## Dependencies
See `requirements.txt` for the full list of dependencies, including:
- Flask
- face_recognition
- opencv-python
- numpy
- pandas
- openpyxl
- Pillow

## Notes
- Ensure training images are clear and contain only one face per image for best results.
- The face recognition model may struggle with poor lighting, occlusions, or low-quality images.
- The default login credentials (`admin`/`basha`) should be changed in a production environment for security.
- The system resizes images during processing to improve performance, which may affect accuracy for very small faces.

## Troubleshooting
- **No faces detected**: Check image quality and ensure faces are clearly visible.
- **Encoding errors**: Verify that training images are correctly formatted and placed in the appropriate directories.
- **Dependency issues**: Ensure all packages in `requirements.txt` are installed correctly.
- **File path errors**: Confirm that the `static/uploads`, `static/train`, and `static/output` directories exist.

## Future Improvements
- Add real-time webcam support for live attendance capturing.
- Implement a database backend for persistent attendance records.
- Enhance security with proper user authentication and session management.
- Optimize face recognition for larger datasets using more efficient encoding storage.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

