import os
import sys


def count_different_bits(file1, file2):
    with open(file1, 'rb') as f1, open(file2, 'rb') as f2:
        different_bits = 0

        while True:
            byte1 = f1.read(1)
            byte2 = f2.read(1)

            if not byte1 and not byte2:
                break  # Оба файла достигли конца
            elif byte1 and byte2:
                difference = ord(byte1) ^ ord(byte2)
                different_bits += bin(difference).count('1')
            else:
                # файлы разной длины, добавляем различия в оставшихся байтах
                different_bits += 1

        return different_bits


def compare_directories(dir1, dir2):
    # Получаем список файлов в директориях
    files_1 = [os.path.join(dir1, f) for f in os.listdir(dir1)]
    files_2 = [os.path.join(dir2, f) for f in os.listdir(dir2)]

    identical_files = []
    similar_files = []
    dir1_only_files = []
    dir2_only_files = []

    idn_or_sim_files = []  # можно добавлять все в один список, потому что используем полные названия файлов

    for file_1 in files_1:
        for file_2 in files_2:
            different_bits = count_different_bits(file_1, file_2)
            if different_bits == 0:
                identical_files.append([file_1, file_2])
                idn_or_sim_files.append(file_1)
                idn_or_sim_files.append(file_2)
            else:
                size_1 = os.path.getsize(file_1)
                size_2 = os.path.getsize(file_2)
                max_size = max(size_1, size_2)
                coincidence = (max_size - different_bits) / max_size * 100  # совпадение файлов в процентах

                if coincidence >= 80:  # граница, больше которой файлы считаются похожими
                    similar_files.append([file_1, file_2, round(coincidence, 2)])
                    idn_or_sim_files.append(file_1)
                    idn_or_sim_files.append(file_2)

    for file in files_1:
        if file not in idn_or_sim_files:
            dir1_only_files.append(file)

    for file in files_2:
        if file not in idn_or_sim_files:
            dir2_only_files.append(file)

    return identical_files, similar_files, dir1_only_files, dir2_only_files


if __name__ == "__main__":

    dir_1 = input("Введите полное название первой директории: ")
    while not (os.path.exists(dir_1) and os.path.isdir(dir_1)):
        print(f"Директория {dir_1} не существует или не является директорией.")
        dir_1 = input("Введите полное название первой директории: ")

    dir_2 = input("Введите полное название второй директории: ")
    while not (os.path.exists(dir_2) and os.path.isdir(dir_2)):
        print(f"Директория {dir_2} не существует или не является директорией.")
        dir_2 = input("Введите полное название второй директории: ")

    identical, similar, only_dir1, only_dir2 = compare_directories(dir_1, dir_2)

    print("\nИдентичные файлы в формате [file_1, file_2]:")
    for file in identical:
        print(file)

    print("\nПохожие файлы в формате [file_1, file_2, совпадение в %]:")
    for file in similar:
        print(file)

    print("\nФайлы только в директории 1:")
    for file in only_dir1:
        print(file)

    print("\nФайлы только в директории 2:")
    for file in only_dir2:
        print(file)
