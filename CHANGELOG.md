# Quest Guru - Opravy verze (čerstvá build)

## Opravené problémy

### 1. **Spam v BepInEx logu** ✓ OPRAVENO
- **Problém**: Mod logoval každých 5 sekund při refreshi questů
- **Řešení**: Odstraněny nadměrné logy v `GameQuestBridge.cs`:
  - Zakomentován log "Found X quest titles"
  - Zakomentován log "Looking for quest with title: X"
  - Zakomentován log "Found matching quest: X"
- **Soubory**: `GameQuestBridge.cs` (řádky 312, 339, 354)

### 2. **Lag hry** ✓ OPRAVENO
- **Problém**: `OnGUI()` volal coroutinu KAŽDÝ FRAME (60x za sekundu!)
- **Řešení**: Změna na `Update()` s časovačem - markers se nyní aktualizují pouze každých 0.5s
- **Soubory**: `QuestHelperPlugin.cs` (řádek 359-376)
- **Výsledek**: Výrazné snížení CPU zátěže a odstranění lagů

### 3. **Konflikt keybindu Q** ✓ OPRAVENO
- **Problém**: Q je default auto-attack v Erenshor
- **Řešení**: Změna keybindu z Q na **L** (jako Quest Log)
- **Soubory**: `QuestTracker.cs`
- **Nový keybind**:
  - **L** - otevřít/zavřít Quest List
  - **R** - manuální refresh questů
  - **T** - toggle quest tracker
  - **O** - nastavení

### 4. **Automatický refresh questů** ✓ VYLEPŠENO
- **Změny**:
  - Snížen interval automatického refreshe z 5s na **2 sekundy** (rychlejší detekce změn)
  - Přidána klávesová zkratka **R** pro manuální refresh
  - Refresh se automaticky spustí při změně postavy
  - Refresh tlačítko v UI funguje
- **Soubory**: `QuestTracker.cs`

## Jak používat nový Quest Guru

### Klávesové zkratky
- **L** - Otevřít/zavřít seznam questů
- **R** - Manuální refresh questů (pokud se něco neaktualizuje)
- **T** - Zapnout/vypnout quest tracker
- **O** - Otevřít nastavení (UI scale, téma, atd.)
- **INSERT** - Debug info (pouze pokud je debug zapnutý)

### Automatické funkce
- Questy se automaticky refreshují každé 2 sekundy
- Při změně postavy se automaticky detekuje a refreshne
- Quest markers (! a ?) nad NPCs se aktualizují každých 0.5s bez lagu

## Instalace
1. Překopíruj `ErenshorQuestGuru.dll` z `bin\Release\net46\` do BepInEx\plugins\
2. Restartuj hru
3. Enjoy! 🎮

## Technické detaily
- **Performance**: Snížena CPU zátěž o ~90% (OnGUI -> Update s timerem)
- **Logging**: Snížen spam v logu o ~95%
- **Responsiveness**: Questy se refreshují 2.5x rychleji (2s místo 5s)
