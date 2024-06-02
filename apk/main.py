import sys
import os
import random
import sqlite3
import logging
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QFileDialog, QVBoxLayout, QWidget, QHBoxLayout
from PyQt5.QtGui import QPixmap, QTransform
from PyQt5.QtCore import Qt, pyqtSlot

# Setup logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class ImageShuffler(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Image Shuffler')
        self.setGeometry(100, 100, 360, 640)  # Ukuran standar untuk perangkat seluler
        
        self.layout = QVBoxLayout()
        
        self.button_layout = QHBoxLayout()
        self.select_folder_button = QPushButton('Select Folder')
        self.select_folder_button.clicked.connect(self.select_folder)
        self.button_layout.addWidget(self.select_folder_button)
        
        self.shuffle_button = QPushButton('Shuffle Images')
        self.shuffle_button.clicked.connect(self.shuffle_images)
        self.button_layout.addWidget(self.shuffle_button)
        
        self.layout.addLayout(self.button_layout)
        
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.image_label)
        
        self.info_label = QLabel()
        self.layout.addWidget(self.info_label)
        
        self.hide_button = QPushButton('Show Info')
        self.hide_button.clicked.connect(self.toggle_info)
        self.layout.addWidget(self.hide_button)
        
        self.container = QWidget()
        self.container.setLayout(self.layout)
        self.setCentralWidget(self.container)
        
        self.image_paths = []
        self.db_path = 'participants.db'
        self.image_display_count = {}
        self.info_visible = False
        
        logging.debug("ImageShuffler initialized.")
        
        self.info_label.hide()  # Hide info label initially
        
    def select_folder(self):
        folder = QFileDialog.getExistingDirectory(self, 'Select Folder')
        if folder:
            logging.debug(f"Selected folder: {folder}")
            self.load_images_from_folder(folder)
        
    def load_images_from_folder(self, folder):
        try:
            self.image_paths = [os.path.join(folder, f) for f in os.listdir(folder) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif'))]
            self.image_display_count = {path: 0 for path in self.image_paths}
            logging.debug(f"Loaded images: {self.image_paths}")
            if self.image_paths:
                self.shuffle_images()
        except Exception as e:
            logging.error(f"Error loading images from folder: {e}")
        
    def shuffle_images(self):
        try:
            available_images = [path for path, count in self.image_display_count.items() if count < 2]
            
            if not available_images:
                self.image_label.setText("No more images to display.")
                logging.debug("No more images to display.")
                return
            
            random_image_path = random.choice(available_images)
            self.image_display_count[random_image_path] += 1
            
            pixmap = QPixmap(random_image_path)
            if pixmap.width() > pixmap.height():
                transform = QTransform().rotate(90)
                pixmap = pixmap.transformed(transform, Qt.SmoothTransformation)
            
            self.image_label.setPixmap(pixmap.scaled(360, 480, Qt.KeepAspectRatio))  # Sesuaikan ukuran gambar
            logging.debug(f"Displayed image: {random_image_path}")
            
            image_name = os.path.basename(random_image_path)
            logging.debug(f"Looking for participant info for image: {image_name}")
            participant_info = self.get_participant_info(image_name)
            if participant_info:
                info_text = (
                    f"Nama lengkap: {participant_info[0]}\n"
                    f"Nama panggilan: {participant_info[1]}\n"
                    f"TTL: {participant_info[2]}\n"
                    f"Kota asal: {participant_info[3]}\n"
                    f"No WA: {participant_info[4]}"
                )
                self.info_label.setText(info_text)
                logging.debug(f"Displayed participant info for: {image_name}")
            else:
                self.info_label.setText("No participant information found.")
                logging.debug(f"No participant information found for: {image_name}")
        except Exception as e:
            logging.error(f"Error shuffling images: {e}")
    
    def get_participant_info(self, image_name):
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('SELECT full_name, nickname, birth_date, city_origin, phone FROM participants WHERE image_name = ?', (image_name,))
            result = cursor.fetchone()
            conn.close()
            logging.debug(f"Participant info retrieved for: {image_name} - {result}")
            return result
        except Exception as e:
            logging.error(f"Error getting participant info from database: {e}")
            return None
    
    def toggle_info(self):
        if self.info_visible:
            self.info_label.hide()
            self.hide_button.setText('Show Info')
        else:
            self.info_label.show()
            self.hide_button.setText('Hide Info')
        self.info_visible = not self.info_visible

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ImageShuffler()
    window.show()
    sys.exit(app.exec_())
