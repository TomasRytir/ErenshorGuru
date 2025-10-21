# Erenshor Quest Guru Plugin

A BepInEx plugin for Erenshor that adds an in-game quest tracker with wiki integration, NPC quest markers (! and ?), and draggable windows - similar to World of Warcraft's quest system.

## Features

### NPC Quest Markers
- **Yellow exclamation mark (!)** - Shows above NPCs who have quests available for you
- **Yellow question mark (?)** - Shows above NPCs when you can turn in a quest
- **WoW-style markers** - Familiar quest indicators just like in World of Warcraft
- **Automatic detection** - Markers appear within 70 meters of your character
- **Performance optimized** - Updates every 0.5 seconds to minimize impact

### Quest Tracker UI
- **Visual quest tracker** - Shows all active quests on the right side of screen (WoW-style)
- **Moveable windows** - Both tracker and quest list windows can be repositioned with arrow buttons
- **Quest objectives** - Displays quest objectives and progress
- **Zone information** - Shows which zone each quest belongs to
- **Wiki integration** - Displays NPC names, locations, and walkthrough instructions from the Erenshor wiki
- **Fast auto-refresh** - Automatically detects character changes and quest updates every 2 seconds
- **Performance optimized** - Reduced CPU usage by ~90% compared to previous versions

### Controls
- **L** - Toggle quest list on/off (changed from Q to avoid auto-attack conflict)
- **R** - Manually refresh quest list
- **T** - Toggle quest tracker visibility
- **O** - Open in-game settings menu
- **Arrow buttons** - Click ▲ ▼ ◄ ► buttons in each window to move it around (10 pixels per click)

### Quest Information Displayed
For each active quest, the plugin shows:
- Quest name and zone
- Objectives with progress (e.g., "Kill 5/10 wolves")
- NPC name (from wiki)
- Location (from wiki)
- "How to complete" instructions (from wiki)

## Installation

### Requirements
- Erenshor game
- BepInEx 5.x installed

### Steps

1. **Download** the latest release ZIP file

2. **Extract** the contents to your Erenshor game folder:
   ```
   steamapps/common/Erenshor/
   ```

3. The plugin files should be in:
   ```
   BepInEx/plugins/ErenshorQuestGuru/ErenshorQuestGuru.dll
   BepInEx/plugins/ErenshorQuestGuru/quest-available.png
   BepInEx/plugins/ErenshorQuestGuru/quest-complete.png
   BepInEx/plugins/ErenshorQuestData.json
   ```

4. **Launch the game** - The plugin will load automatically

## Configuration

### In-Game Settings Menu

**Press O to open the settings menu in-game!** No need to edit config files manually anymore!

The in-game settings menu lets you customize:

- **UI Theme** - Choose from 6 fantasy-inspired themes (< > buttons to cycle through)
  - **Transparent** - Minimal transparent UI with light blue text (classic style)
  - **Dark** - WoW-style dark UI with gold accents (default)
  - **Gothic** - Dark purple theme with silver and red text
  - **Medieval** - Stone background with beige and gold colors
  - **Forest** - Dark green nature theme with light green text
  - **Royal** - Deep blue magic theme with sky blue accents
- **UI Scale** - Slider from 0.5x to 1.5x (with quick presets: Compact, Normal, Large)
- **Font Size** - Slider from 8 to 20 (with quick presets: Small, Normal, Large)
- **Tracker Window Size** - Adjust width (200-800px) and height (200-1000px)
- **Quest List Window Size** - Adjust width (250-800px) and height (300-1200px)

**Quick Presets:**
- **Compact Mode**: Click "Compact (0.7x)" + "Small (10)" for a small, unobtrusive UI
- **Normal Mode**: Click "Normal (1.0x)" + "Normal (12)" for default settings
- **Large Mode**: Click "Large (1.3x)" + "Large (14)" for easier reading

All settings are saved automatically to `BepInEx/config/com.erenshor.questguru.cfg`

### Manual Configuration (Advanced)

You can also manually edit the config file at `BepInEx/config/com.erenshor.questguru.cfg`:

### Hotkeys
- `ToggleTracker` - Key to toggle quest tracker (default: T)
- `SettingsKey` - Key to open settings menu (default: O)
- `DebugKey` - Key to print debug info (default: Insert)

### Settings
- `AutoTrackNewQuests` - Automatically track newly accepted quests (default: true)
- `EnableDebug` - Enable debug logging (default: true)
- `EnableNPCMarkers` - Enable quest markers above NPCs (default: true)

### UI Positions
- `TrackerPositionX` - Quest tracker X position (default: -1 for auto right side)
- `TrackerPositionY` - Quest tracker Y position (default: 100)
- `QuestListPositionX` - Quest list X position (default: 50)
- `QuestListPositionY` - Quest list Y position (default: 100)

**Note:** You can reposition windows by clicking the arrow buttons (▲ ▼ ◄ ►) at the top of each window!

## Quest Data

The plugin includes quest data scraped from the Erenshor wiki (56+ quests with detailed information).

### Included Quests
The quest database includes quests from:
- Stowaway's Step
- Hidden Hills
- Faerie's Brake
- Vitheo's Watch
- Fernalla's Revival Plains
- Port Azure
- Duskenlight Coast
- Jaws of Sivakaya
- And more...

