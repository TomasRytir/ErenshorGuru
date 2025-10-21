# Erenshor Wiki Quest Scraper - PowerShell Version
# Scrapes all quest data from https://erenshor.wiki.gg/wiki/Quests

$BaseUrl = "https://erenshor.wiki.gg"
$QuestsUrl = "$BaseUrl/wiki/Quests"

Write-Host "Erenshor Quest Wiki Scraper" -ForegroundColor Cyan
Write-Host "=" * 50

# Function to fetch web page
function Get-WebPage {
    param([string]$Url)

    try {
        $response = Invoke-WebRequest -Uri $Url -UserAgent "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36" -TimeoutSec 10
        return $response.Content
    }
    catch {
        Write-Host "Error fetching $Url : $_" -ForegroundColor Red
        return $null
    }
}

# Function to extract text from HTML element
function Get-TextContent {
    param([string]$Html)

    # Remove HTML tags and decode entities
    $text = $Html -replace '<[^>]+>', ''
    $text = [System.Web.HttpUtility]::HtmlDecode($text)
    return $text.Trim()
}

# Function to extract quest links from main page
function Get-QuestLinks {
    param([string]$Html)

    $questLinks = @()

    # Match all <a> tags with href starting with /wiki/
    $matches = [regex]::Matches($Html, '<a\s+(?:[^>]*?\s+)?href="(/wiki/[^"]+)"[^>]*>([^<]+)</a>')

    foreach ($match in $matches) {
        $href = $match.Groups[1].Value
        $name = Get-TextContent -Html $match.Groups[2].Value

        # Filter out category/special pages and the main Quests page itself
        if ($href -ne '/wiki/Quests' -and
            $href -notmatch 'Category:' -and
            $href -notmatch 'Special:' -and
            $href -notmatch 'File:' -and
            $href -notmatch 'Template:' -and
            $name.Length -gt 0) {

            $fullUrl = $BaseUrl + $href
            $questLinks += @{
                'name' = $name
                'url' = $fullUrl
            }
        }
    }

    # Remove duplicates
    $uniqueLinks = @{}
    foreach ($link in $questLinks) {
        if (-not $uniqueLinks.ContainsKey($link.url)) {
            $uniqueLinks[$link.url] = $link
        }
    }

    return $uniqueLinks.Values
}

