from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

opt = Options()
opt.add_argument('--headless=new')
opt.add_argument('--window-size=1920,1080')
driver = webdriver.Chrome(options=opt)
try:
    driver.get('http://localhost:3710')
    time.sleep(2)
    print('Initial heading:', driver.find_element(By.ID, 'currentTabHeading').text)

    # Click Quick Action: system status
    btn = driver.find_element(By.CSS_SELECTOR, 'button[data-action="system_status"]')
    btn.click()
    time.sleep(1.5)
    toasts = driver.find_elements(By.CLASS_NAME, 'toast')
    print('Toast text:', toasts[0].text if toasts else 'No toast')

    # Switch to files
    driver.find_element(By.CSS_SELECTOR, 'a[data-tab="files"]').click()
    time.sleep(1.5)
    print('Files tab heading:', driver.find_element(By.ID, 'currentTabHeading').text)
    
    # Search for assignment
    searchInput = driver.find_element(By.ID, 'fileSearchInput')
    searchInput.clear()
    searchInput.send_keys('assignment')
    driver.find_element(By.ID, 'fileSearchBtn').click()
    time.sleep(2)
    cards = driver.find_elements(By.CLASS_NAME, 'file-item-card')
    print('File cards found:', len(cards))
    if cards:
        print('First file:', cards[0].find_element(By.CLASS_NAME, 'file-name').text)
finally:
    driver.quit()
