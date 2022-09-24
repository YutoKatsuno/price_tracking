from bs4 import BeautifulSoup
import requests
import lxml
import smtplib
import os


# -----------------------os---------------------- #
ACCEPT_LANGUAGE = os.environ["ACCEPT_LANGUAGE"]
USER_AGENT = os.environ["USER_AGENT"]

MY_EMAIL = os.environ["MY_EMAIL"]
PASSWORD = os.environ["PASSWORD"]


# -----------------------requests---------------------- #
URL = "https://www.amazon.com/dp/B09V7WYKRY/ref=syn_sd_onsite_desktop_242?ie=UTF8&pd_rd_plhdr=t&th=1"

request_header = {
    "Accept-Language": ACCEPT_LANGUAGE,
    "User-Agent": USER_AGENT,
}

response = requests.get(URL, headers=request_header)
html = response.content

soup = BeautifulSoup(html, "lxml")
span_price = soup.find(name="span", class_="a-offscreen").getText()
price = span_price.split("$")[1]
price_as_float = float(price)
title = soup.find(id="productTitle").getText().strip()


# -----------------------smtplib---------------------- #
to_addr = "example@gmail.com"

if price_as_float >= 100:
    message = f"title: {title}\nprice: {price}\nURL: {URL}"

    with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
        connection.starttls()
        connection.login(user=MY_EMAIL, password=PASSWORD)
        connection.sendmail(from_addr=MY_EMAIL,
                            to_addrs=to_addr,
                            msg=f"Subject:Amazon Price Alert\n\n{message}")