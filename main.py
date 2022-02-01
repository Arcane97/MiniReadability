import sys

from file_saver import FileSaver
from universal_parser import UniversalParser


if len(sys.argv) < 2:
    print('Ошибка! Введите ссылку через пробел после названия скрипта')
    exit()

url = sys.argv[1]

parser = UniversalParser(url)
parser.parse_page()
text = parser.formatted_text

saver = FileSaver(url)
saver.create_path_from_url()
saver.save(text)
