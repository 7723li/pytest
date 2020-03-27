from flask import Flask, request, render_template, send_file, make_response, send_from_directory, url_for, redirect, request
from PIL import Image
from io import BytesIO
import os, time, platform, string, shutil, chardet, ctypes, logging

logging.basicConfig(filename='.log', 
                    filemode="w", 
                    format="%(asctime)s %(name)s:%(levelname)s:%(message)s", 
                    datefmt="%d-%m-%Y %H:%M:%S", 
                    level=logging.DEBUG)

g_dict_users_2_pwd = {
    'lzx' : '19951107lzx'
}
g_dict_ip_2_loginstatus = {
    
}
g_dict_ip_2_user = {

}

fuck_him = False

app = Flask(__name__)
root = os.path.dirname(__file__)
os.chdir(root)

system = platform.system()

# 路径分隔符
file_separator_list = {
    "Windows" : '\\',
    "Linux" : '/'
}

def dir_transfer_to_url(dir_):
    url_ = str()
    url_ = os.path.join('*'.join(dir_.split(file_separator_list[system])))
    url_ = os.path.join('**'.join(url_.split(' ')))
    return url_

def url_transfer_to_dir(url_):
    dir_ = str()
    dir_ = os.path.join(" ".join(url_.split('**')))
    dir_ = os.path.join(file_separator_list[system].join(dir_.split('*')))
    return dir_

def move_media_file_to_staticdir(src, dst, cmd):
    assert(cmd == "copy" or cmd == "ffmpeg")

    try:
        if cmd == 'copy':
            shutil.copyfile(src, dst)
        else:
            trans_cmd = "ffmpeg -i %s %s" % (src, dst)
            os.system(trans_cmd)
    except:
        dst_dir = os.path.dirname(dst)
        for filename in os.listdir(dst_dir):
            try:
                os.remove(os.path.join(dst_dir, filename))
            except:
                continue 

@app.route('/')
def index():
    ip = request.remote_addr
    logging.info('/index ip : %s' % str(ip))
    if g_dict_ip_2_loginstatus.get(ip) is not None and g_dict_ip_2_loginstatus[ip] == True:
        return redirect(url_for('get_dir', abs_src_dir='home'))
    
    if fuck_him:
        return render_template("login.html", fuck_him="GO FUCK YOURSELF")
    else:
        return render_template("login.html", fuck_him="")

@app.route('/login', methods=['GET', 'POST'])
def login():
    ip = request.remote_addr
    user = request.form.get('userid')
    password = request.form.get('password')

    global g_dict_ip_2_user
    g_dict_ip_2_user[ip] = str(user)

    global g_dict_ip_2_loginstatus
    global fuck_him

    if g_dict_ip_2_loginstatus.get(ip) is not None and g_dict_ip_2_loginstatus[ip] == True:
        logging.info('/login ip : %s, user : %s, password : %s Already Login' % (str(ip), user, password))
        return redirect(url_for('get_dir', abs_src_dir='home'))

    if user is not None and g_dict_users_2_pwd.get(user) is not None and password == g_dict_users_2_pwd[user]:
        logging.info('/login ip : %s, user : %s, password : %s Login Success' % (str(ip), user, password))
        g_dict_ip_2_loginstatus[ip] = True
        fuck_him = False
        return redirect(url_for('get_dir', abs_src_dir='home'))
    else:
        logging.info('/login ip : %s, user : %s, password : %s Login Failed' % (str(ip), user, password))
        fuck_him = True
        return redirect(url_for('index'))

