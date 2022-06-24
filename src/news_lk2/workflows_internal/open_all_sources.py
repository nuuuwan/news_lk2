import os

from news_lk2.custom_newspapers import newspaper_class_list


def main():
    for newspaper_class in newspaper_class_list:
        for url in newspaper_class.get_index_urls():
            os.system(f'open -a firefox {url}')


if __name__ == '__main__':
    main()
