# Aktualizace software

## Systémové aktualizace
1. **Pravidelné aktualizace**
   ```bash
   sudo apt update
   sudo apt upgrade
   sudo apt dist-upgrade
   sudo apt autoremove
   ```

2. **Kernel aktualizace**
   ```bash
   sudo rpi-update
   sudo reboot
   ```

3. **Firmware aktualizace**
   ```bash
   sudo rpi-eeprom-update -a
   sudo reboot
   ```

## Python aktualizace
1. **Virtuální prostředí**
   ```bash
   source venv/bin/activate
   pip install --upgrade pip
   pip install --upgrade -r requirements.txt
   ```

2. **Knihovny**
   ```bash
   pip list --outdated
   pip install --upgrade package_name
   ```

3. **Pip aktualizace**
   ```bash
   python -m pip install --upgrade pip
   ```

## SDR aktualizace
1. **RTL-SDR**
   ```bash
   sudo apt update
   sudo apt install --only-upgrade rtl-sdr
   ```

2. **GNU Radio**
   ```bash
   sudo apt update
   sudo apt install --only-upgrade gnuradio
   ```

3. **SDR++**
   ```bash
   sudo apt update
   sudo apt install --only-upgrade sdrpp
   ```

## WiFi aktualizace
1. **Aircrack-ng**
   ```bash
   sudo apt update
   sudo apt install --only-upgrade aircrack-ng
   ```

2. **Kismet**
   ```bash
   sudo apt update
   sudo apt install --only-upgrade kismet
   ```

3. **Wireshark**
   ```bash
   sudo apt update
   sudo apt install --only-upgrade wireshark
   ```

## Monitorovací aktualizace
1. **Prometheus**
   ```bash
   sudo apt update
   sudo apt install --only-upgrade prometheus
   sudo systemctl restart prometheus
   ```

2. **Grafana**
   ```bash
   sudo apt update
   sudo apt install --only-upgrade grafana
   sudo systemctl restart grafana-server
   ```

3. **Node Exporter**
   ```bash
   sudo apt update
   sudo apt install --only-upgrade prometheus-node-exporter
   sudo systemctl restart prometheus-node-exporter
   ```

## Automatické aktualizace
1. **Cron úloha**
   ```bash
   crontab -e
   0 3 * * * /path/to/update.sh
   ```

2. **Update skript**
   ```bash
   #!/bin/bash
   sudo apt update
   sudo apt upgrade -y
   sudo apt autoremove -y
   pip install --upgrade -r requirements.txt
   ```

3. **Logování aktualizací**
   ```bash
   sudo nano /etc/logrotate.d/updates
   /var/log/updates.log {
       weekly
       rotate 4
       compress
   }
   ```

## Kontrola aktualizací
1. **Verze balíčků**
   ```bash
   apt list --upgradable
   pip list --outdated
   ```

2. **Systémové informace**
   ```bash
   uname -a
   cat /etc/os-release
   ```

3. **Závislosti**
   ```bash
   pip check
   apt check
   ```

## Zálohování před aktualizací
1. **Konfigurace**
   ```bash
   tar -czf config_backup.tar.gz /etc
   ```

2. **Data**
   ```bash
   tar -czf data_backup.tar.gz /var/lib
   ```

3. **Logy**
   ```bash
   tar -czf logs_backup.tar.gz /var/log
   ```

## Rollback
1. **Konfigurace**
   ```bash
   tar -xzf config_backup.tar.gz -C /
   ```

2. **Balíčky**
   ```bash
   sudo apt install package=version
   ```

3. **Python**
   ```bash
   pip install package==version
   ``` 