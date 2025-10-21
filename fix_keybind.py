#!/usr/bin/env python3
"""Fix keybind conflict - change Q to L"""

# Read QuestTracker.cs
with open('QuestTracker.cs', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace all occurrences of KeyCode.Q with KeyCode.L
content = content.replace('KeyCode.Q', 'KeyCode.L')

# Also update help text
content = content.replace('Press Q to see all active quests', 'Press L to open quest list')
content = content.replace('"Show"} Quest List (Q)"', '"Show"} Quest List (L)"')
content = content.replace('"Hide"} Quest List (Q)"', '"Hide"} Quest List (L)"')
content = content.replace('  Q - Toggle quest list', '  L - Toggle quest list')

# Write back
with open('QuestTracker.cs', 'w', encoding='utf-8') as f:
    f.write(content)

print("Changed keybind from Q to L in QuestTracker.cs")
