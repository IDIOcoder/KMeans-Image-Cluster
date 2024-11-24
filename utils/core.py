import customtkinter as ctk
from tkinter import filedialog
import utils.kmeans as km
from utils.utilities import *
import os
import atexit

ctk.set_appearance_mode("dark")


def select_image(label_file_path: ctk.CTkLabel, label_image_input: ctk.CTkLabel,
                 label_image_output: ctk.CTkLabel, button_save: ctk.CTkButton,
                 label_visualize_input, label_visualize_output):
    button_save.configure(state="disabled")
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.png *.jpeg *.bmp")])
    if file_path:
        # 선택한 파일 경로를 레이블에 표시
        label_file_path.configure(text=f"{file_path}")
        display_image_from_path(file_path, label_image_input)
        display_image_from_path(file_path, label_image_output)
        label_visualize_input.configure(image=None)
        label_visualize_output.configure(image=None)
        label_visualize_input.image = None
        label_visualize_output.image = None


def execute(label_file_path, label_image_output, entry_cluster,
            combobox_dimension, label_visualize_input, label_visualize_output,
            entry_weight, label_text, switch_pca, button_save):
    file_path = label_file_path.cget("text")
    if file_path == "No file selected":
        label_text.configure(text="No file has been selected", text_color="red")
        return

    n_cluster = entry_cluster.get()
    if n_cluster == '':     # number of cluster must be entered
        label_text.configure(text="Clusters must be entered", text_color="red")
        return
    elif int(n_cluster) <= 0:   # number of cluster should be more than 0
        label_text.configure(text="Cluster must be greater than 0", text_color="red")
        return
    else:
        n_cluster = int(n_cluster)

    dimension = combobox_dimension.get()
    compressed_image = None

    # temp save dir
    temp_dir = "temp"
    os.makedirs(temp_dir, exist_ok=True)
    processed_image_path = os.path.join(temp_dir, "compressed_image.png")
    original_graph_path = os.path.join(temp_dir, "original_visualize_rgb.png")
    compressed_graph_path = os.path.join(temp_dir, "compressed_visualize_rgb.png")
    original_pca_path = os.path.join(temp_dir, "original_visualize_pca.png")
    compressed_pca_path = os.path.join(temp_dir, "compressed_visualize_pca.png")

    if dimension == "RGB":      # do k-means on 3d
        original_image, _ = load_image(file_path)
        compressed_image, labels, new_colors = km.kmeans_3d(file_path, n_cluster)

        # visualize
        km.visualize_3d_rgb(original_image, original_graph_path, title="Original Image RGB Distribution")
        km.visualize_3d_rgb(original_image, compressed_graph_path, title="Compressed Image RGB Distribution",
                            labels=labels, center_colors=new_colors)
        display_image_from_path(original_graph_path, label_visualize_input)
        display_image_from_path(compressed_graph_path, label_visualize_output)
    elif dimension == "RGB+XY":     # do k-means on 5d
        weight = entry_weight.get()
        is_pca = switch_pca.get()
        if weight == "":
            label_text.configure(text="Weight must be entered", text_color="red")
            return
        elif float(weight) < 0:
            label_text.configure(text="Weight must be equal to or greater than 0.0", text_color="red")
            return
        else:
            weight = float(weight)
            compressed_image, labels, new_colors = km.kmeans_5d(file_path, n_cluster, weight)   # k-means on 5d

            original_image, _ = load_image(file_path)
            data_5d = km.get_5d_data(original_image, weight)

            # visualize(rgb)
            km.visualize_3d_rgb(original_image, original_graph_path, title="Original Image RGB Distribution")
            km.visualize_3d_rgb(original_image, compressed_graph_path, title="Compressed Image RGB Distribution",
                                labels=labels, center_colors=new_colors)

            # visualize(pca)
            km.visualize_5d_pca(data_5d, original_pca_path, title="Original PCA Visualization")
            km.visualize_5d_pca(km.get_5d_data(compressed_image, weight),
                                compressed_pca_path, title="Compressed PCA Visualization")

            if is_pca == "off":
                display_image_from_path(original_graph_path, label_visualize_input)
                display_image_from_path(compressed_graph_path, label_visualize_output)
            else:
                display_image_from_path(original_pca_path, label_visualize_input)
                display_image_from_path(compressed_pca_path, label_visualize_output)

    # Save processed image to temp
    processed_image = Image.fromarray(compressed_image)
    processed_image.save(processed_image_path)

    # Enable save button
    button_save.configure(state="normal")

    # display processed image
    display_image_from_path(processed_image_path, label_image_output)
    label_image_output.pack(pady=(5, 0), padx=5, fill=ctk.BOTH, expand=True)
    label_text.configure(text="Complete", text_color="green")