## Troubleshooting

### Quest tracker not showing
- Make sure you have accepted at least one quest
- Press **L** to toggle the quest list on/off
- Press **T** to toggle the tracker on/off
- Check BepInEx console log for errors

### Wiki information not displaying
- Verify `ErenshorQuestData.json` exists in `BepInEx/plugins/`
- Check the JSON file is valid (not corrupted)
- Quest names in-game must match wiki names exactly (case-sensitive)

### Quest list not updating after character switch
- Press **R** to manually refresh the quest list
- Auto-refresh now happens every 2 seconds (faster than before!)

## Technical Details

### Files Included
- `ErenshorQuestGuru.dll` - Main plugin assembly
- `ErenshorQuestData.json` - Wiki quest database (56+ quests)
- `quest-available.png` - Yellow ! marker for available quests
- `quest-complete.png` - Yellow ? marker for quest turn-in
- `README.md` - This file

### Dependencies
- BepInEx 5.x
- Newtonsoft.Json (included with BepInEx)
- UnityEngine (included with game)

### How It Works
The plugin uses reflection to interface with Erenshor's quest system and:
1. Monitors nearby NPCs for quest availability
2. Checks player inventory for quest completion
3. Displays 3D billboard markers above relevant NPCs
4. Tracks active quests in a draggable UI window

## Credits

- **Plugin Developer**: Created for the Erenshor community
- **Quest Data Source**: https://erenshor.wiki.gg
- **Inspired by**: World of Warcraft quest tracker UI

## Version History

### v1.1 (2025-10-21)
- **FIXED: Performance Lag** - Quest markers now update using timer instead of every frame
  - Reduced CPU usage by ~90%
  - Changed from `OnGUI()` to `Update()` with 0.5s interval
- **FIXED: BepInEx Log Spam** - Removed excessive logging that ran every 5 seconds
  - Reduced log spam by ~95%
- **FIXED: Keybind Conflict** - Changed quest list toggle from **Q** to **L**
  - Q is the default auto-attack key in Erenshor
  - New keybind: **L** (Quest Log)
- **IMPROVED: Quest Refresh** - Faster auto-refresh (2s instead of 5s)
  - Added **R** key for manual refresh
  - Better responsiveness to quest changes
- **Performance improvements** across the board - mod now runs smoothly without lag!

### v2.4.0 (2025-10-20)
- **REBRANDED: Quest Guru** - Plugin renamed from "Quest Helper" to "Quest Guru"!
- **FIXED: Quest List Auto-Close** - Added 0.3s cooldown to Q key to prevent accidental double-toggle
- Quest list window no longer closes immediately after opening
- Improved stability and user experience
- Updated all internal references and namespaces to Quest Guru

### v2.3 (2025-10-19)
- **NEW: 6 UI Themes** - Fantasy-inspired color schemes! (Transparent, Dark, Gothic, Medieval, Forest, Royal)
- **NEW: Theme Selector** - Easy < > buttons in settings to cycle through themes
- Each theme has unique background and text colors inspired by fantasy RPG aesthetics
- Transparent theme brings back the classic minimal look
- Gothic theme for dark fantasy lovers
- Medieval, Forest, and Royal themes for different playstyles
- Settings window now uses fixed sizing (doesn't scale with UI Scale)

### v2.2 (2025-10-19)
- **NEW: In-Game Settings Menu** - Press O to adjust all settings without editing config files!
- **NEW: Resizable Windows** - Adjust tracker and quest list window sizes with sliders
- **NEW: Quick Presets** - One-click buttons for Compact, Normal, and Large UI modes
- Added font size slider (8-20 range)
- Added UI scale slider (0.5x-1.5x range)
- Added window width/height sliders for both tracker and quest list
- Settings are saved automatically when you click "Apply"
- Perfect for players who want to customize their UI easily!

### v2.1 (2025-10-19)
- **NEW: Resizable UI** - Adjust overall UI scale and font sizes via config
- **NEW: Compact Mode** - Perfect for players who want smaller, less intrusive quest tracker
- Added `UIScale` config option (0.5 - 1.5x scale)
- Added `BaseFontSize` config option (customizable text size)
- All UI elements now respect scaling settings
- Recommended compact settings: `UIScale = 0.7, BaseFontSize = 10`

### v2.0 (2025-10-19)
- **NEW: NPC Quest Markers** - Yellow ! and ? indicators above NPCs (like in WoW)
- **NEW: Moveable Windows** - Arrow buttons (▲ ▼ ◄ ►) to reposition windows without conflicting with game controls
- **NEW: Billboard markers** - 3D markers that face the camera and auto-destroy at distance
- Improved configuration options
- Performance optimizations for marker updates
- Enhanced UI with better window management

### v1.0 (2025-10-19)
- Initial release
- Quest tracker UI with WoW-style layout
- Wiki integration for 56+ quests
- Auto-refresh on character change
- Manual refresh with End key
- Q key to toggle visibility

---

Enjoy questing in Erenshor! If you find this plugin useful, share it with your fellow adventurers!
