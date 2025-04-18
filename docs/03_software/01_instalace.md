# Software Guide

## Zakladni instalace

### 1. Raspbian OS
- **Proč**: Základní operační systém pro Raspberry Pi
- **Specifikace**:
  - Debian-based distribuce
  - ARM64 architektura
  - Podpora pro SDR a WiFi nástroje
  - Aktualizace a bezpečnostní záplaty
- **Interakce**:
  - Poskytuje základní systémové služby
  - Spravuje hardware a ovladače
  - Zajišťuje bezpečnost a stabilitu

## Instalace software

### Systém
```bash
sudo apt update
sudo apt upgrade
```

### SDR
```bash
sudo apt install rtl-sdr
sudo apt install gqrx-sdr
```

### WiFi
```bash
sudo apt install aircrack-ng
sudo apt install kismet
```

### Monitoring
```bash
sudo apt install prometheus
sudo apt install grafana
```

## Konfigurace

### 1. RTL-SDR
```bash
# Vytvoření blacklistu pro RTL-SDR
echo 'blacklist dvb_usb_rtl28xxu' | sudo tee /etc/modprobe.d/rtl-sdr-blacklist.conf

# Načtení nové konfigurace
sudo modprobe -r dvb_usb_rtl28xxu
```

### 2. WiFi adapter
```bash
# Kontrola podpory monitor módu
sudo iw list | grep -A 10 "Supported interface modes"

# Nastavení monitor módu
sudo airmon-ng check kill
sudo airmon-ng start wlan0
```

### 3. Webové rozhraní
```bash
# Povolení SSH
sudo systemctl enable ssh
sudo systemctl start ssh

# Instalace webového serveru
sudo apt install -y nginx

# Instalace PHP pro webové rozhraní
sudo apt install -y php-fpm
```

## Automatizace

### 1. RF Monitoring
```bash
# Vytvoření skriptu pro automatické skenování
cat << EOF > /home/pi/rf-monitor.sh
#!/bin/bash
while true; do
    rtl_power -f 24M:1.7G:1M -g 50 -i 10 -e 1h scan.csv
    sleep 3600
done
EOF

# Nastavení oprávnění
chmod +x /home/pi/rf-monitor.sh
```

### 2. WiFi Monitoring
```bash
# Vytvoření skriptu pro WiFi monitoring
cat << EOF > /home/pi/wifi-monitor.sh
#!/bin/bash
while true; do
    sudo kismet -c wlan0mon --no-ncurses
    sleep 3600
done
EOF

# Nastavení oprávnění
chmod +x /home/pi/wifi-monitor.sh
```

## Služby

### 1. RF Monitoring Service
```bash
# Vytvoření systemd služby
cat << EOF | sudo tee /etc/systemd/system/rf-monitor.service
[Unit]
Description=RF Monitoring Service
After=network.target

[Service]
Type=simple
User=pi
ExecStart=/home/pi/rf-monitor.sh
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# Povolení a spuštění služby
sudo systemctl enable rf-monitor.service
sudo systemctl start rf-monitor.service
```

### 2. WiFi Monitoring Service
```bash
# Vytvoření systemd služby
cat << EOF | sudo tee /etc/systemd/system/wifi-monitor.service
[Unit]
Description=WiFi Monitoring Service
After=network.target

[Service]
Type=simple
User=pi
ExecStart=/home/pi/wifi-monitor.sh
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# Povolení a spuštění služby
sudo systemctl enable wifi-monitor.service
sudo systemctl start wifi-monitor.service
```

## Bezpečnost

### 1. SSH zabezpečení
```bash
# Změna výchozího SSH portu
sudo nano /etc/ssh/sshd_config
# Port 2222

# Restart SSH služby
sudo systemctl restart ssh
```

### 2. Firewall
```bash
# Instalace UFW
sudo apt install -y ufw

# Konfigurace firewallu
sudo ufw allow 2222/tcp  # SSH
sudo ufw allow 80/tcp    # HTTP
sudo ufw allow 443/tcp   # HTTPS
sudo ufw enable
```

## Monitoring a logování

### 1. System monitoring
```bash
# Instalace nástrojů
sudo apt install -y htop iotop

# Instalace logrotate
sudo apt install -y logrotate
```

### 2. Vytvoření logrotate konfigurace
```bash
cat << EOF | sudo tee /etc/logrotate.d/rf-station
/var/log/rf-monitor.log {
    daily
    missingok
    rotate 7
    compress
    delaycompress
    notifempty
    create 0640 pi pi
}
EOF
```

# Software požadavky

## Základní software

### 1. Raspbian OS
- **Proč**: Stabilní OS pro 24/7 monitoring
- **Specifikace**:
  - Debian-based distribuce
  - ARM64 architektura
  - Podpora pro SDR a WiFi nástroje
  - Aktualizace a bezpečnostní záplaty
- **Reference na use cases**: Všechny use cases v docs/08_use_cases.md

### 2. SDR nástroje
- **Proč**: 24/7 monitoring RF signálů
- **Specifikace**:
  - rtl-sdr (základní nástroje pro RTL-SDR)
  - gqrx (GUI pro SDR příjem)
  - gnuradio (framework pro SDR aplikace)
  - hackrf-tools (nástroje pro HackRF)
