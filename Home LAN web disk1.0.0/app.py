from flask import Flask, render_template, request, redirect, url_for, session, send_from_directory
from datetime import datetime, timedelta
import os
import time
import qrcode
import urllib.parse
import pytz

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # 用于会话管理

# 设置登录密码
aPASSWORD = 'your's password'

# 文件存储目录
UPLOAD_FOLDER = 'files'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# 二维码存储目录
QR_FOLDER = 'qr_codes'
if not os.path.exists(QR_FOLDER):
    os.makedirs(QR_FOLDER)

# 在线用户信息
online_users = {}

# 文件信息
file_info = {}

# 获取文件列表
def get_file_list():
    files = []
    for filename in os.listdir(UPLOAD_FOLDER):
        if os.path.isfile(os.path.join(UPLOAD_FOLDER, filename)):
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            file_size = os.path.getsize(file_path)
            file_extension = os.path.splitext(filename)[1][1:].strip().lower()
            files.append({
                '名称': urllib.parse.unquote(filename),
                '大小': f"{file_size / 1024:.2f} KB",
                '格式': file_extension,
                '上传者IP': file_info.get(filename, {}).get('IP', '未知'),
                '下载次数': file_info.get(filename, {}).get('下载次数', 0),
                '下载链接': url_for('download_file', filename=filename)
            })
    return files

# 实时在线人数
def update_online_users():
    user_ip = request.remote_addr
    user_agent = request.user_agent
    device = "PC" if user_agent.platform in ['windows', 'linux', 'macos'] else "移动端"
    user_info = {
        'IP': user_ip,
        '上线时间': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()),
        '设备类型': device,
        '操作系统': user_agent.platform if user_agent.platform else "未知",
        '屏幕大小': request.args.get('screen', '未知')
    }
    online_users[user_ip] = user_info

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        password = request.form['password']
        if password == PASSWORD:
            session['authenticated'] = True
            return redirect(url_for('index'))
        else:
            return "密码错误，请重试。"
    return render_template('login.html')

@app.route('/')
def index():
    if not session.get('authenticated'):
        return redirect(url_for('login'))
    update_online_users()
    return render_template('index.html', 
                           file_list=get_file_list(), 
                           online_users=online_users,
                           current_time=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))

@app.route('/upload', methods=['POST'])
def upload_file():
    if not session.get('authenticated'):
        return redirect(url_for('login'))
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    if file:
        filename = urllib.parse.quote(file.filename)
        file.save(os.path.join(UPLOAD_FOLDER, filename))
        file_info[filename] = {
            'IP': request.remote_addr,
            '下载次数': 0
        }
        return redirect(url_for('index'))

@app.route('/download/<filename>')
def download_file(filename):
    if not session.get('authenticated'):
        return redirect(url_for('login'))
    if filename in file_info:
        file_info[filename]['下载次数'] += 1
    return send_from_directory(UPLOAD_FOLDER, urllib.parse.unquote(filename))

@app.route('/qr/<filename>')
def generate_qr(filename):
    if not session.get('authenticated'):
        return redirect(url_for('login'))
    link = url_for('download_file', filename=filename, _external=True)
    img = qrcode.make(link)
    img_path = os.path.join(QR_FOLDER, f'{filename}.png')
    img.save(img_path)
    return send_from_directory(QR_FOLDER, f'{filename}.png')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
