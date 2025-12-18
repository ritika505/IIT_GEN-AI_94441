from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

chrome_options = Options()
chrome_options.add_argument("--headless")

driver = webdriver.Chrome(options=chrome_options)
url = "https://sunbeaminfo.in/internship"
driver.get(url)

print("Page Title:", driver.title)

wait = WebDriverWait(driver, 10)

# Wait until at least one non-empty td is loaded
wait.until(
    EC.presence_of_element_located((By.XPATH, "//tbody/tr/td[normalize-space()]"))
)

table_rows = driver.find_elements(By.XPATH, "//tbody/tr")

for row in table_rows:
    cols = row.find_elements(By.TAG_NAME, "td")

    if len(cols) < 8:
        continue

    info = {
        "Sr.No": cols[0].text.strip(),"\n"
        "Batch": cols[1].text.strip(),"\n"
        "Batch Duration": cols[2].text.strip(),
        "Start Date": cols[3].text.strip(),
        "End Date": cols[4].text.strip(),
        "Time": cols[5].text.strip(),
        "Fees (Rs.)": cols[6].text.strip(),
        "Download Brochure": cols[7].text.strip()
    }

    print(info)

driver.quit()
