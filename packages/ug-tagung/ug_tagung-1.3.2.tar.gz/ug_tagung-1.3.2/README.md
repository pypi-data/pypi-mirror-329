# ug_tagung.Tagung

Verwaltung für Tagungen.


## Abkürzungen

| Abk. | Ausgeschrieben |
| ---- | -------------- |
| DB   | Datenbank      |
| TB   | Tagungsbüro    |
| TN   | Teilnehmer     |
| VA   | Veranstaltung  |
| WS   | Workshop       |


## Features

* **Verwaltung der Personen Daten**
    * Kontaktdaten
    * Anmeldestatus
    * Bezahlung
* **Verwaltung von Institutions-Daten**
    * Unter Institutionen verstehen wir Firmen, Schulen, Gemeinden usw., also eigentlich alle
    Kontakte, die keine Personen sind, aber etwas mit der Tagung zu tun haben.
    * Es werden im Wesentlichen Kontaktdaten verwaltet.
    * Institutionen können beim Quartier-Management wichtig werden. Siehe dazu weiter unten.
* **Anmelde-Logistik**
    * Online-Anmeldungen werde automatisch in die Datenbank eingefügt
    * Über den Anmeldestatus steuert das TB Bestätigungs* und andere Mails an die TN
* **WS-Logistik**
    * Halbautomatische Zuordnung der WS-Anmeldungen zu den bereits angemeldeten TNn
    * Aussagekräftige Arbeitslisten zur tatsächlichen Zuteilung der TN auf die WSs. Das ist nötig, da die WS-Anmeldungen 1., 2. und 3. Wahl kennen und keine vollautomatische Zuteilung gewünscht ist.
    * TN-Listen für die WSs
    * Es können bis zu 4 unterschiedliche Arten von WSs unabhängig voneinander verwaltet werden. Z.B. könnte es vormittags Gesprächsgruppen und nachmittags künstlerische und sportliche Workshops geben.
* **Gruppen (= Rollen)**
    * Jede Person in der DB kann einer oder mehreren Gruppen angehören. Typische Gruppen sind:
        * TN = Teilnehmer
        * Doz = Dozent
        * Team = Tagungsteam (Vorbereitung und Durchführung)
        * Pr = Priester
    * Es können beliebig weitere Gruppen definiert werden.
* **Veranstaltungs- und Raum-Management**
    * Bei Bedarf (d.h. z.B. Tagungen mit mehr als 300 TN oder mehr als 50 VAen) können sämtliche VAen und alle verfügbaren Räume (incl. Außenflächen u.a.). Später können jeder VA eine oder mehrere Zeiten in den Räumen zugewiesen werden. Die vorhandenen Daten werden ausgewertet zu:
    * Studenplänen für jeden Raum bzw. für jede VA.
    * In den Stundenplänen werden Überschneidungen (= Doppelbelegungen) farblich signalisiert.
