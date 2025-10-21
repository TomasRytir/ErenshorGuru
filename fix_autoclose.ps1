# Fix auto-close issue by adding debounce to Q key

$filePath = "C:\Users\tomas\Desktop\ErenshorQuestHelper\QuestTracker.cs"
$content = Get-Content $filePath -Raw

# Add debounce timer field after line with "private float lastQuestRefresh"
$oldPattern = "private float lastQuestRefresh = 0f;"
$newPattern = @"
private float lastQuestRefresh = 0f;
        private float lastQuestListToggle = -1f;
        private const float questListToggleCooldown = 0.3f; // Prevent accidental double-toggle
"@

$content = $content -replace [regex]::Escape($oldPattern), $newPattern

# Update the Q key toggle logic to use debounce
$oldToggle = @"
            // Toggle quest list with Q key
            if (Input.GetKeyDown(KeyCode.Q))
            {
                showQuestList = !showQuestList;
                QuestGuruPlugin.Logger.LogInfo(`$"Quest List: {(showQuestList ? "Shown" : "Hidden")}");
            }
"@

$newToggle = @"
            // Toggle quest list with Q key (with debounce to prevent accidental double-toggle)
            if (Input.GetKeyDown(KeyCode.Q))
            {
                // Only toggle if enough time has passed since last toggle
                if (Time.time - lastQuestListToggle > questListToggleCooldown)
                {
                    showQuestList = !showQuestList;
                    lastQuestListToggle = Time.time;
                    QuestGuruPlugin.Logger.LogInfo(`$"Quest List: {(showQuestList ? "Shown" : "Hidden")}");
                }
            }
"@

$content = $content -replace [regex]::Escape($oldToggle), $newToggle

Set-Content -Path $filePath -Value $content -NoNewline

Write-Host "Fixed auto-close issue!"
