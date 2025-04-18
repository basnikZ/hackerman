#!/usr/bin/env python3
import subprocess
import json
import os
import time
import signal
import sys
import tempfile
import datetime
import threading

def scan_wifi_networks():
    """Skenuje dostupné WiFi sítě pomocí systémového nástroje na macOS."""
    try:
        # Spustíme system_profiler s JSON výstupem
        result = subprocess.run(
            ["system_profiler", "-json", "SPAirPortDataType"],
            capture_output=True,
            text=True,
            check=True
        )
        
        # Parsujeme JSON výstup
        data = json.loads(result.stdout)
        
        # Extrahujeme informace o WiFi sítích
        networks = []
        
        try:
            # Získáme seznam dostupných sítí
            wifi_interfaces = data["SPAirPortDataType"][0]["spairport_airport_interfaces"]
            
            for interface in wifi_interfaces:
                if "_name" in interface and interface["_name"] == "en0":
                    if "spairport_airport_other_local_wireless_networks" in interface:
                        networks_data = interface["spairport_airport_other_local_wireless_networks"]
                        
                        for network in networks_data:
                            # Vytvoříme záznam pro každou síť
                            network_info = {
                                "ssid": network.get("_name", "Unknown"),
                                "channel": network.get("spairport_network_channel", "Unknown"),
                                "phy_mode": network.get("spairport_network_phymode", "Unknown"),
                                "security": network.get("spairport_security_mode", "Unknown")
                            }
                            
                            # Přidáme sílu signálu, pokud je dostupná
                            if "spairport_signal_noise" in network:
                                network_info["signal_noise"] = network["spairport_signal_noise"]
                            
                            networks.append(network_info)
                    break
        except (KeyError, IndexError) as e:
            print(f"Chyba při parsování dat: {e}")
        
        return networks
    
    except subprocess.CalledProcessError as e:
        print(f"Chyba při spuštění příkazu: {e}")
        return []
    except json.JSONDecodeError as e:
        print(f"Chyba při parsování JSON: {e}")
        return []

def print_wifi_networks(networks):
    """Vypíše nalezené WiFi sítě v přehledném formátu."""
    if not networks:
        print("Nebyly nalezeny žádné WiFi sítě.")
        return
    
    print("\n=== Dostupné WiFi sítě ===")
    print("-" * 70)
    print(f"{'SSID':<20} {'Kanál':<15} {'Režim':<15} {'Zabezpečení':<20}")
    print("-" * 70)
    
    for network in networks:
        ssid = network.get("ssid", "Unknown")
        channel = network.get("channel", "Unknown")
        phy_mode = network.get("phy_mode", "Unknown")
        security = network.get("security", "Unknown").replace("spairport_security_mode_", "")
        
        print(f"{ssid:<20} {channel:<15} {phy_mode:<15} {security:<20}")
        
        # Pokud je dostupná informace o síle signálu, vypíšeme ji
        if "signal_noise" in network:
            print(f"  Síla signálu/šum: {network['signal_noise']}")
    
    print("-" * 70)

def detect_suspicious_networks(networks):
    """Detekuje potenciálně podezřelé WiFi sítě."""
    suspicious = []
    
    for network in networks:
        ssid = network.get("ssid", "")
        security = network.get("security", "")
        
        # Kontrola nezabezpečených sítí
        if "none" in security.lower() or security == "Unknown":
            suspicious.append({
                "network": network,
                "reason": "Nezabezpečená síť (bez šifrování)"
            })
            continue
        
        # Kontrola slabého zabezpečení (WEP, WPA)
        if "wep" in security.lower() or ("wpa" in security.lower() and "wpa2" not in security.lower() and "wpa3" not in security.lower()):
            suspicious.append({
                "network": network,
                "reason": "Zastaralé/slabé zabezpečení"
            })
            continue
        
        # Kontrola potenciálně podvržených sítí (podobné názvy, atd.)
        common_hotspots = ["linksys", "netgear", "default", "setup", "wireless", "wifi", "free", "guest"]
        for hotspot in common_hotspots:
            if hotspot in ssid.lower():
                suspicious.append({
                    "network": network,
                    "reason": f"Potenciálně podvržená síť (obsahuje '{hotspot}')"
                })
                break
    
    return suspicious

