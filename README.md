# Pythonprogramm zur DNS-Abfrage, wahlweisem Portscan und .json Speicherung

Das Programm frägt von einer gegebenen Domain die DNS-Daten ab, macht wahlweise einen portscan mit Nmap und speichert die Ergebnisse in einer .json Datei

## Voraussetzungen

1. [Nmap](https://nmap.org/) muss auf dem Rechner installiert und im System registriert werden
2. Python3 muss installiert sein
3. Die Pythonbibliotheken `dnspython` und `python-nmap` müssen extra geladen und in einer IDE oder im System eingerichtet werden

## Ausführung

Das Programm wird mit 2 Parametern ausgeführt:
`python3 DNSlookup.py [Website] [yes/no]`

**Bsp.:** Der Aufruf `python3 DNSlookup.py google.de no` würde einen DNS lookup durchführen ohne portscan.
Das Ergebnis sieht dann [so](https://github.com/alexanderKalb/dns_portscan_json_python/blob/master/Beispiel.json) aus.

In einer IDE müssen entsprechend die Parameter in der Konfiguration gesetzt werden.

## Nmap Funktion

Nmap überprüft die IPv4-Adresse, die Mailadressen(MX Record) und die Name-Server(NS) Adressen; keine Funktionalität bei IPv6 Adressen
Folgendes macht Nmap im Programm:

1. Überprüft ob die Adresse *up* oder *down* ist
2. Gibt die wahrscheinlichen Betriebssysteme an (OS-Guess)
3. Gibt die Genauigkeit zu dem sich Nmap sicher ist beim OS
4. Scannt die Standard-Ports(0-1023) und listet nach Protokoll
5. Gibt an ob gefunde Ports offen oder geschlossen sind

Nmap ist noch mächtiger, die weiteren Funktionen wurden aber aus Zeit- und Übersichtlichkeitsgründen ausgelassen.
