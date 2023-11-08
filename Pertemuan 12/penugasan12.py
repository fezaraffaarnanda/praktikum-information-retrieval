"""This script serves as an example on how to use Python 
   & Playwright to scrape/extract data from Google Maps"""

from playwright.sync_api import sync_playwright
from dataclasses import dataclass, asdict, field
import pandas as pd
import argparse
import time


@dataclass
class Review:
    """holds reviews data"""
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
        page.goto("https://maps.app.goo.gl/SyXMj8rCRsco4JM38",timeout=60000)

        page.wait_for_timeout(10000)
        page.locator('button:has-text("Ulasan lainnya")').click();

        # total = 30
        # previously_counted = 0
        # while True:
        #     page.mouse.wheel(0, 10)
        #     page.wait_for_timeout(10000)

        #     if (page.locator('//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[9]').count()>= total):
        #         listings = page.locator('//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[9]').all()[:total]
        #         listings = [listing.locator("xpath=..") for listing in listings]
        #         print(f"Total Scraped: {len(listings)}")
        #         break
        #     else:
        #         # logic to break from loop to not run infinitely
        #         # in case arrived at all available listings
        #         if (page.locator('//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[9]').count()== previously_counted):
        #             listings = page.locator('//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[9]').all()
        #             print(f"Arrived at all available\nTotal Scraped: {len(listings)}")
        #             break
        #         else:
        #             previously_counted = page.locator('//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[9]').count()
        #             print(f"Currently Scraped: ",page.locator('//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[9]').count(),)

        # _prev_height = -1
        # _max_scrolls = 100
        # _scroll_count = 0
        # while _scroll_count < _max_scrolls:
        #     # Execute JavaScript to scroll to the bottom of the page
        #     page.evaluate("window.scrollTo(0, 1000)")
        #     # Wait for new content to load (change this value as needed)
        #     time.sleep(0.5)
        #     # Check whether the scroll height changed - means more pages are there
        #     new_height = page.evaluate("document.body.scrollHeight")
        #     if new_height == _prev_height:
        #         break
        #     _prev_height = new_height
        #     _scroll_count += 1
       

        review_list = ReviewList()

        # page.wait_for_timeout(1000)

        
        for i in range(1,total):
            review = Review()

            page.wait_for_timeout(1575)

            # page.hover('//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[9]')

            scroll_element = page.locator('//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]')
            
            # Scroll down to the bottom of the element
            scroll_element.scroll_into_view_if_needed()
            
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

            print(review)
            review_list.review_list.append(review)

            page.mouse.wheel(0, 7000)
            page.wait_for_timeout(3000)

        review_list.save_to_excel("jakarta_aquarium_review")

        browser.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--total", type=int)
    args = parser.parse_args()

    # total number of products to scrape. Default is 10
    if args.total:
        total = args.total
    else:
        total = 10

    main()
