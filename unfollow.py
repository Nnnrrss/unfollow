from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import random

def human_like_delay():
    time.sleep(random.uniform(1.5, 3.5))

def unfollow_all(username, password, max_unfollows=150):
    driver = webdriver.Chrome()
    try:
        # Login
        driver.get("https://instagram.com/accounts/login/")
        time.sleep(3)
        driver.find_element(By.NAME, "username").send_keys(username)
        driver.find_element(By.NAME, "password").send_keys(password)
        driver.find_element(By.XPATH, "//button[@type='submit']").click()
        time.sleep(5)
        
        # Go to following list
        driver.get(f"https://instagram.com/{username}/following/")
        time.sleep(3)
        
        # Unfollow loop
        unfollowed = 0
        while unfollowed < max_unfollows:
            buttons = driver.find_elements(By.XPATH, "//div[text()='Following']")
            if not buttons:
                break
                
            for btn in buttons[:10]:  # Small batches
                try:
                    btn.click()
                    human_like_delay()
                    driver.find_element(By.XPATH, "//button[text()='Unfollow']").click()
                    unfollowed += 1
                    print(f"Unfollowed {unfollowed}/{max_unfollows}")
                    human_like_delay()
                    
                    if unfollowed >= max_unfollows:
                        break
                        
                except Exception as e:
                    print(f"Error: {e}")
                    continue
                    
            # Scroll for more accounts
            driver.execute_script("window.scrollBy(0, 500)")
            time.sleep(2)
            
    finally:
        driver.quit()

# WARNING: Use at your own risk
# human_unfollow_all("your_username", "your_password")