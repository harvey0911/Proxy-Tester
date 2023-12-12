import requests
from bs4 import BeautifulSoup

class IP:
    def __init__(self, ip_address, port, code, country, anonymity, google, https, last_checked):
        self.ip_address = ip_address
        self.port = port
        self.code = code
        self.country = country
        self.anonymity = anonymity
        self.google = google
        self.https = https
        self.last_checked = last_checked

def get_proxy_list(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    table = soup.find('table', class_='table table-striped table-bordered')

    proxy_list = []
    for row in table.find_all('tr')[1:]:
        cols = row.find_all('td')
        ip = IP(cols[0].text.strip(), cols[1].text.strip(), cols[2].text.strip(),
                cols[3].text.strip(), cols[4].text.strip(), cols[5].text.strip(),
                cols[6].text.strip(), cols[7].text.strip())
        proxy_list.append(ip)
    return proxy_list

def test_proxies(proxy_list, test_url):
    functional_proxies = []
    for ip_obj in proxy_list:
        proxy = {'https': f'http://{ip_obj.ip_address}:{ip_obj.port}'}
        try:
            response = requests.get(test_url, proxies=proxy, timeout=15)
            if response.status_code == 200:
                functional_proxies.append(ip_obj)
        except requests.exceptions.RequestException as e:
            print(f"Error with proxy {ip_obj.ip_address}:{ip_obj.port} - {e}")
    return functional_proxies

def print_functional_proxies(country_name, proxies):
    print(f"\nFunctional proxies in {country_name}:")
    for ip_obj in proxies:
        print(f" http {ip_obj.ip_address} {ip_obj.port}")

# Main
url = 'https://free-proxy-list.net/'
all_proxies = get_proxy_list(url)
test_url = 'https://www.google.com'


https_proxies = [ip for ip in all_proxies if ip.https == 'yes']


functional_proxies = test_proxies(https_proxies, test_url)
print_functional_proxies("General", functional_proxies)

