from bs4 import BeautifulSoup
import requests, csv

URL = 'https://hh.ru/search/vacancy?area=1&fromSearchLine=true&text=python+%D1%80%D0%B0%D0%B7%D1%80%D0%B0%D0%B1%D0%BE%D1%82%D1%87%D0%B8%D0%BA&from=suggest_post'
HEADERS = {'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
'user-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36'}
HOST = 'https://hh.ru/'
CSV = 'вакансии.csv'

def get_url(url, params=''):
    req = requests.get(url, headers=HEADERS, params=params)
    return req

def get_info(html):
    collects = BeautifulSoup(html, 'html.parser')
    content_items = collects.find_all('div', class_='vacancy-serp-item')
    vacancies = []
    for content_item in content_items:
        vacancies.append(
            {
                #Список с вариантами трудоустройства
                'work_option': content_item.find('div', class_ = 'bloko-text').get_text(),
                #Наименование вакансии
                'vacancy_name': content_item.find('div', class_ = 'vacancy-serp-item__info').get_text(),
                #Ссылка на вакансию
                'link_vacancy': content_item.find('span', class_ = 'g-user-content').find('a').get('href'),
                #Инфо о компании
                'info_company': content_item.find('div', class_ = 'vacancy-serp-item__meta-info-company').get_text(),
                #Описание требований к вакансии
                'vacancy_requirements': content_item.find('div', class_ = 'g-user-content').get_text(),
            }
        )
    return vacancies

def save_in_csv(content_items, path):
    with open(path, 'w', newline ='') as exelfile:
        writer = csv.writer(exelfile, delimiter=';')
        writer.writerow(['Вариант трудоустройства', 'Наименование вакансии', 'Ссылка на вакансию', 'Информация о компании', 'Требования к вакансии'])
        for content_item in content_items:
            writer.writerow([content_item['work_option'], content_item['vacancy_name'], content_item['link_vacancy'], content_item['info_company'], content_item['vacancy_requirements']])


def go_pars():
    PAGES = int(input('Укажите количество страниц'))
    html = get_url(URL)
    #При успешном ответе достаемнужные данные
    if html.status_code == 200:
        vacancyes =[]
        # Перебираем все страницы контента до PAGES, area - название страницы в hh
        for area in range(1, PAGES):
            html = get_url(URL, params=PAGES)
            vacancyes.extend(get_info(html.text))
            save_in_csv(vacancyes, CSV)
    else:
        print('Ошибка у тебя')

go_pars()















