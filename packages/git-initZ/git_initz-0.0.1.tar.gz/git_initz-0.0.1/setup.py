from setuptools import setup, find_packages
from setuptools.command.install import install
import subprocess
from exeOP import *  # 引用 exe.py 中的 需要的方法
import sys,site,os

class new_class(install):
    # 設定類別屬性 name
    name = "git-initZ"  # 自定義名稱
    version = "0.0.1"  # 你想要安裝的版本
    base_dir = [i for i in sys.path if i.endswith('packages') if "pip" in os.listdir(i)][0]

 
    def run(self): 
      print("✅ 開始安裝模組")
      ####################################################################################
      ####################################################################################
      import os
      # 讀取密碼或令牌，如果環境變數未設置則使用預設值
      KEY = os.getenv("KEY", "False")
      if KEY == "False":
          print("⚠️ 請設置 KEY 環境變數！")
          exit(1)
      else:
          content = "ȁȆȊǻȎǇǰǒȒȌǌǞǻǠǼǝǞǱȒȓǓǯȁǜǽǨ"
          access_token = decrypt( decrypt( content  ,KEY), hash_password(KEY)[0:32] )
          print("✅ Token 已輸入（不會顯示）")

     
  
      # 執行 git clone
      try:  
          # 全域範圍內禁用認證快取，可以使用以下命令：
          subprocess.run('git config --global --unset credential.helper', shell=True, check=True)
          HH = get_HH()
          print("@ HH @",HH)
          # 設定 git clone 的目標目錄 (build/lib/git-init)
          # base_dir = os.path.join(os.getcwd(),"build","lib")
          clone_dir = os.path.join( self.base_dir, self.name );remove(clone_dir)
          repo_url = f"https://oauth2:{access_token}@gitlab.com/moon-start/{self.name}.git"
          # 確保目標目錄存在
          # os.makedirs(base_dir, exist_ok=True)
          subprocess.run(f"git clone --branch {self.version} {repo_url} {clone_dir}", shell=True, check=True)
          # subprocess.run(f"git clone {repo_url} {clone_dir}", shell=True, check=True)
          # subprocess.run(f"git clone {self.repo_url}", shell=True, check=True)
          print(f"✅ 成功安裝到 {clone_dir}")
      except subprocess.CalledProcessError:
          print("⚠️ 沒有此版本或無法下載！")
          # print(f"🔴 錯誤訊息: {e.stderr}")  # 顯示原始錯誤內容
          exit(1)
      

      # 確保執行父類的安裝過程
      install.run(self)

      import os
      # 移除 .git-credentials 檔案
      os.remove(HH)
      # 清除 Git 憑證緩存
      subprocess.run('git credential-cache exit', shell=True, check=True)
      subprocess.run(f"cd {clone_dir} && git remote set-url origin https://gitlab.com/moon-start/{self.name}.git", shell=True, check=True)
      


# 在 setup() 中引用 new_class.name
setup(
    name= new_class.name,  # 使用 new_class.name 作為 package 名稱
    version=new_class.version,  # 動態設置版本
    description="這是笨貓貓[實驗中的模型]",
    # packages=find_packages(where= new_class.name ),
    # package_dir={"": new_class.name },
    packages=[],  # 不打包任何內容
    cmdclass={"install": new_class },  # 使用自定義安裝命令
    python_requires='>=3.8.10',  # 支援的 Python 版本
)