* **TN-Listen und andere PDF-Auswertungen**
    * TN-Liste und alle anderen PDF-Auswertungen werden regelmäßig und in einstellbaren Intervallen automatisch erzeugt und über eine NextCloud zur Ansicht und zum Download bereitgestellt.
    * Zu den möglichen Auswertungen gehören:
        * TN-Gesamtliste
        * Gruppenlisten (d.h. für jede Gruppe eine Liste)
        * Statistik (Überblick über Anmeldungen, zugesagte TN-Beiträge u.a.
    * Die TN-Liste ist so konzipiert, dass sie zu Beginn der Tagung beim Empfang (Counter) alle relevanten Informationen übersichtlich zeigt, s.d. nötigenfalls gezielt Unklarheiten mit dem TN geklärt werden können. Insb. gehört dazu, ob der TN-Beitrag in der zu erwartenden Höhe bereits gezahlt wurde.
* **Quartier-Management**
    * Personen und Instituionen können "Quartiergeber" werden, indem sie ein oder mehrere Quartiere anbieten. Von der Couch im Wohnzimmer bis zum Hotelzimmer ist alles möglich.
    * Andere Personen können in solchen Quartieren untergebracht werden.
    * Diese Unterbringungen werden in den Auswertungen mit ausgegeben.

Das Programm wurde und wird von Ulrich Goebel speziell für die Anforderungen von kirchlichen Tagungen entwickelt.

Das hier verfügbare Paket beinhaltet ausschließlich die GUI für diese Adressverwaltung. Die Daten werden in einer PostgreSQL-Datenbank gehalten, die auf einem eigenen Server läuft. Auswertungen, also PDFs zum Ausdrucken von Adresslisten u.a. werden ebenso auf diesem Server durch einen Cron-Job regelmäßig hergestellt und über eine Nextcloud bereitgestellt.

Durch die spezielle Architektur ist das Paket kaum für jedermann brauchbar. Falls es aber Interesse gibt, kann man sich gerne an Ulrich Goebel wenden (ulrich@fam-goebel.de).


# Systemvoraussetzungen

* Linux (empfohlen), Windows oder Mac
* Python 3


# Installation

## Linux und macOS

Der ganze Installationsvorgang kann mit dem Skript `TagungInstall.sh` durchgeführt werden. Dieses Skript verschicke ich bei Bedarf per eMail. Das Skript macht allerdings auch nichts anderes als was im Folgenden beschrieben ist.

### Python

In aller Regel ist auf Linux-Systemen Python 3 installiert. Falls nicht, muss man es über die üblichen Repositories nachholen. Unter Umständen muss man zusätzlich `python3-venv` installieren.

**Unter macOS ist das Programm bisher nicht getestet. In jedem Fall muss Python 3 installiert werden, evt. zusätzlich die Bibliothek `venv` für Virtuelle Umgebungen (Virtual Environments).**

### Virtual Environment

Es wird dringend empfohlen (und im Folgenden vorausgesetzt), die GUI innerhalb einer Virtuellen Umgebung laufen zu lassen. Dafür:

1. Ein Verzeichnis für die GUI anlegen, z.B.  
`mkdir Tagung`
2. Dort eine virtuelle Umgebung anlegen:  
`cd Tagung`  
`python3 -m venv .venv`  
Damit wird innerhalb des Verzeichnisses `Tagung` eine Virtuelle Umgebung namens `.venv` angelegt.
2. Die Virtuelle Umgebung aktivieren:  
`source .venv/bin/activate`
3. Nach Beendigung der Arbeit die Virtuelle Umgebung deaktivieren:  
`deactivate`

### ug_tagung installieren

Dafür wechseln wir wieder in die Virtuelle Umgebung und installieren dsa Paket dort:

1. In das Verzeichnis wechseln:  
`cd Tagung`
2. Die Virtuelle Umgebung aktivieren:  
`source .venv/bin/activate`
3. Das Paket `ug_tagung` installieren:  
`pip install ug_tagung`
4. Das Programm einmalig im Setup-Modus laufen lassen:  
`python -m ug_tagung.Tagung --setup`
5. Es sollten nun einige Dateien in das aktuelle Verzeichnis kopiert worden sein. Darunter die beiden Skripte `TagungStart.sh` und `TagungUpgrade.sh`.  
6. Diese beiden Skripte ausführbar machen, etwa mit  
`chmod a+x TagungStart.sh TagungUpgrade.sh`
7. Die Virtuelle Umgebung deaktivieren:  
`deactivate`
8. Optional können, wenn man die GUI später per Mausklick ausführen möchte, für die beiden genannten Skripte Starter angelegt werden, einen für  
`TagungStart.sh`  
und einen für  
`TagungUpgrade.sh`  
Mit dem ersten wird spätre die GUI gestartet, mit dem anderen werden - falls verfügbar - Upgrades installiert.  
In beiden Fällen muss das Arbeitsverzeichnis angegeben werden, etwa "Ausführen in:" Dort ist etwa `/home/.../Tagung` anzugeben.  
In beiden Fällen sollte, wenn die Option besteht, etwa "Im Terminal ausführen" aktiviert werden.

## Windows

Der ganze Installationsvorgang kann mit dem PowerShell-Skript `TagungInstall.ps1` durchgeführt werden. Dieses Skript verschicke ich bei Bedarf per eMail. Das Skript macht allerdings auch nichts anderes als was im Folgenden beschrieben ist.

Die Befehlseingaben im folgenden erfolgen immer von der PowerShell aus.

### Python

Es muss Python 3 installiert sein. Das geht am besten über den Microsoft Store, sonst auch über die offizielle [Python-Seite](https://www.python.org/). In jedem Fall ist sicher zu stellen, dass Python sich über die PowerShell aufrufen lässt; dafür öffnet man die PowerShell und gibt ein  
`python --version`  
oder  
`python3 --version`  
Es sollte dann eine Version der Form 3.xx angezeigt werden.

### Virtual Environment

Es wird dringend empfohlen (und im Folgenden vorausgesetzt), die GUI innerhalb einer Virtuellen Umgebung laufen zu lassen. Dafür:

1. Ein Verzeichnis für die GUI anlegen, z.B.  
`mkdir Tagung`
2. Dort eine virtuelle Umgebung anlegen:  
`cd Tagung`  
`python3 -m venv venv`  
oder  
`python -m venv venv`  
Damit wird innerhalb des Verzeichnisses `Tagung` eine Virtuelle Umgebung namens `venv` angelegt.
2. Die Virtuelle Umgebung aktivieren:  
`.\venv\Scripts\Activate.ps1`
3. Nach Beendigung der Arbeit die Virtuelle Umgebung deaktivieren:  
`deactivate`

### ug_tagung installieren

Dafür wechseln wir wieder in die Virtuelle Umgebung und installieren dsa Paket dort:

1. In das Verzeichnis wechseln:  
`cd Tagung`
2. Die Virtuelle Umgebung aktivieren:  
`.\venv\Scripts\Activate.ps1`
3. Das Paket `ug_tagung` installieren:  
`pip install ug_tagung`
4. Das Programm einmalig im Setup-Modus laufen lassen:  
`python -m ug_tagung.Tagung --setup`
5. Es sollten nun einige Dateien in das aktuelle Verzeichnis kopiert worden sein. Darunter die beiden Skripte `TagungStart.ps1` und `TagungUpgrade.ps1`.  
7. Die Virtuelle Umgebung deaktivieren:  
`deactivate`
8. Optional können, wenn man die GUI später per Mausklick ausführen möchte, für die beiden genannten Skripte Starter angelegt werden, einen für  
`TagungStart.ps1`  
und einen für  
`TagungUpgrade.ps1`  
Mit dem ersten wird spätre die GUI gestartet, mit dem anderen werden - falls verfügbar - Upgrades installiert.  
In beiden Fällen muss das Arbeitsverzeichnis angegeben werden, etwa "Ausführen in:" Dort ist etwas wie `...\Tagung` anzugeben.  
In beiden Fällen sollte, wenn die Option besteht, etwa "Im Terminal ausführen" aktiviert werden.


# Programm starten

## Linux und macOS

### Im Terminal

1. Terminal öffnen.  
2. In das entsprechende Verzeichnis wechseln:  
`cd Tagung`
3. Virtuelle Umgebung aktivieren:  
`source .venv/bin/activate`
4. Programm starten:  
`python -m ug_tagung.Tagung`
5. Optional können der Username und das Passwort gleich mit angegeben werden:  
`python -m ug_tagung.Tagung -u username -p password`
6. Nach Programmende die Virtuelle Umgebung deaktivieren:  
`deactivate`

### Im Terminal per Skript TagungStart.sh

1. Terminal öffnen.
2. In das entsprechende Verzeichnis wechseln:  
`cd Tagung`
3. Mit dem Skript die GUI starten:  
`TagungStart.sh`

Die Virtuelle Umgebung wird von dem Skript aktiviert und später wieder deaktiviert.

### Per Starter

Falls während der Installation oder später die beiden erwähnten Starter angelegt wurden, kann die GUI über diese Starter ausgeführt werden.

## Windows

### Im Terminal

1. PowerShell öffnen.  
2. In das entsprechende Verzeichnis wechseln:  
`cd Tagung`
3. Virtuelle Umgebung aktivieren:  
`.\venv\Scripts\Activate.psq`
4. Programm starten:  
`python -m ug_tagung.Tagung`
5. Optional können der Username und das Passwort gleich mit angegeben werden:  
`python -m ug_tagung.Tagung -u username -p password`
6. Nach Programmende die Virtuelle Umgebung deaktivieren:  
`deactivate`

### Im Terminal per Skript TagungStart.ps1

1. PowerShell öffnen.
2. In das entsprechende Verzeichnis wechseln:  
`cd Tagung`
3. Mit dem Skript die GUI starten:  
`TagungStart.ps1`

Die Virtuelle Umgebung wird von dem Skript aktiviert und später wieder deaktiviert.

### Per Starter

Falls während der Installation oder später die beiden erwähnten Starter angelegt wurden, kann die GUI über diese Starter ausgeführt werden.


# Programm Upgrade

Das Programm befindet sich noch in der Weiterentwicklung. Daher gibt es v.a. im Jahr 2025 voraussichtlich immer wieder Upgrades, die Verbesserungen und Erweiterungen bringen oder Fehler beseitigen. Auf wichtige Upgrades werde ich die Benutzer hinweisen; unabhängig davon kann das Upgrade aber von Zeit zu Zeit auch einfach durchgeführt werden.

**Achtung:** Manchmal erkennt die Routine für das Upgrade erst beim zweiten Anlauf, dass tatsächlich ein Upgrade verfügbar ist. Das ist ein technisches Problem, auf das ich keinen Einfaluss habe. Ggf. muss man diese Routine also zweimal starten.

## Linux und macOS

### Im Terminal

1. Terminal öffnen.  
2. In das entsprechende Verzeichnis wechseln:  
`cd Tagung`
3. Virtuelle Umgebung aktivieren:  
`source .venv/bin/activate`
4. Upgrade starten:  
`pip install --no-cache-dir -U ugbib_divers ugbib_modell ugbib_tkinter ugbib_werkzeug`  
`pip install --no-cache-dir -U ug_tagung`
6. Nach Programmende die Virtuelle Umgebung deaktivieren:  
`deactivate`

### Im Terminal per Skript TagungStart.sh

1. Terminal öffnen.
2. In das entsprechende Verzeichnis wechseln:  
`cd Tagung`
3. Mit dem Skript die GUI starten:  
`TagungUpgrade.sh`

Die Virtuelle Umgebung wird von dem Skript aktiviert und später wieder deaktiviert.

### Per Starter

Falls während der Installation oder später die beiden erwähnten Starter angelegt wurden, kann das Upgrade über den entsprechenden Starter ausgeführt werden.

## Windows

### Im Terminal

1. PowerShell öffnen.  
2. In das entsprechende Verzeichnis wechseln:  
`cd Tagung`
3. Virtuelle Umgebung aktivieren:  
`.\venv\Scripts\Activate.psq`
4. Upgrade starten:  
`pip install --no-cache-dir -U ugbib_divers ugbib_modell ugbib_tkinter ugbib_werkzeug`  
`pip install --no-cache-dir -U ug_tagung`
6. Nach Programmende die Virtuelle Umgebung deaktivieren:  
`deactivate`

### Im Terminal per Skript TagungStart.ps1

1. PowerShell öffnen.
2. In das entsprechende Verzeichnis wechseln:  
`cd Tagung`
3. Mit dem Skript die GUI starten:  
`TagungUpgrade.ps1`

Die Virtuelle Umgebung wird von dem Skript aktiviert und später wieder deaktiviert.

### Per Starter

Falls während der Installation oder später die beiden erwähnten Starter angelegt wurden, kann das Upgrade über den entsprechenden Starter ausgeführt werden.


