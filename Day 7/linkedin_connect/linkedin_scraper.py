from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import pandas as pd
from datetime import datetime
import re

# LinkedIn credentials
LINKEDIN_EMAIL = "manupriyan722@gmail.com"
LINKEDIN_PASSWORD = "jeffhardy722"

# Set target month and year
TARGET_MONTH = 6    # June
TARGET_YEAR = 2025

def login_and_get_month_connections():
    options = Options()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=options)

    try:
        # 1. Login
        driver.get("https://www.linkedin.com/login")
        time.sleep(3)
        driver.find_element(By.ID, "username").send_keys(LINKEDIN_EMAIL)
        driver.find_element(By.ID, "password").send_keys(LINKEDIN_PASSWORD)
        driver.find_element(By.XPATH, "//button[@type='submit']").click()
        time.sleep(5)

        # 2. Go to connections page
        driver.get("https://www.linkedin.com/mynetwork/invite-connect/connections/")
        time.sleep(5)

        # 3. Scroll to load all connections
        last_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(3)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        # 4. Extract connections
        connection_blocks = driver.find_elements(By.CSS_SELECTOR, "div[data-view-name='connections-list'] > div")
        data = []

        for conn in connection_blocks:
            try:
                name_elem = conn.find_element(By.CSS_SELECTOR, "a.fb862af6._17d1b836")
                name = name_elem.text.strip()
                profile_url = name_elem.get_attribute("href")

                title_elem = conn.find_element(By.XPATH, ".//p[contains(@class, '_0794129a')]")
                title = title_elem.text.strip()

                date_elem = conn.find_element(By.XPATH, ".//p[contains(text(), 'connected on')]")
                connected_text = date_elem.text.strip()

                match = re.search(r"connected on (.+)", connected_text)
                if match:
                    date_str = match.group(1)
                    connected_date = datetime.strptime(date_str, "%B %d, %Y")

                    if connected_date.month == TARGET_MONTH and connected_date.year == TARGET_YEAR:
                        data.append({
                            "Name": name,
                            "Title": title,
                            "Profile URL": profile_url,
                            "Connected On": connected_date.strftime("%Y-%m-%d"),
                            "Messages": "No",        # Placeholder: update manually or via further automation
                            "Endorsements": "No",    # Placeholder
                            "Events": "No"           # Placeholder
                        })

            except Exception:
                continue

        # 5. Save to CSV
        df = pd.DataFrame(data)
        filename = f"connections_{datetime(TARGET_YEAR, TARGET_MONTH, 1).strftime('%B_%Y')}.csv"
        df.to_csv(filename, index=False)
        print(f"✅ Saved {len(df)} connections made in {filename}")

    finally:
        driver.quit()

if __name__ == "__main__":
    login_and_get_month_connections()
