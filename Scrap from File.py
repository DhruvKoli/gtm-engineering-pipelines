import requests
from bs4 import BeautifulSoup
import time
import os

# ========== CONFIGURATION ==========
WEBHOOK_URL = "http://localhost:5678/webhook/new-lead"  # Production URL
HTML_FOLDER = "html_pages"  # Folder where your HTML files are saved


# ===================================

def process_saved_html():
    # Get all HTML files in the folder
    html_files = [f for f in os.listdir(HTML_FOLDER) if f.endswith(".html")]

    if not html_files:
        print("No HTML files found in the folder!")
        return

    print(f"Found {len(html_files)} HTML files. Processing...\n")

    for file_name in html_files:
        file_path = os.path.join(HTML_FOLDER, file_name)
        print(f"Reading: {file_name}")

        # Read the saved HTML file
        with open(file_path, "r", encoding="utf-8") as f:
            html_content = f.read()

        soup = BeautifulSoup(html_content, "html.parser")
        books = soup.select("article.product_pod")

        for book in books:
            title = book.h3.a["title"]
            price = book.select_one(".price_color").text
            rating = book.p["class"][1]

            payload = {
                "name": title,
                "email": f"{title.lower().replace(' ', '.')[:20]}@example.com",
                "company": "Online Bookstore",
                "source": "Web Scraping",
                "full_name": title,
                "job_title": rating,
                "price": price
            }

            try:
                r = requests.post(WEBHOOK_URL, json=payload, timeout=10)
                print(f"  → Sent: {title[:50]}... | Status: {r.status_code}")
            except Exception as e:
                print(f"  → Error: {e}")

            time.sleep(1)

    print("\n✅ Finished processing all saved HTML files!")


if __name__ == "__main__":
    process_saved_html()