from bs4 import BeautifulSoup
import requests
import re


STRING_WIDTH = 80
HREF_TPL = '%url_text% [%url_href%]'


class UniversalParser:
    def __init__(self, url):
        # ссылка на сайт
        self.url = url

        # промежуточные данные
        self._html_page = None
        self._soup = None
        self.header = ''
        self.paragraphs_obj = None
        self.rendered_text = ''

    def get_request(self):
        try:
            response = requests.get(self.url)
        except Exception as e:
            print(f'Ошибка при выполнении запроса:\n{e}')
            self._html_page = None
            return

        try:
            self._html_page = response.text
        except Exception as e:
            print(f'Ошибка при получении текста из запроса:\n{e}')
            self._html_page = None
            return
        return self._html_page

    def get_soup(self):
        if not self._html_page:
            self._soup = None
            return

        self._soup = BeautifulSoup(self._html_page, "html.parser")
        return self._soup

    def get_header(self):
        """Получение заголовка из <h1> либо <meta name="title" content="<Заголовок>">"""
        header = self._soup.body.find('h1')
        if header != None:
            header = header.get_text()
        else:
            header = self._soup.head.find('meta', attrs={'name': 'title'})
            header = header.attrs['content']

        # header = self.remove_white_spaces(header)
        self.header = header
        # print(self.header)

    def get_paragraphs(self):
        """Получение объектов <p> тегов"""
        class_attrs_for_search = '|'.join(['content', 'context', 'article', 'text'])
        content = self._soup.body.findAll(attrs={"class": re.compile(class_attrs_for_search)})
        p_objects = []
        already_used = []
        for item in content:
            paragraphs = item.findAll('p')
            for p in paragraphs:
                if id(p) in already_used:
                    continue
                if len(p.get_text()) < 30:
                    continue
                p_objects += [p]
                already_used.append(id(p))

        self.paragraphs_obj = p_objects
        # print(self.paragraphs_obj)

    def add_to_paragraph_href(self, paragraph_obj):
        for a in paragraph_obj.findAll('a'):
            if a.has_attr('href') and a.string:
                tpl = HREF_TPL
                # todo исправить ссылки с без https://domen
                tpl = tpl.replace('%url_href%', a.attrs['href'])
                tpl = tpl.replace('%url_text%', a.string)
                a.string.replace_with(tpl)

    @staticmethod
    def split_lines(words='', max_len=80):
        """Разбивка строк по указанному размеру"""
        max_len -= 1
        words_list = words.split()
        strings_list = ''
        tmp = ''

        for i in range(len(words_list)):
            tmp_current = '{} {}'.format(tmp, words_list[i])
            tmp_current = tmp_current.strip()

            if len(tmp_current) == max_len:
                strings_list += tmp_current + '\r\n'
                tmp = ''
            elif len(tmp_current) > max_len:
                tmp += '\r\n'
                strings_list += tmp
                tmp = words_list[i]
            elif len(tmp_current) < max_len:
                tmp += ' {}'.format(words_list[i])
                tmp = tmp.strip()

        strings_list += tmp
        return strings_list.strip()

    def split_all_lines(self, strings='', max_len=80):
        string_list = strings.splitlines()
        new_string_list = []
        for i in range(len(string_list)):
            new_string_list.append(self.split_lines(string_list[i], max_len))

        return '\r\n'.join(new_string_list)

    def render_text(self):
        """Преобразование промежуточных данных в текст для сохранения"""

        string_width = STRING_WIDTH

        rendered_text = f'{self.header}\r\n\r\n'

        paragraphs = ''
        for p in self.paragraphs_obj:
            self.add_to_paragraph_href(p)
            p_string = p.get_text()
            paragraphs += f'{p_string}\r\n\r\n'

        rendered_text += f'{paragraphs}\r\n'
        rendered_text = self.split_all_lines(rendered_text, string_width)

        self.rendered_text = rendered_text
        print(self.rendered_text)


if __name__ == "__main__":
    obj = UniversalParser('https://lenta.ru/news/2022/01/27/budushee_rublya/')  # 'https://www.gazeta.ru/army/2022/01/27/14467249.shtml'
    obj.get_request()
    obj.get_soup()
    obj.get_header()
    obj.get_paragraphs()
    obj.render_text()
