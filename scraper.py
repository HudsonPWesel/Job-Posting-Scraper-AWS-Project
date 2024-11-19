import undetected_chromedriver as uc
from selenium.webdriver.common.by import By

if __name__ == "__main__":
    options = uc.ChromeOptions()
    options.headless = False
    driver = uc.Chrome(use_subprocess=False, options=options)
    driver.get(
        "https://www.indeed.com/q-Penetration-Testing-Intern-jobs.html?vjk=3a8d1aa8176e6055")
    job_title = driver.find_element(
        By.XPATH, '//*[@id="jobsearch-ViewjobPaneWrapper"]/div/div[2]/div[2]/div[1]/div/div[2]/div[1]/h2/span')
    print(job_title.text)