@app.route('/get_dir/<abs_src_dir>')
def get_dir(abs_src_dir):
    ip = request.remote_addr
    dict_dir_2_url = dict()
    dict_dir_2_freespace = dict()
    abs_src_dir = url_transfer_to_dir(abs_src_dir)
    
    logging.info('/get_dir ip : %s, user : %s, get_dir : %s' % (str(ip), str(g_dict_ip_2_user.get(ip)), abs_src_dir))
    if g_dict_ip_2_loginstatus.get(ip) is None or g_dict_ip_2_loginstatus[ip] == False:
        return "<h1>GO FUCK YOURSELF</h1>"

    if abs_src_dir == 'home':
        if system == 'Windows':
            free_bytes = ctypes.c_ulonglong(0)
            for char in string.ascii_uppercase:
                disk = char + ':' + file_separator_list[system]
                if os.path.isdir(disk):
                    ctypes.windll.kernel32.GetDiskFreeSpaceExW(ctypes.c_wchar_p(disk), None, None, ctypes.pointer(free_bytes))
                    dict_dir_2_freespace[disk] = str(free_bytes.value / 1024 / 1024 / 1024) + ' GB left'
                    dict_dir_2_url[disk] = dir_transfer_to_url(disk)    # c:\ -> c:*
        elif system == 'Linux':
            st = os.statvfs('/home')
            dict_dir_2_freespace['/home'] = str(st.f_bavail * st.f_frsize / 1024 / 1024 / 1024)  + ' GB left'
            dict_dir_2_url['/home'] = dir_transfer_to_url('/home')  # /home -> *home
        return render_template("index.html", dict_dir_2_url=dict_dir_2_url, dict_dir_2_freespace=dict_dir_2_freespace, file_separator=file_separator_list[system])
    elif os.path.isdir(abs_src_dir):
        abs_src_dir_listdir = os.listdir(abs_src_dir)
        abs_src_dir_listdir.sort()
        for dir in abs_src_dir_listdir:
            under_abs_src_dir = os.path.join(abs_src_dir, dir)
            dict_dir_2_freespace[under_abs_src_dir] = ""
            dict_dir_2_url[under_abs_src_dir] = dir_transfer_to_url(under_abs_src_dir)
        return render_template("index.html", dict_dir_2_url=dict_dir_2_url, dict_dir_2_freespace=dict_dir_2_freespace, file_separator=file_separator_list[system])
    elif os.path.isfile(abs_src_dir):
        file_format = abs_src_dir.split('.')[-1].lower()
        if file_format in ['md', 'c', 'cpp', 'py', 'txt', 'json', 'html', 'log', 'dat', 'ini', 'inf', 'bat', 'sh']:
            file_open = open(abs_src_dir, 'rb')
            file_content = file_open.read()
            charset = chardet.detect(file_content)['encoding']
            resp = make_response(file_content)
            resp.headers["Content-type"]="text/plan;charset=" + charset
            return resp
        elif file_format in ['mp3'] or file_format in ['mp4', 'mkv', 'flv']:
            static_dir = os.path.join(root, 'static')
            static_media_dir = os.path.join(static_dir, 'media')
            if not os.path.exists(static_media_dir):
                os.mkdir(static_media_dir)

            filename = abs_src_dir.split(file_separator_list[system])[-1]
            abs_to_play_dir = os.path.join(static_media_dir, filename)

            to_play_dir = "/static/media/" + filename
            if file_format in ['mp3']:
                if filename not in os.listdir(static_media_dir):
                    move_media_file_to_staticdir(abs_src_dir, abs_to_play_dir, "copy")
                html  = '''
                <audio width=1000 height=500  controls>
                    <source src="%s" type="audio/mp3">
                </audio>
                ''' % (to_play_dir)
            else:
                if not filename.endswith('.mp4'):
                    filename = filename.replace('.' + file_format, '.mp4')
                    if not filename in os.listdir(static_media_dir):
                        abs_to_play_dir = abs_to_play_dir.replace('.' + file_format, '.mp4')
                        move_media_file_to_staticdir(abs_src_dir, abs_to_play_dir, "ffmpeg")
                else:
                    if not filename in os.listdir(static_media_dir):
                        move_media_file_to_staticdir(abs_src_dir, abs_to_play_dir, "copy")

                html  = '''
                <video width=1000 height=500 controls>
                    <source src="%s" type="video/mp4">
                </video>
                ''' % (to_play_dir)

            return html
        elif file_format in ['jpg', 'bmp', 'png', 'ico']:
            to_sava_format = {
                'jpg' : "JPEG",
                'bmp' : "BMP",
                'png' : "PNG",
                'ico' : 'ICO'
            }

            img_io = BytesIO()
            img = Image.open(abs_src_dir)
            image = img.convert('RGB')
            image.save(img_io, to_sava_format[file_format], quality=70)
            img_io.seek(0)
            return send_file(img_io, mimetype='image/' + to_sava_format[file_format].lower())
        elif file_format in ['pdf']:
            abs_src_dir_split = abs_src_dir.split(file_separator_list[system])
            filename = abs_src_dir_split.pop()
            directory = file_separator_list[system].join(abs_src_dir_split)
            return send_from_directory(directory=directory, filename=filename, mimetype='application/pdf')

with open(os.path.join(root, '.log'), 'w') as log:
    try:
        app.run(host='0.0.0.0', port=8088, debug=True)
    except Exception as e:
        logging.info(str(e))
    