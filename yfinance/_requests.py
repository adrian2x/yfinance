import random
import threading
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

DEFAULT_TIMEOUT = 10  # seconds


thread_local = threading.local()

agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.1 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:67.0) Gecko/20100101 Firefox/67.0",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36"
]


def make_session():
    if not hasattr(thread_local, "session"):
        s = requests.Session()

        s.headers.update(
            {
                "User-Agent": random.choice(agents),
                "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                "accept-encoding": "gzip, deflate, br",
                "accept-language": "en-US,en;q=0.9",
                "dnt": "1",
                "referrer": "https://www.google.com/",
                "cache-control": "max-age=0",
                "upgrade-insecure-requests": "1",
            }
        )

        retry_strategy = Retry(
            total=2,
            status_forcelist=[429, 500, 502, 503, 504],
            method_whitelist=["HEAD", "GET", "OPTIONS"],
            backoff_factor=0.25,
        )

        adapter = HTTPAdapter(max_retries=retry_strategy, pool_block=False)
        s.mount("https://", adapter)
        s.mount("http://", adapter)
        thread_local.session = s
    return thread_local.session


def _get(url, proxy=None, timeout=DEFAULT_TIMEOUT, **kw):
    s = make_session()
    # Some yahoo specific headers
    s.headers.update(
    {
        "authority": "finance.yahoo.com",
        "referrer": url,
        "sec-fetch-mode": "navigate", "sec-fetch-user": "?1", "sec-fetch-site": "same-origin"}
    )
    proxies = kw.get("proxies")
    if not proxies and proxy:
        kw['proxies'] = {"https": proxy, "http": proxy}
    return s.get(url, timeout=timeout, **kw)
