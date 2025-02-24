from PySide6.QtWidgets import(
    
    QWidget,
    
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QTabWidget,
    QMessageBox,
    QGroupBox, 
    QSizePolicy

)
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor
# from vunghixuan.settings import color_fnt_bg
from vunghixuan.settings import color_fnt_bg


class LoginGroupBox(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def set_background(self):
        # Tạo nền xanh
        palette = self.palette()
        palette.setColor(self.backgroundRole(), color_fnt_bg[0])  # Màu xanh lục
        palette.setColor(self.backgroundRole(), color_fnt_bg[1])  # Màu xanh lục

        self.setAutoFillBackground(True)
        self.setPalette(palette)

    def initUI(self):
        # self.set_background()

        layout = QVBoxLayout()
        group_box = QGroupBox("") #Đăng Nhập
        
        lb_login = QLabel('ĐĂNG NHẬP HỆ THỐNG')
        # lb_login.setStyleSheet("font-size: 20px; color: white;") 
        lb_login.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lb_login.setFixedHeight(30)  # Thiết lập chiều cao cố định cho lb_login
        

        lb_login.setStyleSheet(f"background-color: {color_fnt_bg[0]}; color: {color_fnt_bg[1]}; font-size: 18px;")
        # lb_login.setStyleSheet('background-color: #007f8c; font-size: 20px; color: white;')
        # lb_login.setStyleSheet(f"background-color: {QColor(0, 127, 140).name()};")
        # '#007f8c'
        # print(QColor(0, 127, 140).name())

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Tên người dùng")
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Mật khẩu")
        self.password_input.setEchoMode(QLineEdit.Password)
        
        login_button = QPushButton("Đăng Nhập")
        login_button.clicked.connect(self.handle_login)

        layout.addWidget(lb_login)        
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_input)
        layout.addWidget(login_button)
        group_box.setLayout(layout)

        main_layout = QVBoxLayout()
        main_layout.addWidget(group_box)
        self.setLayout(main_layout)

        # Thiết lập kích thước tối thiểu cho form
        self.setMaximumSize(350, 250)
        # self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

    def handle_login(self):
        username = self.username_input.text()
        password = self.password_input.text()
        
        if username == "admin" and password == "password":
            QMessageBox.information(self, "Thành công", "Đăng nhập thành công!")
            self.parent().tab_widget.show()  # Hiện tab
            self.hide()  # Ẩn form đăng nhập
        else:
            QMessageBox.warning(self, "Lỗi", "Tên người dùng hoặc mật khẩu không đúng.")

