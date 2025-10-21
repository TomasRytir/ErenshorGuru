# Rename csproj file

$content = Get-Content "C:\Users\tomas\Desktop\ErenshorQuestHelper\ErenshorQuestHelper.csproj" -Raw

$content = $content -replace 'ErenshorQuestHelper', 'ErenshorQuestGuru'
$content = $content -replace 'Quest Helper for Erenshor', 'Quest Guru for Erenshor'
$content = $content -replace 'Version>1.0.0', 'Version>2.4.0'

Set-Content -Path "C:\Users\tomas\Desktop\ErenshorQuestHelper\ErenshorQuestGuru.csproj" -Value $content -NoNewline

Write-Host "Created ErenshorQuestGuru.csproj"
