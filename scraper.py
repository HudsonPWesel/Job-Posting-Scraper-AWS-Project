import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

'''
    [X] Get page
    [X] Get the links for every post in the page
    [ ] Click to reder full panel prepend https://indeed.com
    [ ] Get that data
    [ ] Once compltee move to next page

'''
if __name__ == "__main__":
    options = uc.ChromeOptions()
    options.headless = False
    driver = uc.Chrome(use_subprocess=False, options=options)
    driver.get(
        "https://www.indeed.com/jobs?q=Penetration%20Testing%20Intern&l=Boston%2C%20MA&from=searchOnDesktopSerp")

    page_source = driver.page_source

    job_links = driver.find_elements(
        By.CSS_SELECTOR, '.jcs-JobTitle')  # Get all LI job postings links

    for link in job_links:
        worker_driver = uc.Chrome(use_subprocess=False)
        worker_driver.get(link.get_attribute("href"))