def continuous_monitoring(interval=10, max_scans=None):
    """Kontinuální monitoring WiFi sítí."""
    known_networks = {}  # Zapamatování dříve viděných sítí
    scan_count = 0
    
    def signal_handler(sig, frame):
        print("\nMonitoring ukončen uživatelem.")
        sys.exit(0)
    
    # Zachycení CTRL+C pro čisté ukončení
    signal.signal(signal.SIGINT, signal_handler)
    
    print(f"Začínám kontinuální monitoring (interval: {interval}s)")
    print("Pro ukončení stiskněte CTRL+C")
    
    try:
        while True:
            networks = scan_wifi_networks()
            scan_count += 1
            
            if max_scans and scan_count > max_scans:
                print(f"\nDosažen maximální počet skenování ({max_scans}).")
                break
            
            print(f"\n[Sken #{scan_count}] Čas: {time.strftime('%H:%M:%S')}")
            print_wifi_networks(networks)
            
            # Detekce nových sítí
            current_ssids = {network.get("ssid") for network in networks}
            
            if scan_count > 1:
                new_ssids = current_ssids - set(known_networks.keys())
                missing_ssids = set(known_networks.keys()) - current_ssids
                
                if new_ssids:
                    print("\n=== NOVÉ SÍTĚ DETEKOVÁNY ===")
                    for ssid in new_ssids:
                        print(f" + {ssid}")
                
                if missing_ssids:
                    print("\n=== SÍTĚ JIŽ NEJSOU VIDITELNÉ ===")
                    for ssid in missing_ssids:
                        print(f" - {ssid}")
            
            # Kontrola podezřelých sítí
            suspicious = detect_suspicious_networks(networks)
            if suspicious:
                print("\n=== PODEZŘELÉ SÍTĚ ===")
                for item in suspicious:
                    network = item["network"]
                    print(f" ! {network.get('ssid', 'Unknown')}: {item['reason']}")
            
            # Aktualizace známých sítí
            for network in networks:
                ssid = network.get("ssid")
                known_networks[ssid] = network
            
            # Pauza před dalším skenem
            if max_scans is None or scan_count < max_scans:
                time.sleep(interval)
    
    except KeyboardInterrupt:
        print("\nMonitoring ukončen uživatelem.")
    except Exception as e:
        print(f"\nChyba během monitoringu: {e}")

