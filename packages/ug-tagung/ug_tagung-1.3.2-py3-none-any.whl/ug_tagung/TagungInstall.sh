#!/bin/bash

##  TagungInstall.sh
##  
##  Diese Datei wird dem User gegeben, damit er damit die Tagung-GUI auf einem Linux-Rechner
##  einfach installieren kann.
##
##  Als Anleitung werden ihm folgende Schritte nahegelegt:
##      1. Ordner/Verzeichnis für die GUI anlegen.
##      2. Das Skript TagungInstall.sh in dieses Verzeichnis speichern.
##      3. Das Skript in diesem Verzeichnis ausführen, d.h.
##         entweder   a) Terminal öffnen
##                    b) Mit cd in das neue Verzeichnis wechseln
##                    c) Linux/macOS: Nötigenfalls das Skrpt ausführbar machen
##                    c) Windows:
##                          - PowerShell als Administrator öffnen und das folgende
##                            Kommando ausführen:
##                          - Set-ExecutionPolicy Bypass
##                          - PowerShell schließen und als normaler Benutzer wieder öffnen
##                    d) Dort das Skript ausführen (./TagungInstall.sh)
##         oder       a) Das Skript im Dateimanager anklicken
##      4. Prüfen, ob die Installation erfolgreich war: In dem Verzeichnis müssen 
##         mindestens folgende Dateien erschienen sein:
##              Tagung.yaml
##              Icons.yaml
##              TagungStart.sh
##              TagungUpgrade.sh
##      5. Damit die GUI bzw. das Upgrade bequem gestartet werden kann, sollte in
##         einem Panel oder auf dem Schreibtisch je ein Starter für TagungStart.sh
##         und TagungUpgrade.sh eingerichtet werden. In beiden Startern sollte
##         "Im Terminal ausführen" aktiviert werden.
##      6. Optional: Um den Programmstart bzw. das dann folgende Login zu erleichtern,
##         kann in dem Skript TagungStart.sh die Zeile
##              python -m ug_tagung.Tagung
##         ersetzt werden durch
##              python -m ug_tagung.Tagung -u username -p password
##         Diese beiden Werte werden dann nach dem Start der GUI automatisch in die
##         entsprechenden Felder übernommen; es braucht nur noch der Login-Button
##         gedrückt zu werden.
##         WARNUNG: Diese Ergänzung sollte nur erfolgen, wenn der Rechner gut
##                  geschützt ist vor Fremdbenutzung usw., weil Username und Passwort
##                  im Klartext gespeichert werden.

##  Virtuelle Umgebung herstellen
echo "Virtuelle Umgebung herstellen"
python3 -m venv .venv

##  Virtuelle Umgebung aktivieren
echo "Virtuelle Umgebung aktivieren"
source .venv/bin/activate

##  GUI Tagung installieren
echo "GUI Tagung installieren"
pip cache purge
pip install --no-cache-dir ug_tagung

##  GUI im Setup-Modus aufrufen.
##  Damit wird von der GUI ein Setup ausgefürhrt, dass folgendes erledigt und dann stoppt:
##      1. Tagung.yaml und Icons.yaml ins aktuelle Verzeichnis kopiert
##      2. Upgrade-Skript TagungUpgrade.sh ins aktuelle Verzeichnis kopiert
##      3. Start-Skript TagungStart.sh ins aktuelle Verzeichnis kopiert
##      4. Die beiden neuen Skripte ausführbar machen
echo "GUI im Setup-Modus aufrufen"
python -m ug_tagung.Tagung --setup
chmod a+x TagungStart.sh TagungUpgrade.sh

##  Virtuelle Umgebung deaktivieren
deactivate
