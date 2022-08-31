from selenium import webdriver
import chromedriver_binary
import time
from selenium.webdriver.chrome import options
from selenium.webdriver.common.by import By
import os
from user_info import *
from send_mail import create_mail, send_gmail


try:
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    campussquare_url = "https://jjh.tmu.ac.jp/campusweb/campusportal.do"

    driver.get(campussquare_url)
    print("campussquareへログイン中...")
    time.sleep(3)

    user_name_form = driver.find_element(by=By.XPATH, value='//*[@id="userNameInput"]')
    password_form = driver.find_element(by=By.XPATH, value='//*[@id="passwordInput"]')
    user_name_form.send_keys(campussquare_user_name)
    password_form.send_keys(campussquare_pw)
    driver.find_element(
        by=By.XPATH, value='//*[@id="LoginFormSimple"]/tbody/tr[3]/td/button[1]/span'
    ).click()
    time.sleep(3)

    # 掲示へ
    driver.find_element(by=By.XPATH, value='//*[@id="tab-kj"]').click()
    time.sleep(3)

    rf = open("last_notice_title.txt", mode="r")
    pretitle = rf.read()

    newest_title = pretitle

    print("情報取得中...")
    elems = driver.find_elements(
        by=By.CSS_SELECTOR,
        value="#keiji-portlet > ul > li:nth-child(5) > .keiji-list > li:not(.right)",
    )
    e_text = [e.text for e in elems]

    for i, e in enumerate(e_text):
        if e == pretitle:
            break
        else:
            if i == 0:
                newest_title = e
            driver.find_element(
                by=By.XPATH,
                value='//*[@id="keiji-portlet"]/ul/li[5]/ul/li[{}]/a'.format(i + 1),
            ).click()
            time.sleep(3)
            driver.switch_to.window(driver.window_handles[1])
            subject = (
                "[CampusSquare]"
                + driver.find_element(
                    by=By.XPATH, value="/html/body/table[1]/tbody/tr/td/span[1]"
                ).text
            )
            text = driver.find_element(by=By.XPATH, value="/html/body/div[2]").text
            mail = create_mail(from_email, to_email, subject, text)
            send_gmail(from_email, password=app_pass, mail=mail)
            print("メールを送信しました．")
            driver.switch_to.window(driver.window_handles[0])

    with open("last_notice_title.txt", mode="w") as wf:
        wf.write(newest_title)
    rf.close()

except Exception as e:
    print(e)
finally:
    driver.quit()
    print("処理が終了しました．")
