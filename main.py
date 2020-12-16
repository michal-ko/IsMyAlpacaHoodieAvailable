import re
import requests
from bs4 import BeautifulSoup
import smtplib

URL = "https://appalachiangearcompany.com/collections/mens/products/mens-all-paca-fleece-hoodie?variant=37538073051334&utm_source=newsletter&utm_medium=email&utm_campaign=earlyDec_inventoryalert&utm_content=menshoodies&goal=0_9cced955d3-074039e033-414922245&mc_cid=074039e033&mc_eid=0fbdc7b9be"
page = requests.get(URL)
soup = BeautifulSoup(page.content, 'html.parser')

results = soup.find(id="js-product-form--3695823192148")
results = results.find_all('div', class_="product-single__variant")
results = str(results).split('\n')

available = list()
soldout = list()

for res in results:
    obj = re.findall(r'option', str(res))
    if len(obj) == 2:
        cleanedup = re.search(r'>(.*)<', str(res)).group(1)
        # check if has 'sold out'
        if bool(re.search(r'Sold Out', cleanedup)):
            soldout.append(cleanedup)
        else:
            available.append(cleanedup)

print(f"Abailable: {available}")
print(f"Soldout: {soldout}")
