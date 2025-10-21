#!/usr/bin/env python3
"""Add R key for manual refresh and decrease refresh interval"""

# Fix QuestTracker.cs
with open('QuestTracker.cs', 'r', encoding='utf-8') as f:
    content = f.read()

# Change refresh interval from 5 seconds to 2 seconds for faster updates
content = content.replace(
    'private float questRefreshInterval = 5f; // Refresh every 5 seconds',
    'private float questRefreshInterval = 2f; // Refresh every 2 seconds for faster quest updates'
)

# Add R key handling in Update() method - find the section with key handling
# We'll add it after the L key toggle
update_section_old = '''            // Toggle settings with O key (or configured key)
            if (Input.GetKeyDown(Plugin.GetSettingsKey()))
            {
                showSettings = !showSettings;
                if (showSettings)
                {
                    UpdateTempSettings(); // Reload current values
                }
                QuestGuruPlugin.Logger.LogInfo($"Settings: {(showSettings ? "Shown" : "Hidden")}");
            }'''

update_section_new = '''            // Toggle settings with O key (or configured key)
            if (Input.GetKeyDown(Plugin.GetSettingsKey()))
            {
                showSettings = !showSettings;
                if (showSettings)
                {
                    UpdateTempSettings(); // Reload current values
                }
                QuestGuruPlugin.Logger.LogInfo($"Settings: {(showSettings ? "Shown" : "Hidden")}");
            }

            // R key - manual refresh quests
            if (Input.GetKeyDown(KeyCode.R))
            {
                RefreshQuestCache();
                QuestGuruPlugin.Logger.LogInfo("Quest list manually refreshed");
            }'''

content = content.replace(update_section_old, update_section_new)

# Write back
with open('QuestTracker.cs', 'w', encoding='utf-8') as f:
    f.write(content)

print("Added R key for manual refresh and decreased refresh interval to 2 seconds")
