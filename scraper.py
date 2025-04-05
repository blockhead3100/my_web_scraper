import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import datetime
import argparse

def get_page_data_selenium(url):
    try:
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        driver = webdriver.Chrome(options=chrome_options)

        driver.get(url)
        time.sleep(5)

        soup = BeautifulSoup(driver.page_source, "html.parser")
        title = soup.title.string.strip() if soup.title else "No title found"
        paragraphs = [p.text.strip() for p in soup.find_all("p")]
        links = [a.get("href") for a in soup.find_all("a") if a.get("href")]
        images = [img.get("src") for img in soup.find_all("img") if img.get("src")]

        driver.quit()

        return {"url": url, "title": title, "paragraphs": paragraphs, "links": links, "images": images}
    except Exception as e:
        return {"url": url, "error": str(e)}

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Web scraper.")
    parser.add_argument("urls", nargs="+", help="URLs to scrape.")
    args = parser.parse_args()

    all_data = []

    for url in args.urls:
        try:
            data = get_page_data_selenium(url)
            all_data.append(data)
        except Exception as e:
            all_data.append({"url": url, "error": str(e)})

    # Save data to JSON file with datetime stamp.
    now = datetime.datetime.now()
    timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"scraped_data_{timestamp}.json"

    with open(filename, "w") as f:
        json.dump(all_data, f, indent=4)

    print(f"Data saved to {filename}")
