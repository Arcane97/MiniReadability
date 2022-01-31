# перенос строки
ENDL = '\r\n'


class UniversalParserConfig:
    # ------------------------ настройки шаблонов форматирования исходного текста статьи
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

    # настройки для поиска тегов и имён классов html
    # словарь вида: {
    #               "domain1.com": {                ключ: нужно указать домен, это всё между "https://" и следующего "/"
    #                   "tags_for_delete":          теги, которые будут удалены,
    #                   "class_attrs_for_delete":   имена классов html, которые будут удалены,
    #                   "tags_for_search":          теги, в которых будет искаться контент,
    #                   "class_attrs_for_search":   имена классов html, в которых будет искаться контент
    #               },
    #               "www.domain2.ru": {...}, ... }
    tag_processing_settings = {
        "default": {
            "tags_for_delete": ['script', 'noscript', 'style', 'noindex', 'form', 'img', 'figcaption'],
            "class_attrs_for_delete": ['social', 'reg', 'auth', 'footer', 'banner', 'mobile', 'comment', 'preview',
                                       'inject', 'incut', 'infoblock'],
            "tags_for_search": ['p'],
            "class_attrs_for_search": ['content', 'context', 'article', 'text']
        },

        "www.forbes.ru": {
            "tags_for_delete": ['script', 'noscript', 'style', 'noindex', 'form', 'img', 'figcaption'],
            "class_attrs_for_delete": ['social', 'reg', 'auth', 'footer', 'banner', 'mobile', 'comment', 'preview',
                                       'inject', 'incut', 'infoblock', '_1614F _3Mele'],
            "tags_for_search": ['p', 'strong', 'h2'],
            "class_attrs_for_search": ['_2LS9B']  # у forbes действительно так называется классы
        },

    }
