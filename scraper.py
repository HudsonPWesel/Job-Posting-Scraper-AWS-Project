import undetected_chromedriver as uc


def main():
    driver = uc.Chrome(use_subprocess=False)
    driver.get("https://www.linkedin.com/jobs/")
    print(driver)
    # close the browser
    driver.quit()


if __name__ == "__main__":
    main()
