import sys, os
from PySide6.QtWidgets import(
    QApplication,
    QMainWindow,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QTabBar, QTabWidget,
    QMessageBox,
    QComboBox

)
from PySide6.QtGui import QColor, QFont
from vunghixuan.login import LoginGroupBox
from PySide6.QtGui import QPixmap
# from vunghixuan.settings import COLOR_FONT_BACKGROUND, color_fnt_bg
from vunghixuan.settings import COLOR_FONT_BACKGROUND, color_fnt_bg

# color_default = COLOR_FONT_BACKGROUND['Xanh lục, chữ trắng']
# print(color_font_background)

class LoginForm(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        self.username = QLineEdit(self)
        self.password = QLineEdit(self)
        self.password.setEchoMode(QLineEdit.Password)
        login_button = QPushButton('Đăng Nhập', self)
        login_button.clicked.connect(self.handle_login)

        layout.addWidget(QLabel("Tên đăng nhập:"))
        layout.addWidget(self.username)
        layout.addWidget(QLabel("Mật khẩu:"))
        layout.addWidget(self.password)
        layout.addWidget(login_button)

        self.setLayout(layout)

    def handle_login(self):
        # Kiểm tra thông tin đăng nhập (đơn giản)
        if self.username.text() == "admin" and self.password.text() == "password":
            self.parent().show_content()  # Hiện nội dung chính
            self.close()  # Đóng form đăng nhập

# Create Header
class Header(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # self.dic_theme = {}
        self.set_background(color_fnt_bg)
        # self.set_background(QColor(0, 127, 140)) ##FF5733
        # self.set_background(QColor('#FF5733')) ##FF5733


        layout = QHBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)  # Căn chỉnh nội dung
        
        # Logo trái
        # ico = QPixmap("src/vunghixuan/img/vunghixuan_logo.png")
        # scaled_ico = ico.scaled(100, 100)  # Thay đổi kích thước thành 100x100 pixel
        # logo = QLabel()
        # logo.setPixmap(scaled_ico)

        logo = QLabel('VuNghiXuan')

        font = QFont('Brush Script MT', 20)
        # font = QFont('Dancing Script', 20)#('Segoe Script', 20)#('Lucida Handwriting', 20)#('Brush Script MT', 20)  # Thay đổi font chữ ở đây

        logo.setFont(font)
        logo.setStyleSheet("color: gold;")

        # logo.setStyleSheet("font-size: 20px; color: gold;") 
        layout.addWidget(logo)

        layout.addStretch()

        
        # # Nút để chuyển đổi giữa chế độ sáng và tối
        # toggle_button = QPushButton('Chế độ sáng/tối', self)
        # toggle_button.clicked.connect(self.toggle_theme)
        # layout.addWidget(toggle_button)

        # Combobox
        self.theme_selector = QComboBox(self)
        list_color = ['-- Chọn nền và màu chữ --']
        for color in COLOR_FONT_BACKGROUND.keys():
            list_color.append(color)

        # self.theme_selector.addItems(["Chế độ sáng", "Chế độ tối"])
        self.theme_selector.addItems(list_color)
        self.theme_selector.currentIndexChanged.connect(self.change_theme)
        layout.addWidget(self.theme_selector)

    

        # login and register
        login = QPushButton('Đăng nhập')
        register = QPushButton('Đăng ký')
        layout.addWidget(login)
        layout.addWidget(register)

        # Tạo layout chính
        main_layout = QVBoxLayout()
        main_layout.addLayout(layout)
        main_layout.setContentsMargins(0, 0, 0, 0)  # Loại bỏ khoảng cách mặc định

        self.setLayout(main_layout)
        
        # Đặt kích thước cho Header
        self.setFixedHeight(50)  # Bạn có thể điều chỉnh chiều cao theo ý muốn    
    
    def change_theme(self, index):
        if index != 0:
            color_name = self.theme_selector.currentText()
            color_fnt_bg = COLOR_FONT_BACKGROUND[color_name]
            
            
            # Tìm kiếm đối tượng MyWindow và gọi phương thức change_theme
            main_window = self.window()  # Lấy đối tượng MyWindow
            main_window.change_theme(color_fnt_bg)


        
    
    def set_background(self, color_fnt_bg):
        # Thay toàn bộ màu nền
        palette = self.palette()
        palette.setColor(self.backgroundRole(), color_fnt_bg[0]) # Thay đổi màu nền
        palette.setColor(self.foregroundRole(), color_fnt_bg[1])  # Thay đổi màu chữ
        self.setAutoFillBackground(True)
        self.setPalette(palette)


    
# Create Header
class Footer(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    

    def initUI(self):
        # self.set_background(QColor(0, 127, 140))

        layout = QHBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)  # Căn chỉnh nội dung

        # Logo
        logo = QLabel("@Copyright 2025 by VuNghiXuan")
        layout.addWidget(logo)

        
        # Tạo layout chính
        main_layout = QVBoxLayout()
        main_layout.addLayout(layout)
        main_layout.setContentsMargins(0, 0, 0, 0)  # Loại bỏ khoảng cách mặc định

        self.setLayout(main_layout)
        
        # Đặt kích thước cho Header
        self.setFixedHeight(50)  # Bạn có thể điều chỉnh chiều cao theo ý muốn    

        # Set background
        self.set_background(color_fnt_bg)

    def set_background(self, color_fnt_bg):
        palette = self.palette()
        palette.setColor(self.backgroundRole(), color_fnt_bg[0])
        palette.setColor(self.foregroundRole(), color_fnt_bg[1])
        self.setAutoFillBackground(True)
        self.setPalette(palette)

    
class Content(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.login_widget = LoginGroupBox()  # Sử dụng LoginGroupBox
        self.tab_widget = QTabWidget()
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        
        self.tab_widget.addTab(self.tab1, "Tab 1")
        self.tab_widget.addTab(self.tab2, "Tab 2")

        layout = QVBoxLayout()
        layout.addWidget(self.login_widget)
        layout.addWidget(self.tab_widget)
        self.setLayout(layout)

        self.tab_widget.hide()  # Ẩn tab ban đầu

    def set_background(self, color_fnt_bg):
        # palette = self.palette()
        # palette.setColor(self.backgroundRole(), color_fnt_bg[0])
        # palette.setColor(self.foregroundRole(), color_fnt_bg[1])
        # self.setAutoFillBackground(True)
        # self.setPalette(palette)
        # Cập nhật màu cho các nhãn        
        for widget in self.findChildren(QLabel):
            # widget.setStyleSheet(f"background-color: {color_fnt_bg[0]}; color: {color_fnt_bg[1]};")
            widget.setStyleSheet(f"background-color: {color_fnt_bg[0]}; color: {color_fnt_bg[1]}; font-size: 18px;")
            
class BackgroundManager:
    def __init__(self, widgets):
        self.widgets = widgets  # Danh sách các widget cần thay đổi màu nền
        

    def set_background(self, color_fnt_bg):
        for widget in self.widgets:
            widget.set_background(color_fnt_bg)
            # palette = widget.palette()
            # palette.setColor(widget.backgroundRole(), color)
            # widget.setAutoFillBackground(True)
            # widget.setPalette(palette)


# Create window
class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        
        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle('Phần mềm VuNghiXuan')

        # Tạo ra Qwidget trung tâm
        center_layout = QWidget()

        # Put layout Header
        main_layout = QVBoxLayout()
        self.header = Header()
        main_layout.addWidget(self.header)

        # Put Content 
        self.content = Content()
        main_layout.addWidget(self.content)


        # Thêm lớp co dãn
        # main_layout.addStretch()


        # Put layout Footer
        self.footer = Footer()
        main_layout.addWidget(self.footer)

        center_layout.setLayout(main_layout)
        
        # Căn chỉnh nội dung
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Set center_layout
        self.setCentralWidget(center_layout)

        # Setting background_manager
        self.background_manager = BackgroundManager([self.header, self.footer, self.content])


    def change_theme(self, color_fnt_bg):
        self.background_manager.set_background(color_fnt_bg)
        self.update_color_theme()

    def update_color_theme(self):
        from vunghixuan import setting_controlls 


        # Lấy thông tin thay đỏi từ giao diện
        color_fnt_bg = self.header.theme_selector.currentText()


        setting_controlls.update_theme(color_fnt_bg)

        # file_path = 'settings/settings.py'
        # if os.path.exists(file_path):
        #     color_fnt_bg = self.header.theme_selector.currentText()
        #     with open(setting_file, 'r', encoding='utf-8' ) as file:
        #         lines = file.readlines()

        #     with open(setting_file, 'w', encoding='utf-8') as file:
        #         for line in lines:
        #             if line.startswith('color_fnt_bg'):
        #                 file.write(f"color_fnt_bg = COLOR_FONT_BACKGROUND['{color_fnt_bg}']\n")
        #             else:
        #                 file.write(line)
        #         file.close()
                
        #     # Copy file settings qua venv
        #     import site, shutil
        #     package_name = 'vunghixuan'
        #     source_folder = os.path.join(site.getsitepackages()[1], package_name)
            
        #     setting_file = os.path.join(source_folder, 'settings.py')

        #     if os.path.exists(setting_file):
        #          shutil.copy(file_path, setting_file)

            
        # else:
        #     print(f"File {setting_file} không tồn tại.")
    # def toggle_theme(self):
    #     current_color = self.palette().color(self.backgroundRole())
    #     new_color = QColor(255, 255, 255) if current_color == QColor(0, 127, 140) else QColor(0, 127, 140)
    #     self.change_theme(new_color)

   

def create_gui():    
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec())
        
        

if __name__=='__main__':
    create_gui()
    # app = QApplication(sys.argv)
    # window = MyWindow()
    # window.show()
    # sys.exit(app.exec())
    # main()
