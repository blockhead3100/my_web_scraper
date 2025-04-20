import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import datetime
import argparse

def get_page_data_selenium(url, data_type):
    driver = None  # Ensure driver is defined
    try:
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        driver = webdriver.Chrome(options=chrome_options)

        driver.get(url)
        # Use WebDriverWait to ensure the page is fully loaded
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

        soup = BeautifulSoup(driver.page_source, "html.parser")
        if data_type == "Text":
            paragraphs = [p.text.strip() for p in soup.find_all("p")]
            data = paragraphs
        elif data_type == "Images":
            images = [img.get("src") for img in soup.find_all("img") if img.get("src")]
            data = images
        elif data_type == "Links":
            links = [a.get("href") for a in soup.find_all("a") if a.get("href")]
            data = links
        elif data_type == "Tables":
            tables = []
            for table in soup.find_all("table"):
                rows = []
                for row in table.find_all("tr"):
                    cells = [cell.text.strip() for cell in row.find_all(["td", "th"])]
                    rows.append(cells)
                tables.append(rows)
            data = tables
        else:
            data = "Unsupported data type"

        return {"url": url, "data_type": data_type, "data": data}
    except Exception as e:
        return {"url": url, "data_type": data_type, "error": str(e)}
    finally:
        if driver:
            driver.quit()  # Ensure driver is closed

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Web scraper.")
    parser.add_argument("urls", nargs="+", help="URLs to scrape.")
    parser.add_argument("--data_type", choices=["Text", "Images", "Links", "Tables"], default="Text", help="Type of data to scrape.")
    args = parser.parse_args()

    all_data = []

    for url in args.urls:
        try:
            data = get_page_data_selenium(url, args.data_type)
            all_data.append(data)
        except Exception as e:
            all_data.append({"url": url, "data_type": args.data_type, "error": str(e)})

    now = datetime.datetime.now()
    timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"scraped_data_{timestamp}.json"

    with open(filename, "w") as f:
        json.dump(all_data, f, indent=4)

    print(f"Data saved to {filename}")
