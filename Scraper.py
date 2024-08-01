from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

# Set up Selenium with Chrome WebDriver
options = Options()
options.headless = True  # Run browser in headless mode (optional)
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--no-sandbox")
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920,1080")
options.add_argument("--remote-debugging-port=9222")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Base URL of the Talabat Oman page
base_url = 'https://www.talabat.com/oman/restaurants?page='

# Create lists to store the scraped data
restaurant_names = []
restaurant_cuisines = []

# Number of pages to scrape
num_pages = 140

# Loop through each page
for page in range(1, num_pages + 1):
    url = base_url + str(page)
    try:
        driver.get(url)
        driver.implicitly_wait(10)

        # Find restaurant elements
        restaurants = driver.find_elements(By.XPATH, "//div[@data-testid='vendor']")

        for restaurant in restaurants:
            try:
                name = restaurant.find_element(By.XPATH, ".//p[@data-testid='vendor-name']").text.strip()
                cuisine = restaurant.find_element(By.XPATH, ".//p[contains(@class, 'muted')]").text.strip()
                
                restaurant_names.append(name)
                restaurant_cuisines.append(cuisine)
            except Exception as e:
                print(f"Error extracting data for a restaurant on page {page}: {e}")

        # Optional: Pause between page requests to be polite to the server
        time.sleep(2)

    except Exception as e:
        print(f"Error loading page {page}: {e}")
        time.sleep(5)  # Wait before retrying
        driver.get(url)

# Close the WebDriver
driver.quit()

# Create a DataFrame from the lists
data = {
    'Name': restaurant_names,
    'Cuisine': restaurant_cuisines
}
df = pd.DataFrame(data)

# Export the DataFrame to an Excel file
df.to_excel('talabat_oman_restaurants.xlsx', index=False)

print('Data has been exported to talabat_oman_restaurants.xlsx')
