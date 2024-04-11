import os
import re

def get_filenames(folder_path):
    filenames = []
    if os.path.exists(folder_path):
        files = os.listdir(folder_path)
        filenames = [file for file in files if os.path.isfile(os.path.join(folder_path, file))]
    return filenames

def generate_img_tag(filename):
    return '<img src="{%% static \'znaki/%s\' %%}" draggable="true" ondragstart="setDragData(event)" />' % filename

# Путь к вашей папке с файлами
folder_path = '/home/yaroslav/rally_obidience/static/znaki'
filenames = get_filenames(folder_path)

# Сортировка имен файлов
sorted_filenames = sorted(filenames, key=lambda x: (not re.search(r'№(\d+)', x), int(re.search(r'№(\d+)', x).group(1)) if re.search(r'№(\d+)', x) else (False, float('inf'))))

# Печать HTML-тега <img> для каждого отсортированного имени файла
for filename in sorted_filenames:
    print(generate_img_tag(filename))
