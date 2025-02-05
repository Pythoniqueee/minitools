import os
import easygui
import shutil

file_etx = ["xls", "xlsx", "doc", "docx", "ppt", "pptx", "txt"]
bin_music_etx = ["mp3", "vwm"]
bin_video_etx = ["mp4", "mpeg", "mpeg-2", "mpeg-4"]
iso_image = ["iso", "ISO", "img", "IMG"]
soft_etx = ["exe", "msi"]
comp_etx = ["rar", "zip"]


def move_file():
    folder_path = easygui.diropenbox("Please select your source path: ")
    dst_path = easygui.diropenbox("Please select your destination path: ")
    folder_name = input("Create your folder name: ")

    show_files = os.listdir(folder_path)
    try:
        for file in show_files:
            file_split = str.strip(file).split(sep=".")

            if file_split[-1] in file_etx:
                shutil.move(os.path.join(folder_path, file), os.path.join(dst_path))
    except Exception as e:
        print(e)


def move_music():
    pass


def move_pictures():
    pass


def move_images():
    pass


def move_softwares():
    pass


if __name__ == '__main__':
    move_file()
