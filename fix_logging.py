#!/usr/bin/env python3
"""Fix excessive logging in GameQuestBridge.cs"""

import re

# Read the file
with open('GameQuestBridge.cs', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the spam logging lines
content = content.replace(
    'QuestGuruPlugin.Logger.LogInfo($"Found {titlesList.Count} quest titles");',
    '// Removed spam logging - runs every 5 seconds!'
)

content = content.replace(
    'QuestGuruPlugin.Logger.LogInfo($"Looking for quest with title: {questTitle}");',
    '// Removed spam logging'
)

content = content.replace(
    'QuestGuruPlugin.Logger.LogInfo($"  Found matching quest: {questName}");',
    '// Removed spam logging'
)

# Write back
with open('GameQuestBridge.cs', 'w', encoding='utf-8') as f:
    f.write(content)

print("Fixed excessive logging in GameQuestBridge.cs")
