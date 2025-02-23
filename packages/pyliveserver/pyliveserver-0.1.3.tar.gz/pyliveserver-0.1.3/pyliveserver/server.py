import os
from livereload import Server
from tkinter import filedialog

root = filedialog.askdirectory(initialdir="/home/")
fileExtensions = ['html', 'css', 'js', 'json', 'xml', 'svg','jpg', 'png', 'webp', 'gif', 'mp4', 'mov']

def watch_directories(server, root):
    for root, dirs, files in os.walk(root):
        for ext in fileExtensions:
            patern = os.path.join(root, f'*.{ext}')
            server.watch(patern)
server = Server()



watch_directories(server, root)

server.watch('index.html')
server.serve(root=root, host='127.0.0.1', port=3000, open_url_delay=True)
