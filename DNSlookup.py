# dnspython und nmap Bibliotheken einbinden
import sys
import json
import dns.resolver
import nmap


# Suchbegriffe für DNS-Suche ohne TXT
dnsKeys = {"A": "IPv4", "AAAA": "IPv6", "CNAME": "CNAME", "MX": "MX", "NS": "NS", "PTR": "PTR",
           "SRV": "SRV", "SOA": "SOA"}
ipListe = []
Scanner = nmap.PortScanner()
Ziel = ""
jsonList = {"Domain": "", "IPv4": "", "IPv6": "", "CNAME": [], "MX": [], "NS": [], "PTR": [], "SRV": [], "SOA": [],
            "Nmap": {}}
zaehler = 1

if __name__ == '__main__':
    # Befehlseingabe korrekt?
    if sys.argv.__len__() == 3:
        # Überprüfung auf gültige Webadresse
        Ziel = sys.argv[1]
        try:
            temp = dns.resolver.query(Ziel, 'A')
        except dns.resolver.NXDOMAIN:
            print("Diese Adresse ist leider nicht gültig.")
        else:
            jsonList["Domain"] = Ziel

            # DNS lookup, speichern der überprüfbaren Werte und hochzählen von Zählvariablen
            for keyWord in dnsKeys:
                try:
                    result = dns.resolver.query(Ziel, keyWord)
                except dns.resolver.NoAnswer:
                    continue
                for ipval in result:
                    print(dnsKeys[keyWord], ipval.to_text())
                    if keyWord is 'A':
                        ipListe.append(ipval.to_text())
                        jsonList["IPv4"] = ipval.to_text()
                    elif keyWord is 'AAAA':
                        jsonList["IPv6"] = ipval.to_text()
                    else:
                        if keyWord is 'NS':
                            ipListe.append(ipval.to_text()[:-1])
                        if keyWord is 'MX':
                            ipListe.append(ipval.to_text()[2:-1])
                        jsonList[keyWord].append(ipval.to_text())

            yesScan = sys.argv[2]
            if yesScan in ["ja", "Ja", "JA", "jA", "Yes", "yes", "j", "y"]:
                print("Nmap-Scan wird durchgeführt")
                for EiPee in ipListe:
                    # Eigentlicher NMAP Scan
                    Scanner.scan(EiPee, ports="0-1024", arguments='-sS -A -T4')
                    # Scandaten in Datei schreiben
                    for hosthier in Scanner.all_hosts():
                        temp = {"IP": hosthier, "State": Scanner[hosthier].state(), "OS": {}, "Protocol": {}}
                        # OS je nach Ziel von 0 bis über 10 mögliche Ergebnisse
                        for opSy in Scanner[hosthier]['osmatch']:
                            temp["OS"][opSy['name']] = opSy['accuracy'] + "% accuracy"
                        for proto in Scanner[hosthier].all_protocols():
                            temp["Protocol"][proto] = []
                            lport = Scanner[hosthier][proto].keys()
                            lport = sorted(lport)
                            for port in lport:
                                tempString = "port " + port.__str__() + " state: " \
                                             + Scanner[hosthier][proto][port]['state']
                                temp["Protocol"][proto].append(tempString)
                        jsonList["Nmap"][Scanner[hosthier].hostname()] = temp
                    # Programmfortschritt anzeigen
                    print("Bitte warten, {} von {} Scans wurden durchgeführt".format(zaehler, ipListe.__len__()))
                    # Zählvariable
                    zaehler += 1
            else:
                print("Kein Scan wird durchgeführt")
        Text = open("portliste.json", "wt")
        Text.write(json.dumps(jsonList, separators=(',', ': '), indent=4))
        Text.close()
    else:
        print("Aufruf im Format >>Backupdata.py internet.com ja/nein<< halten")
