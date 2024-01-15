import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

driver = webdriver.Chrome()  # Replace with your preferred browser driver
url = "https://www.myntra.com/personal-care"

try:
    driver.get(url)

    # Wait for products to load dynamically
    try:
        products = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "product-base"))
        )
    except TimeoutException:
        print("Error: Products didn't load within the timeout period.")
        exit()

    product_data = []
    for product in products:
        try:
            name = product.find_element(By.CLASS_NAME, "product-brand").text
            price = product.find_element(By.CLASS_NAME, "product-discountedPrice").text
            rating = product.find_element(By.CLASS_NAME, "product-ratingsContainer").text
            # made by Debanka Das - https://github.com/erdebankadas; also follow my page - https://fossbyte.in/
            description = product.find_element(By.CLASS_NAME, "product-product").text
            
            actual_price = product.find_element(By.CLASS_NAME, "product-strike").text
            discounted_price = product.find_element(By.CLASS_NAME, "product-discountedPrice").text
            product_discount_percentage = product.find_element(By.CLASS_NAME, "product-discountPercentage").text
            # made by Debanka Das - https://github.com/erdebankadas; also follow my page - https://fossbyte.in/
            breadcrumb = driver.find_element(By.CSS_SELECTOR, "span.breadcrumbs-crumb[style='font-size: 14px; margin: 0px;']").text
           
            product_url_element = product.find_element(By.CSS_SELECTOR, "a[data-refreshpage='true']")
            product_url = product_url_element.get_attribute("href")
           

            product_data.append({
                "name": name,
                "price": price,
                "rating": rating,
                # "name": name,
                "description":description,
                # "product_size":product_size,
                "actual_price": actual_price,
                "discounted_price":discounted_price,
                "product_discount_percentage":product_discount_percentage,
                # "rating": rating,
                "breadcrumb": breadcrumb ,
                # "product_urls":product_urls,
                "product_url": product_url 
                
                
            })
        except NoSuchElementException:
            print("Error: Some product elements not found. Skipping...")

    # Write data to CSV
    with open("my_scraped_products_original_one_pg.csv", "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["name", "price", "rating","description","actual_price","discounted_price","product_discount_percentage","breadcrumb","product_url"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(product_data)
        # made by Debanka Das - https://github.com/erdebankadas; also follow my page - https://fossbyte.in/

    print("Data successfully saved to my_scraped_products_original_one_pg.csv")

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    driver.quit()