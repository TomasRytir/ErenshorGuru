# How to Update Quest Data from Wiki

The quest helper plugin can display quest information from the Erenshor wiki. This guide explains how to update the quest data.

## Current Status

The plugin is ready to load quest data from: `BepInEx/plugins/ErenshorQuestData.json`

A starter file with 5 example quests has been created.

## Option 1: Browser Console Scraper (RECOMMENDED - Gets ALL quests)

This method bypasses Cloudflare protection and gets all quests from the wiki.

### Steps:

1. Open your browser and go to: https://erenshor.wiki.gg/wiki/Quests

2. Press `F12` to open Developer Tools

3. Click on the "Console" tab

4. Open the file `browser_scraper.js` from this folder

5. Copy the ENTIRE contents of `browser_scraper.js`

6. Paste it into the browser console

7. Press Enter

8. Wait for the script to finish (it will show progress in console)

9. When complete, the JSON data will be:
   - Copied to your clipboard automatically (if browser supports it)
   - Displayed in the console for manual copy

10. Save the JSON to:
    - Development: `C:\Users\tomas\Desktop\ErenshorQuestHelper\ErenshorQuestData.json`
    - Game: `C:\Program Files (x86)\Steam\steamapps\common\Erenshor\BepInEx\plugins\ErenshorQuestData.json`

11. Restart the game to load the new quest data

## Option 2: Python Scraper (If you have Python installed)

If you have Python 3 installed with the required packages:

```bash
cd C:\Users\tomas\Desktop\ErenshorQuestHelper
pip install requests beautifulsoup4
python scrape_wiki.py
```

Then copy the generated `QuestData.json` to the game's plugins folder.

## Option 3: Manual Entry

You can manually edit `ErenshorQuestData.json` and add quests following this format:

```json
{
  "version": "1.0",
  "source": "https://erenshor.wiki.gg/wiki/Quests",
  "quests": [
    {
      "name": "Quest Name Here",
      "npc": "NPC Name",
      "location": "Zone Name",
      "objectives": [
        "Objective 1",
        "Objective 2"
      ],
      "instructions": "Detailed walkthrough of how to complete the quest.",
      "rewards": "Reward information",
      "notes": "Any additional notes"
    }
  ]
}
```

## Testing

After updating the quest data:

1. Copy the JSON file to: `C:\Program Files (x86)\Steam\steamapps\common\Erenshor\BepInEx\plugins\ErenshorQuestData.json`

2. Restart Erenshor

3. Accept a quest that's in the wiki data

4. Press `T` to open the quest tracker

5. You should see the wiki information displayed:
   - NPC name
   - Location
   - "How to complete:" instructions

## JSON File Location

The game loads quest data from:
```
C:\Program Files (x86)\Steam\steamapps\common\Erenshor\BepInEx\plugins\ErenshorQuestData.json
```

Keep a backup in your development folder:
```
C:\Users\tomas\Desktop\ErenshorQuestHelper\ErenshorQuestData.json
```

## Troubleshooting

### Quest data not showing
- Check the BepInEx console log for errors
- Verify the JSON file is in the correct location
- Make sure the quest name in the JSON matches exactly (case-sensitive)

### Browser scraper not working
- Make sure you're on the actual quests page before running
- Check browser console for errors
- Try refreshing the page and running again

### Python scraper fails with Cloudflare error
- Use the browser console method instead
- Cloudflare protection blocks simple HTTP requests
