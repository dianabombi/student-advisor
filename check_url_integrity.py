
import sys
import requests

def check_url(url):
    try:
        # Use a real browser user agent to avoid bot blocking
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.head(url, headers=headers, allow_redirects=True, timeout=5)
        print(f"[{response.status_code}] {url} -> {response.url}")
        return response.status_code
    except Exception as e:
        print(f"[ERR] {url}: {e}")
        return 0

def main():
    cities = ['wien', 'graz', 'linz']
    
    print("--- UNIJOBS.AT ---")
    urls_to_test = [
        "https://unijobs.at/jobs",
        "https://unijobs.at/suche",
        "https://unijobs.at/jobs/wien", # Lowercase
        "https://unijobs.at/jobs/Wien", # Capitalized
        "https://unijobs.at/job-suchen?search=&region=Wien",
        "https://unijobs.at/job-suchen?search=&region=wien"
    ]
    for url in urls_to_test:
        check_url(url)

    print("\n--- HOGASTJOB ---")
    urls = [
         "https://www.hogastjob.com",
         "https://www.hogastjob.com/jobs",
         "https://www.hogastjob.com/job-search",
         "https://www.hogastjob.com/jobs?q=Wien"
    ]
    for url in urls:
        check_url(url)

if __name__ == "__main__":
    main()
