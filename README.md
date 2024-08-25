# Home-LAN-web-disk
基于Pyhton的Flask写的家庭局域网网盘，需要登录更加安全，以电脑服务器，文件所在盘为云盘空间，网盘支持其他局域网内设备扫码下载文件，但不支持文件夹


使用教程：
要运行上述代码，你需要确保以下几点：

安装python,
Windows:
访问 Python 官网。
下载适合你系统的最新版本的 Python 安装程序。
运行安装程序，确保选中“Add Python to PATH”选项，然后点击“Install Now”。

安装必要的库： 确保你已经安装了 Flask 和其他依赖库。可以使用以下命令安装这些库：
pip install flask qrcode[pil] pytz

创建必要的目录： 你的代码中有两个目录用于存储文件和二维码，分别是 files 和 qr_codes。如果这些目录还不存在，你的代码会自动创建它们，但确保你有写权限。

配置 Flask： 你需要确保 Flask 应用运行在你所使用的环境中。如果你在本地机器上运行 Flask，请确保端口 5000 没有被其他应用占用。如果你在服务器上运行，请确认服务器的防火墙设置允许通过端口 5000 访问应用。

创建 HTML 模板： 代码中使用了 render_template 来渲染 HTML 文件。你需要在项目目录中创建 templates 文件夹，并在其中放置 login.html 和 index.html 文件。这些模板文件应该包括你希望在网页上展示的内容。

生成二维码： 你提到需要生成二维码。请确保你的计算机上有生成二维码所需的依赖库，如 Pillow。二维码图片会被保存到 qr_codes 目录中。可以使用以下命令安装这个库：
pip install pillow

最后运行“app.py”时，记住第6行的地址（192.168.x.x:5000），那是局域网其他设备访问网盘的地址，电脑作为服务器可用这个地址还可以用“http://localhost:5000”
