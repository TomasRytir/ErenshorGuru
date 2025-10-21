using System;
using System.Collections.Generic;
using UnityEngine;

namespace ErenshorQuestGuru
{
    /// <summary>
    /// Quest wiki data - instructions, locations, NPCs from wiki
    /// </summary>
    public static class QuestWikiData
    {
        private static Dictionary<string, WikiQuestInfo> questDatabase = new Dictionary<string, WikiQuestInfo>();

        static QuestWikiData()
        {
            InitializeQuestData();
        }

        private static void InitializeQuestData()
        {
            // Load from JSON file if exists
            LoadFromJSON();

            // Fallback: Add some common quests manually
            // These will be overridden if JSON exists

            AddQuest("Underloft Compass", new WikiQuestInfo
            {
                GiverNPC = "Asaga Underloft",
                GiverLocation = "Newhaven City",
                Objectives = new List<string>
                {
                    "Retrieve the Underloft Compass",
                    "Return to Asaga Underloft"
                },
                Instructions = "Find the compass and return it to Asaga in Newhaven City.",
                Notes = "Quest starter NPC"
            });

            // Add more quests here as we scrape wiki data
            // For now, this structure is ready to accept data from:
            // 1. Manual entry
            // 2. JSON file loading
            // 3. Future: automatic wiki scraping
        }

        private static void LoadFromJSON()
        {
            try
            {
                string jsonPath = System.IO.Path.Combine(
                    BepInEx.Paths.PluginPath,
                    "ErenshorQuestData.json"
                );

                if (System.IO.File.Exists(jsonPath))
                {
                    string json = System.IO.File.ReadAllText(jsonPath);
                    var data = Newtonsoft.Json.JsonConvert.DeserializeObject<QuestDataFile>(json);

                    if (data != null && data.quests != null)
                    {
                        QuestGuruPlugin.Logger?.LogInfo($"Loading {data.quests.Count} quests from JSON...");

                        int count = 0;
                        foreach (var quest in data.quests)
                        {
                            AddQuest(quest.name, new WikiQuestInfo
                            {
                                GiverNPC = quest.npc,
                                GiverLocation = quest.location,
                                Objectives = quest.objectives ?? new List<string>(),
                                Instructions = quest.instructions,
                                RewardInfo = quest.rewards,
                                Notes = quest.notes
                            });
                            count++;
                        }

                        QuestGuruPlugin.Logger?.LogInfo($"Successfully loaded {count} quests from JSON");

                        // Log first few quest names for debugging
                        int logCount = 0;
                        foreach (var questName in questDatabase.Keys)
                        {
                            if (logCount < 5)
                            {
                                QuestGuruPlugin.Logger?.LogInfo($"  - '{questName}'");
                                logCount++;
                            }
                            else break;
                        }
                        if (questDatabase.Count > 5)
                        {
                            QuestGuruPlugin.Logger?.LogInfo($"  ... and {questDatabase.Count - 5} more");
                        }
                    }
                    else
                    {
                        QuestGuruPlugin.Logger?.LogWarning("JSON data or quests array is null");
                    }
                }
            }
            catch (Exception ex)
            {
                QuestGuruPlugin.Logger?.LogWarning($"Could not load quest JSON: {ex.Message}");
            }
        }

        public static void AddQuest(string questName, WikiQuestInfo info)
        {
            if (!questDatabase.ContainsKey(questName))
            {
                questDatabase[questName] = info;
            }
        }

        public static WikiQuestInfo GetQuestInfo(string questName)
        {
            if (questDatabase.TryGetValue(questName, out WikiQuestInfo info))
            {
                // Removed spam: QuestGuruPlugin.Logger?.LogInfo($"Found wiki data for quest: '{questName}'");
                return info;
            }

            QuestGuruPlugin.Logger?.LogWarning($"No wiki data found for quest: '{questName}'. Available quests: {questDatabase.Count}");

            // Try fuzzy matching (case-insensitive, trim)
            foreach (var kvp in questDatabase)
            {
                if (kvp.Key.Trim().Equals(questName.Trim(), StringComparison.OrdinalIgnoreCase))
                {
                    QuestGuruPlugin.Logger?.LogInfo($"Found quest with fuzzy match: '{kvp.Key}' for '{questName}'");
                    return kvp.Value;
                }
            }

            return null;
        }

        public static bool HasWikiData(string questName)
        {
            return questDatabase.ContainsKey(questName);
        }
    }

    public class WikiQuestInfo
    {
        public string GiverNPC { get; set; }
        public string GiverLocation { get; set; }
        public List<string> Objectives { get; set; }
        public string Instructions { get; set; }
        public string RewardInfo { get; set; }
        public string Notes { get; set; }

        public WikiQuestInfo()
        {
            Objectives = new List<string>();
        }
    }

    // JSON file structure
    public class QuestDataFile
    {
        public string version { get; set; }
        public string source { get; set; }
        public List<QuestDataEntry> quests { get; set; }
    }

    public class QuestDataEntry
    {
        public string name { get; set; }
        public string npc { get; set; }
        public string location { get; set; }
        public List<string> objectives { get; set; }
        public string instructions { get; set; }
        public string rewards { get; set; }
        public string notes { get; set; }
    }
}
