'''
Поиск недопереведенной во время локализации кириллицы.
В параметрах - путь к папке проекта, маски для файлов, флаг рекурсивной проверки вложенных папок.
Кириллица игнорируется внутри пайтоновских комментариев (после символа решетки, или между тремя одиночными кавычками).
'''
import argparse
import glob
import re

def check_cyrillic(file_path):
    cyrillic = r'[А-Яа-я]+'
    fl_ok = True
    str_count = 0
    fl_multi_comm = False
    with open(file_path, 'r') as data:  # открываем файл на чтение, читаем построчно, ведем счетчик строк
        for string in data:
            string = string.strip()
            str_count += 1
            if fl_multi_comm:
                if "'''" in string:  # конец многострочного комментария
                    fl_multi_comm = False
                continue

            com_1 = string.find("'''")
            com_2 = string.find("#")
            if com_2 > -1 and (com_2 < com_1 or com_1 == -1):
                string = string.split("#")[0]
            if com_1 > -1 and (com_1 < com_2 or com_2 == -1):
                if len(string.split("'''")) == 2:  # если три одинарные кавычки встречаются в строке больше чем один раз, считаем что многострочный комментарий закончился на этой же строке, без проверок не начался ли следующий тут же
                    fl_multi_comm = True
                string = string.split("'''")[0]
                    
            res = re.search(cyrillic, string)
            if res:
                if fl_ok:
                    print(file_path)
                    fl_ok = False
                print(str_count, '\t', res.group(0) + '...', '\t', string)
        if not fl_ok:
            print()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Поиск кириллицы в файлах проекта.')
    parser.add_argument('-p', '--path', type=str, default='.', help='Путь до проекта, по умолчанию - .')
    parser.add_argument('-m', '--masks', type=str, default='*.py,*.html', help='Шаблоны имен файлов, по умолчанию - *.py,*.html')
    parser.add_argument('-r', '--recursive', type=bool, default=False, help='Рекурсивный поиск, по умолчанию - False')
    args = parser.parse_args()
    dir_path = args.path
    file_patterns = args.masks.split(',')
    for p in file_patterns:
        if args.recursive: 
            file_param = dir_path + '/**/' + p
        else:
            file_param = dir_path + '/' + p
        files = glob.glob(file_param, recursive=args.recursive)
        if len(files) == 0:
            print('По пути ' + file_param + ' не найдено ни одного файла.\n')
        for f in files:
            check_cyrillic(f)
    
