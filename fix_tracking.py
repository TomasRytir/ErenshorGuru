#!/usr/bin/env python3
"""Fix quest tracking - store QuestID instead of object reference"""

# Fix QuestHelperPlugin.cs
with open('QuestHelperPlugin.cs', 'r', encoding='utf-8') as f:
    content = f.read()

# Change from storing QuestData object to storing int QuestID
content = content.replace(
    'private QuestData currentTrackedQuest;',
    'private int currentTrackedQuestID = -1;  // Store QuestID instead of object to survive cache refresh'
)

# Update TrackQuest method
old_track = '''        // Called by UI when player clicks a quest to track
        public void TrackQuest(QuestData quest)
        {
            currentTrackedQuest = quest;
            Logger.LogInfo($"Now tracking quest: {quest.Name}");
        }'''

new_track = '''        // Called by UI when player clicks a quest to track
        public void TrackQuest(QuestData quest)
        {
            currentTrackedQuestID = quest.QuestID;
            Logger.LogInfo($"Now tracking quest: {quest.Name} (ID: {quest.QuestID})");
        }'''

content = content.replace(old_track, new_track)

# Update UntrackQuest method
content = content.replace(
    'currentTrackedQuest = null;',
    'currentTrackedQuestID = -1;'
)

# Update GetTrackedQuest method - now needs to find quest in cache
old_get = '''        public QuestData GetTrackedQuest()
        {
            return currentTrackedQuest;
        }'''

new_get = '''        public QuestData GetTrackedQuest()
        {
            if (currentTrackedQuestID == -1)
                return null;

            // Find quest in current cache by ID (survives refresh)
            return GameQuestBridge.GetQuestByID(currentTrackedQuestID);
        }'''

content = content.replace(old_get, new_get)

with open('QuestHelperPlugin.cs', 'w', encoding='utf-8') as f:
    f.write(content)

print("Fixed quest tracking - now stores QuestID instead of object reference")
