import requests
from bs4 import BeautifulSoup
import lxml
import smtplib

MY_EMAIL = "python.vinciano@gmail.com"
RECEIVER = "python.vinciano@gmail.com"
MY_PASSWORD = "fsglybcigxvffnon"
BUY_PRICE = 100

URL = "https://www.amazon.com/dp/B075CYMYK6?psc=1&ref_=cm_sw_r_cp_ud_ct_FM9M699VKHTT47YD50Q6"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept-Language": "nl-NL,nl;q=0.9,en-US;q=0.8,en;q=0.7",
}

response = requests.get(url=URL, headers=headers)
amazon_webpage = response.content

soup = BeautifulSoup(amazon_webpage, "lxml")

price = soup.find (name="span", class_="a-offscreen").getText()
price_without_currency = price.split("$")[1]
price_as_float = float(price_without_currency)
print(price_as_float)

title = soup.find(name="span", id="productTitle", class_="a-size-large product-title-word-break").getText()

if price_as_float < BUY_PRICE:
    content = f"{title} is now {price}"
    connection = smtplib.SMTP("smtp.gmail.com", port=587)
    connection.starttls()
    connection.login(MY_EMAIL, MY_PASSWORD)
    message = f"{title} is now {price}\n{URL}"
    connection.sendmail(
        from_addr=MY_EMAIL,
        to_addrs=RECEIVER,
        msg=f"Subject:Price Change Alert\n\n{message}"
    )
    connection.close()

