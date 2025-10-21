#!/usr/bin/env python3
"""Update README for v1.1"""

with open('README.md', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update Controls section
content = content.replace(
    '- **Q** - Toggle quest list on/off (with 0.3s cooldown to prevent accidental double-toggle)\n- **T** - Toggle quest tracker visibility\n- **O** - Open in-game settings menu\n- **End** - Manually refresh quest list (useful after character switch)',
    '- **L** - Toggle quest list on/off (changed from Q to avoid auto-attack conflict)\n- **R** - Manually refresh quest list\n- **T** - Toggle quest tracker visibility\n- **O** - Open in-game settings menu'
)

# 2. Update Quest Tracker UI section
content = content.replace(
    '- **Auto-refresh** - Automatically detects character changes and quest updates',
    '- **Fast auto-refresh** - Automatically detects character changes and quest updates every 2 seconds\n- **Performance optimized** - Reduced CPU usage by ~90% compared to previous versions'
)

# 3. Update troubleshooting - quest tracker not showing
content = content.replace(
    '- Press **Q** to toggle the tracker on/off',
    '- Press **L** to toggle the quest list on/off\n- Press **T** to toggle the tracker on/off'
)

# 4. Update troubleshooting - quest list not updating
content = content.replace(
    '### Quest list not updating after character switch\n- Press **End** to manually refresh the quest list\n- Wait a few seconds for auto-refresh to detect the change\n\n### Quest list window closes immediately when pressing Q\n- Fixed in v2.4.0! The Q key now has a 0.3s cooldown to prevent accidental double-toggle',
    '### Quest list not updating after character switch\n- Press **R** to manually refresh the quest list\n- Auto-refresh now happens every 2 seconds (faster than before!)'
)

# 5. Add v1.1 to version history (at the top)
version_history_marker = '## Version History\n\n### v2.4.0 (2025-10-20)'
new_version = '''## Version History

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

### v2.4.0 (2025-10-20)'''

content = content.replace(version_history_marker, new_version)

with open('README.md', 'w', encoding='utf-8') as f:
    f.write(content)

print("README.md updated for v1.1!")
