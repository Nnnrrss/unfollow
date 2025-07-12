import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

class InstagramUnfollower:
    def __init__(self):
        self.driver = self._setup_driver()
        self.unfollowed_count = 0
        self.max_unfollows = 150  # Stay under hourly limit
        self.delay_range = (1.5, 3.5)  # Random delays between actions

    def _setup_driver(self):
        """Configure browser with basic anti-detection"""
        options = Options()
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36")
        
        service = Service(ChromeDriverManager().install())
        return webdriver.Chrome(service=service, options=options)

    def _human_delay(self):
        """Random delay to appear more human-like"""
        time.sleep(random.uniform(*self.delay_range))

    def login(self, username, password):
        """Manual login is safer - automation gets detected"""
        self.driver.get("https://www.instagram.com/accounts/login/")
        print("Please log in manually in the browser window...")
        print("After successful login, return here and press Enter")
        input("Press Enter to continue...")
        
        # Verify login success
        if "instagram.com" in self.driver.current_url and "login" not in self.driver.current_url:
            return True
        return False

    def unfollow_accounts(self):
        """Main unfollowing logic with safety checks"""
        try:
            # Get following list
            self.driver.get(f"https://www.instagram.com/{self.username}/following/")
            self._human_delay()

            while self.unfollowed_count < self.max_unfollows:
                # Find all Following buttons
                buttons = self.driver.find_elements(
                    By.XPATH, "//div[text()='Following']"
                )
                if not buttons:
                    break

                for btn in buttons:
                    if self.unfollowed_count >= self.max_unfollows:
                        break

                    try:
                        # Unfollow process
                        btn.click()
                        self._human_delay()

                        unfollow_btn = self.driver.find_element(
                            By.XPATH, "//button[text()='Unfollow']"
                        )
                        unfollow_btn.click()
                        
                        self.unfollowed_count += 1
                        print(f"Unfollowed {self.unfollowed_count}/{self.max_unfollows}")
                        self._human_delay()

                    except Exception as e:
                        print(f"Error unfollowing: {str(e)}")
                        continue

                # Scroll to load more accounts
                self.driver.execute_script("window.scrollBy(0, 500)")
                self._human_delay()

        except Exception as e:
            print(f"Critical error: {str(e)}")
        finally:
            print(f"Completed. Total unfollowed: {self.unfollowed_count}")

    def run(self, username, password):
        """Main execution flow"""
        self.username = username
        if self.login(username, password):
            self.unfollow_accounts()
        self.driver.quit()


if __name__ == "__main__":
    print("""
    ⚠️ WARNING ⚠️
    Using automation tools violates Instagram's Terms of Service.
    Your account may be temporarily blocked or permanently banned.
    Proceed at your own risk.
    """)

    tool = InstagramUnfollower()
    
    # For safety, manually enter credentials each time
    username = input("Enter your Instagram username: ")
    password = input("Enter your Instagram password: ")
    
    tool.run(username, password)