- **Reference na use cases**: 3, 4, 8 v docs/08_use_cases.md

### 3. WiFi nástroje
- **Proč**: 24/7 monitoring WiFi sítí
- **Specifikace**:
  - kismet (WiFi analyzer)
  - aircrack-ng (WiFi security tools)
  - wireshark (packet analyzer)
  - hostapd (AP emulace)
- **Reference na use cases**: 1, 2, 4, 5 v docs/08_use_cases.md

### 4. Webové rozhraní
- **Proč**: Vzdálený přístup a monitoring
- **Specifikace**:
  - nginx (web server)
  - php-fpm (PHP procesor)
  - grafana (monitoring)
  - prometheus (metriky)
- **Reference na use cases**: 6, 7, 9 v docs/08_use_cases.md

### 5. Automatizace
- **Proč**: Automatizace 24/7 monitoringu
- **Specifikace**:
  - systemd (správa služeb)
  - cron (plánování úloh)
  - python (skriptování)
  - bash (systémové skripty)
- **Reference na use cases**: 10 v docs/08_use_cases.md

## Instalace a konfigurace

### 1. Základní instalace
```bash
# Aktualizace systému
sudo apt update && sudo apt upgrade -y

# Instalace SDR nástrojů
sudo apt install rtl-sdr gqrx gnuradio hackrf-tools -y

# Instalace WiFi nástrojů
sudo apt install kismet aircrack-ng wireshark hostapd -y

# Instalace webového rozhraní
sudo apt install nginx php-fpm grafana prometheus -y

# Instalace automatizace
sudo apt install python3 python3-pip bash -y
```

### 2. Konfigurace
- **RTL-SDR**:
  - Konfigurace vzorkovací frekvence
  - Nastavení citlivosti
  - Kalibrace frekvence

- **WiFi**:
  - Konfigurace monitor módu
  - Nastavení kanálů
  - Konfigurace filtrování

- **Webové rozhraní**:
  - Nastavení SSL
  - Konfigurace přístupu
  - Nastavení dashboardů

### 3. Automatizace
- **Služby**:
  - systemd jednotky pro SDR
  - systemd jednotky pro WiFi
  - systemd jednotky pro monitoring

- **Skripty**:
  - Automatické spouštění
  - Plánované úlohy
  - Monitoring a alerting

## Instalace pro MacOS

### 1. Homebrew
```bash
# Instalace balíčkového manažeru Homebrew, pokud ještě není nainstalován
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

### 2. Základní SDR software
```bash
# Instalace základních nástrojů
brew install rtl-sdr gqrx soapysdr

# Instalace dekódovacích nástrojů
brew install sox cmake libusb pkg-config portaudio pulseaudio

# Instalace doplňkových aplikací
brew install --cask cubicsdr
```

### 3. Multimon-NG pro dekódování signálů
```bash
# Stažení a kompilace multimon-ng
cd ~/Downloads
git clone https://github.com/EliasOenal/multimon-ng.git
cd multimon-ng
mkdir build && cd build
cmake -DCMAKE_POLICY_VERSION_MINIMUM=3.5 .. && make
sudo make install
```

### 4. Konfigurační kroky pro RTL-SDR na MacOS
```bash
# Příprava proměnných prostředí
echo 'export DYLD_LIBRARY_PATH=/opt/homebrew/lib:$DYLD_LIBRARY_PATH' >> ~/.zshrc
echo 'export PATH=/opt/homebrew/bin:$PATH' >> ~/.zshrc
source ~/.zshrc

# Ověření zařízení
rtl_test -t
```

### 5. Spuštění GQRX s RTL-TCP serverem
```bash
# Spuštění rtl_tcp serveru (v samostatném terminálu)
rtl_tcp -a 127.0.0.1

# Konfigurační instrukce pro GQRX:
# - Device: RTL-TCP
# - Device string: rtl_tcp=127.0.0.1:1234
# - Input rate: 2.4M
# - Decimation: None
```

### 6. Řešení častých problémů na MacOS
- Pokud GQRX crashuje s chybou "Failed to create FFTW wisdom lockfile", spusťte:
  ```bash
  mkdir -p ~/.cache/gnuradio
  sudo chown -R $(whoami) ~/.cache/gnuradio
  ```

- Pokud RTL-SDR není detekováno, zkontrolujte:
  ```bash
  system_profiler SPUSBDataType | grep -A 10 -B 2 "RTL"
  ```

- Pro spuštění multimon-ng s rtl_fm:
  ```bash
  # Ukončete rtl_tcp a GQRX před tímto příkazem
  rtl_fm -f 144.800M -s 22050 | multimon-ng -a POCSAG512 -a POCSAG1200 -a POCSAG2400 -t raw -f alpha /dev/stdin
  ```

## Bezpečnost

### 1. Systémová bezpečnost
- Aktualizace systému
- Konfigurace firewallu
- Nastavení SELinux
- Bezpečnostní politiky

### 2. Síťová bezpečnost
- SSL/TLS certifikáty
- VPN přístup
- Síťová segmentace
- Monitorování síťového provozu

### 3. Aplikační bezpečnost
- Aktualizace aplikací
- Konfigurace přístupu
- Audit logování
- Zálohování dat 