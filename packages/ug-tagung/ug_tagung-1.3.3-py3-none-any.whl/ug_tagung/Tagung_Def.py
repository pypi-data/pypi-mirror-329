import psycopg2, psycopg2.extras

from __main__ import glb
import logging
logger = logging.getLogger()

import os, os.path, shutil
import sys

import yaml
from argparse import ArgumentParser

import psycopg2

import smtplib, ssl
from email.message import EmailMessage

def setup():
    
    def find(name):
        for root, dirs, files in os.walk('./'):
            if name in files:
                return os.path.abspath(os.path.join(root, name))
    
    dateien = (
        find('Tagung.yaml'),
        find('Icons.yaml'),
        find('TagungStart.sh'),
        find('TagungUpgrade.sh'),
        find('TagungStart.ps1'),
        find('TagungUpgrade.ps1'),
        )
    for f in dateien:
        print(f'copy {f} ins aktuelle Verzeichnis.')
        shutil.copy(f, os.path.abspath('./'))

def aktive_tagungen():
    """Liefert eine Liste der aktiven Tagungen zurück
    
      Liest aus der Tabelle public.tbl_tagung die aktiven Tagungen und liefert sie
      als Liste von Dictionaries zurück. Das Dictionary entspricht jeweils einem
      von der Cursor-Factory psycopg2.extras.DictCursor Objekt, vgl. dazu
      http://initd.org/psycopg/docs/extras.html
      
      Das Dictionary kann (u.a.!) über die keys aus der Tabelle (bzw. den ggf. 
      angegebenen Aliases) angesprochen werden.
    """
    sql_tagung = """
        select *
        from public.tbl_tagung
        where aktiv
        order by kurz_bez
    """
    with psycopg2.connect(
                  host        = glb.PSQL_HOST,
                  port        = glb.PSQL_PORT,
                  database    = glb.PSQL_DATABASE,
                  user        = glb.PSQL_USER,
                  password    = glb.PSQL_PASSWORD) as DB:
        with DB.cursor(cursor_factory=psycopg2.extras.DictCursor) as curTagung:
            try:
                curTagung.execute(sql_tagung)
                tagungen = curTagung.fetchall()
            except Exception as e:
                logging.error('Tagungen lassen sich nicht auslesen: {}'.format(e))
                tagungen = [{},]
    return tagungen

def configuration():
    """configuration - Setzt alle (globalen) Einstellungen/Konstanten
    
        configuration setzt globale Konstanten auf Werte, die sich ergeben aus:
        
            Default
                Gesetzt in der lokalen Variable confDefault in YAML-Syntax
                
            Konfi-File
                Konfigurations-Datei in YAML-Syntax
                
            Kommandozeilenparameter
                Klar
        
        Default-Werte werden überschrieben von Einträgen im Konfi-File. Anschließend
        werden die Werte ggf. überschrieben durch Kommandozeilenparameter.
        
        Nicht alle Default-Werte dürfen durch Einträge in Konfi-File überschrieben werden.
        Insb. CONFI_FILE_NAME gehört zu diesen Ausnahmen - es würde auch keinen Sinn ergeben.
        
        Die Werte/Einstellungen werden global, in diesem Fall als Attribut von glb,
        gespeichert. glb kann in Modulen importiert werden, entweder von __main__ (d.h.
        von "hier"), oder von ugbib_diver.bibGlobal.
        
        Außerdem werden dieverse globale Variablen initialisiert:
            glb.DB
    """
    
    ## confDefault hält die Default-Werte der Konstanzen
    #
    confDefault = """
        # Name der Anwendung
        #     Wird insb. zur Ausgabe der Version des Programms verwendet
        
        NAME: 'Tagung'
        
        # Name des Konfi-Files
        
        CONFI_FILE_NAME: 'Tagung.yaml'
        
        # Version des Programms
        
        VERSION: 'x.x'
        
        ##  ICON_THEME - Icon Theme
        #       'oxygen' oder 'breeze'
        ICON_THEME: 'oxygen'
        
        ##  ICON_NAVI_SIZE - Icon größe für Navis
        #       14 ist eine sinnvolle Größe, sonst auch kleiner
        ICON_NAVI_SIZE: 14

        TKINTER_THEME: 'classic'
        
        # Logging Level
        #     Bezieht sich auf Python logging
        
        LOGGING_LEVEL: 'WARNING'
        
        # PostgreSQL Server
        #     Wird im Programm nicht gebraucht, aber von Modulen importiert,
        #     in diesem Fall z.B. von bibModell
        
        PSQL_HOST: '176.9.90.232'
        PSQL_PORT: '22555'
        PSQL_DATABASE: 'cg'
        PSQL_USER: ''
        PSQL_PASSWORD: ''
        
        # Format Strings für Datum, Zeit, DatumZeit
        #     Wird imProgramm nicht gebraucht, aber von Modulen importiert,
        #     in diesem Fall z.B. von bibForm
        
        FORMATS_TIME: ['%H:%M',]
        FORMATS_DATE: ['%d.%m.%Y', '%Y-%m-%d']
        FORMATS_DATETIME: ['%Y-%m-%d %H:%M',]
    """
    #
    # Werte confDefault aus
    yamlConf = yaml.safe_load(confDefault)
    for key in yamlConf:
        glb.setup(key, value=yamlConf[key])
    #
    # Baue Kommandozeilenparameter
    parser = ArgumentParser()
    parser.add_argument('--version',
        action='version',
        version=f'{glb.NAME} {glb.VERSION}')
    parser.add_argument('--setup',
        dest='setup',
        action='store_true',
        help='Holt Tagung.yaml, Icons.yaml und diverse Skripte ins Arbeitsverzeichnis und beendet das Programm.')
    parser.add_argument('-c', '--config',
        dest='confifilename',
        help='Name des Konfi-Files')
    parser.add_argument('-l', '--logging',
        dest='logginglevel',
        choices=('DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'),
        help='Logging Level')
    parser.add_argument('-u', '--user',
        dest='psql_user',
        default='',
        help='Username für die PostgreSQL Datenbank')
    parser.add_argument('-p', '--password',
        dest='psql_password',
        default='',
        help='Password für die PostgreSQL Datenbank')
    parser.add_argument('--host',
        dest='psql_host',
        default='',
        help='Host der Verbindung zum PostgreSQL Server')
    parser.add_argument('--port',
        dest='psql_port',
        default='',
        help='Port der Verbindung zum PostgreSQL Server')
    parser.add_argument('--database',
        dest='psql_database',
        default='',
        help='PostgreSQL Database Name')
    #
    # Lese Kommandozeilenparameter aus
    args = parser.parse_args()
    #
    # Setup durchführen, falls --setup angegeben
    if args.setup:
        setup()
        sys.exit()
    #
    # Setze ggf. Name des Konfi-Files nach Kommandozeilenparameter neu
    if args.confifilename:
        glb.setvalue(CONFI_FILE_NAME, args.confifilename)
    #
    # lese confFileName aus
    with open(glb.CONFI_FILE_NAME, 'r') as confFile:
        yamlConf = yaml.safe_load(confFile)
    #
    # Stelle Konstanten her, vorhandene Werte werden ggf. überschrieben
    for key in yamlConf:
        if key == 'CONFI_FILE_NAME':
            raise RuntimeError(f'{key} darf im Konfi File nicht gesetzt werden.')
        glb.setup(key, yamlConf[key], force=True)
    #
    # Kommandozeilenparameter bearbeiten
    if args.logginglevel:
        glb.setvalue(LOGGING_LEVEL, args.logginglevel)
        logger.setLevel(glb.LOGGING_LEVEL)
    else:
        logging.debug(f'Setze Logging Level auf {glb.LOGGING_LEVEL}')
    logger.setLevel(glb.LOGGING_LEVEL)
    if args.psql_user:
        glb.setvalue('PSQL_USER', args.psql_user)
    if args.psql_password:
        glb.setvalue('PSQL_PASSWORD', args.psql_password)
    if args.psql_host:
        glb.setvalue('PSQL_HOST', args.psql_host)
    if args.psql_port:
        glg.setvalue('PSQL_PORT', args.psql_port)
    #
    # Globale Variablen initialisieren
    glb.setup('DB')
    glb.setup('schema')
    glb.setup('tagung')
    glb.setup('tagungen', value=[])
    glb.setup('aktuelleTagung')

