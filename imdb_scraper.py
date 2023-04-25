from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import csv

# set up Chrome options
options = webdriver.ChromeOptions()
options.add_argument('--headless')  # run the browser in the background
options.add_argument('--no-sandbox')  # bypass OS security model
options.add_argument('--disable-dev-shm-usage')  # avoid memory leak issues

# set up the Chrome driver
driver = webdriver.Chrome(executable_path='YOUR_PATH',options=options)

# set the URL of the movie's review page on IMDB
url = "https://www.imdb.com/title/tt3581920/reviews"

# navigate to the URL and accept cookies
driver.get(url)
try:
    cookies_button = driver.find_element_by_id(" ")
    cookies_button.click()
except:
    pass

# set up a variable to store the reviews
reviews = []

# loop through all pages of reviews
while True:
    # get the HTML content of the page
    html = driver.page_source

    # find all the reviews on the page
    review_elements = driver.find_elements(By.XPATH, "//div[@class='lister-item-content']")

    # extract the review text, rating, and date from each review
    for review_element in review_elements:
        # extract the review text
        review = review_element.find_element(By.XPATH, ".//div[@class='text show-more__control']").\
            get_attribute('textContent').strip()

        # extract the review rating, if available
        rating_element = review_element.find_element(By.XPATH, ".//span[@class='rating-other-user-rating']")
        if rating_element:
            rating = rating_element.find_element(By.XPATH, ".//span[1]").get_attribute('textContent')
        else:
            rating = ""

        # extract the review date
        date = review_element.find_element(By.XPATH, ".//span[@class='review-date']").\
            get_attribute('textContent').strip()

        # add the review, rating, and date to the list of reviews
        reviews.append([review, rating, date])

    # check if there are more pages of reviews
    next_button = driver.find_elements_by_class_name("load-more-data")
    if next_button:
        # click the "Load More" button to load the next page of reviews
        button_element = next_button[0]
        button_element.click()
        time.sleep(2)  # wait for the reviews to load
    else:
        break

# quit the driver
driver.quit()

# save the reviews to a CSV file
with open('reviews_TLOU.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["Review", "Rating", "Date"])
    for review in reviews:
        writer.writerow(review)

print("Done. Reviews saved to reviews.csv.")
