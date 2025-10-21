#!/usr/bin/env python3
"""Merge duplicate Update methods in QuestHelperPlugin.cs"""

with open('QuestHelperPlugin.cs', 'r', encoding='utf-8') as f:
    content = f.read()

# Find the second Update method and remove it (it's the quest marker update)
# We'll add its content to the first Update method instead

# First, remove the second Update() method (lines 360-376)
second_update = '''        private void Update()
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
        }'''

content = content.replace(second_update, '')

# Now find the first Update method and add the quest marker logic to it
first_update_old = '''        private void Update()
        {
            // Toggle tracker visibility
            if (Input.GetKeyDown(toggleTrackerKey.Value))
            {
                showQuestTracker = !showQuestTracker;
                Logger.LogInfo($"Quest Tracker: {(showQuestTracker ? "Shown" : "Hidden")}");
            }

            // Debug key - print quest info
            if (enableDebug.Value && Input.GetKeyDown(debugKey.Value))
            {
                RunDebugCommands();
            }

            // End key - manual refresh quests (useful after character switch)
            if (Input.GetKeyDown(KeyCode.End))
            {
                Logger.LogInfo("Manual quest refresh triggered");
                ForceRefreshQuests();
            }
        }'''

first_update_new = '''        private void Update()
        {
            // Toggle tracker visibility
            if (Input.GetKeyDown(toggleTrackerKey.Value))
            {
                showQuestTracker = !showQuestTracker;
                Logger.LogInfo($"Quest Tracker: {(showQuestTracker ? "Shown" : "Hidden")}");
            }

            // Debug key - print quest info
            if (enableDebug.Value && Input.GetKeyDown(debugKey.Value))
            {
                RunDebugCommands();
            }

            // End key - manual refresh quests (useful after character switch)
            if (Input.GetKeyDown(KeyCode.End))
            {
                Logger.LogInfo("Manual quest refresh triggered");
                ForceRefreshQuests();
            }

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
        }'''

content = content.replace(first_update_old, first_update_new)

with open('QuestHelperPlugin.cs', 'w', encoding='utf-8') as f:
    f.write(content)

print("Merged duplicate Update methods")