def enable_visualize_frame(gui: ctk.CTk, switch_weight: ctk.CTkSwitch, frame_visualize_input, frame_visualize_output):
    if switch_weight.get() == "on":
        gui.minsize(840, 940)
        frame_visualize_input.pack(pady=5, padx=(5, 0), fill=ctk.BOTH, expand=True)
        frame_visualize_output.pack(pady=5, padx=5, fill=ctk.BOTH, expand=True)
    elif switch_weight.get() == "off":
        gui.minsize(840, 520)
        frame_visualize_input.forget()
        frame_visualize_output.forget()


def enable_weight_pca(choice, entry: ctk.CTkEntry, label: ctk.CTkLabel,
                      label_pca: ctk.CTkLabel, switch_pca: ctk.CTkSwitch):
    if choice == "RGB+XY":
        label.configure(text_color="#d6d9dd")
        entry.configure(state="normal", text_color="#d6d9dd")
        label_pca.configure(text_color="#d6d9dd")
        switch_pca.configure(state="normal", button_color="#d6d9dd")
    else:
        label.configure(text_color="#4b4d52")
        entry.configure(state="disabled", text_color="#4b4d52")
        label_pca.configure(text_color="#4b4d52")
        switch_pca.configure(state="disabled", button_color="#4b4d52")


def switch_graph(switch, label_visualize_input, label_visualize_output):
    # temp save dir
    temp_dir = "temp"
    os.makedirs(temp_dir, exist_ok=True)
    original_graph_path = os.path.join(temp_dir, "original_visualize_rgb.png")
    compressed_graph_path = os.path.join(temp_dir, "compressed_visualize_rgb.png")
    original_pca_path = os.path.join(temp_dir, "original_visualize_pca.png")
    compressed_pca_path = os.path.join(temp_dir, "compressed_visualize_pca.png")

    if switch.get() == "off":
        display_image_from_path(original_graph_path, label_visualize_input)
        display_image_from_path(compressed_graph_path, label_visualize_output)
    else:
        display_image_from_path(original_pca_path, label_visualize_input)
        display_image_from_path(compressed_pca_path, label_visualize_output)


def run():
    app = App()
    app.mainloop()
    atexit.register(clean_temp_folder())