# Function to parse individual quest page
function Parse-QuestPage {
    param(
        [string]$Html,
        [string]$QuestName
    )

    $questData = @{
        'name' = $QuestName
        'npc' = ''
        'location' = ''
        'objectives' = @()
        'instructions' = ''
        'rewards' = ''
        'notes' = ''
    }

    # Look for infobox table
    if ($Html -match '<table[^>]*class="[^"]*infobox[^"]*"[^>]*>(.*?)</table>') {
        $infoboxHtml = $matches[1]

        # Extract rows
        $rowMatches = [regex]::Matches($infoboxHtml, '<tr[^>]*>(.*?)</tr>')
        foreach ($row in $rowMatches) {
            $rowHtml = $row.Groups[1].Value

            if ($rowHtml -match '<th[^>]*>(.*?)</th>.*?<td[^>]*>(.*?)</td>') {
                $header = (Get-TextContent -Html $matches[1]).ToLower()
                $data = Get-TextContent -Html $matches[2]

                if ($header -match 'giver|npc') {
                    $questData.npc = $data
                }
                elseif ($header -match 'location|zone|area') {
                    $questData.location = $data
                }
                elseif ($header -match 'reward') {
                    $questData.rewards = $data
                }
            }
        }
    }

    # Extract objectives from lists
    $objectiveMatches = [regex]::Matches($Html, '<(?:h2|h3)[^>]*>(?:<[^>]+>)*(?:Objective|Task|Goal)s?(?:</[^>]+>)*</(?:h2|h3)>(.*?)(?=<(?:h2|h3)|$)')
    if ($objectiveMatches.Count -gt 0) {
        $sectionHtml = $objectiveMatches[0].Groups[1].Value

        # Find list items
        $liMatches = [regex]::Matches($sectionHtml, '<li[^>]*>(.*?)</li>')
        foreach ($li in $liMatches) {
            $objective = Get-TextContent -Html $li.Groups[1].Value
            if ($objective.Length -gt 0) {
                $questData.objectives += $objective
            }
        }
    }

    # Extract walkthrough/guide
    $guideMatches = [regex]::Matches($Html, '<(?:h2|h3)[^>]*>(?:<[^>]+>)*(?:Walkthrough|Guide|How to|Instructions)(?:</[^>]+>)*</(?:h2|h3)>(.*?)(?=<(?:h2|h3)|$)')
    if ($guideMatches.Count -gt 0) {
        $sectionHtml = $guideMatches[0].Groups[1].Value

        # Extract paragraphs
        $paragraphs = @()
        $pMatches = [regex]::Matches($sectionHtml, '<p[^>]*>(.*?)</p>')
        foreach ($p in $pMatches) {
            $text = Get-TextContent -Html $p.Groups[1].Value
            if ($text.Length -gt 10) {
                $paragraphs += $text
            }
        }

        $questData.instructions = ($paragraphs -join ' ')
    }

    # Fallback: get first few paragraphs if no specific instructions
    if ($questData.instructions.Length -eq 0) {
        $pMatches = [regex]::Matches($Html, '<p[^>]*>(.*?)</p>')
        $paragraphs = @()
        foreach ($p in $pMatches | Select-Object -First 3) {
            $text = Get-TextContent -Html $p.Groups[1].Value
            if ($text.Length -gt 20) {
                $paragraphs += $text
            }
        }

        $combined = ($paragraphs -join ' ')
        if ($combined.Length -gt 500) {
            $questData.instructions = $combined.Substring(0, 500)
        } else {
            $questData.instructions = $combined
        }
    }

    return $questData
}

# Load System.Web for HTML decoding
Add-Type -AssemblyName System.Web

# Main scraping logic
Write-Host "Fetching main quests page..." -ForegroundColor Yellow
$mainHtml = Get-WebPage -Url $QuestsUrl

if (-not $mainHtml) {
    Write-Host "Failed to fetch main page. Exiting." -ForegroundColor Red
    exit 1
}

Write-Host "Extracting quest links..." -ForegroundColor Yellow
$questLinks = Get-QuestLinks -Html $mainHtml
Write-Host "Found $($questLinks.Count) potential quest links" -ForegroundColor Green

$allQuests = @()
$counter = 0

foreach ($link in $questLinks) {
    $counter++
    Write-Host "[$counter/$($questLinks.Count)] Scraping: $($link.name)" -ForegroundColor Cyan

    $questHtml = Get-WebPage -Url $link.url
    if ($questHtml) {
        $questData = Parse-QuestPage -Html $questHtml -QuestName $link.name
        $allQuests += $questData

        # Be nice to the server
        Start-Sleep -Milliseconds 500
    }
    else {
        Write-Host "  Failed to fetch quest page" -ForegroundColor Red
    }
}

# Save to JSON
$output = @{
    'version' = '1.0'
    'source' = 'https://erenshor.wiki.gg/wiki/Quests'
    'scraped_date' = (Get-Date -Format 'yyyy-MM-dd')
    'quests' = $allQuests
}

$jsonPath = Join-Path $PSScriptRoot "ErenshorQuestData.json"
$output | ConvertTo-Json -Depth 10 | Out-File -FilePath $jsonPath -Encoding UTF8

Write-Host ""
Write-Host "Saved $($allQuests.Count) quests to ErenshorQuestData.json" -ForegroundColor Green

# Print sample
if ($allQuests.Count -gt 0) {
    Write-Host ""
    Write-Host "Sample quest:" -ForegroundColor Yellow
    $allQuests[0] | ConvertTo-Json -Depth 5 | Write-Host
}

Write-Host ""
Write-Host "Successfully scraped $($allQuests.Count) quests!" -ForegroundColor Green