def capture_traffic(interface='en0', duration=30, packet_count=None, bpf_filter=None, capture_file=None):
    """
    Zachytává síťový provoz pomocí tcpdump.
    
    Args:
        interface (str): Síťové rozhraní pro zachytávání (výchozí: en0)
        duration (int): Doba zachytávání v sekundách (výchozí: 30)
        packet_count (int): Počet paketů k zachycení (výchozí: None = neomezeno)
        bpf_filter (str): Berkeley Packet Filter (výchozí: None = žádný filtr)
        capture_file (str): Soubor pro uložení zachyceného provozu (výchozí: None = automaticky generovaný)
    
    Returns:
        str: Cesta k souboru se zachyceným provozem
    """
    # Vytvoření výchozího názvu souboru, pokud není zadán
    if not capture_file:
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        capture_file = f"/tmp/wifi_capture_{timestamp}.pcap"
    
    # Sestavení příkazu tcpdump
    tcpdump_cmd = ["sudo", "tcpdump", "-i", interface, "-w", capture_file]
    
    # Přidání počtu paketů, pokud je zadán
    if packet_count:
        tcpdump_cmd.extend(["-c", str(packet_count)])
    
    # Přidání BPF filtru, pokud je zadán
    if bpf_filter:
        tcpdump_cmd.append(bpf_filter)
    
    # Vytvoření časovače pro zastavení zachytávání po určené době
    stop_event = threading.Event()
    
    def stop_capture():
        stop_event.set()
    
    # Nastavení časovače, pokud není zadán počet paketů
    if not packet_count and duration:
        timer = threading.Timer(duration, stop_capture)
        timer.daemon = True
        timer.start()
    
    print(f"Spouštím zachytávání provozu na rozhraní {interface}...")
    print(f"Provoz bude uložen do: {capture_file}")
    
    if duration and not packet_count:
        print(f"Zachytávání bude probíhat {duration} sekund.")
    elif packet_count:
        print(f"Zachytávání skončí po zachycení {packet_count} paketů.")
    
    try:
        # Spuštění tcpdump v novém procesu
        process = subprocess.Popen(tcpdump_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Čekání na dokončení zachytávání nebo na signál k zastavení
        while process.poll() is None:
            if stop_event.is_set():
                process.terminate()
                break
            time.sleep(0.1)
        
        print("\nZachytávání dokončeno.")
        print(f"Zachycený provoz uložen do: {capture_file}")
        
        return capture_file
    
    except subprocess.CalledProcessError as e:
        print(f"Chyba při spuštění tcpdump: {e}")
        return None
    except KeyboardInterrupt:
        print("\nZachytávání přerušeno uživatelem.")
        process.terminate()
        return capture_file

def open_in_wireshark(capture_file):
    """
    Otevře zachycený provoz ve Wiresharku (pokud je nainstalovaný).
    
    Args:
        capture_file (str): Cesta k souboru s zachyceným provozem
    """
    if not os.path.exists(capture_file):
        print(f"Soubor {capture_file} nebyl nalezen.")
        return False
    
    try:
        # Kontrola, zda je Wireshark nainstalovaný
        result = subprocess.run(["which", "wireshark"], capture_output=True, text=True)
        
        if result.returncode == 0:
            # Wireshark je nainstalovaný, otevíráme soubor
            subprocess.Popen(["open", "-a", "Wireshark", capture_file])
            print(f"Soubor {capture_file} byl otevřen ve Wiresharku.")
            return True
        else:
            # Wireshark není nainstalovaný, zkusíme otevřít v defaultním programu
            subprocess.Popen(["open", capture_file])
            print(f"Wireshark nebyl nalezen. Soubor {capture_file} byl otevřen v defaultním programu.")
            return True
    
    except Exception as e:
        print(f"Chyba při otevírání souboru: {e}")
        return False

if __name__ == "__main__":
    # Kontrola, zda jsme na macOS
    if os.name != "posix" or not os.path.exists("/usr/sbin/system_profiler"):
        print("Tento skript je určen pouze pro macOS.")
        exit(1)
    
    import argparse
    
    parser = argparse.ArgumentParser(description="WiFi Scanner pro RF Security Station")
    parser.add_argument("-s", "--scan", action="store_true", help="Jednorázový sken WiFi sítí")
    parser.add_argument("-m", "--monitor", action="store_true", help="Kontinuální monitoring WiFi sítí")
    parser.add_argument("-i", "--interval", type=int, default=10, help="Interval mezi skeny (v sekundách)")
    parser.add_argument("-c", "--count", type=int, help="Maximální počet skenů")
    
    # Nové argumenty pro zachytávání provozu
    parser.add_argument("-t", "--traffic", action="store_true", help="Zachytit síťový provoz pomocí tcpdump")
    parser.add_argument("-d", "--duration", type=int, default=30, help="Doba zachytávání v sekundách")
    parser.add_argument("-p", "--packets", type=int, help="Počet paketů k zachycení")
    parser.add_argument("-f", "--filter", help="Berkeley Packet Filter pro filtrování provozu")
    parser.add_argument("-o", "--output", help="Výstupní soubor pro zachycený provoz")
    parser.add_argument("-w", "--wireshark", action="store_true", help="Otevřít zachycený provoz ve Wiresharku")
    parser.add_argument("--interface", default="en0", help="Síťové rozhraní pro zachytávání (výchozí: en0)")
    
    args = parser.parse_args()
    
    if args.traffic:
        # Zachytávání provozu pomocí tcpdump
        capture_file = capture_traffic(
            interface=args.interface,
            duration=args.duration,
            packet_count=args.packets,
            bpf_filter=args.filter,
            capture_file=args.output
        )
        
        if capture_file and args.wireshark:
            open_in_wireshark(capture_file)
    elif args.monitor:
        # Kontinuální monitoring WiFi sítí
        continuous_monitoring(interval=args.interval, max_scans=args.count)
    else:
        # Jednorázový sken WiFi sítí
        networks = scan_wifi_networks()
        print_wifi_networks(networks)
        
        # Kontrola podezřelých sítí
        suspicious = detect_suspicious_networks(networks)
        if suspicious:
            print("\n=== PODEZŘELÉ SÍTĚ ===")
            for item in suspicious:
                network = item["network"]
                print(f" ! {network.get('ssid', 'Unknown')}: {item['reason']}") 