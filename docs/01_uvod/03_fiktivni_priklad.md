# Fiktivni priklad monitoringu

## Uvod do situace
```console
Stredne velka IT firma se rozhodla implementovat zakladni monitoring
RF spektra po tom, co zjistila, ze jejich bezpecnostni senzory
byly nekolikrat deaktivovany neznamym zpusobem. Zvolili cenove
dostupne reseni s vyuzitim SDR prijmacu.

Proc prave SDR?
▶ Cenova dostupnost (RTL-SDR v3 stoji cca 800 Kc)
▶ Siroka podpora v Linux nastrojich
▶ Moznost zachytit a analyzovat ruzne typy signalu
▶ Snadna rozsiritelnost systemu
```

## Hardwarove vybaveni a jeho rozmisteni
```console
RTL-SDR #1: Serverovna (433-435 MHz)
▶ Proc: Vetsina bezpecnostnich senzoru komunikuje na 433.92 MHz
▶ Dosah: Cca 20 metru skrz zdi
▶ Antena: Skladana dipol antena pro 433 MHz
▶ Zisk: 4.5 dBi pro optimalni prijem slabych signalu

RTL-SDR #2: Technicka mistnost (868 MHz)
▶ Proc: Evropske ISM pasmo pro IoT zarizeni
▶ Dosah: 15-20 metru v budove
▶ Antena: 868 MHz whip antena
▶ Zisk: 3 dBi, vertikalni polarizace

WiFi adapter (Alfa AWUS036ACH):
▶ Proc: Podporuje monitor mode a packet injection
▶ Umisteni: Centralni chodba pro nejlepsi pokryti
▶ Antena: Dual-band 2.4/5 GHz, 5 dBi
▶ Chip: Realtek RTL8812AU (podporovan v Linuxu)
```

## Slovnicek technickych pojmu
```console
Zakladni pojmy:
▶ SDR (Software Defined Radio)
   - Zarizeni, ktere umi prijmat radiove signaly v sirokém pasmu
   - Prevadi radiove signaly do digitalni podoby pro analyzu
   - Levnejsi alternativa k profesionalnim analyzatorum

▶ Paket
   - Maly kousek dat posilany pres sit
   - Obsahuje hlavicku (adresa odesilatele, prijemce) a data
   - Neco jako digitalni obalka s obsahem a adresou

▶ dBm
   - Jednotka pro mereni sily signalu
   - -30 dBm je velmi silny signal (blizkost vysilace)
   - -90 dBm je slaby signal (daleko od vysilace)

▶ MAC adresa
   - Unikatni identifikator kazdeho sitoveho zarizeni
   - Neco jako "rodne cislo" pro sitove karty
   - Format: 6 dvojic cisel (napr. 00:11:22:33:44:55)

Typy utoku:
▶ Evil Twin utok
   - Utocnik vytvori kopii legitimni WiFi site
   - Snazi se presvedcit uzivatele, aby se pripojili k jeho siti
   - Muze odchytavat hesla a data
   - Podobne jako kdyz nekdo vytvori falesnou pobocku banky

▶ Deauth utok
   - Utocnik posila specialni pakety, ktere odpojuji zarizeni
   - Jako kdyby nekdo porad mackal "odpojit" tlacitko
   - Casto prvni krok pred Evil Twin utokem

▶ Replay utok
   - Zachyceni legitimniho signalu a jeho opakovane vysilani
   - Jako kdyby nekdo nahral zvuk klice v zamku a prehral ho

Nastroje:
▶ Wireshark
   - Program pro analyzu sitoveho provozu
   - Umi cist a analyzovat pakety
   - Neco jako mikroskop pro sitovou komunikaci

▶ tcpdump
   - Nastroj pro zachytavani sitoveho provozu
   - Jako videokamera pro sit

▶ GQRX
   - Program pro vizualizaci radioveho spektra
   - Ukazuje, jake signaly jsou ve vzduchu
   - Jako osciloskop pro radiove signaly
```