class SaveWindow(ctk.CTkToplevel):
    def __init__(self, parent, dimension: str):
        super().__init__(parent)
        self.dimension = dimension
        self.minsize(250, 350)
        self.resizable(False, False)

        self.label_image = ctk.CTkLabel(self, text="Image", fg_color="#333333", corner_radius=10)
        self.check_image_output = ctk.CTkCheckBox(self, text="Output", onvalue="on", offvalue="off")
        self.label_visualize_rgb = ctk.CTkLabel(self, text="RGB 3D Graph", fg_color="#333333", corner_radius=10)
        self.check_rgb_input = ctk.CTkCheckBox(self, text="Input", onvalue="on", offvalue="off")
        self.check_rgb_output = ctk.CTkCheckBox(self, text="Output", onvalue="on", offvalue="off")
        self.label_visualize_pca = ctk.CTkLabel(self, text="PCA 3D Graph", fg_color="#333333", corner_radius=10)
        self.check_pca_input = ctk.CTkCheckBox(self, text="Input", onvalue="on", offvalue="off")
        self.check_pca_output = ctk.CTkCheckBox(self, text="Output", onvalue="on", offvalue="off")
        self.label_extension = ctk.CTkLabel(self, text="Extension", fg_color="#333333", corner_radius=10)
        self.combobox_extension = ctk.CTkComboBox(self, values=["PNG", "JPEG", "BMP"])
        self.button_save = ctk.CTkButton(self, text="SAVE", command=lambda: self.save_image())

        self.pack_widget()

    def pack_widget(self):
        self.label_image.pack(padx=20, pady=(20, 0), fill=ctk.X, expand=True)
        self.check_image_output.pack(padx=20, pady=(10, 0), anchor='w', expand=True)
        self.label_visualize_rgb.pack(padx=20, pady=(20, 0), fill=ctk.X, expand=True)
        self.check_rgb_input.pack(padx=20, pady=(10, 0), anchor='w', expand=True)
        self.check_rgb_output.pack(padx=20, pady=(10, 0), anchor='w', expand=True)
        self.label_visualize_pca.pack(padx=20, pady=(20, 0), fill=ctk.X, expand=True)
        if self.dimension == "RGB":
            self.check_pca_input.configure(state="disabled")
            self.check_pca_output.configure(state="disabled")
        else:
            self.check_pca_input.configure(state="normal")
            self.check_pca_output.configure(state="normal")
        self.check_pca_input.pack(padx=20, pady=(10, 0), anchor='w', expand=True)
        self.check_pca_output.pack(padx=20, pady=(10, 0), anchor='w', expand=True)
        self.label_extension.pack(padx=20, pady=(20, 0), fill=ctk.X, expand=True)
        self.combobox_extension.pack(padx=20, pady=(10, 0), fill=ctk.X, expand=True)
        self.button_save.pack(padx=20, pady=20, fill=ctk.X, expand=True)

    def save_image(self):
        extension = self.combobox_extension.get()
        # 저장 경로 선택
        save_dir = filedialog.askdirectory(title="Select Save Directory")
        if not save_dir:
            return
        if self.check_image_output.get() == "on":
            copy_file("compressed_image.png", save_dir, extension)
        if self.check_rgb_input.get() == "on":
            copy_file("original_visualize_rgb.png", save_dir, extension)
        if self.check_rgb_output.get() == "on":
            copy_file("compressed_visualize_rgb.png", save_dir, extension)
        if self.check_pca_input.get() == "on":
            copy_file("original_visualize_pca.png", save_dir, extension)
        if self.check_pca_output.get() == "on":
            copy_file("compressed_visualize_pca.png", save_dir, extension)
        self.destroy()


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.minsize(840, 520)
        self.title("Image Clustering GUI")

        create_temp_dir()
        clean_temp_folder()

        # 이미지 저장 윈도우
        self.save_window = None

        # 상단 프레임
        self.top_frame = ctk.CTkFrame(self)
        frame_top_select = ctk.CTkFrame(self.top_frame)
        frame_top_settings = ctk.CTkFrame(self.top_frame)

        # 파일 경로 표시 레이블 (상단)
        self.label_file_path = ctk.CTkLabel(frame_top_select, text="No file selected", wraplength=500)

        frame_image = ctk.CTkFrame(self)    # 이미지 표시 프레임(중단)
        frame_image_input = ctk.CTkFrame(frame_image)
        frame_image_output = ctk.CTkFrame(frame_image)

        # 원본 이미지 표시 레이블 (하단)
        self.label_image_input = ctk.CTkLabel(frame_image_input, text="", image=None)
        # 결과 이미지 표시 레이블 (하단)
        self.label_image_output = ctk.CTkLabel(frame_image_output, text="", image=None)
        # 원본 이미지 시각화 프레임 (하단)
        self.label_visualize_input = ctk.CTkLabel(frame_image_input, text="")
        # 결과 이미지 시각화 프레임 (하단)
        self.label_visualize_output = ctk.CTkLabel(frame_image_output, text="")

        # 파일 선택 버튼 (상단)
        self.button_select_file = ctk.CTkButton(
            frame_top_select,
            text="Select Image",
            command=lambda: select_image(self.label_file_path, self.label_image_input,
                                         self.label_image_output, self.button_save,
                                         self.label_visualize_input, self.label_visualize_output)
        )
        
        # 파일 저장 버튼 (하단)
        self.button_save = ctk.CTkButton(
            frame_top_select,
            text="Save",
            state="disabled",
            command=lambda: self.open_save_window()
        )

        # 클러스터 입력 (상단)
        self.label_cluster = ctk.CTkLabel(frame_top_settings, text="Cluster(K) :")
        self.entry_cluster = ctk.CTkEntry(frame_top_settings, width=50)

        # 가중치 입력 (상단)
        self.label_weight = ctk.CTkLabel(frame_top_settings, text="Weight :", text_color="#4b4d52")
        self.entry_weight = ctk.CTkEntry(frame_top_settings, width=50, state="disabled")

        # pca 설정 (상단)
        self.label_pca = ctk.CTkLabel(frame_top_settings, text="PCA :", text_color="#4b4d52")
        self.switch_pca = ctk.CTkSwitch(
            frame_top_settings,
            text="",
            onvalue="on",
            offvalue="off",
            state="disabled",
            button_color="#4b4d52",
            command=lambda: switch_graph(self.switch_pca, self.label_visualize_input, self.label_visualize_output)
        )

        # 차원 설정 (상단)
        self.label_dimension = ctk.CTkLabel(frame_top_settings, text="Dimension :")
        self.combobox_dimension = ctk.CTkComboBox(
            frame_top_settings,
            values=["RGB", "RGB+XY"],
            width=100,
            command=lambda choice: enable_weight_pca(choice, self.entry_weight, self.label_weight,
                                                     self.label_pca, self.switch_pca)
        )

        # 시각화 설정 (상단)
        self.switch_visualize = ctk.CTkSwitch(
            frame_top_settings,
            text="Visualize",
            onvalue="on",
            offvalue="off",
            command=lambda: enable_visualize_frame(self, self.switch_visualize,
                                                   self.label_visualize_input, self.label_visualize_output)
        )

        # 알림 텍스트 레이블 (상단)
        self.label_text = ctk.CTkLabel(self, text="", height=10)

        # 실행 버튼 (상단)
        self.button_run = ctk.CTkButton(
            frame_top_select,
            text="RUN",
            command=lambda: execute(self.label_file_path, self.label_image_output,
                                    self.entry_cluster, self.combobox_dimension,
                                    self.label_visualize_input, self.label_visualize_output,
                                    self.entry_weight, self.label_text, self.switch_pca, self.button_save)
        )

        # 배치 ----------------------------------------------------------
        # 상단 프레임
        self.top_frame.pack(side=ctk.TOP, fill=ctk.X)
        frame_top_select.pack(side=ctk.TOP, fill=ctk.X)
        frame_top_settings.pack(side=ctk.TOP, fill=ctk.X)

        self.button_select_file.pack(pady=10, padx=10, side=ctk.LEFT)
        self.label_file_path.pack(pady=10, padx=10, side=ctk.LEFT)
        self.button_run.pack(padx=10, pady=10, side=ctk.RIGHT)
        self.button_save.pack(pady=10, side=ctk.RIGHT)

        self.label_cluster.pack(padx=10, pady=10, side=ctk.LEFT)
        self.entry_cluster.pack(pady=10, side=ctk.LEFT)
        self.label_dimension.pack(padx=10, pady=10, side=ctk.LEFT)
        self.combobox_dimension.pack(pady=10, side=ctk.LEFT)
        self.label_weight.pack(padx=10, pady=10, side=ctk.LEFT)
        self.entry_weight.pack(pady=10, side=ctk.LEFT)
        self.label_pca.pack(padx=10, pady=10, side=ctk.LEFT)
        self.switch_pca.pack(pady=10, side=ctk.LEFT)
        self.switch_visualize.pack(padx=(0, 30), pady=10, side=ctk.RIGHT)

        self.label_text.pack(pady=2, side=ctk.TOP, fill=ctk.X)

        # 하단
        frame_image.pack(expand=True, fill=ctk.BOTH)

        # 내부 프레임 배치
        frame_image_input.pack(side=ctk.LEFT, expand=True, fill=ctk.BOTH, padx=5, pady=5)
        frame_image_output.pack(side=ctk.RIGHT, expand=True, fill=ctk.BOTH, padx=5, pady=5)

        # 각 프레임에 이미지 레이블 배치
        self.label_image_input.pack(pady=(5, 0), padx=(5, 0), fill=ctk.BOTH, expand=True)
        self.label_image_output.pack(pady=(5, 0), padx=5, fill=ctk.BOTH, expand=True)

    def open_save_window(self):
        dimension = self.combobox_dimension.get()
        if self.save_window is None or not self.save_window.winfo_exists():
            self.save_window = SaveWindow(self, dimension)
        else:
            self.save_window.focus()
