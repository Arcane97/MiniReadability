from bs4 import BeautifulSoup
import requests
import re

from utils import get_domain_name_from_url


ENDL = '\r\n'
STRING_WIDTH = 80
HREF_TEMPLATE = '%url_text% [%url_href%]'
TAGS_FOR_DELETE = ['script', 'noscript', 'style', 'noindex', 'form', 'img']
CLASS_ATTRS_FOR_DELETE = ['social', 'reg', 'auth', 'footer', 'banner', 'mobile', 'comment', 'preview', 'inject', 'incut', 'infoblock']
CLASS_ATTRS_FOR_SEARCH = ['content', 'context', 'article', 'text']


class UniversalParser:
    """ Класс для парсинга сайтов со статьями.
    Парсит заголовок и абзацы.
    """
    def __init__(self, url: str):
        """
        :param url: ссылка на сайт вида: 'https://lenta.ru/news/2022/01/27/budushee_rublya/'
        """
        # ссылка на сайт
        self.url = url

        self._string_width = STRING_WIDTH

        # html код старицы (str)
        self._html_page = ''
        # BeautifulSoup объект страницы
        self._soup_obj = None
        # заголовок страницы (str)
        self._header = 'Заголовок'
        # список объектов абзацев [bs4.element.Tag, ]
        self._paragraphs_obj_list = []
        # отформатированный текст
        self.formatted_text = ''

    def _send_request(self):
        """ Отправка запроса для получения страницы
        """
        try:
            response = requests.get(self.url)
        except Exception as e:
            print(f'Ошибка при выполнении запроса:{ENDL}{e}')
            self._html_page = None
            return

        try:
            self._html_page = response.text
        except Exception as e:
            print(f'Ошибка при получении текста из запроса:{ENDL}{e}')
            self._html_page = None

    def _create_soup_obj(self):
        """ Создание объекта BeautifulSoup
        """
        if not self._html_page:
            self._soup_obj = None
            return

        self._soup_obj = BeautifulSoup(self._html_page, "html.parser")

    def _delete_unnecessary_tags(self):
        """ Удаление не нужных тегов из супа.
        """
        tags_for_delete = TAGS_FOR_DELETE
        class_attrs_for_search = '|'.join(CLASS_ATTRS_FOR_DELETE)

        if tags_for_delete:
            for tag in self._soup_obj.body.findAll(tags_for_delete):
                tag.extract()

        if class_attrs_for_search:
            for tag in self._soup_obj.body.findAll(attrs={'class': re.compile(class_attrs_for_search)}):
                tag.extract()

    def _find_header_from_soup(self):
        """ Нахождение заголовка из self._soup_obj
        """
        header = self._soup_obj.body.find('h1')
        if header is not None:
            header = header.get_text()
        else:
            header = self._soup_obj.head.find('meta', attrs={'name': 'title'})
            header = header.attrs['content']

        self._header = header

    def _find_paragraphs(self):
        """ Нахождение тегов (bs4.element.Tag) с абзацами
        """
        class_attrs_for_search = '|'.join(CLASS_ATTRS_FOR_SEARCH)
        content_pattern = re.compile(class_attrs_for_search)
        content = self._soup_obj.body.findAll(attrs={"class": content_pattern})
        p_objects = []
        already_used = []

        for item in content:
            paragraphs = item.findAll('p')
            for p in paragraphs:
                if id(p) in already_used:
                    continue
                p_objects.append(p)
                already_used.append(id(p))

        self._paragraphs_obj_list = p_objects

    def _add_to_paragraph_href(self, paragraph_obj):
        """ Добавление в текст объекта параграфа URL в квадратных скобках
        :param paragraph_obj: bs4.element.Tag
        """
        for a in paragraph_obj.findAll('a'):
            if a.has_attr('href') and a.string:
                href_template = HREF_TEMPLATE
                href = a.attrs['href']
                if href[0] == '/':
                    href = f'https://{get_domain_name_from_url(self.url)}{href}'
                href_template = href_template.replace('%url_href%', href)
                href_template = href_template.replace('%url_text%', a.string)
                a.string.replace_with(href_template)

    def _split_paragraph(self, paragraph=''):
        """ Разбивка одного абзаца по указанному размеру self._string_width.
        :param paragraph: абзац.
        :return: строка разбитая по максимальной длине
        """
        max_len = self._string_width
        words_list = paragraph.split()
        formatted_paragraph = ''
        tmp = ''

        for word in words_list:
            current_tmp = f'{tmp} {word}'.strip()

            if len(current_tmp) == max_len:
                formatted_paragraph += f'{current_tmp}{ENDL}'
                tmp = ''
            elif len(current_tmp) > max_len:
                formatted_paragraph += f'{tmp}{ENDL}'
                tmp = word
            else:  # len(tmp_current) < max_len
                tmp = current_tmp

        formatted_paragraph += tmp
        return formatted_paragraph.strip()

    def _split_all_paragraphs(self, paragraphs=''):
        """ Разбивка всех абзацев по указанному размеру.
        :param paragraphs: абзацы.
        :return:
        """
        string_list = paragraphs.splitlines()
        new_string_list = []
        for string in string_list:
            new_string_list.append(self._split_paragraph(string))

        return ENDL.join(new_string_list)

    def _formate_text(self):
        """ Форматирование промежуточных данных в текст для сохранения
        """
        # todo сделать возможность использования шаблонов
        # добавление заголовка
        rendered_text = f'{self._header}{2 * ENDL}'
        paragraphs = ''

        # добавление абзацев
        for p_obj in self._paragraphs_obj_list:
            self._add_to_paragraph_href(p_obj)
            p_string = p_obj.get_text()
            paragraphs += f'{p_string}{2*ENDL}'
        rendered_text += f'{paragraphs}{ENDL}'

        # разбиение на максимальную длину
        rendered_text = self._split_all_paragraphs(rendered_text)

        self.formatted_text = rendered_text

    def parse_page(self):
        """ Парсинг страницы
        """
        # todo добавить оповещение пользователя о состоянии работы
        self._send_request()
        self._create_soup_obj()
        if self._soup_obj is not None:
            self._delete_unnecessary_tags()
            self._find_header_from_soup()
            self._find_paragraphs()
            self._formate_text()


if __name__ == "__main__":
    lenta_url = 'https://lenta.ru/news/2022/01/27/budushee_rublya/'
    gazeta_url = 'https://www.gazeta.ru/politics/2022/01/29/14476321.shtml'
    obj = UniversalParser(gazeta_url)
    obj.parse_page()
    text_ = obj.formatted_text
    print(text_)
