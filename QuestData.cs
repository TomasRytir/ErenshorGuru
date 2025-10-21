using System;
using System.Collections.Generic;
using UnityEngine;

namespace ErenshorQuestGuru
{
    /// <summary>
    /// Holds all information about a quest and its objectives
    /// </summary>
    public class QuestData
    {
        public string Name { get; set; }
        public string Description { get; set; }
        public int QuestID { get; set; }
        public QuestObjective CurrentObjective { get; set; }
        public List<QuestObjective> AllObjectives { get; set; }
        public QuestStatus Status { get; set; }
        public int Level { get; set; }

        public QuestData()
        {
            AllObjectives = new List<QuestObjective>();
            Status = QuestStatus.Active;
        }

        /// <summary>
        /// Gets the position where the player should go for current objective
        /// </summary>
        public Vector3 GetCurrentObjectivePosition()
        {
            if (CurrentObjective == null)
                return Vector3.zero;

            return CurrentObjective.TargetPosition;
        }

        /// <summary>
        /// Gets readable description of current step
        /// </summary>
        public string GetCurrentStepDescription()
        {
            if (CurrentObjective == null)
                return "Quest completed";

            return CurrentObjective.Description;
        }

        /// <summary>
        /// Gets the map/zone name for current objective
        /// </summary>
        public string GetCurrentZone()
        {
            if (CurrentObjective == null)
                return "Unknown";

            return CurrentObjective.ZoneName;
        }
    }

    /// <summary>
    /// Represents a single quest objective/step
    /// </summary>
    public class QuestObjective
    {
        public string Description { get; set; }
        public QuestObjectiveType Type { get; set; }
        public Vector3 TargetPosition { get; set; }
        public string TargetNPCName { get; set; }
        public string ZoneName { get; set; }
        public string RequiredItem { get; set; }
        public int RequiredAmount { get; set; }
        public int CurrentAmount { get; set; }
        public bool IsCompleted { get; set; }

        public string GetProgressText()
        {
            if (Type == QuestObjectiveType.Collect || Type == QuestObjectiveType.Kill)
            {
                return $"{CurrentAmount}/{RequiredAmount}";
            }

            return IsCompleted ? "Complete" : "In Progress";
        }
    }

    public enum QuestObjectiveType
    {
        TalkTo,        // Talk to NPC
        Kill,          // Kill X enemies
        Collect,       // Collect X items
        GoTo,          // Go to location
        TurnIn,        // Turn in quest
        Interact,      // Interact with object
        Explore        // Discover location
    }

    public enum QuestStatus
    {
        Active,        // Quest is active
        Completed,     // Quest is done but not turned in
        TurnedIn       // Quest fully finished
    }
}
