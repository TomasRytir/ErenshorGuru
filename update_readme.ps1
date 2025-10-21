# Update README with Quest Guru branding

$content = Get-Content "C:\Users\tomas\Desktop\ErenshorQuestHelper\README.md" -Raw

$content = $content -replace 'ErenshorQuestHelper', 'ErenshorQuestGuru'
$content = $content -replace 'Quest Helper', 'Quest Guru'
$content = $content -replace 'quest helper', 'quest guru'

Set-Content -Path "C:\Users\tomas\Desktop\ErenshorQuestHelper\README.md" -Value $content -NoNewline

Write-Host "README.md updated!"
