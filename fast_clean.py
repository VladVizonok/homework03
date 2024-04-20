import re 
import shutil
import sys
from pathlib import Path
from threading import Thread

main_folder = Path(sys.argv[1])
folders = []

# Створюємо папки для сортування.
folder_list = ['images', 'video', 'documents', 'audio', 'archive', 'other']

image_dir = Path(f'{main_folder}/images')
image_dir.mkdir(exist_ok=True)

video_dir = Path(f'{main_folder}/video')
video_dir.mkdir(exist_ok=True)

documents_dir = Path(f'{main_folder}/documents')
documents_dir.mkdir(exist_ok=True)

audio_dir = Path(f'{main_folder}/audio')
audio_dir.mkdir(exist_ok=True)

archive_dir = Path(f'{main_folder}/archive')
archive_dir.mkdir(exist_ok=True)

other_dir = Path(f'{main_folder}/other')
other_dir.mkdir(exist_ok=True)

# Створюємо словник розширень
folder_dict = {
    'image' : ['JPEG', 'PNG', 'JPG', 'SVG'],
    'video' : ['AVI', 'MP4', 'MOV', 'MKV'],
    'documents' : ['DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX'],
    'audio' : ['MP3', 'OGG', 'WAV', 'AMR'],
    'archive' : ['ZIP', 'GZ', 'TAR'],
}


def normalize(file_name):
    CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
    TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
                    "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g")

    TRANS = {}
    for key, value in zip(CYRILLIC_SYMBOLS, TRANSLATION):
        TRANS[ord(key)] = value
        TRANS[ord(key.upper())] = value.upper()

    file_name, *extencion = file_name.name.split('.')
    new_file_name = re.sub(r'\W', '_', file_name).translate(TRANS)

    return f"{new_file_name}.{'.'.join(extencion)}"

def get_extencion(file_name):
    return Path(file_name).suffix[1:].upper()

def manage_archive(archive_name, extencion):

    # Нормалізуємо імʼя архіву та видаляємо формат файлу для створення імʼя папки 

    new_archive_name = normalize(archive_name).replace(f'.{extencion.lower()}', '') 
    archive_folder = archive_dir/new_archive_name
    archive_folder.mkdir(exist_ok=True)

    # Розпаковуємо архів 

    try:
        shutil.unpack_archive(str(archive_name.resolve()), str(archive_folder.resolve()))
    except shutil.ReadError:
        archive_folder.rmdir()
        return
    except FileNotFoundError:
        archive_folder.rmdir()
        return
    archive_name.unlink()

def remove_empty_folder(folder_name):
    for item in folder_name.iterdir():
        if item.is_dir() and item.name not in folder_list:
            remove_empty_folder(item)
            try:
                item.rmdir()
            except FileNotFoundError:
                pass
            except OSError:
                pass
                
def grabs_folder(path: Path) -> None:
    for el in path.iterdir():
        if el.is_dir():
            folders.append(el)
            grabs_folder(el)

def main(folder_for_sort=main_folder):
    
    for file in folder_for_sort.iterdir():
        try:
            if file.name in folder_list:
                continue

        # Рекурсивно перевіряємо папки та видаляємо пусті
            if file.is_dir:
                try:
                    main(file)
                except NotADirectoryError:
                    pass
            remove_empty_folder(folder_for_sort)

        # Сортуємо файли за їх розширеннями 

            if get_extencion(file) in folder_dict['image']:
                file.replace(image_dir/normalize(file))

            if get_extencion(file) in folder_dict['video']:
                file.replace(video_dir/normalize(file))

            if get_extencion(file) in folder_dict['documents']:
                file.replace(documents_dir/normalize(file))

            if get_extencion(file) in folder_dict['audio']:
                file.replace(audio_dir/normalize(file))

            if get_extencion(file) in folder_dict['archive']:
                manage_archive(file, get_extencion(file))
            else:
                try:   
                    file.replace(other_dir/normalize(file))
                except FileNotFoundError:
                    continue
                except OSError:
                    continue
        except FileNotFoundError:
            continue
  
if __name__ == '__main__':
    main_folder = Path(sys.argv[1])
    folders.append(main_folder)
    grabs_folder(main_folder)

for folder in folders:
    th = Thread(target=main, args=(folder,))
    th.start()




  