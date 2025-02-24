from pathlib import Path
import os
import sys

"1. Khai báo đường dẫn chung dự án"
# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = str(Path(__file__).parent.parent)
sys.path.append(BASE_DIR)

# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_URL = 'sqlite:///data.db'  # Thay đổi nếu sử dụng DB khác

STATIC_DIR = os.path.join(BASE_DIR, 'static')

MENUS_INFO = {
            "File": {
                    "New": f'{STATIC_DIR}/icon/icons8-file-64.png',
                    "Open": f'{STATIC_DIR}/icon/icons8-opened-folder-50.png',
                    "Save": None,
                },

            
            "Edit": {
                    "Cut": f'{STATIC_DIR}/icon/icons8-file-64.png',
                    "Copy": f'{STATIC_DIR}/icon/icons8-opened-folder-50.png',
                    "Paste": None,
                },
            
            "Help": {
                "About": None,
                "Documentation": None
            }
            
        }
# TABS_INFO = {
#         "Xi Ngoài": [["Xi ngoài", "Xi nội bộ", "Xuất tạm"]],
#         "Phân Kim": [["Chưa code 1", "chưa code 2", "chưa code 2---------------------------------------------------------"]], 
#         "Hàng O": [["Chưa code 1", "chưa code 2"]], 
#         "Hệ thống": [["Đăng ký", "Nhóm truy cập", 'Quyền truy cập']], 
#     }

TABS_INFO = {
            "Quản lý tài khoản": {
                    "Đăng nhập": f'{STATIC_DIR}/icon/icon_sys.png',
                    "Đăng ký": f'{STATIC_DIR}/icon/icon_user_64.png',
                    "Cập nhật": f'{STATIC_DIR}/icon/update.png',
                },

            "Nhập dữ liêu Xi ngoài": {
                    "Xi ngoài": f'{STATIC_DIR}/icon/icons8-file-64.png',
                    "Xi nội bộ": f'{STATIC_DIR}/icon/icons8-opened-folder-50.png',
                    "Xuất tạm": None,
                },
            "Tab 2": {
                "Action 1": None,
                "Action 2": None,
            },
            "Tab 3": {
                "Action 3": None,
                "Action 4": None,
    },
        }

# https://getemoji.com/
ICON = {
    'eye_open': '👁️',  # Mắt mở
    'eye_closed': '👁️‍🗨️',  # Mắt đóng
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


# {
#             "Xi Ngoài": ["Xi ngoài", "Xi nội bộ", "Xuất tạm"],
#             "Hệ thống": ["Đăng ký", "Nhóm truy cập", 'Quyền truy cập'],
#         }

if __name__ == "__main__":
    print(STATIC_DIR)