using UnityEngine;

namespace ErenshorQuestGuru
{
    /// <summary>
    /// Marks the type of quest marker (! for available, ? for turn-in)
    /// </summary>
    public class QuestMarker : MonoBehaviour
    {
        public enum Type
        {
            Available,  // Yellow ! - quest available
            TurnIn      // Yellow ? - quest ready to turn in
        }

        public Type markerType;
    }
}
