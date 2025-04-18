# Slovník pojmů

## Hardware

### SDR zařízení
- **RTL-SDR**: Levný SDR přijímač založený na RTL2832U čipu
  - Frekvenční rozsah: 24MHz - 1.7GHz
  - Vzorkovací frekvence: 2.4MS/s
  - Rozlišení: 8 bitů
  - Použití: RF monitoring, ADS-B, AIS

- **HackRF**: Pokročilý SDR transceiver
  - Frekvenční rozsah: 1MHz - 6GHz
  - Vzorkovací frekvence: 20MS/s
  - Rozlišení: 8 bitů
  - Použití: Pokročilý RF monitoring, testování

- **Bias-Tee**: Napájení aktivních antén
  - Funkce: Dodává napájení po signálovém kabelu
  - Použití: Aktivní antény, LNA
  - Napětí: 3-5V
  - Proud: až 500mA

- **LNA**: Low Noise Amplifier
  - Funkce: Zesiluje slabé signály
  - Šum: < 1dB
  - Zisk: 20-30dB
  - Použití: Zlepšení citlivosti

## Software

### SDR nástroje
- **GNU Radio**: Grafické prostředí pro SDR
  - Funkce: Vizuální programování SDR aplikací
  - Moduly: Filtry, demodulátory, analyzátory
  - Použití: Vývoj vlastních SDR aplikací

- **SDR++**: Moderní SDR přijímač
  - Funkce: Příjem a analýza signálů
  - Podpora: RTL-SDR, HackRF, Airspy
  - Použití: RF monitoring, analýza

- **Aircrack-ng**: WiFi testování
  - Funkce: Analýza WiFi sítí
  - Nástroje: airodump, aireplay, aircrack
  - Použití: Testování zabezpečení

- **Prometheus**: Monitorovací systém
  - Funkce: Sběr a ukládání metrik
  - Grafana: Vizualizace dat
  - Alerting: Upozornění na události

## WiFi

### Základní pojmy
- **SSID**: Název sítě
  - Identifikátor WiFi sítě
  - Viditelný při vyhledávání
  - Může být skrytý

- **BSSID**: MAC adresa AP
  - Unikátní identifikátor
  - Fyzická adresa přístupového bodu
  - Použití pro identifikaci

- **WPA2**: Bezpečnostní standard
  - Šifrování: AES-CCMP
  - Autentizace: PSK nebo 802.1X
  - Bezpečnostní protokol

- **Handshake**: Výměna klíčů
  - Proces: 4-way handshake
  - Účel: Výměna šifrovacích klíčů
  - Zachytávání: Pro analýzu

## SDR

### Technické pojmy
- **IQ Data**: Komplexní signál
  - I: In-phase složka
  - Q: Quadrature složka
  - Reprezentace: Komplexní čísla

- **Sample Rate**: Vzorkovací frekvence
  - Jednotka: Samples per second
  - Nyquist: 2x vyšší než frekvence
  - Ovlivňuje: Rozlišení

- **Bandwidth**: Šířka pásma
  - Rozsah: Frekvenční pásmo
  - Ovlivňuje: Množství dat
  - Význam: Pro příjem

- **SNR**: Poměr signál/šum
  - Výpočet: Signál/Šum
  - Jednotka: dB
  - Význam: Kvalita signálu

## Bezpečnost

### Bezpečnostní pojmy
- **MITM**: Man in the Middle
  - Útok: Zachytávání komunikace
  - Prevence: Šifrování
  - Detekce: Certifikáty

- **DoS**: Denial of Service
  - Útok: Přetížení služby
  - Typy: Flood, Crash
  - Ochrana: Firewall

- **AES**: Šifrovací standard
  - Délka klíče: 128/256 bitů
  - Použití: WPA2, VPN
  - Bezpečnost: Vysoká

- **VPN**: Virtuální privátní síť
  - Funkce: Šifrované tunely
  - Protokoly: OpenVPN, WireGuard
  - Použití: Bezpečná komunikace 