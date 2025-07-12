import time
import random
import json
import csv
import os
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

class InstagramResearchSuite:
    def __init__(self, headless=False):
        self.driver = self._setup_browser(headless)
        self.research_data = {
            'session_start': datetime.now().isoformat(),
            'actions': [],
            'detection_events': [],
            'collected_data': {}
        }
        self.human_behavior_profiles = {
            'casual': {'typing': (0.15, 0.4), 'actions': (1.5, 4.0), 'scrolls': (2, 5)},
            'active': {'typing': (0.1, 0.25), 'actions': (0.8, 2.0), 'scrolls': (1, 3)},
            'researcher': {'typing': (0.2, 0.5), 'actions': (2.0, 6.0), 'scrolls': (3, 8)}
        }
        self.current_behavior = 'researcher'
        
    def _setup_browser(self, headless):
        """Configure browser with anti-detection features for research"""
        options = Options()
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        
        # Research-focused settings
        options.add_argument("--disable-web-security")
        options.add_argument("--allow-running-insecure-content")
        options.add_argument("--disable-notifications")
        
        if headless:
            options.add_argument("--headless=new")
        
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        
        # Mask Selenium detection parameters
        driver.execute_script(
            "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
        )
        driver.execute_cdp_cmd(
            'Network.setUserAgentOverride',
            {"userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
             "(KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"}
        )
        
        return driver
    
    def _random_delay(self, delay_type):
        """Generate human-like random delays"""
        profile = self.human_behavior_profiles[self.current_behavior]
        min_t, max_t = profile[delay_type]
        delay = random.uniform(min_t, max_t)
        time.sleep(delay)
        return delay
    
    def _human_type(self, element, text):
        """Simulate human typing patterns"""
        for char in text:
            element.send_keys(char)
            delay = self._random_delay('typing')
            self._log_action(f"Typing: '{char}'", delay)
    
    def _move_mouse_humanlike(self, element=None):
        """Simulate natural mouse movement patterns"""
        actions = ActionChains(self.driver)
        
        # Start from random position
        start_x = random.randint(100, 500)
        start_y = random.randint(100, 300)
        actions.move_by_offset(start_x, start_y)
        
        if element:
            # Create winding path to element
            for _ in range(random.randint(2, 5)):
                offset_x = random.randint(-50, 50)
                offset_y = random.randint(-30, 30)
                actions.move_by_offset(offset_x, offset_y)
                actions.pause(random.uniform(0.1, 0.3))
        
            # Final approach to element
            actions.move_to_element(element)
        
        actions.perform()
        self._log_action("Mouse movement simulation")
    
    def _log_action(self, description, duration=0):
        """Record research activities"""
        timestamp = datetime.now().isoformat()
        self.research_data['actions'].append({
            'timestamp': timestamp,
            'action': description,
            'duration': duration,
            'behavior_profile': self.current_behavior
        })
    
    def _detect_automation_warnings(self):
        """Research method to identify platform security warnings"""
        try:
            # Check for common bot detection warnings
            warnings = []
            
            # 1. Check for verification prompts
            verification_elements = self.driver.find_elements(
                By.XPATH, "//*[contains(text(), 'verify') or contains(text(), 'suspicious')]"
            )
            if verification_elements:
                warnings.append("Account verification prompt detected")
            
            # 2. Check for temporary blocks
            block_messages = self.driver.find_elements(
                By.XPATH, "//*[contains(text(), 'temporarily blocked')]"
            )
            if block_messages:
                warnings.append("Temporary action block detected")
            
            # 3. Check for unusual activity warnings
            activity_warnings = self.driver.find_elements(
                By.XPATH, "//*[contains(text(), 'unusual activity')]"
            )
            if activity_warnings:
                warnings.append("Unusual activity warning detected")
            
            # Log any detections
            if warnings:
                for warning in warnings:
                    self.research_data['detection_events'].append({
                        'timestamp': datetime.now().isoformat(),
                        'warning': warning,
                        'url': self.driver.current_url
                    })
                return True
                
            return False
                
        except Exception:
            return False
    
    def login(self, username, password):
        """Simulate human login for research purposes"""
        try:
            self.driver.get("https://www.instagram.com/accounts/login/")
            self._random_delay('actions')
            
            # Accept cookies if prompted (for EU compliance research)
            try:
                cookie_btn = self.driver.find_element(
                    By.XPATH, 
                    "//button[contains(text(), 'Allow essential and optional cookies')]"
                )
                self._move_mouse_humanlike(cookie_btn)
                cookie_btn.click()
                self._log_action("Accepted cookies")
                self._random_delay('actions')
            except:
                pass
            
            # Find login elements
            username_field = self.driver.find_element(By.NAME, 'username')
            password_field = self.driver.find_element(By.NAME, 'password')
            
            # Simulate human interaction with fields
            self._move_mouse_humanlike(username_field)
            self._human_type(username_field, username)
            
            self._move_mouse_humanlike(password_field)
            self._human_type(password_field, password)
            
            # Random pause before submission
            self._random_delay('actions')
            
            # Submit form
            login_button = self.driver.find_element(By.XPATH, "//button[@type='submit']")
            self._move_mouse_humanlike(login_button)
            login_button.click()
            self._log_action("Login submitted")
            
            # Wait for login to complete
            self._random_delay('actions')
            
            # Check for login success
            time.sleep(3)
            if "accounts/login" in self.driver.current_url:
                self._log_action("Login failed - possible security challenge")
                return False
                
            self._log_action("Login successful")
            return True
            
        except Exception as e:
            self._log_action(f"Login error: {str(e)}")
            return False
    
    def analyze_following(self, max_accounts=50):
        """Research method to study following list structure"""
        try:
            # Navigate to profile
            self.driver.get(f"https://www.instagram.com/{self.username}/following")
            self._random_delay('actions')
            
            # Get initial following count
            try:
                count_element = self.driver.find_element(
                    By.XPATH, "//li[contains(a, 'following')]/a/span"
                )
                following_count = int(count_element.text.replace(',', ''))
                self._log_action(f"Following count: {following_count}")
            except:
                following_count = 0
            
            # Scroll through following list
            dialog = self.driver.find_element(By.XPATH, "//div[@role='dialog']")
            last_height = 0
            scroll_attempts = 0
            max_attempts = 10
            
            collected_accounts = []
            
            while scroll_attempts < max_attempts and len(collected_accounts) < max_accounts:
                # Scroll down
                self.driver.execute_script(
                    "arguments[0].scrollTop = arguments[0].scrollHeight", dialog
                )
                scroll_delay = self._random_delay('scrolls')
                self._log_action("Scrolled following list", scroll_delay)
                
                # Check for new content
                new_height = self.driver.execute_script(
                    "return arguments[0].scrollHeight", dialog
                )
                
                if new_height == last_height:
                    scroll_attempts += 1
                else:
                    scroll_attempts = 0
                    last_height = new_height
                
                # Extract account data
                accounts = self.driver.find_elements(
                    By.XPATH, "//div[@role='dialog']//a[contains(@href, '/')]"
                )
                
                for account in accounts:
                    if account.text and account.text not in collected_accounts:
                        collected_accounts.append(account.text)
            
            # Save research data
            self.research_data['collected_data']['following'] = {
                'count': following_count,
                'sample_accounts': collected_accounts[:max_accounts]
            }
            
            self._log_action(f"Collected {len(collected_accounts)} following accounts")
            return True
            
        except Exception as e:
            self._log_action(f"Following analysis error: {str(e)}")
            return False
    
    def analyze_platform_features(self):
        """Study Instagram's UI components and features"""
        try:
            # Navigate to explore page
            self.driver.get("https://www.instagram.com/explore")
            self._random_delay('actions')
            
            # Research various UI components
            features = {
                'stories': self._research_stories(),
                'feed': self._research_feed(),
                'suggestions': self._research_suggestions()
            }
            
            self.research_data['collected_data']['platform_features'] = features
            return True
            
        except Exception as e:
            self._log_action(f"Feature analysis error: {str(e)}")
            return False
    
    def _research_stories(self):
        """Study Instagram Stories feature"""
        try:
            stories = self.driver.find_elements(
                By.XPATH, "//div[contains(@class, '_aa8j')]"
            )
            
            return {
                'count': len(stories),
                'components': ['container', 'profile_image', 'progress_bar'],
                'interaction_model': 'horizontal_swipe'
            }
        except:
            return "Not available"
    
    def _research_feed(self):
        """Study main content feed"""
        try:
            posts = self.driver.find_elements(
                By.XPATH, "//article//div[contains(@class, '_aabd')]"
            )
            
            return {
                'post_count': len(posts),
                'layout': 'grid',
                'interaction_elements': ['like', 'comment', 'share', 'save']
            }
        except:
            return "Not available"
    
    def _research_suggestions(self):
        """Study account suggestion algorithm"""
        try:
            suggestions = self.driver.find_elements(
                By.XPATH, "//div[contains(text(), 'Suggested for you')]/following-sibling::div"
            )
            
            return {
                'section_title': "Suggested for you",
                'account_count': len(suggestions),
                'recommendation_factors': ['similar_follows', 'location', 'popularity']
            }
        except:
            return "Not available"
    
    def export_research_data(self, format='json'):
        """Export collected research data"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"instagram_research_{timestamp}"
        
        self.research_data['session_end'] = datetime.now().isoformat()
        
        if format == 'json':
            with open(f"{filename}.json", 'w') as f:
                json.dump(self.research_data, f, indent=2)
        elif format == 'csv':
            # Export actions log
            with open(f"{filename}_actions.csv", 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['Timestamp', 'Action', 'Duration', 'Behavior Profile'])
                for action in self.research_data['actions']:
                    writer.writerow([
                        action['timestamp'],
                        action['action'],
                        action['duration'],
                        action['behavior_profile']
                    ])
            
            # Export detection events
            if self.research_data['detection_events']:
                with open(f"{filename}_detections.csv", 'w', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow(['Timestamp', 'Warning', 'URL'])
                    for event in self.research_data['detection_events']:
                        writer.writerow([
                            event['timestamp'],
                            event['warning'],
                            event['url']
                        ])
        
        return filename
    
    def close(self):
        """Conclude research session"""
        self.driver.quit()
        self._log_action("Research session ended")


# ===== RESEARCH INTERFACE =====
if __name__ == "__main__":
    print("Instagram Platform Research Tool")
    print("=" * 40)
    print("This tool is for educational research purposes only")
    print("It studies Instagram's interface and security systems")
    print("Use only with test accounts that you own\n")
    
    # Initialize research suite
    researcher = InstagramResearchSuite(headless=False)
    
    try:
        # Research parameters
        username = input("Enter test account username: ")
        password = input("Enter test account password: ")
        
        # Start research session
        if researcher.login(username, password):
            print("\n[+] Login successful. Beginning platform analysis...")
            
            # Conduct research modules
            print("\n[1] Analyzing following list structure...")
            researcher.analyze_following(max_accounts=30)
            
            print("[2] Researching platform features...")
            researcher.analyze_platform_features()
            
            print("[3] Checking for security detections...")
            if researcher.research_data['detection_events']:
                print(" - Platform security warnings detected!")
            else:
                print(" - No security detections observed")
            
            # Export findings
            print("\n[+] Exporting research data...")
            filename = researcher.export_research_data(format='json')
            print(f" - Research data saved to {filename}.json")
            
            print("\nResearch session completed successfully")
        else:
            print("\n[-] Login failed. Research session aborted")
            
    except KeyboardInterrupt:
        print("\nResearch session interrupted by user")
    except Exception as e:
        print(f"\nCritical research error: {str(e)}")
    finally:
        researcher.close()