/**
 * Erenshor Wiki Quest Scraper - Browser Console Version
 *
 * HOW TO USE:
 * 1. Open https://erenshor.wiki.gg/wiki/Quests in your browser
 * 2. Press F12 to open Developer Tools
 * 3. Go to "Console" tab
 * 4. Copy and paste this entire script
 * 5. Press Enter
 * 6. Wait for it to finish (it will scrape all quest pages)
 * 7. Copy the JSON output and save to ErenshorQuestData.json
 */

(async function() {
    console.log('Erenshor Quest Wiki Scraper - Browser Version');
    console.log('='.repeat(50));

    const BASE_URL = 'https://erenshor.wiki.gg';
    const delay = ms => new Promise(resolve => setTimeout(resolve, ms));

    // Function to fetch a page
    async function fetchPage(url) {
        try {
            const response = await fetch(url);
            const html = await response.text();
            const parser = new DOMParser();
            return parser.parseFromString(html, 'text/html');
        } catch (error) {
            console.error(`Error fetching ${url}:`, error);
            return null;
        }
    }

    // Function to extract quest links from main page
    function extractQuestLinks(doc) {
        const links = [];
        const seenUrls = new Set();

        // Find all links in the page
        const allLinks = doc.querySelectorAll('a[href^="/wiki/"]');

        for (const link of allLinks) {
            const href = link.getAttribute('href');
            const name = link.textContent.trim();

            // Filter out special pages
            if (href === '/wiki/Quests' ||
                href.includes('Category:') ||
                href.includes('Special:') ||
                href.includes('File:') ||
                href.includes('Template:') ||
                name.length === 0) {
                continue;
            }

            const fullUrl = BASE_URL + href;

            if (!seenUrls.has(fullUrl)) {
                seenUrls.add(fullUrl);
                links.push({ name, url: fullUrl });
            }
        }

        return links;
    }

    // Function to parse individual quest page
    function parseQuestPage(doc, questName) {
        const questData = {
            name: questName,
            npc: '',
            location: '',
            objectives: [],
            instructions: '',
            rewards: '',
            notes: ''
        };

        // Look for infobox
        const infobox = doc.querySelector('table.infobox, table[class*="infobox"]');
        if (infobox) {
            const rows = infobox.querySelectorAll('tr');
            for (const row of rows) {
                const header = row.querySelector('th');
                const data = row.querySelector('td');

                if (header && data) {
                    const headerText = header.textContent.trim().toLowerCase();
                    const dataText = data.textContent.trim();

                    if (headerText.includes('giver') || headerText.includes('npc')) {
                        questData.npc = dataText;
                    } else if (headerText.includes('location') || headerText.includes('zone') || headerText.includes('area')) {
                        questData.location = dataText;
                    } else if (headerText.includes('reward')) {
                        questData.rewards = dataText;
                    }
                }
            }
        }

        // Look for objectives
        const headers = doc.querySelectorAll('h2, h3');
        for (const header of headers) {
            const headerText = header.textContent.toLowerCase();

            if (headerText.includes('objective') || headerText.includes('task') || headerText.includes('goal')) {
                let nextElem = header.nextElementSibling;
                while (nextElem && !['H2', 'H3'].includes(nextElem.tagName)) {
                    if (nextElem.tagName === 'UL' || nextElem.tagName === 'OL') {
                        const items = nextElem.querySelectorAll('li');
                        for (const item of items) {
                            const text = item.textContent.trim();
                            if (text) questData.objectives.push(text);
                        }
                    }
                    nextElem = nextElem.nextElementSibling;
                }
            } else if (headerText.includes('walkthrough') || headerText.includes('guide') ||
                       headerText.includes('how to') || headerText.includes('instructions')) {
                const paragraphs = [];
                let nextElem = header.nextElementSibling;
                while (nextElem && !['H2', 'H3'].includes(nextElem.tagName)) {
                    if (nextElem.tagName === 'P') {
                        const text = nextElem.textContent.trim();
                        if (text.length > 10) paragraphs.push(text);
                    }
                    nextElem = nextElem.nextElementSibling;
                }
                questData.instructions = paragraphs.join(' ');
            }
        }

        // Fallback: get first few paragraphs
        if (!questData.instructions) {
            const paragraphs = doc.querySelectorAll('p');
            const texts = [];
            for (let i = 0; i < Math.min(3, paragraphs.length); i++) {
                const text = paragraphs[i].textContent.trim();
                if (text.length > 20) texts.push(text);
            }
            questData.instructions = texts.join(' ').substring(0, 500);
        }

        return questData;
    }

    // Main scraping logic
    console.log('Fetching main quests page...');
    const mainDoc = await fetchPage(window.location.href);

    if (!mainDoc) {
        console.error('Failed to parse main page');
        return;
    }

    console.log('Extracting quest links...');
    const questLinks = extractQuestLinks(mainDoc);
    console.log(`Found ${questLinks.length} potential quest links`);

    const allQuests = [];
    let counter = 0;

    for (const link of questLinks) {
        counter++;
        console.log(`[${counter}/${questLinks.length}] Scraping: ${link.name}`);

        const questDoc = await fetchPage(link.url);
        if (questDoc) {
            const questData = parseQuestPage(questDoc, link.name);
            allQuests.push(questData);

            // Be nice to the server
            await delay(500);
        } else {
            console.warn(`  Failed to fetch quest page: ${link.url}`);
        }

        // Progress update every 10 quests
        if (counter % 10 === 0) {
            console.log(`Progress: ${counter}/${questLinks.length} quests processed`);
        }
    }

    // Create output JSON
    const output = {
        version: '1.0',
        source: 'https://erenshor.wiki.gg/wiki/Quests',
        scraped_date: new Date().toISOString().split('T')[0],
        quests: allQuests
    };

    console.log('\n' + '='.repeat(50));
    console.log(`Successfully scraped ${allQuests.length} quests!`);
    console.log('='.repeat(50));
    console.log('\nCopy the JSON below and save to ErenshorQuestData.json:');
    console.log('\n' + JSON.stringify(output, null, 2));

    // Also copy to clipboard if possible
    try {
        await navigator.clipboard.writeText(JSON.stringify(output, null, 2));
        console.log('\n✓ JSON copied to clipboard!');
    } catch (e) {
        console.log('\nCould not copy to clipboard automatically. Please copy manually from above.');
    }

    return output;
})();
