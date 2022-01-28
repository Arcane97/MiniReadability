import re


def get_domain_name_from_url(url):
    domain_name_tpl = '://(.*?)/'
    match_domain = re.search(domain_name_tpl, url)
    if match_domain:
        return match_domain.group(1)
    return ''


if __name__ == "__main__":
    url_ = 'https://lenta.ru/news/2022/01/27/budushee_rublya/'
    domain_name = get_domain_name_from_url(url_)
    print(domain_name)
