from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from time import sleep
from dotenv import load_dotenv
import os
import subprocess
import re
import datetime

# Get environment variables
load_dotenv()
EMAIL = os.environ['EMAIL']
PASSWORD = os.environ['PASSWORD']

def get_monthly_bills():
    # Define browser(on chromedriver)
    options = webdriver.ChromeOptions()
    #options.add_argument("--headless")
    #options.add_argument("--disable-gpu")
    options.add_argument("--hide-scrollbars")
    options.add_argument("--single-process")
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--window-size=880x996")
    options.add_argument("--no-sandbox")
    options.add_argument("--homedir=/tmp")
    options.add_argument(
        f'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36')

    browser = webdriver.Chrome(
        ChromeDriverManager().install(),
        options=options
    )

    # Login (in Sign-in Page)
    print('start login')

    # Jump to sing-in page
    url_login = 'https://id.moneyforward.com/sign_in/email'
    browser.get(url_login)
    sleep(3)

    # Enter Email
    elem_mail_input = browser.find_element(By.CSS_SELECTOR, 'input.inputItem')
    elem_mail_input.send_keys(EMAIL)
    elem_mail_next = browser.find_element(By.CSS_SELECTOR, 'input.submitBtn')
    elem_mail_next.click()
    sleep(3)

    # Enter Password
    elem_pw_input = browser.find_element(By.CSS_SELECTOR, 'input.inputItem')
    elem_pw_input.send_keys(PASSWORD)
    elem_pw_next = browser.find_element(By.CSS_SELECTOR, 'input.submitBtn')
    elem_pw_next.click()
    sleep(3)
    
    #Jump to MoneyFW Top Page
    browser.get('https://moneyforward.com/sign_in/')
    sleep(3)
    elem_pre_next = browser.find_element(By.CSS_SELECTOR, 'input.submitBtn.homeDomain')
    elem_pre_next.click()
    sleep(3)

    # Get Montyly Bills
    browser.get('https://moneyforward.com/cf')
    xpath_target_mth = '//*[@data-year="2022"][@data-month="11"]'
    elem_target_mth = browser.find_element(By.XPATH, xpath_target_mth)
    print(elem_target_mth)
    elem_target_mth.click()
    sleep(5)
    '''
    # Get Monthly Bills
    # Jump to Money Forward ME Top page
    elem_choose_account = browser.find_element_by_xpath(
        '/html/body/main/div/div/div/div/div[1]/section/form/div[2]/div/div[2]/input')
    elem_choose_account.click()
    sleep(3)

    # Jump to Money Forward ME household expenses page
    elem_household_expenses = browser.find_element_by_xpath(
        '//*[@id="header-container"]/header/div[2]/ul/li[2]/a')
    elem_household_expenses.click()

    print('start getting bills')

    last_month = datetime.datetime.now().month - 1
    text = f'{last_month}月の公共料金\n'
    bills = [{'title': '電気代: ', 'service': '楽天でんき'},
             {'title': 'ガス代: ', 'service': '楽天ガス'},
             {'title': '水道代: ', 'service': '水道利用'},
             {'title': '通信費: ', 'service': '楽天ブロードバンド'}]

    # Create text content to send to LINE
    text = calc_bills(browser, bills, text)
    messages = TextSendMessage(text=text)

    print('everything done')
'''
    #browser.close()

def calc_bills(browser, bills, text):
    total = 0
    for bill in bills:
        span_tags = browser.find_elements_by_xpath(
            f'//span[contains(text(), "{bill["service"]}")]')
        # Add only available bills to text
        if not span_tags:
            text += f'\n{bill["title"]}0円'
        else:
            for span_tag in span_tags:
                price = span_tag.find_element_by_xpath('../../../td[4]')
                print(price.text)
                text += f'\n{bill["title"]}{price.text[1:]}円'
                total += int(price.text[1:].replace(',', ''))

