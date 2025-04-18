# Frekvenční monitoring - Kompletní průvodce

## 1. Příprava hardware

### 1.1 Potřebné komponenty
```
┌─────────────────────────────────────────────────────────────┐
│ Raspberry Pi 5                                              │
├─────────────────────────────────────────────────────────────┤
│ Nooelec NESDR SMArTee v2                                   │
│ Alfa AWUS036ACH WiFi adapter                               │
│ RG174 anténní kabel                                        │
│ SMA antény pro různé pásma                                 │
│ MicroSD karta (min. 32GB)                                  │
└─────────────────────────────────────────────────────────────┘
```

### 1.2 Instalace základního software
```bash
# Aktualizace systému
sudo apt update
sudo apt upgrade -y

# Instalace základních nástrojů
sudo apt install -y rtl-sdr gqrx-sdr aircrack-ng kismet wireshark
```

## 2. Monitoring VHF pásma (30-300 MHz)

### 2.1 Letecké pásmo (108-137 MHz)
```bash
# Instalace potřebného software
sudo apt install -y dump1090-fa

# Spuštění ADS-B přijímače
dump1090-fa --interactive --net
```

### 2.2 Námořní VHF (156-174 MHz)
```bash
# Instalace AIS dekodéru
sudo apt install -y aisdecoder

# Spuštění AIS monitoru
rtl_ais -n
```

### 2.3 Amatérské pásmo (144-146 MHz)
```bash
# Instalace multimode dekodéru
sudo apt install -y multimon-ng

# Spuštění monitoru
rtl_fm -f 144.8M -M fm -s 200k -r 48k | multimon-ng -t raw -a POCSAG512 -a POCSAG1200 -a POCSAG2400 -f alpha -
```

## 3. Monitoring UHF pásma (300 MHz - 3 GHz)

### 3.1 IoT zařízení (433 MHz)
```bash
# Instalace RTL_433
sudo apt install -y rtl-433

# Spuštění monitoru
rtl_433 -f 433.92M -s 250k
```

### 3.2 Smart měřiče (868 MHz)
```bash
# Instalace mqttwarn
sudo apt install -y mqttwarn

# Spuštění monitoru
rtl_433 -f 868M -s 250k -F json | mqttwarn
```

### 3.3 Průmyslové sítě (900 MHz)
```bash
# Instalace GNU Radio
sudo apt install -y gnuradio

# Spuštění monitoru
python3 -c "from gnuradio import blocks, gr; tb = gr.top_block(); tb.run()"
```

## 4. Monitoring WiFi pásem

### 4.1 2.4 GHz pásmo
```bash
# Nastavení monitor módu
sudo airmon-ng check kill
sudo airmon-ng start wlan0

# Spuštění Kismet
kismet -c wlan0mon
```

### 4.2 5 GHz pásmo
```bash
# Nastavení monitor módu pro 5GHz
sudo iwconfig wlan0mon freq 5.18G

# Spuštění monitoru
kismet -c wlan0mon
```

## 5. Monitoring mobilních sítí

### 5.1 GSM (900 MHz)
```bash
# Instalace gr-gsm
sudo apt install -y gr-gsm

# Spuštění monitoru
grgsm_scanner

# Skenování pro GSM 900
./quick_scan.sh 925M 960M 200k

# Skenování pro GSM 1800
./quick_scan.sh 1805M 1880M 200k
```

### 5.2 LTE (2600 MHz)
```bash
# Instalace LTE monitoru
sudo apt install -y srslte

# Spuštění monitoru
srsue
```

## 6. Automatizace monitoringu

### 6.1 Skript pro automatické spouštění
```bash
#!/bin/bash
# frekvencni_monitor.sh

# Funkce pro kontrolu běžících procesů
check_process() {
    if pgrep -x "$1" >/dev/null; then
        echo "$1 je již spuštěn"
        return 1
    else
        return 0
    fi
}

# Spuštění monitorů
start_monitors() {
    # ADS-B
    if check_process "dump1090-fa"; then
        dump1090-fa --interactive --net &
    fi

    # AIS
    if check_process "rtl_ais"; then
        rtl_ais -n &
    fi

    # IoT
    if check_process "rtl_433"; then
        rtl_433 -f 433.92M -s 250k &
    fi

    # WiFi
    if check_process "kismet"; then
        kismet -c wlan0mon &
    fi
}

# Hlavní program
start_monitors
```

### 6.2 Systemd služba
```bash
# Vytvoření systemd služby
sudo nano /etc/systemd/system/freq-monitor.service

[Unit]
Description=Frekvenční monitoring služba
After=network.target

[Service]
Type=simple
User=pi
ExecStart=/usr/local/bin/frekvencni_monitor.sh
Restart=always

[Install]
WantedBy=multi-user.target
```

