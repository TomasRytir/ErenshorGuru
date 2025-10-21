#!/usr/bin/env python3
"""
Erenshor Wiki Quest Scraper
Scrapes all quest data from https://erenshor.wiki.gg/wiki/Quests
"""

import requests
from bs4 import BeautifulSoup
import json
import time
import re

BASE_URL = "https://erenshor.wiki.gg"
QUESTS_URL = f"{BASE_URL}/wiki/Quests"

def get_page(url):
    """Fetch a page with retry logic"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return response.text
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None

def extract_quest_links(html):
    """Extract all quest page links from main quests page"""
    soup = BeautifulSoup(html, 'html.parser')
    quest_links = []

    # Find all links that point to quest pages
    for link in soup.find_all('a', href=True):
        href = link['href']
        # Quest links typically start with /wiki/ and aren't category/special pages
        if href.startswith('/wiki/') and not any(x in href.lower() for x in ['category', 'special', 'file:', 'template']):
            # Skip the main Quests page itself
            if href != '/wiki/Quests':
                full_url = BASE_URL + href
                quest_name = link.get_text(strip=True)
                if quest_name and len(quest_name) > 0:
                    quest_links.append({
                        'name': quest_name,
                        'url': full_url
                    })

    # Remove duplicates
    seen = set()
    unique_links = []
    for link in quest_links:
        if link['url'] not in seen:
            seen.add(link['url'])
            unique_links.append(link)

    return unique_links

def parse_quest_page(html, quest_name):
    """Parse individual quest page for details"""
    soup = BeautifulSoup(html, 'html.parser')

    quest_data = {
        'name': quest_name,
        'npc': '',
        'location': '',
        'objectives': [],
        'instructions': '',
        'rewards': '',
        'notes': ''
    }

    # Look for infobox (common wiki pattern)
    infobox = soup.find('table', class_=re.compile('infobox|quest-infobox', re.I))
    if infobox:
        rows = infobox.find_all('tr')
        for row in rows:
            header = row.find('th')
            data = row.find('td')
            if header and data:
                header_text = header.get_text(strip=True).lower()
                data_text = data.get_text(strip=True)

                if 'giver' in header_text or 'npc' in header_text:
                    quest_data['npc'] = data_text
                elif 'location' in header_text or 'zone' in header_text or 'area' in header_text:
                    quest_data['location'] = data_text
                elif 'reward' in header_text:
                    quest_data['rewards'] = data_text

    # Look for objectives section
    content = soup.find('div', id=re.compile('content|mw-content-text', re.I))
    if content:
        # Find objectives
        obj_header = content.find(['h2', 'h3'], string=re.compile('objective|task|goal', re.I))
        if obj_header:
            next_elem = obj_header.find_next_sibling()
            if next_elem and next_elem.name in ['ul', 'ol']:
                for li in next_elem.find_all('li'):
                    objective = li.get_text(strip=True)
                    if objective:
                        quest_data['objectives'].append(objective)

        # Find walkthrough/guide section
        guide_header = content.find(['h2', 'h3'], string=re.compile('walkthrough|guide|how to|instructions', re.I))
        if guide_header:
            instructions = []
            next_elem = guide_header.find_next_sibling()
            while next_elem and next_elem.name not in ['h2', 'h3']:
                text = next_elem.get_text(strip=True)
                if text and len(text) > 10:
                    instructions.append(text)
                next_elem = next_elem.find_next_sibling()
            quest_data['instructions'] = ' '.join(instructions)

        # Get first few paragraphs as general info if no specific instructions
        if not quest_data['instructions']:
            paragraphs = content.find_all('p', limit=3)
            text_parts = [p.get_text(strip=True) for p in paragraphs if len(p.get_text(strip=True)) > 20]
            if text_parts:
                quest_data['instructions'] = ' '.join(text_parts)[:500]  # Limit length

    return quest_data

def scrape_all_quests():
    """Main scraping function"""
    print("Fetching main quests page...")
    html = get_page(QUESTS_URL)
    if not html:
        print("Failed to fetch main page")
        return []

    print("Extracting quest links...")
    quest_links = extract_quest_links(html)
    print(f"Found {len(quest_links)} potential quest links")

    all_quests = []

    for i, quest_link in enumerate(quest_links):
        print(f"[{i+1}/{len(quest_links)}] Scraping: {quest_link['name']}")

        quest_html = get_page(quest_link['url'])
        if quest_html:
            quest_data = parse_quest_page(quest_html, quest_link['name'])
            all_quests.append(quest_data)

            # Be nice to the server
            time.sleep(0.5)
        else:
            print(f"  Failed to fetch quest page")

    return all_quests

def save_to_json(quests, filename='QuestData.json'):
    """Save quest data to JSON file"""
    output = {
        'version': '1.0',
        'source': 'https://erenshor.wiki.gg/wiki/Quests',
        'scraped_date': time.strftime('%Y-%m-%d'),
        'quests': quests
    }

    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"\nSaved {len(quests)} quests to {filename}")

if __name__ == '__main__':
    print("Erenshor Quest Wiki Scraper")
    print("=" * 50)

    quests = scrape_all_quests()

    if quests:
        save_to_json(quests)
        print(f"\nSuccessfully scraped {len(quests)} quests!")

        # Print sample
        if quests:
            print("\nSample quest:")
            print(json.dumps(quests[0], indent=2))
    else:
        print("\nNo quests scraped. Check errors above.")
