import subprocess
from asyncio.subprocess import create_subprocess_shell, create_subprocess_exec
import asyncio
import aiofiles
import os
from asgiref.sync import sync_to_async


def get_zip_archive(original_folder, archive_folder, file_archive_name=None):

    if file_archive_name:
        archive_path = os.path.join(os.getcwd(), archive_folder)
        file_path = os.path.join(archive_path, file_archive_name)
        os.makedirs(archive_folder, exist_ok=True)
        process = subprocess.run(['zip', '-r', f'{file_path}', f'{original_folder}'])
        func_return = None
    else:
        process = subprocess.run(
            ['zip', '-r', '-', f'{original_folder}'],
            capture_output=True,
        )
        func_return = process.stdout

    if process.returncode:
        raise ValueError('Archive process has problems, check dependencies!')

    return func_return


async def get_binary_zip_archive(original_folder, kb):
    byte = 1024 * kb
    all_stdout = bytes()
    cmd = f'zip -r - {" ".join(os.listdir(original_folder))}'
    process = await create_subprocess_shell(
        cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
        cwd=original_folder
    )
    while True:
        stdout = await process.stdout.read(byte)
        all_stdout += stdout
        if process.stdout.at_eof():
            break

    return all_stdout


async def write_binary_archive_to_zip(binary_archive, file_archive_name, archive_folder):
    """Запись байтового архива в файл"""

    file_path = os.path.join(os.getcwd(), archive_folder)
    os.makedirs(file_path, exist_ok=True)
    file = os.path.join(file_path, file_archive_name)
    async with aiofiles.open(file, 'wb') as binary_file:
        await binary_file.write(binary_archive)


def unpack_archive(file_archive_name, unpack_folder, archive_folder):
    """
    Распаковка архива file_name в папку folder_name текущей директории
    из папки archive_folder
    """

    archive_path = os.path.join(os.getcwd(), archive_folder)
    unpacking_file_path = os.path.join(archive_path, file_archive_name)
    if os.path.isfile(unpacking_file_path):
        file_path = os.path.join(os.getcwd(), unpack_folder)
        os.makedirs(file_path, exist_ok=True)
        try:
            subprocess.run(
                ['unzip', f'{unpacking_file_path}', '-d', f'{file_path}'],
                capture_output=True,
                timeout=2
            )
        except subprocess.TimeoutExpired:
            print('Архив уже распакован')


async def a_unpack_archive(file_archive_name, unpack_folder, archive_folder):
    """
    Распаковка архива file_name в папку folder_name текущей директории
    из папки archive_folder
    """

    unpacking_file_path = os.path.join(os.getcwd(), archive_folder, file_archive_name)
    file_path = os.path.join(os.getcwd(), unpack_folder)
    os.makedirs(file_path, exist_ok=True)
    cmd = f'unzip {unpacking_file_path} -d {file_path}'
    await create_subprocess_shell(cmd)


async def main():
    # archive = get_zip_archive(ORIGINAL_FOLDER, ARCHIVE_FOLDER, file_archive_name=None)
    archive = await get_binary_zip_archive(ORIGINAL_FOLDER, 300)
    await write_binary_archive_to_zip(archive, ARCHIVE_FILE, ARCHIVE_FOLDER)
    await sync_to_async(unpack_archive)(ARCHIVE_FILE, UNPACK_FOLDER, ARCHIVE_FOLDER)


if __name__ == '__main__':
    ARCHIVE_FOLDER = 'archives'
    ARCHIVE_FILE = 'archive.zip'
    UNPACK_FOLDER = 'unpack_archive'
    ORIGINAL_FOLDER = 'original_photo'
    asyncio.run(main())
