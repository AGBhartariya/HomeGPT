# import cv2
# import numpy as np
# import os
# from sklearn.metrics.pairwise import cosine_similarity

# def load_face_encoding(img_path):
#     face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
#     img = cv2.imread(img_path)
#     gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#     faces = face_cascade.detectMultiScale(gray, 1.3, 5)

#     if len(faces) == 0:
#         return None

#     x, y, w, h = faces[0]
#     face = cv2.resize(gray[y:y+h, x:x+w], (100, 100))
#     return face.flatten().astype("float32") / 255.0

# def verify_user_face(live_img_path="assets/live.jpg", reference_img_path="assets/face_reference.jpg", threshold=0.6):
#     reference_encoding = load_face_encoding(reference_img_path)
#     live_encoding = load_face_encoding(live_img_path)

#     if reference_encoding is None or live_encoding is None:
#         return False, "Could not detect face"

#     similarity = cosine_similarity([reference_encoding], [live_encoding])[0][0]
#     print(f"Similarity: {similarity}")
#     return similarity > threshold, f"Match Score: {similarity:.2f}"

# import cv2

# def capture_live_image(filename="assets/live.jpg"):
#     cap = cv2.VideoCapture(0)
#     if not cap.isOpened():
#         raise IOError("Cannot access webcam")

#     ret, frame = cap.read()
#     if ret:
#         cv2.imwrite(filename, frame)
#     cap.release()

# import cv2
# import os
# import json
# from cryptography.fernet import Fernet

# # Load encryption key
# with open("secret.key", "rb") as key_file:
#     key = key_file.read()
# fernet = Fernet(key)

# def detect_and_crop_face(image_path, save_path=None):
#     img = cv2.imread(image_path)
#     gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#     face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
#     faces = face_cascade.detectMultiScale(gray, 1.3, 5)

#     if len(faces) == 0:
#         return None

#     x, y, w, h = faces[0]
#     cropped = img[y:y+h, x:x+w]

#     if save_path:
#         cv2.imwrite(save_path, cropped)
#     return cropped

# def save_password(site, password, face_image_path):
#     with open("password.json", "r") as f:
#         data = json.load(f)

#     enc_password = fernet.encrypt(password.encode()).decode()
#     data[site] = {
#         "password": enc_password,
#         "face_image": face_image_path
#     }

#     with open("password.json", "w") as f:
#         json.dump(data, f, indent=4)

# def match_faces(img1, img2):
#     orb = cv2.ORB_create()
#     kp1, des1 = orb.detectAndCompute(img1, None)
#     kp2, des2 = orb.detectAndCompute(img2, None)

#     if des1 is None or des2 is None:
#         return False

#     bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
#     matches = bf.match(des1, des2)

#     similarity = len(matches) / max(len(kp1), len(kp2))
#     return similarity > 0.3  # Tunable threshold

# def retrieve_password(site, live_image_path="assets/live.jpg"):
#     with open("password.json", "r") as f:
#         data = json.load(f)

#     if site not in data:
#         return "❌ Site not found."

#     stored_image_path = data[site]["face_image"]

#     stored_face = detect_and_crop_face(stored_image_path)
#     live_face = detect_and_crop_face(live_image_path)

#     if stored_face is None or live_face is None:
#         return "❌ Face not clearly visible."

#     if match_faces(stored_face, live_face):
#         enc_password = data[site]["password"]
#         return fernet.decrypt(enc_password.encode()).decode()
#     else:
#         return "❌ Face verification failed."

# def capture_live_image(filename="assets/live.jpg"):
#     cap = cv2.VideoCapture(0)
#     if not cap.isOpened():
#         raise IOError("Cannot access webcam")
#     ret, frame = cap.read()
#     if ret:
#         cv2.imwrite(filename, frame)
#     cap.release()


import json
import os
from cryptography.fernet import Fernet

# Set up encryption key
KEY_FILE = "secret.key"
if not os.path.exists(KEY_FILE):
    key = Fernet.generate_key()
    with open(KEY_FILE, "wb") as f:
        f.write(key)
else:
    with open(KEY_FILE, "rb") as f:
        key = f.read()
cipher = Fernet(key)

PASSWORD_FILE = "passwords.json"

def initialize_passwords_file():
    """Ensure the passwords file exists and is valid JSON."""
    if not os.path.exists(PASSWORD_FILE):
        with open(PASSWORD_FILE, "w") as f:
            json.dump({"passwords": []}, f)
    else:
        try:
            with open(PASSWORD_FILE, "r") as f:
                json.load(f)
        except json.JSONDecodeError:
            with open(PASSWORD_FILE, "w") as f:
                json.dump({"passwords": []}, f)

def save_password(site, password, user):
    """Encrypt and save a password for a site and user."""
    initialize_passwords_file()
    try:
        with open(PASSWORD_FILE, "r+") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = {"passwords": []}
            encrypted_password = cipher.encrypt(password.encode()).decode()
            # Check if entry exists
            found = False
            for entry in data["passwords"]:
                if entry["site"] == site and entry["user"] == user:
                    entry["password"] = encrypted_password
                    found = True
                    break
            if not found:
                data["passwords"].append({
                    "site": site,
                    "user": user,
                    "password": encrypted_password
                })
            f.seek(0)
            json.dump(data, f, indent=2)
            f.truncate()
        return True
    except Exception as e:
        print(f"Error saving password: {e}")
        return False

def retrieve_password(site, user):
    """Retrieve and decrypt a password for a site and user."""
    initialize_passwords_file()
    try:
        with open(PASSWORD_FILE, "r") as f:
            data = json.load(f)
        for entry in data["passwords"]:
            if entry["site"] == site and entry["user"] == user:
                try:
                    decrypted = cipher.decrypt(entry["password"].encode()).decode()
                    return decrypted
                except Exception as e:
                    print(f"Error decrypting password: {e}")
                    return None
        return None
    except Exception as e:
        print(f"Error retrieving password: {e}")
        return None

# Dummy function for compatibility; does nothing
def capture_live_image(user):
    return None
