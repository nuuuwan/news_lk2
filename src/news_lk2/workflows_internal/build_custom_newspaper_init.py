import os

from utils import File, hashx, timex

DIR_CUSTOM_NEWSPAPERS = 'src/news_lk2/custom_newspapers'
INIT_FILE_ONLY = '__init__.py'


def get_class_name_list():
    class_name_list = []
    for file_only in os.listdir(DIR_CUSTOM_NEWSPAPERS):
        if file_only[-3:] != '.py':
            continue
        if file_only == INIT_FILE_ONLY:
            continue
        class_name = file_only[:-3]
        class_name_list.append(class_name)
    class_name_list = sorted(class_name_list, key=lambda x: x.lower())
    return class_name_list


def build_init(class_name_list):
    lines = []
    hash = hashx.md5(str(class_name_list))
    lines.append('# Auto-Generated with build_custom_newspaper_init.py')
    timex.get_time_id()
    lines.append(f'# {hash}')

    lines += list(
        map(
            lambda x: f'from news_lk2.custom_newspapers.{x} import {x}',
            class_name_list,
        )
    )
    lines.append('')
    lines.append('newspaper_class_list = [')
    lines += list(
        map(
            lambda x: f'    {x},',
            class_name_list,
        )
    )
    lines.append(']')
    lines.append('')

    init_file_name = os.path.join(DIR_CUSTOM_NEWSPAPERS, INIT_FILE_ONLY)
    File(init_file_name).write_lines(lines)


def main():
    class_name_list = get_class_name_list()
    build_init(class_name_list)


if __name__ == '__main__':
    main()
