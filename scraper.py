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
        worker_driver.get(link.get_attribute("href"))

        try:
            posting_data['title'] = worker_driver.find_element(
                By.XPATH, '//*[@id="viewJobSSRRoot"]/div[2]/div[3]/div/div/div[1]/div[2]/div[1]/div[1]/h1/span').text
        except Exception as e:
            posting_data['title'] = worker_driver.find_element(
                By.CLASS_NAME, 'jobsearch-JobInfoHeader-title ').text
            print(e)
            print(link.get_attribute("href"))

        posting_data['company-name'] = worker_driver.find_element(
            By.CLASS_NAME, 'css-1ioi40n').text

        posting_data['location'] = worker_driver.find_element(
            By.XPATH, '/html/body/div[1]/div[2]/div[3]/div/div/div[1]/div[2]/div[1]/div[2]/div/div/div/div[2]/div').text

        salary_jobtype_text = worker_driver.find_element(
            By.XPATH, '/html/body/div[1]/div[2]/div[3]/div/div/div[1]/div[2]/div[2]/div/div').text.split(' ')

        salary = ([float(word[1:])
                   for word in salary_jobtype_text if '$' in word]) or 'Unspecified'

        if salary != 'Unspecified' and len(salary) > 1:
            posting_data['salary-low'] = min(salary[0], salary[1])
            posting_data['salary-high'] = max(salary[0], salary[1])
        elif len(salary) == 1:
            posting_data['salary-high'] = salary[0]
        else:
            posting_data['salary-low'] = ''
            posting_data['salary-high'] = ''
        posting_data['job_type'] = ','.join([word for word in salary_jobtype_text if word.lower()
                                             in job_types])

        # posting_data['description'] = worker_driver.find_element(
        # By.XPATH, '/html/body/div[1]/div[2]/div[3]/div/div/div[1]/div[3]/div/div[2]/div[10]').text.split('\n')
        posting_data['posting-link'] = link.get_attribute("href")

        with open('jobs.txt', 'a') as f:
            f.write('\n'.join(' : '.join((item[0], str(item[1])))
                              for item in posting_data.items()))
