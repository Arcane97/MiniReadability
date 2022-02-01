# MiniReadability
Тестовое задание для Тензор.

Программа парсит сайты с новостями и статьями, игнорируя рекламу, навигацию, получая 
сам текст статьи. И сохраняет результат в текстовый файл.

___
### Зависимости
Используемые библиотеки находятся в файле requirements.txt.

Чтобы установить библиотеки, используйте в консоли:
```console
pip install -r requirements.txt
```
___
### Использование
Исполняемый файл main.py

Чтобы запустить программу введите в консоль:
```console
python main.py https://www.domain.ru/news/article.html
```
Если текста нет, значит дефолтный конфиг не подошёл. 
Нужно добавить в конфиг настройки для поиска тегов и имён классов **tag_processing_settings**
для введенного сайта.
___

### Алгоритм
* Получение html страницы с помощью библиотеки requests
* Преобразование html страницы в объект класса BeautifulSoup из библиотеки bs4
* Удаление ненужных мешающих тегов, по их названию **tags_for_delete**, 
и по названию классов **class_attrs_for_delete**. 
Теги и названия классов для удаления можно задать в файле config.py
* Получение заголовка статьи. Заголовок ищется в теге `<h1>` или `<meta name="title">` 
* Получение текста статьи из тегов с названием **tags_for_search** и 
в тегах с именами классов **class_attrs_for_search**. 
Теги и названия классов для поиска можно задать в файле config.py
* Форматирование текста по заданным шаблонам форматирования. 
Шаблоны форматирования можно задать в файле config.py
* Сохранение статьи в текстовый файл. Имя выходного файла формируется автоматически по URL.
___

### Класс UniversalParser
Основной класс программы. В нём реализовано получение html страницы, 
очистка от ненужных тегов, поиск заголовка и абзацев, форматирование текста.
Класс получает на вход ссылку на сайт (url), с которого будет парситься текст.


#### Использование класса UniversalParser
```python
parser = UniversalParser(url)
parser.parse_page()
text = parser.formatted_text
```
___

### Класс FileSaver
Класс сохраняющий текст в файл.
Может создавать путь файла на основе url (метод create_path_from_url),
также можно задать путь явно в конструкторе или в поле path.

#### Использование класса FileSaver
```python
saver = FileSaver(url)
saver.create_path_from_url()
saver.save(text)

```
___

### config.py - Класс UniversalParserConfig 


Настройки шаблонов форматирования исходного текста статьи:
```python
# Ширина строки
string_width = 80
# Шаблон форматирования ссылок. %url_text% - текст ссылки. %url_href% - адрес ссылки.
href_template = '%url_text% [%url_href%]'
# Шаблон форматирования заголовка. %header% - текст заголовка.
header_template = f'%header%{2*ENDL}'
# Шаблон форматирования статьи. %article% - весь текст статьи.
article_template = f'%article%{ENDL}'
# Шаблон форматирования абзаца. %paragraph% - текст параграфа.
paragraph_template = f'%paragraph%{2*ENDL}'
```
Настройки для поиска тегов и имён классов html:
```
tag_processing_settings =  {
"domain1.com": {               ключ: нужно указать домен, это всё между "https://" и следующего "/"
   "tags_for_delete":          теги, которые будут удалены,
   "class_attrs_for_delete":   имена классов html, которые будут удалены,
   "tags_for_search":          теги, в которых будет искаться контент,
   "class_attrs_for_search":   имена классов html, в которых будет искаться контент
},
"www.domain2.ru": {...}, 
... 
}
```

___

### Список URL, на которых проверено решение:
* https://lenta.ru/news/2022/01/27/budushee_rublya/  -> [текст](saved_pages/lenta.ru/news/2022/01/27/budushee_rublya.txt) 
* https://www.gazeta.ru/politics/2022/01/29/14476321.shtml -> [текст](saved_pages/www.gazeta.ru/politics/2022/01/29/14476321.txt)
* https://tass.ru/ekonomika/13568909 -> [текст](saved_pages/tass.ru/ekonomika/13568909.txt)
* https://www.forbes.ru/society/453925-kak-vyrosla-ekonomika-ssa-pri-dzo-bajdene -> [текст](saved_pages/www.forbes.ru/society/453925-kak-vyrosla-ekonomika-ssa-pri-dzo-bajdene.txt)
* https://www.forbes.ru/tekhnologii/453891-kriptovalutnyj-kurs-mogut-li-minfin-i-cb-dogovorit-sa-o-sud-be-cifrovyh-aktivov 
-> [текст](saved_pages/www.forbes.ru/tekhnologii/453891-kriptovalutnyj-kurs-mogut-li-minfin-i-cb-dogovorit-sa-o-sud-be-cifrovyh-aktivov.txt)
* https://ufa1.ru/text/gorod/2022/01/31/70411958/ -> [текст](saved_pages/ufa1.ru/text/gorod/2022/01/31/70411958.txt)

Результаты находятся в папке /saved_pages/.
___


### Направления дальнейшего улучшения
Можно сделать некого бота, который бы искал интересные новости или статьи по заданным сайтам.
Бот бы искал статьи по популярности и по заданным категориям.
Также реализовать отправку статей в соцсети. 
___