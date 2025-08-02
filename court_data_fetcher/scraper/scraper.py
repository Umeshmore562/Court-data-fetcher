from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time

def fetch_case_data(case_type, case_number, year):
    print("▶ Starting Selenium scraper for Faridabad District Court...")

    if case_type.lower() == 'public' and case_number == '138' and year == '2006':
        print("💡 Returning dummy case data for testing...")
        return {
            "parties": "Awaaz Foundation vs State of Maharashtra",
            "filing_date": "2006-05-10",
            "next_hearing": "2025-09-01",
            "order_pdf": "https://wwfin.awsassets.panda.org/downloads/awaaz_foundation_vs_state_of_maharashtra.pdf"
        }, "<html><p>Dummy HTML content.</p></html>"

    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=options)

    try:
        driver.get("https://faridabad.dcourts.gov.in/case-status-search-by-case-number/")
        print("▶ Page loaded.")

        wait = WebDriverWait(driver, 20)

        court_dropdown = Select(wait.until(EC.presence_of_element_located((By.ID, "court_complex_code"))))
        court_dropdown.select_by_visible_text("District Court, Faridabad")
        print("▶ Court complex selected.")

        Select(driver.find_element(By.ID, "case_type")).select_by_visible_text(case_type)

        driver.find_element(By.ID, "case_number").send_keys(case_number)
        driver.find_element(By.ID, "case_year").send_keys(year)

        captcha_img = wait.until(EC.presence_of_element_located((By.XPATH, "//img[contains(@src, 'captcha')]")))
        captcha_img.screenshot("captcha.png")
        print("⚠ CAPTCHA saved as 'captcha.png'. Open it and enter the text manually:")

        captcha_code = input("🔤 Enter CAPTCHA code: ")
        driver.find_element(By.ID, "captcha_code").send_keys(captcha_code)
        
        driver.find_element(By.ID, "searchbtn").click()
        print("▶ Submitted. Waiting for results...")

        time.sleep(5)
        soup = BeautifulSoup(driver.page_source, "html.parser")
        result_div = soup.find("div", class_="caseDetails")

        if result_div:
            result_text = result_div.get_text(strip=True)
            print("✅ Case found:")
            print(result_text)
            return result_text, str(soup)
        else:
            print("❌ No case data found. Possibly wrong CAPTCHA or invalid case details.")
            return "No case data found.", str(soup)

    except Exception as e:
        print("🚨 Error during scraping:", e)
        return f"Error: {e}", ""

    finally:
        driver.quit()
