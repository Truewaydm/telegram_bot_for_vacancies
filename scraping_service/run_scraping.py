import asyncio
import codecs
import os, sys
import datetime

from django.contrib.auth import get_user_model
from django.db import DatabaseError

project = os.path.dirname(os.path.abspath('manage.py'))
sys.path.append(project)
os.environ["DJANGO_SETTINGS_MODULE"] = "scraping_service.settings"

import django

django.setup()

from parser import *
from scraping.models import Vacancy, City, Language, Errors, Url

User = get_user_model()

parser = (
    (work_ua, 'work_ua'),
    (dou_ua, 'dou_ua'),
    (djinni_co, 'djinni_co'),
    (rabota_ua, 'rabota_ua')
)
jobs, errors = [], []


def get_settings():
    query_set_users = User.objects.filter(send_email=True).values()
    global settings_list
    try:
        if query_set_users.exists():
            settings_list = set((qs['city_id'], qs['language_id']) for qs in query_set_users)
            return settings_list
    except ValueError:
        print(settings_list, 'have not city_id or language_id')


def get_urls(settings):
    query_set_urls = Url.objects.all().values()
    url_dict = {(qs['city_id'], qs['language_id']): qs['url_data'] for qs in query_set_urls}
    urls = []
    global pair
    try:
        for pair in settings:
            if pair in url_dict:
                tmp = {}
                tmp['city'] = pair[0]
                tmp['language'] = pair[1]
                url_data = url_dict.get(pair)
                if url_data:
                    tmp['url_data'] = url_dict.get(pair)
                    urls.append(tmp)
        return urls
    except ValueError:
        print(pair + ' not in ' + url_dict)


async def main(value):
    func, url, city, language = value
    job, error = await loop.run_in_executor(None, func, url, city, language)
    errors.extend(error)
    jobs.extend(job)


settings = get_settings()
url_list = get_urls(settings)

# city = City.objects.filter(slug='kyiv').first()
# language = Language.objects.filter(slug='python').first()

loop = asyncio.get_event_loop()
temp_task = [(func, data['url_data'][key], data['city'], data['language'])
             for data in url_list
             for func, key in parser]
# for data in url_list:
#     for func, key in parser:
#         url = data['url_data'][key]
#         j, e = func(url, city=data['city'], language=data['language'])
#         jobs += j
#         errors += e
if temp_task:
    tasks = asyncio.wait([loop.create_task(main(f)) for f in temp_task])
    loop.run_until_complete(tasks)
    loop.close()

for job in jobs:
    variable = Vacancy(**job)
    try:
        variable.save()
    except DatabaseError:
        pass
if errors:
    query_set_errors = Errors.objects.filter(timestamp=datetime.date.today())
    if query_set_errors.exists():
        error = query_set_errors.first()
        error.data.update({'errors': errors})
        error.save()
    else:
        error = Errors(data=f'errors:{errors}').save()

work_result = codecs.open('parser_vacancy.json', 'w', 'utf-8')
work_result.write(str(jobs))
work_result.close()

ten_days_ago = datetime.date.today() - datetime.timedelta(10)
# Field Lookups - lte (less than, or equal to)
# The lte lookup is used to get records that are less than, or equal to, a specified value.
# The SQL equivalent to the example above will be:
# WHERE id <= 10;
Vacancy.objects.filter(timestamp__lte=ten_days_ago).delete()
