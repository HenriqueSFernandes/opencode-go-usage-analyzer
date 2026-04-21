import requests
import os
import re
from dotenv import load_dotenv
from rich.console import Console
from rich.table import Table
from bs4 import BeautifulSoup

load_dotenv()

auth_token = os.getenv("COOKIE_AUTH")
workspace_id = os.getenv("WORKSPACE_ID")


cookies = {
    'auth': auth_token,
    'oc_locale': 'en'
}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

url = f"https://opencode.ai/workspace/{workspace_id}/go"

def sendRequest(url: str, cookies: dict, headers: dict):
    try:
        response = requests.get(url, cookies=cookies, headers=headers)
        return response
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None

def parseResponse(response):
    if response is None:
        return None
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup

def isAuthenticated(soup):
    if soup is None:
        return False
    googleLink = soup.find(lambda tag: tag.name == "a" and "Continue with Google" in tag.get_text())  
    return googleLink is None

def extractUsage(soup):
    if soup is None:
        return None
    usage_div = soup.find('div', attrs={"data-slot": "usage"})
    if usage_div:
        usage_text = usage_div.get_text(strip=True)
        pattern = r"(Rolling|Weekly|Monthly) Usage(\d+%)Resets in(.*?)(?=Rolling|Weekly|Monthly|$)"
        matches = re.findall(pattern, usage_text)

        usage_data = []

        for match in matches:
            usage_type, percentage, reset_time = match
            usage_data.append({
                "type": usage_type,
                "percentage": percentage,
                "resets_in": reset_time.strip()
            })
        return usage_data

    return None

def print_usage(usage_data):
    console = Console()

    # Create the table structure
    table = Table(title="[bold cyan]Account Usage Limits[/bold cyan]", show_header=True, header_style="bold magenta")
    
    table.add_column("Usage Type", style="dim", width=12)
    table.add_column("Capacity", justify="right")
    table.add_column("Reset Timer", style="green")
    
    # Populate the rows
    for entry in usage_data:
        # Logic to color-code the percentage
        percent_val = int(entry['percentage'].replace('%', ''))
        color = "red" if percent_val >= 90 else "yellow" if percent_val > 50 else "green"
        
        table.add_row(
            entry['type'], 
            f"[{color}]{entry['percentage']}[/{color}]", 
            entry['resets_in']
        )
    
    console.print(table)


response = sendRequest(url, cookies, headers)
# response = sendRequest(url, cookies={}, headers=headers)

soup = parseResponse(response)

if isAuthenticated(soup):
    usage_data = extractUsage(soup)
    if usage_data:
        print_usage(usage_data)
    else:
        print("Could not extract usage data.")
    
else:    
    print("User is not authenticated.")
