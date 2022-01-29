import os
import re


class FileSaver:
    """ Класс сохраняющий текст в файл.
        Может создавать путь файла на основе url (метод create_path_from_url),
        также можно задать пусть явно в конструкторе или в поле path.

        Использование:
        file_saver = FileSaver('https://domen.ru/news/page.html')
        file_saver.create_path_from_url()
        text = 'example text'
        file_saver.save(text)
    """
    def __init__(self, url='', path='', folder='saved_pages'):
        """
        :param url:
        :param path:
        :param folder:
        """
        self.url = url
        self.path = path
        self.folder = folder

        self._cur_dir = os.path.join(os.getcwd(), self.folder)

    def create_path_from_url(self):
        """ Создание пути из url для сохранения страницы.
        """
        url_cut = re.findall(r'.*://(.*)', self.url)[0]

        if url_cut.endswith('/'):
            url_cut = url_cut[:-1]

        directory, file_name = os.path.split(url_cut)
        if file_name.find('.') != '-1':
            file_name = re.sub(r'\.(.*)', '.txt', file_name)
        else:
            file_name += '.txt'

        path = os.path.join(self._cur_dir, directory, file_name)
        self.path = os.path.abspath(path)

    def save(self, text):
        """ Сохранение в файл.
        :param text: (str) текст.
        """
        directory, file_name = os.path.split(self.path)
        if directory and not os.path.isdir(directory):
            os.makedirs(directory)

        if self.path != '':
            print(f'Сохраняем в {self.path}')
        else:
            print('Введите путь для сохранения')
            return

        text = text.encode('UTF-8')

        with open(self.path, 'wb') as f:
            f.write(text)


if __name__ == "__main__":
    obj = FileSaver('https://www.gazeta.ru/army/2022/01/27/14467249.shtml')
    obj.create_path_from_url()
    obj.save('123')
