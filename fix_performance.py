#!/usr/bin/env python3
"""Fix performance issues in QuestHelperPlugin.cs"""

# Read the file
with open('QuestHelperPlugin.cs', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Find the line with _questMarkerUpdateInterval
for i, line in enumerate(lines):
    if '_questMarkerUpdateInterval = 0.5f;' in line:
        # Add new field after this one
        lines.insert(i+1, '        private float _lastQuestMarkerUpdate = 0f;\n')
        break

# Replace OnGUI method with Update method that uses timer
new_ongui = '''        private void Update()
        {
            // Quest marker updates - but NOT every frame! Use timer to avoid lag
            if (enableNPCMarkers.Value &&
                GameData.PlayerControl != null &&
                !GameData.InCharSelect &&
                !GameData.Zoning &&
                !_updatingQuestMarkers)
            {
                // Only update markers every 0.5 seconds
                if (Time.time - _lastQuestMarkerUpdate > _questMarkerUpdateInterval)
                {
                    _lastQuestMarkerUpdate = Time.time;
                    StartCoroutine(UpdateQuestMarkersCoroutine());
                }
            }
        }
'''

# Find and replace OnGUI method
in_ongui = False
ongui_start = -1
ongui_end = -1

for i, line in enumerate(lines):
    if 'private void OnGUI()' in line:
        in_ongui = True
        ongui_start = i
    elif in_ongui and line.strip() == '}' and 'StartCoroutine(UpdateQuestMarkersCoroutine());' in ''.join(lines[ongui_start:i]):
        ongui_end = i
        break

if ongui_start >= 0 and ongui_end >= 0:
    # Replace OnGUI method with Update method
    lines[ongui_start:ongui_end+1] = [new_ongui + '\n']

# Write back
with open('QuestHelperPlugin.cs', 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("Fixed performance issue in QuestHelperPlugin.cs - changed OnGUI to Update with timer")
