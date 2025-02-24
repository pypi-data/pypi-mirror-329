# config.py
from pathlib import Path
import os
import sys
from config_menubar import create_menubar



"1. Khai báo đường dẫn chung dự án"
# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = Path(__file__).parent
sys.path.append(BASE_DIR)

class Config:
    def __init__(self):
        # self.apps_dir = os.path.join(BASE_DIR, 'apps')
        self.resources_url = os.path.join(BASE_DIR, 'resources')
        # self.database_url = f"sqlite:///{BASE_DIR}/resources/database.db"
        self.templates_url = f"{BASE_DIR}/resources/templates"
        self.logo_url = f"{BASE_DIR}/resources/logo"
        
        # 1. app_mainGui 
        self.app_mainGui = f"{BASE_DIR}/app_mainGui" 

        "2. Khai báo các app được sử dụng"
        self.apps = ['app_mainGui', 'resources']
        self.apps_dir = {}
        # Thêm đường dẫn của các thư mục con nếu cần
        for app in self.apps:
            app_dir = os.path.join(BASE_DIR, app)
            
            # Thêm đường dẫn vào danh mục đường dẫn dự án
            sys.path.append(app_dir)
            self.apps_dir[app] = app_dir


        "3. File Excel"
        # Khai báo file Excel và các sheet sử dụng
        EXCEL_FILE = {
            "path": f"{self.apps_dir['resources']}/templates/input.xlsm",
            'sheet_names': ['Nhap_DoiDe', 'Nhap_MuaDe', 'Nhap_BanDe', 'GiaVang', 'LoaiVang'],
            
        }

        "4. Khởi tạo  menubar"
        self.menubar = create_menubar()

        

        # self.app_metalStool = os.path.join(self.apps_dir, 'app_metalStool')
        # self.app2_dir = os.path.join(self.apps_dir, 'App2')
        # self.app3_dir = os.path.join(self.apps_dir, 'App3')
        # ... thêm các đường dẫn khác theo nhu cầu
# url_config = Config()  # Khởi tạo biến toàn cục






# class UrlConfig:
#     def __init__(self) -> None:
#         self.base_dir = Path(__file__).resolve().parent
#         self.database_url = f"sqlite:///{self.base_dir}/resources/database.db"
#         self.logo_url = f"{self.base_dir}/resources/logo"

# url_config = UrlConfig()  # Khởi tạo biến toàn cục

# main.py
# import config

# # Kết nối đến database
# engine = create_engine(config.DATABASE_URL)

if __name__ == "__main__":

    config = Config()
    print('BASE_DIR:', BASE_DIR)
    print('apps_dir:', config.apps_dir)
    print('DATABASE_URL:',config.templates_url)
    print('LOGO_URL:', config.logo_url)
    print('app_gui_excel:', config.app_mainGui)

    
