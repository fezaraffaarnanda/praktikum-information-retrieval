"""Script ini digunakan untuk mengekstrak data review dari suatu tempat di Google Maps"""

from playwright.sync_api import sync_playwright
from dataclasses import dataclass, asdict, field
import pandas as pd
import argparse
import time
import sys
import math


@dataclass
class Review:
    """holds maps reviews data"""
    # id_review: str = None
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
        page.goto("https://www.tripadvisor.co.id/Attraction_Review-g297720-d777660-Reviews-Losari_Beach-Makassar_South_Sulawesi_Sulawesi.html",timeout=60000)

        page.mouse.wheel(0, 1570)

        review_list = ReviewList()

        total_halaman = math.ceil(total/ 10)

        # total_scraped = 0

        print("============ Scraping ===========")

        for i in range(1,total_halaman+1):
            for j in range(1,11):
                #delay 2s
                page.wait_for_timeout(2000)

                review = Review()

                page.wait_for_timeout(200)

                reviewer_name_xpath = '//*[@id="tab-data-qa-reviews-0"]/div/div[5]/div/div['+str(j)+']/div/div/div[1]/div[1]/div[2]/span'
                reviewer_name = page.locator(reviewer_name_xpath).inner_text()
                
                review_xpath = '//*[@id="tab-data-qa-reviews-0"]/div/div[5]/div/div['+str(j)+']/div/div/div[5]/div[1]/div/span/span'
                review_text = page.locator(review_xpath).inner_text()
                
                # memasukkan variabel ke class Review
                review.name = reviewer_name
                review.review_text = review_text

                review_list.review_list.append(review)
                #delay 2s
                page.wait_for_timeout(2000)
                # total_scraped += 1 

                # Print halaman, nomor, dan empat huruf pertama dari nama reviewer
                print(f"Halaman : {i}  , No : {j}   | Reviewer Name: {reviewer_name[:4]}")

                # Klik tombol next jika sudah di akhir halaman dan semua review pada halaman itu sudah terscrape.
                if(j%10==0):
                    page.wait_for_timeout(1000)
                    next_xpath = '//*[@id="tab-data-qa-reviews-0"]/div/div[5]/div/div[11]/div[1]/div/div[1]/div[2]/div/a'
                    page.locator(next_xpath).click();   
                    #delay 5s  
                    page.wait_for_timeout(5000)

                #delay 2s
                page.wait_for_timeout(2000)
                #scroll
                page.mouse.wheel(0, 300)
            
        page.wait_for_timeout(5000)
        print("\n======== Menyimpan ke Excel ========")
        review_list.save_to_excel("pantai_losari_review")

        browser.close()

if __name__ == "__main__":

    """""
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--total", type=int)
    args = parser.parse_args()

    # Total review yang akan di scrape, defaulnya 10
    # argumen yagng harus diinput adalah kelipatan 10
    if args.total:
        total = args.total
    else:
        total = 10
    """

    while True:
        try:
            total = int(input("Masukkan jumlah review (harus kelipatan 10): "))
            if total % 10 == 0:
                break  # Keluar dari loop jika jumlah review kelipatan 10
            else:
                print("Masukkan harus kelipatan 10. Silakan coba lagi.")
        except ValueError:
            print("Masukkan harus berupa angka. Silakan coba lagi.")

    main()
