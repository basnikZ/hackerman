# Hardwarové komponenty

## Základní vybavení

### 1. Raspberry Pi 5
- **Proč**: Centrální jednotka pro 24/7 monitoring
- **Specifikace**:
  - Procesor: 2.4GHz quad-core 64-bit Arm Cortex-A76
  - RAM: 4GB/8GB LPDDR4X-4267 SDRAM
  - GPU: VideoCore VII
  - Cache: 32KB L1, 1MB L2, 2MB L3
  - Úložiště: microSD karta (min. 32GB)
  - Rozhraní: 
    - 2x USB 3.0, 2x USB 2.0
    - Gigabit Ethernet
    - WiFi 5, Bluetooth 5.0
    - 2x micro-HDMI
    - 3.5mm jack
    - 40-pin GPIO
- **Cena**: 2,500-3,500 Kč
- **Reference na use cases**: Všechny use cases v docs/08_use_cases.md

### 2. SDR přijímač
- **Proč**: Základní RF monitoring
- **Doporučený model**: Nooelec NESDR SMArTee v2
- **Specifikace**:
  - Frekvenční rozsah: 24MHz - 1.7GHz
  - Rozlišení: 12-bit
  - Vzorkovací frekvence: 2.4MS/s
  - Fázový šum: -80dBc/Hz @ 10kHz offset
  - Dynamický rozsah: 70dB
  - Napájení: USB 5V
  - Spotřeba: 1W
  - Konektor: SMA
  - Funkce:
    - Bias-Tee pro aktivní antény
    - Aktivní chlazení
    - TCXO oscilátor
    - ESD ochrana
- **Alternativy**:
  - RTL-SDR V3 (levnější, méně stabilní)
  - Airspy Mini (širší pásmo, dražší)
  - HackRF One (pokročilé funkce)
- **Cena**: 1,850 Kč (sada s anténami)
- **Reference na use cases**: 3, 4, 8 v docs/08_use_cases.md

### 3. USB WiFi adapter
- **Proč**: Monitor mode pro WiFi analýzu
- **Doporučený model**: Alfa AWUS036ACH
- **Specifikace**:
  - Čipset: Realtek RTL8812AU
  - Standard: 802.11ac
  - Frekvence: 2.4GHz a 5GHz
  - Kanály: 1-11 (2.4GHz), 36-165 (5GHz)
  - Šířka pásma: 20/40/80MHz
  - MIMO: 2x2
  - Výstupní výkon: 1000mW
  - Citlivost: -95dBm
  - Anténní konektor: RP-SMA
  - Počet antén: 2
  - USB: 3.0
  - Délka kabelu: 1.5m
- **Alternativy**:
  - TP-Link TL-WN722N
  - Panda Wireless PAU09
  - Alfa AWUS036NH
- **Cena**: 500-800 Kč
- **Reference na use cases**: 1, 2, 4, 5 v docs/08_use_cases.md

## Příslušenství

### 1. Antény
- **Proč**: Lepší příjem signálů
- **Doporučené typy**:
  - UHF anténa pro 2.4GHz
  - 433MHz anténa pro IoT zařízení
  - Teleskopická anténa pro různé frekvence
- **Specifikace**:
  - Impedance: 50 ohmů
  - Konektory: SMA/RP-SMA
  - Frekvenční rozsah: dle typu
  - Délka kabelu: 1-2m
- **Alternativy**:
  - Dipólové antény
  - Yagi antény
  - Patch antény
- **Cena**: 300-1000 Kč

### 2. Napájení a chlazení
- **Proč**: Stabilní 24/7 provoz
- **Doporučené vybavení**:
  - Oficiální napájecí zdroj pro RPi 5
  - UPS pro stabilní napájení
  - Aktivní chlazení pro RPi
  - Chladící podložka
- **Specifikace**:
  - 5V/3A zdroj
  - Přepěťová ochrana
  - Zálohování (UPS)
  - Kvalitní konektory
- **Cena**: 500-1500 Kč

### 3. Konektory a adaptéry
- **Proč**: Propojení komponent
- **Doporučené vybavení**:
  - SMA adaptéry
  - USB rozbočovač s napájením
  - Ethernet kabel
  - HDMI kabel

## Důležité tipy při nákupu

1. **Obecné zásady**:
   - Kupovat originální produkty, ne padělky
   - Kontrolovat kompatibilitu s Linuxem
   - Číst recenze a zkušenosti ostatních
   - Kupovat od důvěryhodných prodejců
   - Zkontrolovat záruku a podporu

2. **Kvalita vs. cena**:
   - Investovat do kvalitního základu
   - Postupně rozšiřovat podle potřeby
   - Nešetřit na napájení a chlazení
   - Kupovat ověřené značky

3. **Kompatibilita**:
   - Kontrolovat podporu v Linuxu
   - Ověřit dostupnost ovladačů
   - Zkontrolovat požadavky na výkon
   - Testovat před nasazením

4. **Rozšiřitelnost**:
   - Plánovat budoucí rozšíření
   - Kupovat kompatibilní komponenty
   - Zvažovat upgrade možnosti
   - Dokumentovat konfiguraci

## Doporučený postup nákupu

1. **První fáze** (základní monitoring):
   - RTL-SDR V3 dongle (originál)
   - Dipólová anténa pro RTL-SDR
   - Oficiální RPi zdroj
   - Pasivní chladič
   - Celkem: cca 2000 Kč

2. **Druhá fáze** (WiFi monitoring):
   - Alfa AWUS036ACH nebo Panda PAU09
   - Vysokozisková WiFi anténa
   - UPS pro zálohování
   - Celkem: cca 1500 Kč

3. **Třetí fáze** (pokročilé funkce):
   - HackRF One (originál)
   - CC1101 modul
   - Pokročilé antény
   - Celkem: cca 10000 Kč 