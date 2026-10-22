import requests
from bs4 import BeautifulSoup
import time
import os

# ========== CONFIGURATION ==========
WEBHOOK_URL = "http://localhost:5678/webhook/new-lead"  # Use Production URL
BASE_URL = "https://books.toscrape.com/catalogue/page-{}.html"
MAX_PAGES = 2
DELAY = 1
HTML_FOLDER = "html_pages"   # Folder to save HTML files
# ===================================

# Create folder if it doesn't exist
os.makedirs(HTML_FOLDER, exist_ok=True)

def scrape_and_send():
    for page in range(1, MAX_PAGES + 1):
        url = BASE_URL.format(page)
        print(f"\nDownloading page {page}: {url}")

        # 1. Download the page
        response = requests.get(url)
        response.raise_for_status()

        # 2. Save HTML to file
        file_path = os.path.join(HTML_FOLDER, f"page_{page}.html")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(response.text)
        print(f"Saved: {file_path}")

        # 3. Read from the saved HTML file
        with open(file_path, "r", encoding="utf-8") as f:
            html_content = f.read()

        soup = BeautifulSoup(html_content, "html.parser")
        books = soup.select("article.product_pod")

        for book in books:
            title = book.h3.a["title"]
            price = book.select_one(".price_color").text
            rating = book.p["class"][1]

            # Map to your workflow fields
            payload = {
                "name": title,
                "email": f"{title.lower().replace(' ', '.')[:20]}@example.com",
                "company": "Online Bookstore",
                "source": "Web Scraping",
                "full_name": title,
                "job_title": rating,
                "price": price
            }

            # Send to n8n
            try:
                r = requests.post(WEBHOOK_URL, json=payload, timeout=10)
                print(f"Sent: {title[:45]}... | Status: {r.status_code}")
            except Exception as e:
                print(f"Error sending {title}: {e}")

            time.sleep(0.3)

        time.sleep(DELAY)

    print("\n✅ All pages saved as HTML + data sent to n8n!")

if __name__ == "__main__":
    scrape_and_send()