def checkLogin():
    """checkLogin - check loginDaten gegen PostgreSQL-DB u.a.
    
        checkLogin checkt die (globalen!) loginDaten
        (glb.PSQL_USER, glb.PSQL_PASSWORD) gegen die
        PostgreSQL-DB. Das dadurch, dass versucht wird, ein DB-Konnektor
        herzustellen. Im Falle des Erfolges wird dieser Konnektor global
        als glb.DB bereitgestellt und True zurück gegeben. Andernfalls
        bleibt glb.DB undefiniert und es wird False zurück gegeben.
        
        Anschließend werden die aktiven Tagungen durchsucht nach solchen,
        auf die der User ausreichend Rechte hat. Diese Tagungen werden
        in glb.tagungen bereitgestellt.
        
        Ergebnis
            True    Erfolgreich DB-Konnektor aufgebaut, d.h. loginDaten
                    sind gültig, und Tagungen gesucht
            False   Sonst
        
        Nebeneffekte
            glb.DB          Gültiger DB-Konnektor des Users
            glb.tagungen    Liste der Tagungen, auf denen der User arbeiten
                            kann und darf.
    """
    #
    # DB-Konnektor herstellen
    try:
        glb.setvalue(
            'DB',
            psycopg2.connect(
                host=glb.PSQL_HOST,
                port=glb.PSQL_PORT,
                dbname=glb.PSQL_DATABASE,
                user=glb.PSQL_USER,
                password=glb.PSQL_PASSWORD)
            )
        logging.info(f'Login erfolgreich als {glb.PSQL_USER}')
    except:
        logging.info(f'Login fehlgeschlagen als {glb.PSQL_USER}')
        return False
    #
    # Aktive Tagungen suchen und filtern nach Rechten, die der Benutzer darauf hat
    # Das Ergebnis speichern wir in glb.Tagungen
    for G in aktive_tagungen():
        schema = G['schema']
        sql = f"select has_schema_privilege ('{schema}', 'USAGE')"
        hasUsage = False
        with glb.DB.cursor() as Cur:
            Cur.execute(sql)
            hasUsage = Cur.fetchone()[0]
            glb.DB.commit()
        if hasUsage:
            glb.tagungen.append(G)
    #
    # Wenn bis hier keine Fehler aufgetreten sind, geben wir die Erolgsmeldung zurück
    return True
