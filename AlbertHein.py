
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
    r = requests.get('https://www.ah.nl/producten/aardappel-groente-fruit/fruit/sinaasappels-mandarijnen/mandarijnen?soort=1312')
    soup = BeautifulSoup(r.text, 'html.parser')
    results = soup.find_all('article', attrs={'class': 'product-card-portrait_root__sZL4I product-grid-lane_gridItem__eqh9g'})
  
    records = []
    nowDate = datetime.now()
    Day = nowDate.strftime('%d')
    Month = nowDate.strftime('%m')
    Year = nowDate.strftime('%Y')
    Time = nowDate.strftime('%H:%M:%S"')
    retailer = 'Albert Hein'

    for result in results:
        main = result.find('span', attrs={'class': 'line-clamp_root__1FX_J line-clamp_active__Yb_HA title_lineclamp__1dS7X'})
        value = result.find('div', attrs={'class': 'price-amount_root__37xv2 price-amount_highlight__3WjBM price_amount__2Gk9i price_highlight__3B97G'})
        desc = result.find('span', attrs={'class': 'price_unitSize__8gRVX'})
   
        product = main.contents[0]
        weightValueDesc = desc.contents[0]
        discountCurrentPrice = value.contents[0].text + value.contents[1].text + value.contents[2].text

        records.append((retailer, product, discountCurrentPrice, weightValueDesc ))

    with pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password) as conn:
        with conn.cursor() as cursor:
            for p in records:
                format_str = "INSERT INTO WS_ClientWebsite (retailer, Day, Month, Year, Time, product, discountCurrentPrice, weightValueDesc) VALUES ('{w_retailer}', '{w_day}', '{w_month}', '{w_year}', '{w_time}', '{w_product}', '{w_discountCurrentPrice}', '{w_weightValueDesc}');"
                sql_command = format_str.format(w_retailer=p[0], w_day=Day, w_month=Month, w_year=Year, w_time=Time, w_product=p[1], w_discountCurrentPrice=p[2], w_weightValueDesc = p[3])
                cursor.execute(sql_command)


               