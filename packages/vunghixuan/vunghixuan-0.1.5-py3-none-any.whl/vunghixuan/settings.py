# settings/settings.py

# Cặp màu nền và chữ
COLOR = {
    'Trắng' : '#FFFFFF',
    'Đen' : '#000000',
    'Đỏ': 'F70000',
    'Xanh lục' : '#007f8c',
    'Xanh lục tối':'#29465B',
    'Xanh lá cây':'#006400',
    'Vàng gold': '#FFD700',

    
}
COLOR_FONT_BACKGROUND ={
'Nền xanh lục, chữ trắng': ['#007f8c', '#FFFFFF'], # xanh lục tối
'Nền xanh xám, chữ vàng Gold': ['#29465B', '#FFD700'], #Gold (W3C)
'Nền xanh xám, chữ trắng': ['#29465B', '#FFFFFF'], # xanh lục tối #29465B
'Nền đen, chữ trắng': ['#000000', '#FFFFFF'],
'Nền đen, chữ vàng': ['#000000', '#FFD700'],

}
color_fnt_bg = COLOR_FONT_BACKGROUND['Nền xanh xám, chữ vàng Gold']

from pathlib import Path
import os
import sys
import site
import importlib.util as is_package

class Settings:
    def __init__(self):
        self.APP_NAME = "My PySide6 App"
        self.VERSION = "1.0.0"
        self.DEBUG = True
        self.BASE_DIR = str(Path(__file__).parent.parent)
        # self.path = self.get_path()
        # sys.path.append(self.BASE_DIR)

        # # BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        self.DATABASE_URL = 'sqlite:///data.db'  # Thay đổi nếu sử dụng DB khác

        # STATIC_DIR = os.path.join(BASE_DIR, 'static')

        # self.DATABASE = self.get_database_config()
        # self.FNT_BG_COLOR = self.get_color_config()
        self.MENUS_INFO = self.get_menus_info()
        self.TABS_INFO = self.get_tabs_info()
        self.ICON = self.get_icon_config()
        self.STATIC_DIR = self.get_static_dir()

    # def get_database_config(self):
    #     # return {
    #     #     'NAME': 'mydatabase.db',
    #     #     'USER': 'user',
    #     #     'PASSWORD': 'password',
    #     #     'HOST': 'localhost',
    #     #     'PORT': 5432,
    #     # }
    #     return {
    #     'ENGINE': 'sqlite',
    #     'NAME': self.BASE_DIR / "db.sqlite3",
    # }
    

    def get_color_config(self):
        return {
            'Trắng': '#FFFFFF',
            'Đen': '#000000',
            'Đỏ': '#F70000',
            'Xanh lục': '#007f8c',
            'Xanh lục tối': '#29465B',
            'Xanh lá cây': '#006400',
            'Vàng gold': '#FFD700',
        }
    def get_color_fnt_bg(self):
        return {
        'Nền xanh lục, chữ trắng': ['#007f8c', '#FFFFFF'], # xanh lục tối
        'Nền xanh xám, chữ vàng Gold': ['#29465B', '#FFD700'], #Gold (W3C)
        'Nền xanh xám, chữ trắng': ['#29465B', '#FFFFFF'], # xanh lục tối #29465B
        'Nền đen, chữ trắng': ['#000000', '#FFFFFF'],
        'Nền đen, chữ vàng': ['#000000', '#FFD700'],

        }
# color_fnt_bg = COLOR_FONT_BACKGROUND['Nền xanh xám, chữ vàng Gold']

    def get_menus_info(self):
        static_dir = self.get_static_dir()
        return {
            "File": {
                "New": f'{static_dir}/icon/icons8-file-64.png',
                "Open": f'{static_dir}/icon/icons8-opened-folder-50.png',
                "Save": None,
            },
            "Edit": {
                "Cut": f'{static_dir}/icon/icons8-file-64.png',
                "Copy": f'{static_dir}/icon/icons8-opened-folder-50.png',
                "Paste": None,
            },
            "Help": {
                "About": None,
                "Documentation": None
            }
        }

    def get_tabs_info(self):
        static_dir = self.get_static_dir()
        return {
            "Quản lý tài khoản": {
                "Đăng nhập": f'{static_dir}/icon/icon_sys.png',
                "Đăng ký": f'{static_dir}/icon/icon_user_64.png',
                "Cập nhật": f'{static_dir}/icon/update.png',
            },
            "Nhập dữ liệu Xi ngoài": {
                "Xi ngoài": f'{static_dir}/icon/icons8-file-64.png',
                "Xi nội bộ": f'{static_dir}/icon/icons8-opened-folder-50.png',
                "Xuất tạm": None,
            },
        }

    def get_icon_config(self):
        return {
            'eye_open': '👁️',
            'eye_closed': '👁️‍🗨️',
            'smile': '😀',
            'party': '🎉',
            'rocket': '🚀',
            'star': '🌟',
            'heart': '❤️',
            'thumbs_up': '👍',
            'fire': '🔥',
            'check_mark': '✔️',
            'clap': '👏',
            'sun': '☀️',
            'moon': '🌙',
            'sparkles': '✨',
            'gift': '🎁',
            'music': '🎵',
            'folder': '📁',
            'file': '📄',
            'add_button': '➕',
            'remove_button': '➖',
            'edit_button': '✏️',
            'open_folder': '📂',
            'close_folder': '📁',
            'user': '👤',
            'sys': '🖥️',
            'lock': '🔒',
            'unlock': '🔓',
            'search': '🔍',
            'settings': '⚙️',
            'warning': '⚠️',
        }

    def get_static_dir(self):
        return str(Path(__file__).parent.parent / 'static')

if __name__ == "__main__":
    settings = Settings()
    print(settings.STATIC_DIR)