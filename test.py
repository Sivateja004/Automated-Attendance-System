import os

base_dir = "C:/Users/nagur/Desktop/Attendance_project/training_images"

for folder in os.listdir(base_dir):
    folder_path = os.path.join(base_dir, folder)
    if os.path.isdir(folder_path):
        for filename in os.listdir(folder_path):
            name, ext = os.path.splitext(filename)
            correct_name = folder + ext
            current_path = os.path.join(folder_path, filename)
            new_path = os.path.join(folder_path, correct_name)
            if filename != correct_name:
                os.rename(current_path, new_path)
                print(f"Renamed: {filename} ➝ {correct_name}")