## Detekovane signaly - rozbor incidentu
```console
09:15 - Prvni naznak utoku (433 MHz)
▶ Co jsme videli: 
   - Silny signal na frekvenci nasich bezpecnostnich cidel
   - Frekvence 433.92 MHz je bezna pro domaci zarizeni
   - Je to jako radic od garazovych vrat nebo domovni zvonek

▶ Proc je to podezrele: 
   - Signal byl 2x silnejsi nez normalni
   - Je to jako kdyby nekdo krical misto normalni mluvy
   - Bezne signaly jsou slabsi kvuli prekazkam a vzdalenosti

▶ Technicke detaily: 
   - 0xA5FF01... = typicky zacatek paketu nasich senzoru
     (jako kdyby kazda zprava zacinala "POZOR:")
   - -35 dBm = signal az podezrele silny 
     (normalne -60 az -50 dBm, tedy 4x az 8x slabsi)

▶ Pouzity SW: rtl_433 s vlastnim dekoderem
   - rtl_433 je jako prekladatel z reci senzoru do PC
   - Vlastni dekoder potrebujeme, protoze kazdy vyrobce
     mluvi svym vlastnim "jazykem"

09:20 - Potvrzeni utoku (WiFi)
▶ Co je deauth utok: 
   - Utocnik posila "ODPOJ SE!" prikazy vsem zarizenim
   - Je to legitimni prikaz, ale zneuzity
   - Jako kdyby nekdo v restauraci predstiral cisnika
     a rikal hostum, ze musi odejit

▶ Jak funguje: 
   - WiFi protokol veri temto prikazum automaticky
   - Zarizeni se odpoji a zkusi se znovu pripojit
   - Utocnik muze tento proces porad opakovat

▶ Proc je to nebezpecne: 
   - Priprava pro Evil Twin: Utocnik muze vytvorit
     falesnou kopii nasi site, kdyz jsou zarizeni odpojene
   - Odpojeni uzivatelu: Preruseni prace, ztrata spojeni

▶ Detekcni nastroje:
   - tcpdump: Zachytava vsechny pakety (jako kamera)
   - tshark: Filtrace a analyza (jako detektor pohybu)

09:35 - Rozsireni utoku (868 MHz)
▶ Proc je to zajimave: 
   - Signal na frekvenci nasich termostatu
   - 868 MHz je vyhrazena pro IoT zarizeni v EU
   - Malo ruseni = vetsi sance na uspesny utok

▶ FSK modulace: 
   - Frekvencni modulace, jako FM radio
   - Data jsou zakodovana zmenami frekvence
   - Odolnejsi vuci ruseni nez AM modulace

▶ Analyza:
   - GQRX: Vizualni kontrola spektra
     (jako dalkohled pro radiove vlny)
   - inspectrum: Detailni analyza modulace
     (jako mikroskop pro radiove signaly)
```

## Reakce a obrana
```console
Okamzita reakce (prvnich 5 minut):
▶ Packet capture (-w incident.pcap)
   - Proc: Forenzni analyza po incidentu
   - Format: PCAP pro snadnou analyzu ve Wireshark
   
▶ Zaloha logu z RTL_433
   - Co obsahuji: Casove razitko, silu signalu, dekodovana data
   - Proc: Dokazovy material a analyza vzorcu utoku

▶ Lokalizace pomoci SDR
   - Jak: Mereni sily signalu z ruznych mist
   - Proc: Najit fyzicky zdroj signalu
   
▶ Notifikace pres Slack
   - Proc Slack: Rychla reakce tymu, integrace s dalsimi nastroji
   - Format: Automaticky alert s grafy a daty

Navazujici kroky (dalsich 15 minut):
▶ Zalohovani WiFi: Prepnuti na sekundarni AP s jinym SSID
▶ Deaktivace senzoru: Docasne prepnuti na dratove zalohy
▶ Fyzicka kontrola: Hledani podezrelych zarizeni
▶ Rozsireny monitoring: Kismet pro komplexni WiFi analyzu
```

## Technicka analyza a forenzika
```console
WiFi analyza:
▶ Wireshark - co hledame:
   - Zdrojove MAC adresy utocnika
   - Vzorce v casovani paketu
   - Specificke signatury nastroju
   - Metadata v 802.11 ramcich

▶ Analyza 433 MHz:
   - Universal Radio Hacker (URH)
     - Dekodovani protokolu
     - Analyza timingu
     - Hledani vzorcu v datech
   - Porovnani s legitimnimi signaly
     - Rozdily v modulaci
     - Anomalie v casovani
     - Nestandardni delka paketu
```

## Zlepseni zabezpeceni
```console
Technicke upravy:
▶ Rotujici kody v senzorech
   - Proc: Zabraneni replay utokum
   - Jak: Rolling code s AES-128
   
▶ WiFi IDS (Suricata)
   - Detekce: Deauth, Krack, PMKID utoky
   - Alerting: Integrace se SIEM
   
▶ Vlastni dekodery
   - Presnejsi detekce anomalii
   - Mene false positive alertu

Dokumentace a procesy:
▶ RF site survey
   - Baseline legitimniho provozu
   - Mapa pokryti a ruseni
   - Identifikace slepych mist

▶ Incident Response
   - Postupy pro ruzne typy utoku
   - Kontaktni osoby a eskalace
   - Pravidelne testovani postupu
``` 