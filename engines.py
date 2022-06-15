class SearchEngine:
    def __init__(self,
                 name: str,
                 result_selector: str,
                 host: str,
                 next_selector: str,
                 bar_name: str = 'q',
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
    '//h2/a',
    'https://bing.com/',
    '(//*[@id="b_results"]/li/nav/ul/li/a)[last()]'
)

brave = SearchEngine(
    'Brave',
    '//a[@class="result-header"]',
    'https://search.brave.com/',
    '//*[@id="pagination"]/a'
)

qwant = SearchEngine(
    'Qwant',
    "//a[contains(@class, 'external')]",
    'https://www.qwant.com/',
    '//*[@id="root"]/div[2]/div[3]/div[1]/div[2]/section/button'
)

google = SearchEngine(
    'Google',
    '//div[@class="yuRUbf"]/a',
    'https://www.google.com/',
    '//a[@id="pnnext"]'
)


mojeek = SearchEngine(
    'Mojeek',
    'a.ob',
    'https://www.mojeek.com/search',
    '',
    headless=True
)

_engines = [google, mojeek, brave, bing, qwant]
