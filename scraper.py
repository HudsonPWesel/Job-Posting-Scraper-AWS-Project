import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

'''
    [X] Get page 
    [X] Get the links for every post in the page
    [ ] Click to render full panel
    [ ] Get that data
    [ ] Once complete write to file
    [ ] Move to next page
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

    # soup = BeautifulSoup(output, 'html.parser')
