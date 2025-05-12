from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException
import pandas as pd
import time
import traceback

# LinkedIn credentials - replace with your actual credentials
LINKEDIN_EMAIL = "adityatawde9699@gmail.com"  # Replace with your email
LINKEDIN_PASSWORD = "Aditya@9699"  # Replace with your password

# Configure Edge WebView2 for Selenium
options = webdriver.EdgeOptions()
options.use_chromium = True  # Ensure it uses Chromium-based Edge

# Add some additional options to make browser more stable
options.add_argument("--start-maximized")
options.add_argument("--disable-notifications")
options.add_argument("--disable-popup-blocking")

# Initialize Selenium WebView2 driver
driver = webdriver.Edge(options=options)
wait = WebDriverWait(driver, 15)  # Increased wait time to 15 seconds

try:
    # Open LinkedIn login page
    print("Opening LinkedIn login page...")
    driver.get("https://www.linkedin.com/login")
    time.sleep(3)  # Wait for page to load
    
    print("Entering login credentials...")
    # Enter email
    email_input = wait.until(EC.element_to_be_clickable((By.ID, "username")))
    email_input.clear()
    email_input.send_keys(LINKEDIN_EMAIL)
    
    # Enter password
    password_input = wait.until(EC.element_to_be_clickable((By.ID, "password")))
    password_input.clear()
    password_input.send_keys(LINKEDIN_PASSWORD)
    
    # Click login button
    login_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']")))
    login_button.click()
    
    # Wait for login to complete
    try:
        wait.until(EC.url_contains("linkedin.com/feed") or 
                  EC.url_contains("linkedin.com/checkpoint") or 
                  EC.url_contains("linkedin.com/home"))
        print("Successfully logged in to LinkedIn")
    except TimeoutException:
        print("Login page transition not detected. Current URL:", driver.current_url)
        input("Press Enter after completing any additional verification steps...")
    
    # Wait for a moment after login
    time.sleep(5)
    print(f"Current URL after login: {driver.current_url}")
    
    # Navigate to LinkedIn job search page
    print("Navigating to jobs page...")
    driver.get("https://www.linkedin.com/jobs/")
    time.sleep(5)  # Increased wait time for page to load
    print(f"Current URL after navigation to jobs: {driver.current_url}")

    # Define job search criteria
    job_title = ["Data Scientist", "AI Engineer", "Full-Stack Developer"]
    job_location = ["India", "USA", "UK", "Japan"]

    print("Looking for search input fields...")
    
    # Find job title input field
    title_input = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[aria-label='Search by title, skill, or company']")))
    print("Found title input using standard selector")
    
    title_input.clear()
    title_input.send_keys(job_title)
    print(f"Entered job title: {job_title}")

    # Find location input field
    location_input = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[aria-label='City, state, or zip code']")))
    print("Found location input using standard selector")
    
    location_input.clear()
    location_input.send_keys(job_location)
    print(f"Entered location: {job_location}")
    
    # Press Enter to search
    location_input.send_keys(Keys.RETURN)
    
    print("Waiting for search results...")
    time.sleep(8)  # Increased wait time for search results
    
    print(f"Current URL after search: {driver.current_url}")
    
    # Take a screenshot of search results page
    driver.save_screenshot("search_results.png")
    print("Search results screenshot saved as 'search_results.png'")

    # Create lists to store job data
    job_titles = []
    company_names = []
    locations = []
    job_links = []

    # Try to find job cards
    print("Looking for job listings...")
    
    # Try different selectors for job cards
    job_cards = None
    selectors = [
        ".jobs-search-results__list-item",
        "[data-job-id]",
        ".job-search-card",
        ".jobs-search-result-item",
        ".occludable-update",
        ".scaffold-layout__list-item"
    ]
    
    for selector in selectors:
        try:
            job_cards = driver.find_elements(By.CSS_SELECTOR, selector)
            if job_cards and len(job_cards) > 0:
                print(f"Found {len(job_cards)} job cards with '{selector}' selector")
                break
        except Exception as e:
            continue
    
    if not job_cards or len(job_cards) == 0:
        # Try a different approach - look at entire page source
        print("Couldn't find job cards with standard selectors, analyzing page source...")
        
        # Save a screenshot and page source for debugging
        driver.save_screenshot("job_search_debug.png")
        with open("job_search_html.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)
        
        # Try to find divs that might contain job information
        print("Looking for any job-related elements...")
        
        # Try to extract job information directly from the page
        # Use JavaScript to extract job information
        job_data = driver.execute_script("""
            // Try to find job elements
            let jobElements = [];
            
            // Try different container selectors
            const containers = [
                document.querySelectorAll('.jobs-search-results__list-item'),
                document.querySelectorAll('[data-job-id]'),
                document.querySelectorAll('.job-search-card'),
                document.querySelectorAll('.jobs-search-result-item'),
                document.querySelectorAll('.occludable-update'),
                document.querySelectorAll('.scaffold-layout__list-item')
            ];
            
            // Use the first non-empty container
            for (const container of containers) {
                if (container && container.length > 0) {
                    jobElements = Array.from(container);
                    break;
                }
            }
            
            if (jobElements.length === 0) {
                // If we still can't find job cards, look for any elements with job-related text
                const allElements = document.querySelectorAll('*');
                jobElements = Array.from(allElements).filter(el => {
                    const text = el.innerText || '';
                    return (
                        text.includes('Data Scientist') || 
                        text.includes('data scientist') ||
                        text.includes('hiring') ||
                        text.includes('job')
                    ) && (
                        el.tagName === 'DIV' || 
                        el.tagName === 'LI' || 
                        el.tagName === 'ARTICLE'
                    );
                });
            }
            
            // Extract job information
            return jobElements.slice(0, 10).map(el => {
                // Try to find a title
                let title = '';
                const titleElements = [
                    el.querySelector('h3'),
                    el.querySelector('.job-card-list__title'),
                    el.querySelector('.job-card-container__link'),
                    el.querySelector('a[data-control-name="job_card_title"]'),
                    el.querySelector('a[href*="/jobs/view/"]')
                ];
                
                for (const titleEl of titleElements) {
                    if (titleEl && titleEl.innerText) {
                        title = titleEl.innerText.trim();
                        break;
                    }
                }
                
                // Try to find company name
                let company = '';
                const companyElements = [
                    el.querySelector('h4'),
                    el.querySelector('.job-card-container__company-name'),
                    el.querySelector('.job-card-container__primary-description'),
                    el.querySelector('a[data-control-name="job_card_company"]')
                ];
                
                for (const companyEl of companyElements) {
                    if (companyEl && companyEl.innerText) {
                        company = companyEl.innerText.trim();
                        break;
                    }
                }
                
                // Try to find location
                let location = '';
                const locationElements = [
                    el.querySelector('.job-card-container__metadata-item'),
                    el.querySelector('.job-card-container__metadata'),
                    el.querySelector('.artdeco-entity-lockup__caption'),
                    el.querySelector('[data-test-job-location]')
                ];
                
                for (const locationEl of locationElements) {
                    if (locationEl && locationEl.innerText) {
                        location = locationEl.innerText.trim();
                        break;
                    }
                }
                
                // Try to find link
                let link = '';
                const linkElements = [
                    el.querySelector('a[href*="/jobs/view/"]'),
                    el.querySelector('a')
                ];
                
                for (const linkEl of linkElements) {
                    if (linkEl && linkEl.href) {
                        link = linkEl.href;
                        break;
                    }
                }
                
                return { title, company, location, link };
            });
        """)
        
        print(f"Found {len(job_data)} job items using JavaScript extraction")
        
        # Add extracted data to our lists
        for job in job_data:
            job_titles.append(job['title'] if job['title'] else "Title not found")
            company_names.append(job['company'] if job['company'] else "Company not found")
            locations.append(job['location'] if job['location'] else "Location not found")
            job_links.append(job['link'] if job['link'] else "#")
            
            print(f"Scraped job: {job_titles[-1]} at {company_names[-1]}")
    else:
        # Process the job cards we found
        max_jobs = min(10, len(job_cards))
        print(f"Will attempt to scrape {max_jobs} jobs")
        
        for i in range(max_jobs):
            try:
                job_card = job_cards[i]
                
                # Take a screenshot of this specific job card for debugging
                try:
                    driver.execute_script("arguments[0].scrollIntoView();", job_card)
                    driver.save_screenshot(f"job_card_{i+1}.png")
                except:
                    print(f"Couldn't take screenshot of job card {i+1}")
                
                # Analyze job card HTML structure
                card_html = job_card.get_attribute('outerHTML')
                with open(f"job_card_{i+1}.html", "w", encoding="utf-8") as f:
                    f.write(card_html)
                
                # Try to extract using JavaScript for this specific job card
                job_data = driver.execute_script("""
                    const el = arguments[0];
                    
                    // Try to find a title
                    let title = '';
                    const titleElements = [
                        el.querySelector('h3'),
                        el.querySelector('.job-card-list__title'),
                        el.querySelector('.job-card-container__link'),
                        el.querySelector('a[data-control-name="job_card_title"]'),
                        el.querySelector('a[href*="/jobs/view/"]'),
                        el.querySelector('.base-search-card__title')
                    ];
                    
                    for (const titleEl of titleElements) {
                        if (titleEl && titleEl.innerText) {
                            title = titleEl.innerText.trim();
                            break;
                        }
                    }
                    
                    // Try to find company name
                    let company = '';
                    const companyElements = [
                        el.querySelector('h4'),
                        el.querySelector('.job-card-container__company-name'),
                        el.querySelector('.job-card-container__primary-description'),
                        el.querySelector('a[data-control-name="job_card_company"]'),
                        el.querySelector('.base-search-card__subtitle')
                    ];
                    
                    for (const companyEl of companyElements) {
                        if (companyEl && companyEl.innerText) {
                            company = companyEl.innerText.trim();
                            break;
                        }
                    }
                    
                    // Try to find location
                    let location = '';
                    const locationElements = [
                        el.querySelector('.job-card-container__metadata-item'),
                        el.querySelector('.job-card-container__metadata'),
                        el.querySelector('.artdeco-entity-lockup__caption'),
                        el.querySelector('[data-test-job-location]'),
                        el.querySelector('.job-search-card__location')
                    ];
                    
                    for (const locationEl of locationElements) {
                        if (locationEl && locationEl.innerText) {
                            location = locationEl.innerText.trim();
                            break;
                        }
                    }
                    
                    // Try to find link
                    let link = '';
                    const linkElements = [
                        el.querySelector('a[href*="/jobs/view/"]'),
                        el.querySelector('a')
                    ];
                    
                    for (const linkEl of linkElements) {
                        if (linkEl && linkEl.href) {
                            link = linkEl.href;
                            break;
                        }
                    }
                    
                    return { title, company, location, link };
                """, job_card)
                
                job_titles.append(job_data['title'] if job_data['title'] else "Title not found")
                company_names.append(job_data['company'] if job_data['company'] else "Company not found")
                locations.append(job_data['location'] if job_data['location'] else "Location not found")
                job_links.append(job_data['link'] if job_data['link'] else "#")
                
                print(f"Scraped job {i+1}: {job_titles[-1]} at {company_names[-1]}")
            except Exception as e:
                print(f"Error scraping job {i+1}: {e}")
                # Add placeholder values
                job_titles.append(f"Error retrieving job {i+1}")
                company_names.append("Error retrieving")
                locations.append("Error retrieving")
                job_links.append("#")
    
    # Create DataFrame with job information
    print("Creating DataFrame with collected job data...")
    jobs_df = pd.DataFrame({
        'Job Title': job_titles,
        'Company': company_names,
        'Location': locations,
        'Job URL': job_links
    })
    
    # Save results to CSV
    jobs_df.to_csv('linkedin_jobs.csv', index=False)
    print(f"Successfully scraped {len(jobs_df)} jobs and saved to 'linkedin_jobs.csv'")

except Exception as e:
    print(f"An error occurred: {e}")
    print("Detailed traceback:")
    traceback.print_exc()
    # Save screenshot for debugging
    try:
        driver.save_screenshot("error_screenshot.png")
        print("Error state screenshot saved as 'error_screenshot.png'")
    except:
        print("Could not save error screenshot")

finally:
    # Close the browser
    print("Closing browser...")
    driver.quit()
    print("Script execution complete")