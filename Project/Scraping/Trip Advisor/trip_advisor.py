"""
Script ini digunakan untuk mengekstrak data review dari suatu tempat di Trip Advisor
Copyright by Tim Scraping - 3SD2
"""

from playwright.sync_api import sync_playwright
from dataclasses import dataclass, asdict, field
import pandas as pd
import argparse
import time
import sys
import math
import datetime
import random
import string


@dataclass
class Review:
    """holds maps reviews data"""
    place: str = "Pantai Losari"
    id_review: str = None 
    collecting_time:str = None 
    review_time: str = None 
    username: str = None 
    rating: str = None
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


# Fungsi untuk membuat review id secara random
# karena tidak ada id review pada website tripadvisor
def generate_review_id():
    pattern = 'nccnccnccnccnccnccnccnccnccnccnccncc'
    
    review_id = ''
    for char in pattern:
        if char == 'n':
            review_id += str(random.randint(0, 9))
        elif char == 'c':
            review_id += random.choice(string.ascii_letters)
    
    return review_id

def save_and_exit(review_list, filename):
    review_list.save_to_excel(filename)
    sys.exit("Script exited due to an error.")

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto("https://www.tripadvisor.co.id/Attraction_Review-g297720-d777660-Reviews-Losari_Beach-Makassar_South_Sulawesi_Sulawesi.html",timeout=60000)

        # Scroll 
        page.mouse.wheel(0, 1575)

        # Object ReviewList
        review_list = ReviewList()

        # Menghitung total halaman dikarenakan setiap halaman hanya menampilkan 10 review
        total_halaman = math.ceil(total/10)

        print("Copyright by Tim Scraping - 3SD2")
        print("============ Scraping ===========")

        for i in range(1,total_halaman+1):
            for j in range(1,11):

                page.wait_for_timeout(1500)

                review = Review()

                # collecting time
                current_datetime = datetime.datetime.now()
                formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
                
                # reviewer name
                reviewer_name_xpath = '//*[@id="tab-data-qa-reviews-0"]/div/div[5]/div/div[' + str(j) + ']/div/div/div[1]/div[1]/div[2]/span/a'
                try:
                    reviewer_name = page.locator(reviewer_name_xpath).inner_text()
                except:
                    print(f"Error: Nama reviewer tidak ditemukan di halaman {i}, review {j}")
                    save_and_exit(review_list, "pantai_losari_review_tripadvisor_error")

                # review time
                for div_index in [8, 7, 6, 5, 4, 3, 2, 1]:
                    review_time_xpath = f'//*[@id="tab-data-qa-reviews-0"]/div/div[5]/div/div[{j}]/div/div/div[{div_index}]/div[1]'
                    review_time_locator = page.locator(review_time_xpath)

                    # Cek apakah element review time sudah ada dan visible
                    # Pada web trip advisor, element xpath review time tidak selalu konsisten, ada yang div[8], div[7], dst.
                    if review_time_locator.is_visible():
                        review_time = review_time_locator.inner_text()
                        print(f"Review Time: {review_time}")
                        break  # Break jika sudah ketemu
                    else:
                        print(f"Review Time untuk div[{div_index}] tidak ditemukan atau tidak terlihat [non-visible].")

                # rating score
                rating_xpath = "//html[1]/body[1]/div[1]/main[1]/div[1]/div[2]/div[2]/div[2]/div[1]/div[1]/section[7]/div[1]/div[1]/div[1]/section[1]/section[1]/div[1]/div[1]/div[5]/div[1]/div["+str(j)+"]/div[1]/div[1]/div[2]/*[name()='svg'][1]"
                try:
                    rating = page.query_selector(rating_xpath).get_attribute('aria-label')
                except:
                    print(f"Error: Rating skor xpath tidak ditemukan di halaman {i}, review {j}")
                    save_and_exit(review_list, "pantai_losari_review_tripadvisor_error")

                review_xpath = '//*[@id="tab-data-qa-reviews-0"]/div/div[5]/div/div['+str(j)+']/div/div/div[5]'

                if "Selengkapnya" in page.locator(review_xpath).inner_text():
                    button_selengkapnya_xpath = '//*[@id="tab-data-qa-reviews-0"]/div/div[5]/div/div['+str(j)+']/div/div/div[5]/div[2]/button/span'
                    page.locator(button_selengkapnya_xpath).click();
            
                review_text = page.locator(review_xpath).inner_text()
                
                # memasukkan variabel ke class Review
                # review id dibuat random dikarenakan tidak ada id review pada website tripadvisor
                review.id_review = generate_review_id()
                review.collecting_time = formatted_datetime
                review.review_time = review_time
                review.rating = rating
                review.username = reviewer_name
                review.review_text = review_text

                review_list.review_list.append(review)
                page.wait_for_timeout(500)

                # Print halaman, nomor, dan empat huruf pertama dari nama reviewer
                print(f"Halaman : {i}  , No : {j}   | Reviewer Name: {reviewer_name[:4]}")

                # Klik tombol next jika sudah di akhir halaman dan semua review pada halaman itu sudah terscrape.
                if(j%10==0):
                    page.wait_for_timeout(1000)
                    next_xpath = '//*[@id="tab-data-qa-reviews-0"]/div/div[5]/div/div[11]/div[1]/div/div[1]/div[2]/div/a'
                    page.locator(next_xpath).click();
                    page.wait_for_timeout(1200)

                page.wait_for_timeout(900)
                #scroll
                page.mouse.wheel(0, 350)
            
        page.wait_for_timeout(5000)
        print("\n======== Menyimpan ke Excel ========")
        review_list.save_to_excel("pantai_losari_review_tripadvisor")

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
                break  # break jika total kelipatan 10
            else:
                print("Masukkan harus kelipatan 10. Silakan coba lagi.")
        except ValueError:
            print("Masukkan harus berupa angka. Silakan coba lagi.")

    main()
