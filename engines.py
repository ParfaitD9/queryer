from selenium.webdriver.common.by import By


class SearchEngine:
    def __init__(self,
                 name: str,
                 result_selector: tuple[str],
                 host: str,
                 next_selector: tuple[str],
                 bar_name: tuple[str] = ('name', 'q'),
                 headless: bool = False
                 ) -> None:

        self.name = name
        self.result_selector = result_selector
        self.host = host
        self.next_selector = next_selector
        self.headless = headless
        self.bar_name = bar_name

    def __str__(self) -> str:
        return self.name


bing = SearchEngine(
    'Bing',
    (By.XPATH, '//h2/a'),
    'https://bing.com/',
    (By.XPATH, '(//*[@id="b_results"]/li/nav/ul/li/a)[last()]')
)

brave = SearchEngine(
    'Brave',
    (By.XPATH, '//a[@class="result-header"]'),
    'https://search.brave.com/',
    (By.XPATH, '//*[@id="pagination"]/a'),
    bar_name=('id', 'searchbox')
)

qwant = SearchEngine(
    'Qwant',
    (By.XPATH, "//a[contains(@class, 'external')]"),
    'https://www.qwant.com/',
    (By.XPATH, '//*[@id="root"]/div[2]/div[3]/div[1]/div[2]/section/button')
)

google = SearchEngine(
    'Google',
    (By.XPATH, '//div[@class="yuRUbf"]/a'),
    'https://www.google.com/',
    (By.XPATH, '//a[@id="pnnext"]')
)


mojeek = SearchEngine(
    'Mojeek',
    (By.CSS_SELECTOR, 'a.ob'),
    'https://www.mojeek.com/search',
    '',
    headless=True
)

_engines = [google, mojeek, brave, bing, qwant]
