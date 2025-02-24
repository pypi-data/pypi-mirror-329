#!/bin/bash

##  TagungStart.sh
##
##  Mit diesem Skript soll der Programmstart der GUI vereinfacht werden. Insb. kann die GUI
##  dann über einen Starter auch pre Mausklick gestartet werden.

##  Virtuelle Umgebung aktivieren
echo "Virtuelle Umgebung aktivieren"
source .venv/bin/activate

##  GUI  starten
python -m ug_tagung.Tagung
##  alternativ:
# python -m -ug_. -u username -p password

##  Virtuelle Umgebung deaktivieren
echo "Virtuelle Umgebung deaktivieren"
deactivate
