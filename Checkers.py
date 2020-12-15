import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pyodbc



server = 'mouton.database.windows.net'
database = 'SQL_Produksie'
username = 'OptimusPrime'
password = 'OPMEGATRON123!'   
driver= '{ODBC Driver 17 for SQL Server}'

def ScrapeFunction():
    r = requests.get('https://www.checkers.co.za/c-2420/All-Departments/Food/Fresh-Food/Fresh-Fruit/Oranges%2C-Lemons-and-Citrus-Fruit')
    soup = BeautifulSoup(r.text, 'html.parser')
    results = soup.find_all('div', attrs={'class': 'item-product__details'})


    records = []
    nowDate = datetime.now()
    Day = nowDate.strftime('%d')
    Month = nowDate.strftime('%m')
    Year = nowDate.strftime('%Y')
    Time = nowDate.strftime('%H:%M:%S"')
    retailer = 'Checkers'

    for result in results:
        main = result.find('h3', attrs={'class': 'item-product__name'})
        value = result.find('span', attrs={'class': 'now'})
   
        product = main.contents[1].text
        product= product.strip()
        discountCurrentPrice =value.contents[0]+value.contents[1].text
        discountCurrentPrice= discountCurrentPrice.strip()

        records.append((retailer, product, discountCurrentPrice, '' ))


    with pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password) as conn:
        with conn.cursor() as cursor:
            for p in records:
                format_str = "INSERT INTO WS_ClientWebsite (retailer, Day, Month, Year, Time, product, discountCurrentPrice, weightValueDesc) VALUES ('{w_retailer}', '{w_day}', '{w_month}', '{w_year}', '{w_time}', '{w_product}', '{w_discountCurrentPrice}', '{w_weightValueDesc}');"
                sql_command = format_str.format(w_retailer=p[0], w_day=Day, w_month=Month, w_year=Year, w_time=Time, w_product=p[1], w_discountCurrentPrice=p[2], w_weightValueDesc = p[3])
                cursor.execute(sql_command)


               