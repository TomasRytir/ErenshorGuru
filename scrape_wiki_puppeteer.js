/**
 * Erenshor Wiki Quest Scraper - Puppeteer Version
 * Automatically scrapes ALL quests from the wiki
 */

const puppeteer = require('puppeteer');
const fs = require('fs');
const path = require('path');

const BASE_URL = 'https://erenshor.wiki.gg';
const QUESTS_URL = `${BASE_URL}/wiki/Quests`;

async function delay(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

async function scrapeAllQuests() {
    console.log('Erenshor Quest Wiki Scraper');
    console.log('='.repeat(50));

    console.log('Launching browser...');
    const browser = await puppeteer.launch({
        headless: 'new',
        args: ['--no-sandbox', '--disable-setuid-sandbox']
    });

    try {
        const page = await browser.newPage();
        await page.setUserAgent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36');

        console.log('Loading main quests page...');
        await page.goto(QUESTS_URL, { waitUntil: 'networkidle2', timeout: 60000 });

        console.log('Extracting quest links...');
        const questLinks = await page.evaluate((baseUrl) => {
            const links = [];
            const seenUrls = new Set();

            document.querySelectorAll('a[href^="/wiki/"]').forEach(link => {
                const href = link.getAttribute('href');
                const name = link.textContent.trim();

                // Filter out special pages
                if (href === '/wiki/Quests' ||
                    href.includes('Category:') ||
                    href.includes('Special:') ||
                    href.includes('File:') ||
                    href.includes('Template:') ||
                    name.length === 0) {
                    return;
                }

                const fullUrl = baseUrl + href;

                if (!seenUrls.has(fullUrl)) {
                    seenUrls.add(fullUrl);
                    links.push({ name, url: fullUrl });
                }
            });

            return links;
        }, BASE_URL);

        console.log(`Found ${questLinks.length} potential quest links`);

        const allQuests = [];
        let counter = 0;

        for (const link of questLinks) {
            counter++;
            console.log(`[${counter}/${questLinks.length}] Scraping: ${link.name}`);

            try {
                await page.goto(link.url, { waitUntil: 'networkidle2', timeout: 30000 });

                const questData = await page.evaluate((questName) => {
                    const data = {
                        name: questName,
                        npc: '',
                        location: '',
                        objectives: [],
                        instructions: '',
                        rewards: '',
                        notes: ''
                    };

                    // Look for infobox
                    const infobox = document.querySelector('table.infobox, table[class*="infobox"]');
                    if (infobox) {
                        const rows = infobox.querySelectorAll('tr');
                        rows.forEach(row => {
                            const header = row.querySelector('th');
                            const cell = row.querySelector('td');

                            if (header && cell) {
                                const headerText = header.textContent.trim().toLowerCase();
                                const cellText = cell.textContent.trim();

                                if (headerText.includes('giver') || headerText.includes('npc')) {
                                    data.npc = cellText;
                                } else if (headerText.includes('location') || headerText.includes('zone') || headerText.includes('area')) {
                                    data.location = cellText;
                                } else if (headerText.includes('reward')) {
                                    data.rewards = cellText;
                                }
                            }
                        });
                    }

                    // Look for objectives
                    const headers = document.querySelectorAll('h2, h3');
                    headers.forEach(header => {
                        const headerText = header.textContent.toLowerCase();

                        if (headerText.includes('objective') || headerText.includes('task') || headerText.includes('goal')) {
                            let nextElem = header.nextElementSibling;
                            while (nextElem && !['H2', 'H3'].includes(nextElem.tagName)) {
                                if (nextElem.tagName === 'UL' || nextElem.tagName === 'OL') {
                                    const items = nextElem.querySelectorAll('li');
                                    items.forEach(item => {
                                        const text = item.textContent.trim();
                                        if (text) data.objectives.push(text);
                                    });
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
                            data.instructions = paragraphs.join(' ');
                        }
                    });

                    // Fallback: get first few paragraphs
                    if (!data.instructions) {
                        const paragraphs = document.querySelectorAll('p');
                        const texts = [];
                        for (let i = 0; i < Math.min(3, paragraphs.length); i++) {
                            const text = paragraphs[i].textContent.trim();
                            if (text.length > 20) texts.push(text);
                        }
                        data.instructions = texts.join(' ').substring(0, 500);
                    }

                    return data;
                }, link.name);

                allQuests.push(questData);

                // Be nice to the server
                await delay(500);

            } catch (error) {
                console.error(`  Error scraping ${link.name}: ${error.message}`);
            }

            // Progress update every 10 quests
            if (counter % 10 === 0) {
                console.log(`Progress: ${counter}/${questLinks.length} quests processed`);
            }
        }

        console.log('\n' + '='.repeat(50));
        console.log(`Successfully scraped ${allQuests.length} quests!`);
        console.log('='.repeat(50));

        // Create output JSON
        const output = {
            version: '1.0',
            source: 'https://erenshor.wiki.gg/wiki/Quests',
            scraped_date: new Date().toISOString().split('T')[0],
            quests: allQuests
        };

        // Save to file
        const outputPath = path.join(__dirname, 'ErenshorQuestData.json');
        fs.writeFileSync(outputPath, JSON.stringify(output, null, 2), 'utf8');
        console.log(`\nSaved to: ${outputPath}`);

        // Print sample
        if (allQuests.length > 0) {
            console.log('\nSample quest:');
            console.log(JSON.stringify(allQuests[0], null, 2));
        }

        return output;

    } finally {
        await browser.close();
    }
}

// Run the scraper
scrapeAllQuests()
    .then(() => {
        console.log('\n✓ Scraping complete!');
        process.exit(0);
    })
    .catch(error => {
        console.error('Error:', error);
        process.exit(1);
    });
