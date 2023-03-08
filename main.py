import subprocess
import os


def get_zip_archive(folder_name, archive_folder, file_name=None):

    if file_name:
        archive_path = os.path.join(os.getcwd(), archive_folder)
        file_path = os.path.join(archive_path, file_name)
        os.makedirs(archive_folder, exist_ok=True)
        process = subprocess.run(
            ['zip', '-r', f'{file_path}', f'{folder_name}'],
            capture_output=True,
        )
    else:
        process = subprocess.run(
            ['zip', '-r', '-', f'{folder_name}'],
            capture_output=True,
        )

    if process.returncode:
        raise ValueError('Archive process has problems, check dependencies!')

    return process.stdout


def unpack_archive(file_name, folder_name, archive_folder):
    """
    Распаковка архива file_name в папку folder_name текущей директории
    из папки archive_folder
    """

    archive_path = os.path.join(os.getcwd(), archive_folder)
    unpacking_file_path = os.path.join(archive_path, file_name)
    if os.path.isfile(unpacking_file_path):
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
    ARCHIVE_FILE = 'ppp.zip'
    get_zip_archive('original_photo', ARCHIVE_FOLDER, file_name=None)
    unpack_archive(ARCHIVE_FILE, 'unpack_archive', ARCHIVE_FOLDER)
