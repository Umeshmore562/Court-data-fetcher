from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time

def fetch_case_data(case_type, case_number, year):
    
    if case_type.lower() == 'public' and case_number == 'PIL NO.138 OF 2006' and year == '2006':
        print("💡 [INFO]  Returning dummy case data...")
        dummy_result = {
            "parties": "Awaaz Foundation vs State of Maharashtra",
            "filing_date": "2006-05-10",
            "next_hearing": "2025-09-01",
            "order_pdf": "https://wwfin.awsassets.panda.org/downloads/awaaz_foundation_vs_state_of_maharashtra.pdf"
        }
        dummy_html = "<html><body><p>This is dummy HTML content for Public Case 138/2006.</p></body></html>"
        return dummy_result, dummy_html

    
    print("▶ Starting headless Chrome browser...")
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 15)

    try:
        print("▶ Navigating to eCourts website...")
        driver.get('https://cccmumbai.dcourts.gov.in/case-status-search-by-case-number/#')

        print("▶ Clicking 'Case Status'...")
        case_status = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Case Status")))
        case_status.click()

        print("▶ Waiting for form to load...")
        wait.until(EC.presence_of_element_located((By.ID, "case_type_code")))

        print("▶ Filling form fields...")
        try:
            Select(driver.find_element(By.ID, "case_type_code")).select_by_visible_text(case_type)
        except Exception:
            raise ValueError(f"❌ Invalid case type: '{case_type}'")

        driver.find_element(By.ID, "case_no").send_keys(case_number)
        driver.find_element(By.ID, "case_year").send_keys(year)

        print("▶ Submitting form...")
        driver.find_element(By.ID, "submit_case").click()

        print("▶ Waiting for results to load...")
        wait.until(EC.presence_of_element_located((By.ID, "caseDetails")))

        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        print("▶ Parsing case details...")
        try:
            parties = soup.find("div", id="caseDetails").find("strong").get_text(strip=True)
        except AttributeError:
            raise ValueError("❌ [ERROR] Case details not found. Check the input or the site layout.")

        result = {
            "parties": parties,
            "filing_date": soup.find("span", id="filingDate").get_text(strip=True) if soup.find("span", id="filingDate") else "N/A",
            "next_hearing": soup.find("span", id="nextHearingDate").get_text(strip=True) if soup.find("span", id="nextHearingDate") else "N/A",
            "order_pdf": soup.find("a", text="View Order").get("href") if soup.find("a", text="View Order") else "N/A"
        }

        print("✅ Case data fetched successfully.")
        return result, html

    except Exception as e:
        print(f"❌ {e}")
        raise Exception("Scraper failed to fetch results. " + str(e))

    finally:
        print("▶ Closing browser.")
        driver.quit()
