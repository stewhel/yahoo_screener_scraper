import requests
from datetime import datetime, timedelta
import sched, time
import yagmail
from discord.ext import commands
import asyncio
import sys

import sys
sys.path.append('c:/users/steph/appdata/local/programs/python/python39/lib/site-packages')

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

sys.path.append('C:/Users/steph/anaconda3/pkgs/beautifulsoup4-4.9.3-pyhb0f4dca_0/site-packages')
import bs4
from bs4 import BeautifulSoup

body = ""

def scrape():

    print("Starting scrape for Yahoo's Top 10 Gainers (Mid & Large Cap)...")
    
    # Update with URL for your custom screener
    url = "https://login.yahoo.com/?.src=finance&.intl=us&.done=https://finance.yahoo.com/screener/7c804763-431d-47be-98d1-0bcf58cb957d"
    option = Options()
    option.add_argument("--incognito")
    option.add_argument("--disable-notifications")
    driver = webdriver.Chrome(executable_path = r'c:/users/steph/downloads/chromedriver_win32/chromedriver.exe')
    driver.get(url)

    WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.NAME,"username"))).send_keys("{EMAIL USERNAME HERE]")
    WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.NAME,"signin"))).click()
    WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.NAME,"password"))).send_keys("{EMAIL PASSWORD HERE}")
    WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.ID,"login-signin"))).click()

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.close()

    tables = soup.findChildren('table')
    my_table = tables[0]
    rows = my_table.findChildren(['tbody', 'tr'])

    body = "Today's Top Ten Movers (Under $10): \n"

    for row in rows[2:12]:
        body += "\n"
        cells = row.findChildren('td')
        for cell in [cells[0], cells[4]]:
            value = str(cell.text)
            body += value + " "

    print("Scrape finished!")

    bot = commands.Bot(command_prefix='!')

    TOKEN = '{YOUR BOT TOKEN HERE}'


    async def post():
        await bot.wait_until_ready()
        msg_sent = False

        if not msg_sent:
            channel = bot.get_channel('{YOUR CHANNEL HERE}')
            await channel.send(body)
            msg_sent = True
            sys.exit()

    bot.loop.create_task(post())
    bot.run(TOKEN)

scrape()
