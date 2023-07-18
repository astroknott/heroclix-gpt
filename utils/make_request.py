from selenium import webdriver
from selenium.webdriver import Proxy
from selenium.webdriver.common.proxy import ProxyType
from itertools import cycle

proxy_pool = cycle([
    'gate.smartproxy.com:10020',
    'gate.smartproxy.com:10021',
    'gate.smartproxy.com:10022',
    'gate.smartproxy.com:10023',
    'gate.smartproxy.com:10024',
    'gate.smartproxy.com:10025',
    'gate.smartproxy.com:10026',
    'gate.smartproxy.com:10027',
    'gate.smartproxy.com:10028',
    'gate.smartproxy.com:10029',
])  

username = 'sp9q681sjd'
password = 'e6sRCgi3nzysQ5qGc7'

def make_request(url):
    PROXY = next(proxy_pool)

    proxy = Proxy({
        "ProxyType": ProxyType.MANUAL,
        "httpProxy": PROXY,
        "sslProxy": PROXY        
    })
    options = webdriver.FirefoxOptions()
    options.proxy = proxy

    browser = webdriver.Firefox(options=options)

    try:
        # Open the webpage
        browser.get(url)

        # Let the page load
        import time
        time.sleep(3)

        # Get the page source
        html = browser.page_source

        # Close the browser
        browser.quit()
        
        return html
    except Exception as e:
        print(f"Error occurred with proxy {proxy}: {e}")
        # If the request failed (e.g., due to a connection error), try the next proxy
        return make_request(url)
