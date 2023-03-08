import subprocess
import os


def get_zip_archive(file_name, folder_name, archive_folder):
    archive_path = os.path.join(os.getcwd(), archive_folder)
    file_path = os.path.join(archive_path, file_name)
    os.makedirs(archive_folder, exist_ok=True)
    process = subprocess.run(
        ['zip', '-r', f'{file_path}', f'{folder_name}'],
        capture_output=True,
    )
    if process.returncode:
        raise ValueError('Archive process has problems, check dependencies!')


def unpack_archive(file_name, folder_name, archive_folder):
    """Распакаовка архива в папку folder_name текущей директории"""
    archive_path = os.path.join(os.getcwd(), archive_folder)
    unpacking_file_path = os.path.join(archive_path, file_name)
    file_path = os.path.join(os.getcwd(), folder_name)
    os.makedirs(file_path, exist_ok=True)
    try:
        process = subprocess.run(
            ['unzip', f'{unpacking_file_path}', '-d', f'{file_path}'],
            capture_output=True,
            timeout=2
        )
    except subprocess.TimeoutExpired:
        print('Архив уже распакован')


if __name__ == '__main__':
    ARCHIVE_FOLDER = 'archives'
    get_zip_archive('photo.zip', 'original_photo', ARCHIVE_FOLDER)
    unpack_archive('photo.zip', 'unpack_archive', ARCHIVE_FOLDER)
