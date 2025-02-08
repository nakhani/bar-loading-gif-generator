import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QLabel, QLineEdit, QPushButton, QColorDialog, QFileDialog, QWidget, QMessageBox
from PySide6.QtGui import QColor
from PySide6.QtCore import Qt
from PIL import Image, ImageDraw
import imageio
import os

class LoadingBar:
    def __init__(self, width, height, duration, frame_rate, color):
        self.width = width
        self.height = height
        self.duration = duration  # Duration in seconds
        self.frame_rate = frame_rate  # Frames per second
        self.color = color
        self.total_frames = duration * frame_rate
        self.images = []

    def create_frame(self, progress):
        image = Image.new("RGBA", (self.width, self.height), (0, 0, 0, 0))  # Transparent background
        draw = ImageDraw.Draw(image)
        draw.rectangle([5, 35, 395, 65], outline=self.color)  # Draw the frame
        draw.rectangle([10, 40, 10 + progress, 60], fill=self.color)  # Draw progress bar
        return image

    def generate_animation(self):
        for frame in range(self.total_frames + 1):
            progress_width = int((frame / self.total_frames) * (self.width - 20))  # 10px padding on each side
            frame_image = self.create_frame(progress_width)
            self.images.append(frame_image)

    def save_animation(self, filename):
        self.images[0].save(
            filename,
            save_all=True,
            append_images=self.images[1:],
            duration=1000 // self.frame_rate,
            loop=0,
            transparency=0,  # Set transparency index to handle transparency in GIFs
        )

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Loading Bar GIF Generator")
        self.setGeometry(100, 100, 400, 200)

        self.layout = QVBoxLayout()

        self.duration_label = QLabel("Enter Duration (seconds):")
        self.layout.addWidget(self.duration_label)

        self.duration_input = QLineEdit()
        self.layout.addWidget(self.duration_input)

        self.color_button = QPushButton("Select Bar Color")
        self.color_button.clicked.connect(self.select_color)
        self.layout.addWidget(self.color_button)

        self.file_button = QPushButton("Select Output File")
        self.file_button.clicked.connect(self.select_file)
        self.layout.addWidget(self.file_button)

        self.save_button = QPushButton("Generate and Save GIF")
        self.save_button.clicked.connect(self.generate_gif)
        self.layout.addWidget(self.save_button)

        self.color = "white"  # Default color
        self.output_file = ""

        container = QWidget()
        container.setLayout(self.layout)
        self.setCentralWidget(container)

    def select_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.color = color.name()
            self.color_button.setStyleSheet(f"background-color: {self.color}")

    def select_file(self):
        options = QFileDialog.Options()
        file, _ = QFileDialog.getSaveFileName(self, "Select Output File", "", "GIF Files (*.gif);;All Files (*)", options=options)
        if file:
            self.output_file = file

    def generate_gif(self):
        try:
            duration = int(self.duration_input.text())
            if not self.output_file:
                raise ValueError("Output file not selected")
            
            width = 400
            height = 100
            frame_rate = 30  # Frames per second

            loading_bar = LoadingBar(width, height, duration, frame_rate, self.color)
            loading_bar.generate_animation()
            loading_bar.save_animation(self.output_file)

            self.show_message("GIF generated successfully!")
        except Exception as e:
            self.show_message(f"Error: {str(e)}")

    def show_message(self, message):
        msg_box = QMessageBox()
        msg_box.setText(message)
        msg_box.exec()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
