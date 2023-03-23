import requests
import codecs
import time
from bs4 import BeautifulSoup as BS
from selenium import webdriver
from random import randint

__all__ = ('work_ua', 'rabota_ua', 'dou_ua', 'djinni_co')

headers = [
    {'User-Agent': 'Mozilla/5.0 (Windows NT 5.1; rv:47.0) Gecko/20100101 Firefox/47.0',
     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'},
    {
        'User-Agent': 'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'},
    {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:53.0) Gecko/20100101 Firefox/53.0',
     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}
]


def work_ua(url, city=None, language=None):
    jobs: list = []
    errors: list = []
    domain: str = 'https://www.work.ua'
    # url: str = 'https://www.work.ua/jobs-kyiv-python/'
    if url:
        work_request = requests.get(url, headers=headers[randint(0, 2)])
        if work_request.status_code == 200:
            soup = BS(work_request.content, 'html.parser')
            main_div = soup.find('div', attrs={'id': 'pjax-job-list'})
            if main_div:
                div_list = main_div.find_all('div', attrs={'class': 'job-link'})
                for div in div_list:
                    title = div.find('h2')
                    href = title.a['href']
                    description = div.p.text
                    company = 'No name'
                    logo = div.find('img')
                    if logo:
                        company = logo['alt']
                    jobs.append(
                        {'title': title.text,
                         'url': domain + href,
                         'description': description,
                         'company': company,
                         'city_id': city,
                         'language_id': language})
                else:
                    errors.append({'url': url, 'title': 'div does not exists'})
            else:
                errors.append({'url': url, 'title': 'Page do not response'})
        return jobs, errors


def rabota_ua(url, city=None, language=None):
    jobs: list = []
    errors: list = []
    domain: str = 'https://rabota.ua'
    # url: str = 'https://rabota.ua/ua/zapros/python/%D0%BA%D0%B8%D0%B5%D0%B2'
    if url:
        driver = webdriver.Chrome()
        driver.get(url)
        time.sleep(10)
        rabota_ua_request = requests.get(url, headers=headers[randint(0, 2)])
        if rabota_ua_request.status_code == 200:
            soup = BS(driver.page_source, 'html.parser')
            main_div = soup.find('div', attrs={'class': 'santa-flex santa-flex-col santa-gap-y-20'})
            if main_div:
                div_list = main_div.find_all('div', attrs={'class': 'santa--mb-20 ng-star-inserted santa-min-h-0'})
                for div in div_list:
                    title = div.find('h2')
                    href = div.a['href']
                    description = div.span.text
                    company = 'No name'
                    logo = div.find('img')
                    if logo:
                        company = logo['alt']
                        jobs.append(
                            {'title': title.text,
                             'url': domain + href,
                             'description': description,
                             'company': company,
                             'city_id': city,
                             'language_id': language})
                    else:
                        errors.append({'url': url, 'title': 'div does not exists'})
            else:
                errors.append({'url': url, 'title': 'There are no vacancies for your request yet'})
        else:
            errors.append({'url': url, 'title': 'Page do not response'})
    return jobs, errors


def dou_ua(url, city=None, language=None):
    jobs: list = []
    errors: list = []
    domain: str = 'https://jobs.dou.ua'
    # url: str = 'https://jobs.dou.ua/vacancies/?category=Python'
    if url:
        dou_ua_request = requests.get(url, headers=headers[randint(0, 2)])
        if dou_ua_request.status_code == 200:
            soup = BS(dou_ua_request.content, 'html.parser')
            main_div = soup.find('div', id='vacancyListId')
            if main_div:
                li_list = main_div.find_all('li', attrs={'class': 'l-vacancy'})
                for li in li_list:
                    if '__hot' not in li['class']:
                        title = li.find('div', attrs={'class': 'title'})
                        href = title.a['href']
                        content = li.find('div', attrs={'class': 'sh-info'})
                        description = content.text
                        company = 'No name'
                        a = title.find('a', attrs={'class': 'company'})
                        if a:
                            company = a.text
                        jobs.append({'title': title.text,
                                     'url': href,
                                     'description': description,
                                     'company': company,
                                     'city_id': city,
                                     'language_id': language})
            else:
                errors.append({'url': url, 'title': 'li does not exists'})
        else:
            errors.append({'url': url, 'title': 'Page do not response'})
    return jobs, errors


def djinni_co(url, city=None, language=None):
    jobs: list = []
    errors: list = []
    domain: str = 'https://djinni.co'
    if url:
        dou_ua_request = requests.get(url, headers=headers[randint(0, 2)])
        if dou_ua_request.status_code == 200:
            soup = BS(dou_ua_request.content, 'html.parser')
            main_ul = soup.find('ul', attrs={'class': 'list-jobs'})
            if main_ul:
                li_list = main_ul.find_all('li', attrs={'class': 'list-jobs__item'})
                for li in li_list:
                    title = li.find('div', attrs={'class': 'list-jobs__title'})
                    href = title.a['href']
                    content = li.find('div', attrs={'class': 'list-jobs__description'})
                    description = content.text
                    company = 'No name'
                    div = li.find('div', attrs={'class': 'list-jobs__details__info'})
                    if div:
                        company = div.text
                    jobs.append(
                        {'title': title.text,
                         'url': domain + href,
                         'description': description,
                         'company': company,
                         'city_id': city,
                         'language_id': language})
            else:
                errors.append({'url': url, 'title': 'li does not exists'})
        else:
            errors.append({'url': url, 'title': 'Page do not response'})
    return jobs, errors


if __name__ == '__main__':
    url = 'https://rabota.ua/ua/zapros/python/%D0%BA%D0%B8%D0%B5%D0%B2'
    jobs, errors = rabota_ua(url)
    work_result = codecs.open('parser_vacancy.json', 'w', 'utf-8')
    work_result.write(str(jobs))
    work_result.close()
