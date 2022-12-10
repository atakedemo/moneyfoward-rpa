from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from time import sleep
from dotenv import load_dotenv
import os
import datetime

# Get environment variables
load_dotenv()
EMAIL = os.environ['EMAIL']
PASSWORD = os.environ['PASSWORD']

def get_monthly_bills():
    # Define browser(on chromedriver)
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
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
    sleep(2)

    # Enter Email
    elem_mail_input = browser.find_element(By.CSS_SELECTOR, 'input.inputItem')
    elem_mail_input.send_keys(EMAIL)
    elem_mail_next = browser.find_element(By.CSS_SELECTOR, 'input.submitBtn')
    elem_mail_next.click()
    sleep(2)

    # Enter Password
    elem_pw_input = browser.find_element(By.CSS_SELECTOR, 'input.inputItem')
    elem_pw_input.send_keys(PASSWORD)
    elem_pw_next = browser.find_element(By.CSS_SELECTOR, 'input.submitBtn')
    elem_pw_next.click()
    sleep(2)
    
    #Jump to MoneyFW Top Page
    browser.get('https://moneyforward.com/sign_in/')
    sleep(2)
    elem_pre_next = browser.find_element(By.CSS_SELECTOR, 'input.submitBtn.homeDomain')
    elem_pre_next.click()
    sleep(2)

    # Get Montyly Bills
    browser.get('https://moneyforward.com/cf')
    elem_target_today = browser.find_element(By.CSS_SELECTOR, 'button.fc-button.fc-button-today')
    elem_target_today.click()
    sleep(2)
    elem_target_pre = browser.find_element(By.CSS_SELECTOR, 'button.fc-button.fc-button-prev')
    elem_target_pre.click()
    sleep(2)

    browser.get('https://moneyforward.com/cf/summary')
    last_month = datetime.datetime.now().month - 1
    text = f'先月（{last_month}月）の費用\n'

    text = calc_bills(browser, text)

    return text
    browser.close()

def calc_bills(browser, text):
    total = 0
    elems_sum = browser.find_elements(By.CSS_SELECTOR, '#outgo.sum')
    for elem in elems_sum:
        # Add bills to text
        title = elem.find_element(By.CSS_SELECTOR, 'td:nth-child(1)')
        price = elem.find_element(By.CSS_SELECTOR, 'td:nth-child(2)')
        text += f'\n{title.text} : {price.text}'
        price_int = int(price.text.replace(',', '').replace('円', ''))
        total += price_int
    
    total = f'\n\n合計: {total}円'
    text += total
    return text

