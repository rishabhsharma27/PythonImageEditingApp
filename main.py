# Import Modules
import os
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QVBoxLayout, QFileDialog, QHBoxLayout, QApplication, QWidget, QLabel, QPushButton, QListWidget, QComboBox
from PIL import Image, ImageEnhance, ImageFilter 
from PyQt5.QtGui import QPixmap
#from random import choice

# Main App Object and Settings


# Create all App Object
class Image_Edit(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Image Editor")
        self.resize(1000, 1000)
        self.image = None
        self.original = None
        self.filename = None
        self.save_folder = "edits/"

        #title = QLabel("Cal")

        # All widgets 
        self.btn_folder = QPushButton("Folder")
        self.file_list = QListWidget()

        self.btn_left = QPushButton("Left")
        self.btn_right = QPushButton("Right")
        self.mirror = QPushButton("Mirror")
        self.sharpness = QPushButton("Sharpness")
        self.gray = QPushButton("B/W")
        self.saturation = QPushButton("Saturation")
        self.contrast = QPushButton("Contrast")
        self.blur = QPushButton("Blur") 


        # Drop Box
        self.filter_box = QComboBox()
        self.filter_box.addItem("Original")
        self.filter_box.addItem("Left")
        self.filter_box.addItem("Right")
        self.filter_box.addItem("Mirror")
        self.filter_box.addItem("Sharpness")
        self.filter_box.addItem("B/W")
        self.filter_box.addItem("Saturation")
        self.filter_box.addItem("Contrast")
        self.filter_box.addItem("Blur")

        self.picture_box = QLabel("Image will appear here!")

        # All Design Here
        master_layout = QHBoxLayout()

        self.col1 = QVBoxLayout()
        self.col2 = QVBoxLayout()

        self.col1.addWidget(self.btn_folder)
        self.col1.addWidget(self.file_list)
        self.col1.addWidget(self.filter_box)
        self.col1.addWidget(self.btn_left)
        self.col1.addWidget(self.btn_right)
        self.col1.addWidget(self.mirror)
        self.col1.addWidget(self.sharpness)
        self.col1.addWidget(self.gray)
        self.col1.addWidget(self.saturation)
        self.col1.addWidget(self.contrast)
        self.col1.addWidget(self.blur) 

        self.col2.addWidget(self.picture_box)

        master_layout.addLayout(self.col1, 20)
        master_layout.addLayout(self.col2, 80)

        self.setLayout(master_layout)

    # Events
        self.btn_folder.clicked.connect(self.get_Work_Dic)
        self.file_list.currentRowChanged.connect(self.displayImage)
        self.filter_box.currentTextChanged.connect(self.handle_filter)


    # Create Functions
    # Filter filename
    def filter(self, files, extensions):
        results = []
        for file in files:
            for ext in extensions:
                if file.endswith(ext):
                    results.append(file)
        return results

    def get_Work_Dic(self):
        global working_directory
        working_directory = QFileDialog.getExistingDirectory()
        extensions = ['.jpg','.png','.jpeg', '.svg']
        self.filenames = os.listdir(working_directory)
        self.list_filename = self.filenames
        self.file_list.clear()
        #print(self.list_filename )
        for filename in self.list_filename:
            for ext in extensions:
                if ext in filename:
                    self.file_list.addItem(filename)

    def load_image(self, filename):
        self.filename = filename  
        fullname = os.path.join(working_directory, self.filename)   
        self.image = Image.open(fullname)
        self.original = self.image.copy()

    def save_image(self):
        self.path = os.path.join(working_directory, self.save_folder)   
        if not(os.path.exists(self.path) or os.path.isdir(self.path)):
            os.mkdir(self.path)
        self.fullname = os.path.join(self.path, self.filename)
        self.image.save(self.fullname)

    def show_image(self, path):
        self.picture_box.hide()
        image = QPixmap(path)
        w, h = self.picture_box.width(), self.picture_box.height()
        image = image.scaled(w,h,Qt.KeepAspectRatio)
        self.picture_box.setPixmap(image)
        self.picture_box.show()

    def displayImage(self):
        if self.file_list.currentRow() >= 0:
            self.filename = self.file_list.currentItem().text()
            self.load_image(self.filename)
            self.show_image(os.path.join(working_directory, self.filename))

    def apply_filter(self, filter_name):
        if filter_name == "Original":
            self.image = self.original.copy()
        else:
            mapping = {
                "Left" : lambda image : image.transpose(Image.ROTATE_90),
                "Right" : lambda image : image.transpose(Image.ROTATE_270),
                "Mirror" : lambda image : image.transpose(Image.FLIP_LEFT_RIGHT),
                "Sharpness" : lambda image : image.filter(ImageFilter.SHARPEN),
                "B/W" : lambda image : image.convert("L"),
                "Saturation" : lambda image : ImageEnhance.Color(image).enhance(1.2),
                "Contrast" : lambda image : ImageEnhance.Contrast(image).enhance(1.2),
                "Blur" : lambda image : image.filter(ImageFilter.BLUR)
            }
            filter_function = mapping.get(filter_name)
            if filter_function:
                self.image = filter_function(self.image)
                self.save_image()
                self.image_path = os.path.join(working_directory, self.save_folder, self.filename)
                self.show_image(self.image_path)
            pass

        self.save_image()
        image_path = os.path.join(working_directory, self.save_folder, self.filename)
        self.show_image(image_path)

    def handle_filter(self):
        if self.file_list.currentRow() >= 0:
            select_filter = self.filter_box.currentText()
            self.apply_filter(select_filter)


# Show/Run our App'
if __name__ in "__main__":
    app = QApplication([])
    #main = Image_Edit()
    main_window = Image_Edit()
    main_window.show()
    app.exec_()
