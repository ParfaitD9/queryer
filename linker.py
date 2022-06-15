from collections import Counter
import csv
import json
import time
from bs4 import BeautifulSoup, Tag
from requests.sessions import Session
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
import dotenv as de
import os
import re
from urllib.parse import urljoin, urlparse
from engines import SearchEngine, _engines
from requests.sessions import Session


class Linker:
    def __init__(self) -> None:
        opts = Options()
        opts.add_argument('--headless')
        s = Service(
            executable_path=os.getenv('CHROMEDRIVER_PATH'))
        self.driver = webdriver.Chrome(
            service=s,
            options=opts
        )
        self.session = Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:101.0) Gecko/20100101 Firefox/101.0',
            'Accept-Encoding': 'gzip, deflate, br'
        })

    def get(self, url, callback=None):
        self.driver.get(url)

        if callback:
            return callback(self.driver.page_source)

    def search(self, engine: SearchEngine, keywords: str = "Hello, World", deep=1) -> list[str]:
        results = list()
        if engine.headless:
            with self.session as s:
                for i in range(deep):
                    r = s.get(engine.host, params={
                        engine.bar_name: keywords,
                        's': i*10 + 1
                    }
                    )
                    soup = BeautifulSoup(r.text, 'html.parser')
                    results.extend([
                        Linker.clean(link.attrs.get('href')) for link in soup.select(engine.result_selector)
                    ])
        else:
            self.get(engine.host)
            self.driver.implicitly_wait(4)
            bar = self.driver.find_element(By.NAME, engine.bar_name)
            bar.send_keys(keywords)
            bar.send_keys(Keys.RETURN)
            time.sleep(2)

            for _ in range(deep):
                results.extend(
                    [Linker.clean(el.get_attribute('href')) for el in self.driver.find_elements(
                        By.XPATH, engine.result_selector) if (Linker.is_external(el.get_attribute('href'))
                                                              and not Linker.is_commercial(el.get_attribute('href')))]
                )

                try:
                    _next = self.driver.find_element(
                        By.XPATH, engine.next_selector)
                except (Exception, ) as e:
                    break
                else:
                    ActionChains(self.driver).move_to_element(
                        _next).click().perform()
                    if engine.name == 'Qwant':
                        time.sleep(3)
                self.driver.implicitly_wait(3)
        return results

    def close(self):
        self.driver.close()

    @staticmethod
    def is_external(link: str) -> bool:
        return bool(
            re.match('^(https://)(www.)*', link)
        )

    @staticmethod
    def is_commercial(link: str) -> bool:
        host = urlparse(link).netloc

        return bool(re.search(r'.*\.(qwant|google|youtube|bing|mojeek)\..*', host))

    @staticmethod
    def clean(url: str) -> str:
        _url = urlparse(url)
        return f'{_url.scheme}://{_url.netloc}{_url.path}'

    @staticmethod
    def get_host(url: str) -> str:
        _url = urlparse(url)
        return f'{_url.scheme}://{_url.netloc}'


def claim_mail(host) -> tuple[str]:
    with Session() as s:
        s.headers.update({
            'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.61 Safari/537.36"
        })
        mail_regex = '^mailto:(?P<mail>\w+@[a-zA-Z_]+?\.[a-zA-Z]{2,3})$'
        tel_regex = '^(tel:|https://wa.me/)(?P<tel>.+)$'
        try:
            r = s.get(host)
        except (Exception,) as e:
            print(f'{e.__class__} : {e.args[0]}')
        else:
            mail = tel = None
            if r.ok:
                soup = BeautifulSoup(r.text, 'html.parser')
                for a in soup.find_all('a', {'href': True}):
                    a: Tag
                    if re.match(mail_regex, a.attrs.get('href')):
                        mail = re.match(
                            mail_regex,
                            a.attrs.get('href')
                        ).group('mail')

                    if re.match(tel_regex, a.attrs.get('href')):
                        tel = re.match(
                            tel_regex,
                            a.attrs.get('href')
                        ).group('tel')

                if not any([mail, tel]):
                    if re.match('(?P<mail>^\w+@[a-zA-Z_]+?\.[a-zA-Z]{2,3})$', soup.get_text()):
                        mail = re.match(
                            '(?P<mail>^\w+@[a-zA-Z_]+?\.[a-zA-Z]{2,3})$',
                            soup.get_text()
                        ).group('mail')
                    if re.match('^(?P<a>\(\d{3}\)|\d{3})[- ](?P<b>\d{3})[- ](?P<c>\d{4})', soup.get_text()):
                        tel = re.match(
                            '^(?P<a>\(\d{3}\)|\d{3})[- ](?P<b>\d{3})[- ](?P<c>\d{4})',
                            soup.get_text()
                        ).group('tel')
    return (mail, tel)


def parse_link(res, out):
    results: list[dict] = list()
    treated = list()
    for lk in set(res):
        print(f'Parsing {Linker.get_host(lk)} ...')
        mail, tel = claim_mail(Linker.get_host(lk))
        if not any([mail, tel]):
            mail, tel = claim_mail(
                urljoin(Linker.get_host(lk), '/contact'))

        if any([mail, tel]):
            treated.append({
                'host': Linker.get_host(lk),
                'path': lk,
                'mail': mail,
                'tel': tel
            })
        results.append({
            'host': Linker.get_host(lk),
            'path': lk,
            'mail': mail,
            'tel': tel
        })
    print(Counter([result.get('path') for result in results]))
    with open(out, 'w') as f:
        json.dump(results, f)


def slug(chain: str):
    return chain.lower().strip()\
        .encode('ascii', 'ignore').decode().replace(' ', '-')


def _search(engines: str = '0123', search: str = 'Hello', out: str = 'results.json', deep: int = 5):
    res = list()
    linker = Linker()
    for i in [int(k) for k in engines]:
        eng = _engines[i]
        print(f'Crawling with {eng.name} ....')
        try:
            res.extend(linker.search(eng, search, deep))
        except (Exception, ) as e:
            print(f'{e.__class__} : {e.args[0]}')

    linker.close()
    print('Fin des recherches!')
    uniks = set(res)
    final = sorted([{
        'path': path,
        'rate': res.count(path)
    } for path in uniks], key=lambda x: x.get('rate'))

    with open(f'results/{out}', 'w') as w:
        if out.split('.')[-1] == 'json':
            json.dump(final, w)
        elif out.split('.')[-1] == 'csv':
            writer = csv.writer(w)
            writer.writerow(('path', 'rate'))
            writer.writerows([(row.get('path'), row.get('rate'))
                             for row in final])


if __name__ == '__main__':
    de.load_dotenv()
    _search(search='nettoyeur à pression', deep=4, out='nettoyeur.json')
