using UnityEngine;

namespace ErenshorQuestGuru
{
    /// <summary>
    /// Makes a UI element always face the camera (billboard effect)
    /// </summary>
    public class BillboardToCamera : MonoBehaviour
    {
        private Camera _cam;
        private Transform _player;

        private void Start()
        {
            _cam = GameData.PlayerControl?.camera;
            PlayerControl playerControl = GameData.PlayerControl;
            _player = playerControl != null ? playerControl.transform : null;
        }

        private void LateUpdate()
        {
            // Update camera reference if null
            if (_cam == null)
            {
                _cam = GameData.PlayerControl?.camera;
            }

            // Update player reference if null
            if (_player == null)
            {
                PlayerControl playerControl = GameData.PlayerControl;
                _player = playerControl != null ? playerControl.transform : null;
            }

            if (_cam == null || _player == null)
                return;

            // Make object face camera
            transform.rotation = Quaternion.LookRotation(transform.position - _cam.transform.position);

            // Destroy marker if player is too far away (optimization)
            float distance = Vector3.Distance(transform.position, _player.position);
            if (distance > 80f)
            {
                Destroy(gameObject);
            }
        }
    }
}
