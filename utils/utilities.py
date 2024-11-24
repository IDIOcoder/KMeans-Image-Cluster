import os
import cv2
import customtkinter as ctk
from PIL import Image, ImageTk


def load_image(image_path, max_width=400, max_height=400):
    # 이미지 읽기 및 RGB변환
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # 원본 크기 가져오기
    original_height, original_width = image.shape[:2]

    # 가로 및 세로 비율 계산
    width_ratio = max_width / original_width
    height_ratio = max_height / original_height

    # 가장 작은 비율 선택
    resize_ratio = min(width_ratio, height_ratio)

    # 원본 비율을 유지하면서 크기 조정
    if resize_ratio < 1:  # 원본보다 크기를 줄여야 할 경우에만 리사이즈
        new_width = int(original_width * resize_ratio)
        new_height = int(original_height * resize_ratio)
        image = cv2.resize(image, (new_width, new_height))

    return image, image.shape


def display_image_from_path(file_path, label_image: ctk.CTkLabel, max_width=400, max_height=400):
    # 이미지 로드
    img = Image.open(file_path)

    # 원본 비율 유지하며 크기 조정
    img_width, img_height = img.size
    ratio = min(max_width / img_width, max_height / img_height)  # 가로와 세로 중 작은 비율을 선택
    new_width = int(img_width * ratio)
    new_height = int(img_height * ratio)
    img = img.resize((new_width, new_height), Image.LANCZOS)  # 비율 유지한 리사이즈

    # Tkinter에서 표시 가능하도록 변환
    img_tk = ImageTk.PhotoImage(img)
    label_image.configure(image=img_tk)
    label_image.image = img_tk


# def display_image_from_array(image_array, label_image: ctk.CTkLabel, max_width=400, max_height=400):
#     # NumPy 배열을 PIL 이미지로 변환
#     img = Image.fromarray(image_array)
#
#     # 원본 비율 유지하며 크기 조정
#     img_width, img_height = img.size
#     ratio = min(max_width / img_width, max_height / img_height)
#     new_width = int(img_width * ratio)
#     new_height = int(img_height * ratio)
#     img = img.resize((new_width, new_height), Image.LANCZOS)
#
#     # Tkinter에서 표시 가능하도록 변환
#     img_tk = ImageTk.PhotoImage(img)
#     label_image.configure(image=img_tk)
#     label_image.image = img_tk


def clean_temp_folder():
    temp_dir = "temp"
    if os.path.exists(temp_dir):
        for file in os.listdir(temp_dir):
            file_path = os.path.join(temp_dir, file)
            if os.path.isfile(file_path):
                os.remove(file_path)


def create_temp_dir():
    temp_dir = "temp"
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)


def copy_file(source: str, save_dir: str, extension: str):
    temp_dir = "temp"
    temp_path = os.path.join(temp_dir, source)

    saves_name = f"{os.path.splitext(source)[0]}.{extension.lower()}"
    saves_path = os.path.join(save_dir, saves_name)

    with Image.open(temp_path) as img:
        rgb_image = img.convert("RGB")
        rgb_image.save(saves_path, extension)
