# Skripty a jejich použití

## Monitorovací skripty
1. **SDR monitor**
   ```python
   #!/usr/bin/env python3
   from rtlsdr import RtlSdr
   import numpy as np
   
   sdr = RtlSdr()
   sdr.sample_rate = 2.4e6
   sdr.center_freq = 433e6
   
   samples = sdr.read_samples(1024)
   power = np.mean(np.abs(samples)**2)
   print(f"Výkon signálu: {power} dB")
   ```

2. **WiFi skener**
   ```python
   #!/usr/bin/env python3
   from scapy.all import *
   import pandas as pd
   
   def packet_handler(pkt):
       if pkt.haslayer(Dot11Beacon):
           bssid = pkt[Dot11].addr2
           ssid = pkt[Dot11Elt].info.decode()
           print(f"BSSID: {bssid}, SSID: {ssid}")
   
   sniff(iface="wlan0mon", prn=packet_handler)
   ```

3. **Systémový monitor**
   ```python
   #!/usr/bin/env python3
   import psutil
   import time
   
   while True:
       cpu = psutil.cpu_percent()
       memory = psutil.virtual_memory().percent
       print(f"CPU: {cpu}%, Memory: {memory}%")
       time.sleep(5)
   ```

## Automatizační skripty
1. **Zálohování**
   ```bash
   #!/bin/bash
   BACKUP_DIR="/backup"
   DATE=$(date +%Y%m%d)
   
   tar -czf $BACKUP_DIR/backup_$DATE.tar.gz /etc /var/log
   find $BACKUP_DIR -type f -mtime +7 -delete
   ```

2. **Čištění**
   ```bash
   #!/bin/bash
   LOG_DIR="/var/log"
   MAX_SIZE="100M"
   
   find $LOG_DIR -type f -size +$MAX_SIZE -exec truncate -s 0 {} \;
   ```

3. **Aktualizace**
   ```bash
   #!/bin/bash
   apt update
   apt upgrade -y
   pip3 install --upgrade -r requirements.txt
   ```

## Bezpečnostní skripty
1. **Firewall kontrola**
   ```python
   #!/usr/bin/env python3
   import subprocess
   
   def check_firewall():
       result = subprocess.run(['ufw', 'status'], capture_output=True)
       return "Status: active" in result.stdout.decode()
   
   if not check_firewall():
       print("Varování: Firewall není aktivní!")
   ```

2. **Log analýza**
   ```python
   #!/usr/bin/env python3
   import re
   
   def analyze_logs(log_file):
       with open(log_file) as f:
           for line in f:
               if "error" in line.lower():
                   print(f"Nalezena chyba: {line.strip()}")
   ```

3. **Skenování portů**
   ```python
   #!/usr/bin/env python3
   import socket
   
   def scan_ports(host, ports):
       for port in ports:
           sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
           result = sock.connect_ex((host, port))
           if result == 0:
               print(f"Port {port} je otevřený")
           sock.close()
   ```

## Webové skripty
1. **API endpoint**
   ```python
   #!/usr/bin/env python3
   from flask import Flask, jsonify
   
   app = Flask(__name__)
   
   @app.route('/api/status')
   def status():
       return jsonify({"status": "ok"})
   
   if __name__ == '__main__':
       app.run(host='0.0.0.0')
   ```

2. **Dashboard**
   ```python
   #!/usr/bin/env python3
   from flask import Flask, render_template
   import psutil
   
   app = Flask(__name__)
   
   @app.route('/')
   def dashboard():
       cpu = psutil.cpu_percent()
       memory = psutil.virtual_memory().percent
       return render_template('dashboard.html', cpu=cpu, memory=memory)
   ```

3. **Konfigurační rozhraní**
   ```python
   #!/usr/bin/env python3
   from flask import Flask, request, jsonify
   
   app = Flask(__name__)
   
   @app.route('/api/config', methods=['POST'])
   def update_config():
       config = request.json
       # Uložit konfiguraci
       return jsonify({"status": "success"})
   ```

## Spouštění skriptů
1. **Systemd služby**
   ```bash
   sudo systemctl enable monitoring.service
   sudo systemctl start monitoring.service
   ```

2. **Cron úlohy**
   ```bash
   crontab -e
   * * * * * /path/to/script.py
   ```

3. **Manuální spuštění**
   ```bash
   chmod +x script.py
   ./script.py
   ``` 