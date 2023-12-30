import requests
from bs4 import BeautifulSoup
import smtplib
from decouple import config
URL_HEADERS={
    "Accept-Language":"en-US,en;q=0.9",
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"
}
MAIL_PROVIDER_SMTP_ADDRESS = "smtp.gmail.com"
MY_EMAIL = config('MY_EMAIL')
MY_PASSWORD = config('MY_PASSWORD')
email=config('email')
URL_ENDPOINT="https://www.amazon.com/Apple-MacBook-10-core-Storage-English/dp/B0C8GNFTJQ/ref=ex_alt_wg_d?_encoding=UTF8&pd_rd_i=B0C8GNFTJQ&pd_rd_w=nXSd5&pf_rd_p=4e1b46a8-daf9-4433-b97e-d6df97cf3699&pf_rd_r=AGX8NY92FJXPMKH1VPN6&pd_rd_wg=vaHr0&pd_rd_r=1595bdb6-a1af-43a5-8a7c-e5e5ad131351&content-id=amzn1.sym.4e1b46a8-daf9-4433-b97e-d6df97cf3699&th=1"
response=requests.get(URL_ENDPOINT, headers=URL_HEADERS)
amazon_webpage=response.text
soup=BeautifulSoup(amazon_webpage, "html.parser")
price=soup.find(class_="a-offscreen").get_text()
print(price)
int_price=price.split("$",)[1].split(",")
final_price=float("".join(int_price))


def send_emails( message):
    with smtplib.SMTP(host=MAIL_PROVIDER_SMTP_ADDRESS, port=587) as connection:
        connection.starttls()
        connection.login(user=MY_EMAIL, password=MY_PASSWORD)
        connection.sendmail(
                from_addr=MY_EMAIL,
                to_addrs=email,
                msg=f"Subject:New Low Price Alert!\n\n{message}".encode('utf-8')
            )
low_price=1800
if final_price<low_price:
    send_emails(f"Late 2021 Apple MacBook Pro with Apple M1 Pro chip 10-core CPU (16 inch, 16GB RAM,1TB SSD Storage) (QWERTY English) Space Gray (Renewed Premium) is Now at ${low_price}! Place your order now!")
