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
        soup = BeautifulSoup(worker_driver.page_source, 'html5lib')

        posting_data['job-title'] = soup.select_one(
            '.jobsearch-JobInfoHeader-title-container').text.split(' - ')[0]

        posting_data['location'] = soup.select_one(
            'div[data-testid="inlineHeader-companyLocation"]').text

        salary_low = salary_high = job_type = 'Unspecified'
        try:
            salary_range = soup.select_one('.css-19j1a75').text.split(' - ')

            def parse_salary(salary_range): return [float(
                salary_item[1:]) for salary_item in salary_range]

            salary_range = parse_salary(salary_range)

            if len(salary_range) == 1:
                posting_data['salary_high'] = salary_range[0]

            elif len(salary_range) == 2:
                posting_data['salary_low'], posting_data['salary_high'] = salary_range[0], salary_range[1]
        except:
            print('Failed to extract salary!')
            print(link)

        try:
            posting_data['job-type'] = soup.select_one(
                '.css-k5flys').text.split(' ')

        except:
            print('Failed to extract job-type')
            print(link)

        posting_data['posting-link'] = link.get_attribute("href")
        # posting_data['job_type'] = ','.join([word for word in salary_jobtype_info if word.lower()
        #                                      in job_types])

        # # posting_data['description'] = worker_driver.find_element(
        # # By.XPATH, '/html/body/div[1]/div[2]/div[3]/div/div/div[1]/div[3]/div/div[2]/div[10]').text.split('\n')

        print(posting_data)

        with open('jobs.txt', 'w') as f:
            f.write('\n'.join(' : '.join((item[0], str(item[1])))
                              for item in posting_data.items()))
