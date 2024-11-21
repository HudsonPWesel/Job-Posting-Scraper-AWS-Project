from curses.ascii import isdigit
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from selenium import webdriver

'''
    [X] Get page
    [X] Get the links for every post in the page
    [X] Click to reder full panel
    [ ] Get that data
        [X] Title
        [X] Company Name
        [X] Location (Missouri (remote if includes (•Remote)
        [X] Salary
        [X] Position type (intern, part-time, full-time, etc.)
        [X] Job Description
        [X] Remote vs On-site vs Unspecified
        [ ] Qualifications
        [ ] Keywords
        [X] Link to posting
    [ ] Once complete move to next page

'''
if __name__ == "__main__":
    options = webdriver.ChromeOptions()
    options.headless = False
    options.add_argument("start-maximized")
    driver = uc.Chrome(use_subprocess=False, options=options)
    driver.get(
        "https://www.indeed.com/jobs?q=Penetration%20Testing%20Intern&l=Boston%2C%20MA&from=searchOnDesktopSerp")

    page_source = driver.page_source

    job_links = driver.find_elements(
        By.CSS_SELECTOR, '.jcs-JobTitle')  # Get all LI job postings links

    data = []
    job_types = ['seasonal', 'full-time', 'part-time',
                 'internship', 'intern', 'temp', 'temporary']
    for link in job_links:
        posting_data = {}
        worker_driver = uc.Chrome(use_subprocess=False)
        worker_driver.get(link.get_attribute('href'))

        soup = BeautifulSoup(worker_driver.page_source, 'html5lib')

        job_title_data = soup.select_one('h1') or soup.select_one(
            'span[data-testid="jobsearch-JobInfoHeader-title"]') or soup.find_all('h1')

        posting_data['job-title'] = job_title_data.text if job_title_data else 'Unspecified'

        location_data = soup.select_one(
            'div[data-testid="inlineHeader-companyLocation"]') or soup.select_one('.css-1ojh0u')

        posting_data['location'] = location_data.text if location_data else 'Unspecified'

        salary_low = salary_high = job_type = 'Unspecified'

        # Salary is really weird so I wrap in try/except
        salary_data = soup.select_one(
            'span.css-19j1a75') or soup.select_one('.salaryInfoAndJobType') or soup.select_one('.css-1xkrvql')

        salary_data = salary_data.text.split(
            ' ') if salary_data else 'Unspecified'

        salary_range = [float(salary_item[1:].replace(',', ''))
                        for salary_item in salary_data if '$' in salary_item]

        if len(salary_range) == 1:
            posting_data['salary_high'] = posting_data['salary_low'] = salary_range[0]

        elif len(salary_range) == 2:
            posting_data['salary_low'], posting_data['salary_high'] = salary_range[0], salary_range[1]
        else:
            posting_data['salary_low'] = posting_data['salary_high'] = 0.00

        job_type_data = soup.select_one(
            '.css-k5flys') or soup.select_one('div[id="salaryInfoAndJobType"]')

        if job_type_data:
            job_type_data = job_type_data.text.split(' ')
            posting_data['job-type'] = [job_type_item.replace(',', '') for job_type_item in job_type_data if len(
                job_type_item) > 1 and (job_type_item.replace(',', '').lower() in job_types)]
        else:
            posting_data['job-type'] = ['Unspecified']

        posting_data['posting-link'] = link.get_attribute("href")

        print(posting_data)
