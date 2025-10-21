# Rename ErenshorQuestHelper to ErenshorQuestGuru

$files = Get-ChildItem -Path "C:\Users\tomas\Desktop\ErenshorQuestHelper" -Filter *.cs -Recurse

foreach ($file in $files) {
    Write-Host "Processing: $($file.FullName)"

    $content = Get-Content $file.FullName -Raw

    # Replace all occurrences
    $content = $content -replace 'ErenshorQuestHelper', 'ErenshorQuestGuru'
    $content = $content -replace 'QuestHelperPlugin', 'QuestGuruPlugin'
    $content = $content -replace 'questhelper', 'questguru'
    $content = $content -replace 'Quest Helper', 'Quest Guru'

    Set-Content -Path $file.FullName -Value $content -NoNewline
    Write-Host "Updated: $($file.FullName)"
}

Write-Host "All CS files updated!"
