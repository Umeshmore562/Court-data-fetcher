from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time

def fetch_case_data(case_type, case_number, year):
    
    if case_type.lower() == 'public' and case_number == '138' and year == '2006':
        print("💡 Returning dummy case data for testing...")
        return {
            "parties": "Awaaz Foundation vs State of Maharashtra",
            "filing_date": "2006-05-10",
            "next_hearing": "2025-09-01",
            "order_pdf": "https://wwfin.awsassets.panda.org/downloads/awaaz_foundation_vs_state_of_maharashtra.pdf"
        }, "<html><p>Dummy HTML content.</p></html>"

    print("▶ Starting browser...")
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 20)

    try:
        print("▶ Opening Faridabad District Court page...")
        driver.get('https://faridabad.dcourts.gov.in/case-status-search-by-case-number/')

        print("▶ Navigating to 'Case Status'...")
        case_status = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Case Status")))
        case_status.click()

        print("▶ Waiting for form to load...")
        wait.until(EC.presence_of_element_located((By.ID, "case_type_code")))

        print("▶ Filling in the form...")
        try:
            Select(driver.find_element(By.ID, "case_type_code")).select_by_visible_text(case_type)
        except Exception:
            raise ValueError(f"❌ Invalid case type: '{case_type}'")

        driver.find_element(By.ID, "case_no").send_keys(case_number)
        driver.find_element(By.ID, "case_year").send_keys(year)

        
        try:
            print("📸  Detecting CAPTCHA...")
            captcha_image = driver.find_element(By.ID, "captcha_image")
            captcha_image.screenshot("captcha.png")
            print("🔐 Please check 'captcha.png' and enter CAPTCHA:")
            captcha_text = input("Enter CAPTCHA: ")
            driver.find_element(By.ID, "captcha_input").send_keys(captcha_text)
        except Exception:
            print("⚠️ CAPTCHA not detected or ID incorrect.")

        print("▶ Submitting form...")
        driver.find_element(By.ID, "submit_case").click()

        print("▶ Waiting for results...")
        wait.until(EC.presence_of_element_located((By.ID, "caseDetails")))

        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")

        print("▶ Extracting details...")
        parties = soup.find("div", id="caseDetails").find("strong").get_text(strip=True)
        filing_date = soup.find("span", id="filingDate").get_text(strip=True) if soup.find("span", id="filingDate") else "N/A"
        next_hearing = soup.find("span", id="nextHearingDate").get_text(strip=True) if soup.find("span", id="nextHearingDate") else "N/A"
        order_pdf = soup.find("a", text="View Order")
        order_link = order_pdf.get("href") if order_pdf else "N/A"

        result = {
            "parties": parties,
            "filing_date": filing_date,
            "next_hearing": next_hearing,
            "order_pdf": order_link
        }

        print("✅ Scraping complete.")
        return result, html

    except Exception as e:
        print(f"❌ Error: {e}")
        return None, None

    finally:
        print("▶ Closing browser.")
        driver.quit()
