from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import re
import time
import datetime
import pandas as pd

banner = []
dates = []
revenue = []
ranking = []


def get_names():
    names = soup.body.find_all(
        'h3', attrs={"id": re.compile("content_2.[1-9]")})
# [<h3 id="content_2_1">アルベドピックアップ</h3>, <h3 id="content_2_2">鍾離ピックアップ</h3>, <h3 id="content_2_3">タルタリヤピックアップ</h3>, <h3 id="content_2_5">クレーピックアップ</h3>, <h3 id="content_2_7">ウェンティピックアップ</h3>]
    for el in names:
        banner.append(el.string)


# def yen_to_USD(str):
#     reg = re.match(r"(\d)+\.(\d+)", str).group(0)
#     return float(reg)*100000000*0.0067


def get_table_data():
    data = soup.find_all("div", {"class": "ie5"})
    valid_tables = []
    for el in data:
        tables = el.find_all("table", {"class": "style_table"})
        for table in tables:
            if (table.find("a")) == None:
                valid_tables.append(table)

    for table in valid_tables:
        trs = table.find_all("tr")
        dates.append(trs[0].find_all(
            "td", {"class": "style_td"})[-1].get_text())
        # revenue.append(yen_to_USD(trs[1].find_all(
        #     "td", {"class": "style_td"})[-1].get_text()))
        revenue.append(trs[1].find_all(
            "td", {"class": "style_td"})[-1].get_text())
        ranking.append(trs[2].find_all(
            "td", {"class": "style_td"})[-1].get_text())


chromedriver_path = "/Users/connietsang/Downloads/chromedriver"
service = Service(chromedriver_path)
driver = webdriver.Chrome(executable_path=chromedriver_path)
url_2020 = "https://game-i.daa.jp/?%E3%82%AC%E3%83%81%E3%83%A3%E5%88%86%E6%9E%90%2F%E5%8E%9F%E7%A5%9E&yyyy=2020"
url_2021 = "https://game-i.daa.jp/?%E3%82%AC%E3%83%81%E3%83%A3%E5%88%86%E6%9E%90%2F%E5%8E%9F%E7%A5%9E&yyyy=2021"
url_2022 = "https://game-i.daa.jp/?%E3%82%AC%E3%83%81%E3%83%A3%E5%88%86%E6%9E%90%2F%E5%8E%9F%E7%A5%9E&yyyy=2022"

links = [url_2020, url_2021, url_2022]
for link in links:
    driver.get(link)
    time.sleep(5)
    html = driver.page_source
    # A Python tree representation of the HTML
    soup = BeautifulSoup(html, 'html.parser')
    get_names()
    get_table_data()
    driver.delete_all_cookies

driver.quit()
df = pd.DataFrame({'Banner': banner, 'Banner Date': dates,
                   'Revenue': revenue, 'Ranking': ranking})
df.to_csv("banner_data.csv")