## 7. Užitečné repository

### 7.1 SDR nástroje
- [RTL-SDR](https://github.com/rtlsdrblog/rtl-sdr)
- [GNU Radio](https://github.com/gnuradio/gnuradio)
- [RTL_433](https://github.com/merbanan/rtl_433)

### 7.2 WiFi nástroje
- [Kismet](https://github.com/kismetwireless/kismet)
- [Aircrack-ng](https://github.com/aircrack-ng/aircrack-ng)
- [Wireshark](https://github.com/wireshark/wireshark)

### 7.3 Mobilní sítě
- [gr-gsm](https://github.com/ptrkrysik/gr-gsm)
- [srsLTE](https://github.com/srsLTE/srsLTE)
- [OpenBTS](https://github.com/RangeNetworks/openbts)

## 8. Doporučené antény

### 8.1 VHF antény
- Dipólová anténa pro 2m pásmo
- Ground plane anténa pro VHF
- Discone anténa pro širokopásmový příjem

### 8.2 UHF antény
- Yagi anténa pro 433 MHz
- Patch anténa pro 868 MHz
- Log-periodická anténa pro široké pásmo

### 8.3 WiFi antény
- Vysokozisková WiFi anténa
- Panelová anténa pro 5 GHz
- Omni anténa pro 2.4 GHz

## 9. Bezpečnostní opatření

### 9.1 Před spuštěním
- Zkontrolovat legálnost monitoringu
- Nastavit správné frekvence
- Ověřit oprávnění

### 9.2 Během monitoringu
- Sledovat systémové zdroje
- Dokumentovat činnost
- Respektovat soukromí

### 9.3 Po ukončení
- Zálohovat data
- Vypnout zařízení
- Dokumentovat výsledky

## 10. Troubleshooting

### 10.1 Časté problémy
1. **Nízký signál**
   - Zkontrolovat antény
   - Upravit zesílení
   - Ověřit frekvenci

2. **Interference**
   - Změnit kanál
   - Použít filtr
   - Upravit citlivost

3. **Systémové problémy**
   - Aktualizovat software
   - Zkontrolovat ovladače
   - Ověřit konfiguraci

### 10.2 Řešení problémů
1. **Logování**
   ```bash
   journalctl -u freq-monitor.service
   ```

2. **Diagnostika**
   ```bash
   rtl_test -t
   ```

3. **Optimalizace**
   ```bash
   sudo renice -n -20 -p $(pgrep rtl_433)
   ```

## 11. Dekódování digitálních signálů

### 11.1 Instalace dekódovacích nástrojů pro MacOS

```bash
# Instalace závislostí
brew install cmake libusb pkg-config portaudio pulseaudio sox

# Kompilace a instalace multimon-ng
git clone https://github.com/EliasOenal/multimon-ng.git
cd multimon-ng
mkdir build && cd build
cmake -DCMAKE_POLICY_VERSION_MINIMUM=3.5 .. && make
sudo make install
```

### 11.2 Dekódování různých protokolů

#### POCSAG (Paging systémy)
```bash
# Dekódování POCSAG na frekvenci 144.800 MHz (amatérské pásmo)
rtl_fm -f 144.800M -s 22050 | multimon-ng -a POCSAG512 -a POCSAG1200 -a POCSAG2400 -t raw -f alpha /dev/stdin

# Dekódování komerčních pagerů na 466.075 MHz
rtl_fm -f 466.075M -s 22050 | multimon-ng -a POCSAG512 -a POCSAG1200 -a POCSAG2400 -t raw -f alpha /dev/stdin
```

#### ACARS (Letecká datová komunikace)
```bash
# Dekódování ACARS zpráv na frekvenci 131.725 MHz
rtl_fm -f 131.725M -s 2400000 -r 48000 - | multimon-ng -a ACARS -t raw /dev/stdin
```

#### AIS (Lodní identifikační systém)
```bash
# Dekódování AIS zpráv (161.975 MHz nebo 162.025 MHz)
rtl_fm -f 161.975M -p 50 -s 48k | multimon-ng -t raw -a FLEX -a POCSAG512 -a POCSAG1200 -a POCSAG2400 -a SCOPE -a FMSFSK -a AFSK1200 /dev/stdin
```

#### IoT zařízení (433 MHz)
```bash
# Dekódování digitálních signálů na 433.92 MHz
rtl_fm -f 433.92M -M fm -s 250k -r 48k | multimon-ng -t raw -a FSK9600 /dev/stdin
```

### 11.3 Konfigurace GQRX pro optimální příjem

#### Pro POCSAG/FLEX (Pagery)
- **Mode**: FM-N (Narrow FM)
- **Filter width**: 15-25 kHz
- **AGC**: Fast
- **Squelch**: Nízká hodnota (kolem -100 dB)

#### Pro ACARS (Letecká data)
- **Mode**: AM
- **Filter width**: 10-15 kHz
- **AGC**: Medium
- **Squelch**: Střední hodnota

#### Pro AIS (Lodní data)
- **Mode**: FM-N
- **Filter width**: 12-20 kHz
- **AGC**: Medium
- **Squelch**: Nízká hodnota

### 11.4 Optimální frekvence v České republice

| Typ signálu | Frekvence | Mód | Aktivita |
|------------|-----------|-----|----------|
| POCSAG (amatérský) | 144.800 MHz | FM-N | Střední |
| POCSAG (komerční) | 466.075 MHz | FM-N | Vysoká v obchodních centrech a nemocnicích |
| ACARS | 131.725 MHz | AM | Vysoká poblíž letišť |
| AIS | 161.975 MHz | FM-N | Aktivní poblíž větších vodních ploch |
| IoT zařízení | 433.920 MHz | FM-N/AM | Vysoká v městských oblastech |
| Meteostanice | 868.300 MHz | FM-N | Střední |

### 11.5 Řešení problémů při dekódování

1. **Žádná data nejsou dekódována**
   - Zkontroluj, zda je frekvence přesně nastavena
   - Zvyš gain (-g parametr v rtl_fm)
   - Zlepši pozici antény
   - Ověř, zda je v okolí aktivní vysílač

2. **Špatná kvalita signálu**
   - Použij vhodnou anténu pro danou frekvenci
   - Redukuj okolní rušení (odstraň USB 3.0 zařízení v blízkosti)
   - Experimentuj s různými hodnotami gain

3. **RTL-SDR není detekováno**
   - Odpoj a znovu připoj zařízení
   - Zkontroluj, zda není zařízení používáno jiným programem
   - Spusť `rtl_test -t` pro diagnostiku
   - Zkus jiný USB port (ideálně USB 2.0) 

#!/bin/bash
# mac_sdr_launcher.sh
# Skript pro rychle spusteni ruznych monitorovacich nastroju na MacOS

MODE=$1
FREQ=$2

case "$MODE" in
    "pocsag")
        rtl_tcp -a 127.0.0.1 & sleep 2
        rtl_fm -f ${FREQ:-144.8M} -s 22050 | multimon-ng -a POCSAG512 -a POCSAG1200 -a POCSAG2400 -t raw -f alpha /dev/stdin
        ;;
    "acars")
        rtl_tcp -a 127.0.0.1 & sleep 2
        rtl_fm -f ${FREQ:-131.725M} -s 2400000 -r 48000 - | multimon-ng -a ACARS -t raw /dev/stdin
        ;;
    "iot")
        rtl_tcp -a 127.0.0.1 & sleep 2
        rtl_fm -f ${FREQ:-433.92M} -M fm -s 250k -r 48k | multimon-ng -t raw -a FSK9600 /dev/stdin
        ;;
    "gqrx")
        rtl_tcp -a 127.0.0.1 & sleep 2
        gqrx &
        ;;
    *)
        echo "Pouziti: $0 [pocsag|acars|iot|gqrx] [frekvence]"
        exit 1
        ;;
esac 

#!/bin/bash
# radiolink_scanner.sh - Zaměření na frekvence používané pro radioreléové spoje

LOG_DIR="$HOME/radiolink_logs"
mkdir -p $LOG_DIR

TIMESTAMP=$(date +"%Y%m%d_%H%M%S")

# Známé rozsahy pro radioreléové spoje (nižší frekvence dosažitelné s RTL-SDR)
RANGES=(
  "330M:400M:100k"   # Starší analogové spoje
  "400M:420M:100k"   # Utility frekvence
  "1.35G:1.5G:250k"  # L-band spoje
)

echo "Skenování frekvenčních rozsahů radioreléových spojů"
echo "Výsledky budou uloženy do: $LOG_DIR"

for range in "${RANGES[@]}"; do
  echo "Skenuji rozsah: $range"
  OUTPUT_FILE="$LOG_DIR/radiolink_${range//[:.]/}_${TIMESTAMP}.csv"
  
  rtl_power -f $range -g 40 -i 30 -e 600s $OUTPUT_FILE
  
  # Najdi Top 5 nejsilnějších signálů v tomto rozsahu
  echo "Top 5 signálů v rozsahu $range:"
  awk -F, 'NR>1 {if ($7 > -70) print $2 "MHz: " $7 "dB"}' $OUTPUT_FILE | sort -nr -k2 | head -5
  
  echo "----------------------------------------"
done 

#!/bin/bash
# telco_24h_monitor.sh - 24-hodinový cyklický monitoring provozu telekomunikačního objektu

LOG_DIR="$HOME/telco_logs/$(date +"%Y%m%d")"
mkdir -p $LOG_DIR

echo "Začínám 24-hodinový monitoring České telekomunikace"
echo "Výsledky budou ukládány do: $LOG_DIR"

# Funkce pro uložení časového razítka a popis aktivity
log_activity() {
  local time=$(date +"%H:%M:%S")
  local message="$1"
  echo "[$time] $message" >> "$LOG_DIR/activity_log.txt"
  echo "[$time] $message"
}

# Hlavní monitorovací smyčka
for hour in {0..23}; do
  current_hour=$(date +"%H")
  log_activity "=== Začínám monitoring pro hodinu $current_hour ==="
  
  # Rozsahy k monitorování (rotující podle hodiny, abychom pokryli více pásem)
  case $((hour % 6)) in
    0) # Údržbové frekvence
      log_activity "Monitoruji údržbové frekvence (410-430 MHz)"
      rtl_power -f 410M:430M:25k -g 40 -i 60 -e 600s "$LOG_DIR/maintenance_${current_hour}.csv"
      ;;
    1) # PMR a komunikační frekvence
      log_activity "Monitoruji PMR446 frekvence"
      rtl_power -f 446M:447M:6.25k -g 40 -i 30 -e 600s "$LOG_DIR/pmr_${current_hour}.csv"
      ;;
    2) # Firemní komunikace
      log_activity "Monitoruji firemní rádiové sítě (450-470 MHz)"
      rtl_power -f 450M:470M:25k -g 40 -i 60 -e 600s "$LOG_DIR/business_${current_hour}.csv"
      ;;
    3) # Mikrovlnné spoje nižších frekvencí
      log_activity "Monitoruji nižší mikrovlnné pásmo (1.3-1.5 GHz)"
      rtl_power -f 1.3G:1.5G:100k -g 40 -i 60 -e 600s "$LOG_DIR/microwave_${current_hour}.csv"
      ;;
    4) # GSM a mobilní služby
      log_activity "Monitoruji GSM pásmo (925-960 MHz)"
      rtl_power -f 925M:960M:100k -g 40 -i 60 -e 600s "$LOG_DIR/gsm_${current_hour}.csv"
      ;;
    5) # LTE pásmo
      log_activity "Monitoruji LTE pásmo (790-862 MHz)"
      rtl_power -f 790M:862M:100k -g 40 -i 60 -e 600s "$LOG_DIR/lte_${current_hour}.csv"
      ;;
  esac
  
  # Analýza zachycených dat
  LATEST_CSV=$(ls -t "$LOG_DIR"/*.csv | head -1)
  if [ -n "$LATEST_CSV" ]; then
    log_activity "Analyzuji data z: $LATEST_CSV"
    
    # Extrahuj nejsilnější signály
    STRONG_SIGNALS=$(awk -F, 'NR>1 {if ($7 > -50) printf "%.3f MHz: %.1f dB\n", $2, $7}' "$LATEST_CSV" | sort -nr -k2 | head -5)
    
    if [ -n "$STRONG_SIGNALS" ]; then
      log_activity "Nalezeny silné signály:"
      echo "$STRONG_SIGNALS" >> "$LOG_DIR/strong_signals.txt"
      echo "$STRONG_SIGNALS"
      
      # Extrahuj frekvenci nejsilnějšího signálu pro poslech
      TOP_FREQ=$(echo "$STRONG_SIGNALS" | head -1 | awk '{print $1}' | sed 's/MHz/M/')
      
      if [ -n "$TOP_FREQ" ]; then
        log_activity "Poslouchám nejsilnější signál na $TOP_FREQ"
        rtl_fm -f "$TOP_FREQ" -M fm -s 12k | sox -t raw -r 12k -e signed-integer -b 16 -c 1 - "$LOG_DIR/signal_${TOP_FREQ//./}_${current_hour}.wav" trim 0 30
      fi
    else
      log_activity "Žádné silné signály nebyly nalezeny v tomto cyklu"
    fi
  fi
  
  log_activity "Dokončuji monitoring pro hodinu $current_hour"
  log_activity "----------------------------------------"
  
  # Čekej do další hodiny (s rezervou 5 minut)
  sleep 3300
done

log_activity "24-hodinový monitoring dokončen" 