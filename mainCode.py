import requests
from bs4 import BeautifulSoup
import argparse
import csv
from urllib.parse import urljoin


def scrape_titles_and_links(url, output="news.csv"):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")

        articles = []

        for tag in soup.find_all(["h1", "h2", "h3"]):
            title = tag.get_text(strip=True)
            parent_link = tag.find_parent("a")

            if title:
                link = parent_link["href"] if parent_link and parent_link.has_attr(
                    "href") else None
                full_link = urljoin(url, link) if link else None

                articles.append({"title": title, "link": full_link})

        # Save to CSV
        with open(output, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["title", "link"])
            writer.writeheader()
            for article in articles:
                writer.writerow(article)

        print(f"[✓] Saved {len(articles)} items to {output}")

    except Exception as e:
        print(f"[!] Error: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Scrape headlines and links from a news site")
    parser.add_argument("url", help="The URL of the website")
    parser.add_argument("-o", "--output", default="news.csv",
                        help="Output CSV file name")
    args = parser.parse_args()

    scrape_titles_and_links(args.url, args.output)
