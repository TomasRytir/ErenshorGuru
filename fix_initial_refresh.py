#!/usr/bin/env python3
"""Add initial quest refresh in Start() to fix empty quest list on startup"""

with open('QuestTracker.cs', 'r', encoding='utf-8') as f:
    content = f.read()

# Find Start() method and add initial refresh
old_start = '''            // Initialize temp settings values
            UpdateTempSettings();
        }

        private void UpdateTempSettings()'''

new_start = '''            // Initialize temp settings values
            UpdateTempSettings();

            // IMPORTANT: Do initial quest refresh on startup so quests show immediately
            RefreshQuestCache();
            lastQuestRefresh = Time.time;
        }

        private void UpdateTempSettings()'''

content = content.replace(old_start, new_start)

with open('QuestTracker.cs', 'w', encoding='utf-8') as f:
    f.write(content)

print("Added initial quest refresh in Start()")
