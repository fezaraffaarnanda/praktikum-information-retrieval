"""Script ini digunakan untuk mengekstrak data review dari suatu tempat di Google Maps"""

from playwright.sync_api import sync_playwright
from dataclasses import dataclass, asdict, field
import pandas as pd
import argparse
import time
import sys


@dataclass
class Review:
    """holds maps reviews data"""
    id_review: str = None
    name: str = None
    review_text: str = None


@dataclass
class ReviewList:
    """holds list of Review objects,
    and save to both excel and csv
    """

    review_list: list[Review] = field(default_factory=list)

    def dataframe(self):
        """transform review_list to pandas dataframe

        Returns: pandas dataframe
        """
        return pd.json_normalize((asdict(review) for review in self.review_list), sep="_")

    def save_to_excel(self, filename):
        """saves pandas dataframe to excel (xlsx) file

        Args:
            filename (str): filename
        """
        self.dataframe().to_excel(f"{filename}.xlsx", index=False)

    def save_to_csv(self, filename):
        """saves pandas dataframe to csv file

        Args:
            filename (str): filename
        """
        self.dataframe().to_csv(f"{filename}.csv", index=False)

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto("https://maps.app.goo.gl/AYpKaMWT53zHgQtU7",timeout=60000)

        page.wait_for_timeout(10000)
        page.locator('button:has-text("Ulasan lainnya")').click();
        
        review_list = ReviewList()

        print("============ Scraping ===========")

        for i in range(1,total):
            review = Review()

            page.wait_for_timeout(1575)
            
            review_element = page.query_selector('//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[9]/div['+str(3*i+-2)+']/div/div/div[2]/div[2]/div[1]/button')
            review_id = review_element.get_attribute('data-review-id')

            reviewer_name_xpath = '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[9]/div['+str(3*i-2)+']/div/div/div[2]/div[2]/div[1]/button/div[1]'
            reviewer_name = page.locator(reviewer_name_xpath).inner_text()
            
            review_xpath = '//*[@id="'+review_id+'"]'

            if "… Lainnya" in page.locator(review_xpath).inner_text():
                button_lainnya_xpath = '//*[@id="'+review_id+'"]/span[2]/button'
                page.locator(button_lainnya_xpath).click();
            
            review_text = page.locator(review_xpath).inner_text()
            review.id_review = review_id
            review.name = reviewer_name
            review.review_text = review_text

            # print(review)
            review_list.review_list.append(review)

            page.mouse.wheel(0, 1500)
            page.wait_for_timeout(3000)
            # Print empat huruf terakhir review id dan total review yang sudah di scrape
            print(f"Review ID: ...{review_id[-4:]} | Currently Scraped: {i}", end='\r')
            sys.stdout.flush()
            
        print("\n======== Menyimpan ke Excel ========")
        review_list.save_to_excel("pantai_losari_review")

        browser.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--total", type=int)
    args = parser.parse_args()

    # Total review yang akan di scrape, defaulnya 10
    if args.total:
        total = args.total+1
    else:
        total = 10

    main()