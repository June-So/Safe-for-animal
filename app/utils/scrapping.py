from selenium import webdriver
import pandas as pd
from app.models import Review, Society
from app import db
import time


def scrap_data_reviews(name):
    # Init window
    driver = webdriver.Firefox()
    driver.fullscreen_window()
    # google search
    url = 'https://www.google.com/search?q='+name
    driver.get(url)
    # find google review container
    avis = driver.find_element_by_xpath("//a/span[contains(text(),'avis Google')]")
    avis.click()
    driver.implicitly_wait(10)
    review_container = driver.find_element_by_xpath("//div[contains(@class,'review-dialog-list')]")

    # Scroll the review container until the end for load all the reviews
    while True:
        # get height before scrolling move for know when it's end of container
        last_height = driver.execute_script("return arguments[0].scrollHeight", review_container)
        driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', review_container)
        time.sleep(1)
        # get height after scrolling move for know when it's end of container
        review_container = driver.find_element_by_xpath("//div[contains(@class,'review-dialog-list')]")
        height = driver.execute_script("return arguments[0].scrollHeight", review_container)

        if height == last_height:
            break

    # gopen "voir plus.." for load all texts reviews
    view_more = review_container.find_elements_by_xpath("//a[contains(@class, 'review-more-link')]")
    for button in view_more:
        button.click()

    # get informations review, date and text
    date_reviews = [date_review.text for date_review in review_container.find_elements_by_xpath("//div[contains(@class, '__google-review')]/div[1]/div[3]/div[1]")]
    reviews = [review.text for review in review_container.find_elements_by_xpath("//div[contains(@class, '__google-review')]/div[1]/div[3]/div[2]")]

    # Save scrapp reviews in dataframe, export in csv
    df_reviews = pd.DataFrame({'date_publication': date_reviews, 'text': reviews})
    df_reviews.to_csv('app/data/reviews_' + name + '.csv')

    # add new society
    society = Society(name)
    db.session.add(society)
    db.session.commit()

    # save scrapp reviews in database
    for k, review in df_reviews.iterrows():
        r = Review(society, review.text, review.date_publication)
        db.session.add(r)
    db.session.commit()
    # end of connection
    driver.close()
