"""Tagung.py - Tagung Adressverwaltung GUI

"""

import logging
from ugbib_werkzeug.bibWerkzeug import log_init
log_init('Tagung')
logger = logging.getLogger()

import os, sys
sys.path.append('/home/ulrich/PythonHobby/bibs/bibtkinter/src/ugbib_tkinter/')

import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
import tkinter.font as tkFont
import tkinter.messagebox as dialog
import tkinter.filedialog as filedialog

from ugbib_divers.bibGlobal import glb
from ugbib_tkinter.bibForm import *

from ugbib_modell.bibModell import setSearchPath

from .Tagung_Def import *
from .Tagung_Modelle import (
    Person, PersonJugend, PersonStatus, PersonFinanzen, PersonFinanzenListe,
    Raum, Veranstaltung,
    DozentListe, RaumbelegungListe,
    Gruppe, GruppeListe, Farbe, Laender, Mailart, Raumart, Veranstaltungart,
    PersonGruppeListe,
    Tagung, Status, StatusListe, Mail,
    AnmWSListe, PersonWSAnmListe, PersonWSListe,
    Jobs, JobsListe
    )
for M in [
        Person, PersonJugend, PersonStatus, PersonFinanzen, PersonFinanzenListe,
        Raum, Veranstaltung,
        DozentListe, RaumbelegungListe,
        Gruppe, GruppeListe, Farbe, Laender, Mailart, Raumart, Veranstaltungart,
        PersonGruppeListe,
        Tagung, Status, StatusListe, Mail,
        AnmWSListe, PersonWSAnmListe, PersonWSListe,
        Jobs, JobsListe
        ]:
    M.Init(M)

class Hauptprogramm(tk.Tk):
    
    def __init__(self):
        super().__init__()
        self.style = ttk.Style()
        glb.icons = TkIcons()
        self.baueMenuBar()
        self.basics()
        self.baueLayout()
        self.baueValidatoren()
        self.baueWidgets()
        self.nbkMain.config(takefocus=False)
        self.disableMainNotebook()
        self.activateLogin()
    
    def basics(self):
        self.title('Tagung Adressverwaltung')
        self.bind_all('<Control-q>', self.handleQuit)
        self.style.theme_use('classic')    # Nur damit wird PanedWindows Trenner sichtbar
        #
        # Schriftgröße
        tkFont.nametofont('TkDefaultFont').configure(size=8)
        tkFont.nametofont('TkTextFont').configure(size=8)
        tkFont.nametofont('TkMenuFont').configure(size=8)
        tkFont.nametofont('TkFixedFont').configure(size=8)
        
        
    def handleQuit(self, event):
        """handleQuit - Beendet das Programm nach HotKey
        
            Ruft einfach nur ende auf.
        """
        self.ende()
    
    def ende(self):
        self.logout(tolerant=True)
        self.quit()
    
    def handleLogin(self):
        glb.PSQL_USER = self.varGlbUser.get()
        glb.PSQL_PASSWORD = self.varGlbPassword.get()
        if checkLogin():
            tagungAuswahl = [(T['schema'], T['kurz_bez'] + ': ' + T['titel']) for T in glb.tagungen]
            self.activateTagung()
            self.cmbGlbTagung.fill(tagungAuswahl)
            notify(f'Erfolgreich angemeldet als: {glb.PSQL_USER}', 'Erfolg')
            notify('Bitte Tagung auswählen', 'Hinweis')
            self.cmbGlbTagung.event_generate('<Down>')
        else:
            self.activateLogin()
    
    def handleLogout(self):
        self.disableMainNotebook()
        self.activateLogin()
        self.logout()
    
    def handleTagungAusgewaehlt(self, event):
        glb.setvalue('schema', self.cmbGlbTagung.getValue())
        for T in glb.tagungen:
            if T['schema'] == glb.schema:
                glb.setvalue('aktuelleTagung', T)
                break
        logger.debug(f'{glb.aktuelleTagung["schema"]}, public')
        if not setSearchPath(f'{glb.aktuelleTagung["schema"]}, public'):
            sys.exit(f'Auswahl der Tagung fehlgeschlagen. Einzelheiten s. Tagung.log.')
        notify('Tagung erfolgreich ausgewählt.', 'Erfolg')
        Form.resetForms()
        self.enableMainNotebook()
    
    def activateLogin(self):
        """activateLogin - Hält den User auf den Login-Feldern
        
            Aktiviert die Login-Widgets und deaktiviert die Gemeinde-Auswahl
        """
        self.entGlbUser['state'] = tk.NORMAL
        self.entGlbUser.focus()
        self.entGlbPassword['state'] = tk.NORMAL
        self.btnGlbLogin.configure(state=tk.NORMAL)
        self.entGlbUser.focus()
        
        self.btnGlbLogout.configure(state=tk.DISABLED)
    
    def activateTagung(self):
        """activateTagung - Hält den User auf der Tagungs-Auswahl
        
            Aktiviert die Tagungs-Auswahl und deaktiviert die Login-Widgets
        """
        self.btnGlbLogout.configure(state=tk.NORMAL)
        self.cmbGlbTagung.focus()
        
        self.entGlbUser.configure(state=tk.DISABLED)
        self.entGlbPassword.config(state=tk.DISABLED)
        self.btnGlbLogin.config(state=tk.DISABLED)

    def baueMenuBar(self):
        #
        # Menu Bar anlegen und zeigen
        top = self.winfo_toplevel()
        self.mnuBar = tk.Menu(top)
        top['menu'] = self.mnuBar
        #
        # Menüs anlegen
        self.mnuDatei = tk.Menu(self.mnuBar, tearoff=0)
        self.mnuDB = tk.Menu(self.mnuDatei, tearoff=0)
        self.mnuHilfe = tk.Menu(self.mnuBar, tearoff=0)
        #
        # Menüs füllen
        #
        # Menü Bar füllen
        self.mnuBar.add_cascade(label='Datei', menu=self.mnuDatei)
        self.mnuBar.add_cascade(label='Hilfe', menu=self.mnuHilfe)
        # Menü Datei füllen
        self.mnuDatei.add_cascade(
            label='Datenbank',
            image=glb.icons.getIcon('database'),
            menu=self.mnuDB)
        self.mnuDatei.add_separator()
        self.mnuDatei.add_command(
            label='Beenden',
            accelerator='Strg-Q',
            image=glb.icons.getIcon('quit'),
            command=lambda : self.ende())
        # Menü DB (Datenbank) füllen
        # Menü Hilfe füllen
        self.mnuHilfe.add_command(
            label='Navi Buttons',
            command=lambda: DialogHilfeNaviButtons(self)
            )
    
    
    def logout(self, tolerant=False):
        """handleMnuLogout - Behandelt Menü Logout Button
        """
        # Falls DB Connector existiert, versuche zu schließen
        try:
            glb.DB.close()
            notify('Verbindung zur DB geschlossen', 'Erfolg')
            logging.info(f'Verbindung zur DB geschlossen.')
            glb.PSQL_PASSWORD = ''
        except Exception as e:
            if not tolerant:
                notify(e, 'Fehler')
                logging.info(f'Fehler beim Logout: {e}')
        # Koptzeile leeren
        self.varGlbDB.set('')
        self.varGlbUser.set('')
        self.varGlbPassword.set('')
        self.varGlbTagung.set('')
        glb.PSQL_PASSWORD = ''
        glb.PSQL_USER = ''
    
    def baueValidatoren(self):
      
        def invalidHoldFocus(widgetName):
            widget = self.nametowidget(widgetName)
            widget.focus_force()
            notify('Wert ungültig', 'Warnung')
        #
        # Validatoren
        self.valDate = self.register(Validator.valDate)
        self.valTime = self.register(Validator.valTime)
        self.valInt = self.register(Validator.valInt)
        #
        # Funktionen für invalidcommand
        self.invalidHoldFocus = self.register(invalidHoldFocus)
    
    def baueWidgets(self):
        #
        # Kopfzeile (Top) - Information über DB-Verbindung
        #
        # Variablen
        self.varGlbDB = tk.StringVar()
        self.varGlbUser = tk.StringVar()
        self.varGlbPassword = tk.StringVar()
        self.varGlbTagung = tk.StringVar()
        
        self.varGlbDB.set(glb.PSQL_DATABASE)
        self.varGlbUser.set(glb.PSQL_USER)
        self.varGlbPassword.set(glb.PSQL_PASSWORD)
        #
        # User, Password, Tagung, Datenbank
        self.lblGlbUser = ttk.Label(self.frmTop, text='Benutzer:')
        self.lblGlbUser.pack(side=tk.LEFT)
        self.entGlbUser = ttk.Entry(
            self.frmTop,
            textvariable=self.varGlbUser)
        Tooltip(self.entGlbUser, 'Username PostgreSQL Datenbank')
        self.entGlbUser.pack(side=tk.LEFT)
        
        self.lblGlbPassword = ttk.Label(self.frmTop, text='Passwort:')
        self.lblGlbPassword.pack(side=tk.LEFT)
        self.entGlbPassword = ttk.Entry(
            self.frmTop,
            textvariable=self.varGlbPassword,
            show='*'
            )
        Tooltip(self.entGlbPassword, 'Passwort PostgreSQL Datenbank')
        self.entGlbPassword.pack(side=tk.LEFT)
        
        self.btnGlbLogin = ButtonWithEnter(
            self.frmTop,
            text='Login',
            image=glb.icons.getIcon('connect'),
            compound=tk.LEFT,
            command=self.handleLogin
            )
        self.btnGlbLogin.pack(side=tk.LEFT)
        
        self.btnGlbLogout = ButtonWithEnter(
            self.frmTop,
            text='Logout',
            image=glb.icons.getIcon('disconnect'),
            compound=tk.LEFT,
            command=self.handleLogout
            )
        self.btnGlbLogout.pack(side=tk.LEFT)
        
        self.lblGlbTagung = ttk.Label(self.frmTop, text='Tagung:')
        self.lblGlbTagung.pack(side=tk.LEFT)
        self.cmbGlbTagung = ComboboxValueLabel(
            self.frmTop,
            textvariable=self.varGlbTagung,
            width=40)
        self.cmbGlbTagung.bind('<<ComboboxSelected>>', self.handleTagungAusgewaehlt, add='+')
        self.cmbGlbTagung.pack(side=tk.LEFT)
        
        self.lblGlbDB = ttk.Label(self.frmTop, text='Datenbank:')
        self.lblGlbDB.pack(side=tk.LEFT)
        self.entGlbDB = ttk.Entry(
            self.frmTop,
            textvariable=self.varGlbDB,
            state=tk.DISABLED)
        self.entGlbDB.pack(side=tk.LEFT)
        #
        # Notify Widget in Fußbereich
        self.wdgNotify = Notify(self.frmBottom)
        self.wdgNotify.pack(expand=tk.YES, fill=tk.BOTH)
        notify('Nachrichten aller Art', 'Hinweis')
        #
        # Personen Jugend Einzelheiten
        with Form() as form:
            glb.formPersJuEinzel = form
            #
            # Navi herstellen und einsetzen
            navi = NaviForm(self.frmPersJuEinzelNavi)
            form.setNavi(navi)
            navi.pack(fill=tk.BOTH, expand=True)
            #
            # Navi konfigurieren
            navi.connectToModell(
                PersonJugend,
                selects=('g_ansprechpartner_id', 'status'),
                keyFeldNavi='id',
                labelFelder=('name', 'vorname', 'id',),
                filterFelder=('name', 'vorname', 'strasse', 'ort',),
                Sort='name, vorname')
            #
            # Unterformulare herstellen und an Navi hängen
            #
            # ... für Gruppen
            def FactoryFormPersJuEinzelGruppe():
                uform = Form()
                #
                # Navi herstellen und einsetzen
                unavi = NaviForm(self.frmPersJuEinzelGruppen, elemente=('save', 'delete'))
                uform.setNavi(unavi)
                #
                # Navi konfigurieren
                unavi.connectToModell(
                    PersonGruppeListe,
                    selects=('gruppe_kurz_bez',))
                #
                # Widgets
                uform.addWidget(
                    'id',
                    ttk.Entry(self.frmPersJuEinzelGruppen, state=tk.DISABLED, width=6),
                    'int',
                    label='ID')
                uform.addWidget(
                    'person_id',
                    ttk.Entry(self.frmPersJuEinzelGruppen, state=tk.DISABLED, width=6),
                    'int',
                    label='P-ID')
                uform.addWidget(
                    'gruppe_kurz_bez',
                    ComboboxValueLabel(self.frmPersJuEinzelGruppen, width=20),
                    'text',
                    label='Gruppe'
                    )
                #
                # Formular zurückgeben
                return uform
            
            FL = FormListeUnterformular(
                self.frmPersJuEinzelGruppen,
                FactoryFormPersJuEinzelGruppe,
                linkFeld='person_id',
                linkFeldHauptformular='id'
                )
            FL.setGetterDicts(PersonGruppeListe().FactoryGetterDicts(
                keyFeld='person_id',
                Sort='gruppe_kurz_bez'))
            FL.setHauptformular(form)
            navi.formListen['gruppen'] = FL
            #
            # Widgets herstellen, zeigen und in Formular aufnehmen
            form.addWidget(
                'id',
                ttk.Entry(self.frmPersJuEinzelDaten, state=tk.DISABLED, width=6),
                'int',
                label='ID')
            form.lbl_id.grid(column=0, row=0, sticky=tk.W)
            form.id.grid(column=0, row=1, sticky=tk.W)
            
            form.addWidget(
                'name',
                ttk.Entry(self.frmPersJuEinzelDaten),
                'text',
                label='Name'
                )
            form.lbl_name.grid(column=0, row=2, sticky=tk.W)
            form.name.grid(column=0, row=3, sticky=tk.W)
            
            form.addWidget(
                'vorname',
                ttk.Entry(self.frmPersJuEinzelDaten),
                'text',
                label='Vorname'
                )
            form.lbl_vorname.grid(column=1, row=2, columnspan=2, sticky=tk.W)
            form.vorname.grid(column=1, row=3, columnspan=2, sticky=tk.W)
            
            form.addWidget(
                'gebdat',
                ttk.Entry(self.frmPersJuEinzelDaten,
                      width=15,
                      validate='focusout',
                      validatecommand=(self.valDate, '%P'),
                      invalidcommand=(self.invalidHoldFocus, '%W')
                      ),
                'date',
                label='Geb.-Dat.'
                )
            form.lbl_gebdat.grid(column=3, row=2, sticky=tk.W)
            form.gebdat.grid(column=3, row=3, sticky=tk.W)
            
            form.addWidget(
                'geschlecht',
                ComboboxValueLabel(self.frmPersJuEinzelDaten, width=20),
                'text',
                label='Geschlecht'
                )
            form.getWidget('geschlecht').fill((
                ('m', 'männlich'),
                ('w', 'weiblich'),
                ('d', 'divers'),
                ('?', 'nicht erfasst')
                ))
            form.lbl_geschlecht.grid(column=4, row=2, sticky=tk.W)
            form.geschlecht.grid(column=4, row=3, sticky=tk.W)
            
            form.addWidget(
                'strasse',
                ttk.Entry(self.frmPersJuEinzelDaten),
                'text',
                label='Straße'
                )
            form.lbl_strasse.grid(column=0, row=4, sticky=tk.W)
            form.strasse.grid(column=0, row=5, sticky=tk.W)
            
            form.addWidget(
                'plz',
                ttk.Entry(self.frmPersJuEinzelDaten, width=6),
                'text',
                label='PLZ'
                )
            form.lbl_plz.grid(column=1, row=4, sticky=tk.W)
            form.plz.grid(column=1, row=5, sticky=tk.W)
            
            form.addWidget(
                'ort',
                ttk.Entry(self.frmPersJuEinzelDaten),
                'text',
                label='Ort'
                )
            form.lbl_ort.grid(column=2, row=4, columnspan=2, sticky=tk.W)
            form.ort.grid(column=2, row=5, columnspan=2, sticky=tk.W)
            
            form.addWidget(
                'land',
                ttk.Entry(self.frmPersJuEinzelDaten),
                'text',
                label='Land'
                )
            form.lbl_land.grid(column=4, row=4, columnspan=2, sticky=tk.W)
            form.land.grid(column=4, row=5, columnspan=2, sticky=tk.W)
            
            form.addWidget(
                'land_kurz',
                ttk.Entry(self.frmPersJuEinzelDaten, state=tk.DISABLED, width=4),
                'text',
                label='kurz'
                )
            form.lbl_land_kurz.grid(column=6, row=4, sticky=tk.W)
            form.land_kurz.grid(column=6, row=5, sticky=tk.W)
            
            form.addWidget(
                'email',
                ttk.Entry(self.frmPersJuEinzelDaten, width=40),
                'text',
                label='eMail'
                )
            form.lbl_email.grid(column=0, row=6, columnspan=2, sticky=tk.W+tk.N)
            form.email.grid(column=0, row=7, columnspan=2, sticky=tk.W+tk.N)
            
            form.addWidget(
                'tel_heimat',
                ttk.Entry(self.frmPersJuEinzelDaten),
                'text',
                label='Tel. Heimat'
                )
            form.lbl_tel_heimat.grid(column=2, row=6, columnspan=2, sticky=tk.W)
            form.tel_heimat.grid(column=2, row=7, columnspan=2, sticky=tk.W)
            
            form.addWidget(
                'tel_mobil',
                ttk.Entry(self.frmPersJuEinzelDaten),
                'text',
                label='Tel. mobil'
                )
            form.lbl_tel_mobil.grid(column=4, row=6, columnspan=2, sticky=tk.W)
            form.tel_mobil.grid(column=4, row=7, columnspan=2, sticky=tk.W)
            
            self.frmPersJuEinzelReisegruppe = ttk.LabelFrame(
                self.frmPersJuEinzelDaten,
                text='Reisegruppe'
                )
            self.frmPersJuEinzelReisegruppe.grid(column=0, row=8, columnspan=6, sticky=tk.W)
            
            form.addWidget(
                'g_ansprechpartner',
                ttk.Checkbutton(self.frmPersJuEinzelReisegruppe),
                'bool',
                label='Gr-Leiter'
                )
            Tooltip(form.g_ansprechpartner, 'Person ist Ansprechpartner für eine Reisegruppe,\nz.B. Konfirmandengruppe')
            form.lbl_g_ansprechpartner.grid(column=0, row=0, sticky=tk.W)
            form.g_ansprechpartner.grid(column=0, row=1, sticky=tk.W)
            
            form.addWidget(
                'g_beschreibung',
                ttk.Entry(self.frmPersJuEinzelReisegruppe, width=50),
                'text',
                label='Beschreibung'
                )
            Tooltip(form.g_beschreibung, 'Z.B. Konfirmandengruppe Hintertupfingen')
            form.lbl_g_beschreibung.grid(column=1, row=0, sticky=tk.W)
            form.g_beschreibung.grid(column=1, row=1, sticky=tk.W)
            
            form.addWidget(
                'g_anzahl',
                ttk.Entry(
                    self.frmPersJuEinzelReisegruppe,
                    width=8,
                    justify='right',
                    validate='key',
                    validatecommand=(self.valInt, '%P')
                    ),
                'int',
                label='Anzahl TN'
                )
            form.lbl_g_anzahl.grid(column=2, row=0, sticky=tk.W)
            form.g_anzahl.grid(column=2, row=1, sticky=tk.W)
            
            form.addWidget(
                'g_ansprechpartner_id',
                ComboboxValueLabel(
                    self.frmPersJuEinzelReisegruppe,
                    noneAllowed=True,
                    filterEnabled=True,
                    width=50),
                'text',
                label=ttk.Label(self.frmPersJuEinzelReisegruppe, text='Gehört zur Gruppe:')
                )
            Tooltip(form.g_ansprechpartner_id, 'Person gehört zu einer Reisegruppe\nvon...')
            form.lbl_g_ansprechpartner_id.grid(column=0, row=2, columnspan=2, sticky=tk.W)
            form.g_ansprechpartner_id.grid(column=0, row=3, columnspan=2, sticky=tk.W)
            
            form.addWidget(
                'sprachen',
                ttk.Entry(self.frmPersJuEinzelDaten),
                'text',
                label='Sprachen'
                )
            Tooltip(form.sprachen, 'Spricht diese Sprachen')
            form.lbl_sprachen.grid(column=0, row=9, sticky=tk.W)
            form.sprachen.grid(column=0, row=10, sticky=tk.W)
            
            form.addWidget(
                'aufgabe',
                ttk.Entry(self.frmPersJuEinzelDaten),
                'text',
                label='Aufgabe'
                )
            Tooltip(form.aufgabe, 'Aufgabe(n) auf der Tagung, z.B. "Di spülen"')
            form.lbl_aufgabe.grid(column=1, row=9, columnspan=2, sticky=tk.W)
            form.aufgabe.grid(column=1, row=10, columnspan=2, sticky=tk.W)
            
            form.addWidget(
                'vegetarier',
                ttk.Checkbutton(self.frmPersJuEinzelDaten),
                'bool',
                label='vegetarisch'
                )
            form.lbl_vegetarier.grid(column=0, row=11, sticky=tk.E)
            form.vegetarier.grid(column=1, row=11, sticky=tk.W)
            
            form.addWidget(
                'vegan',
                ttk.Checkbutton(self.frmPersJuEinzelDaten),
                'bool',
                label='vegan'
                )
            form.lbl_vegan.grid(column=0, row=12, sticky=tk.E)
            form.vegan.grid(column=1, row=12, sticky=tk.W)
            
            form.addWidget(
                'glutenfrei',
                ttk.Checkbutton(self.frmPersJuEinzelDaten),
                'bool',
                label='glutenfrei'
                )
            form.lbl_glutenfrei.grid(column=0, row=13, sticky=tk.E)
            form.glutenfrei.grid(column=1, row=13, sticky=tk.W)
            
            form.addWidget(
                'lactosefrei',
                ttk.Checkbutton(self.frmPersJuEinzelDaten),
                'bool',
                label='lactosefrei'
                )
            form.lbl_lactosefrei.grid(column=0, row=14, sticky=tk.E)
            form.lactosefrei.grid(column=1, row=14, sticky=tk.W)
            
            form.addWidget(
                'ws_a',
                ttk.Entry(self.frmPersJuEinzelDaten, width=8),
                'text',
                label='WS A:'
                )
            form.lbl_ws_a.grid(column=2, row=11, sticky=tk.E)
            form.ws_a.grid(column=3, row=11, sticky=tk.W)
            
            form.addWidget(
                'ws_b',
                ttk.Entry(self.frmPersJuEinzelDaten, width=8),
                'text',
                label='WS B:'
                )
            form.lbl_ws_b.grid(column=2, row=12, sticky=tk.E)
            form.ws_b.grid(column=3, row=12, sticky=tk.W)
            
            form.addWidget(
                'ws_c',
                ttk.Entry(self.frmPersJuEinzelDaten, width=8),
                'text',
                label='WS C:'
                )
            form.lbl_ws_c.grid(column=2, row=13, sticky=tk.E)
            form.ws_c.grid(column=3, row=13, sticky=tk.W)
            
            form.addWidget(
                'ws_d',
                ttk.Entry(self.frmPersJuEinzelDaten, width=8),
                'text',
                label='WS D:'
                )
            form.lbl_ws_d.grid(column=2, row=14, sticky=tk.E)
            form.ws_d.grid(column=3, row=14, sticky=tk.W)
            
            ttk.Label(self.frmPersJuEinzelDaten, text='Beitrag').grid(
                  column=4,
                  row=10,
                  columnspan=2,
                  sticky=tk.E)
            
            form.addWidget(
                'beitr_anm',
                ttk.Entry(
                    self.frmPersJuEinzelDaten,
                    width=6,
                    justify='right',
                    validate='key',
                    validatecommand=(self.valInt, '%P')
                    ),
                'int',
                label='Anm.'
                )
            Tooltip(form.beitr_anm, 'TN-Beitrag, wie bei\nder Anmeldung angegeben')
            form.lbl_beitr_anm.grid(column=4, row=11, sticky=tk.E)
            form.beitr_anm.grid(column=5, row=11, sticky=tk.W)
            
            form.addWidget(
                'beitr_erm',
                ttk.Entry(
                    self.frmPersJuEinzelDaten,
                    width=6,
                    justify='right',
                    validate='key',
                    validatecommand=(self.valInt, '%P')
                    ),
                'int',
                label='Erm.'
                )
            Tooltip(form.beitr_erm, 'Ermäßigter TN-Beitrag,\nwie verabredet.\n1 für vollständigen Nachlass')
            form.lbl_beitr_erm.grid(column=4, row=12, sticky=tk.E)
            form.beitr_erm.grid(column=5, row=12, sticky=tk.W)
            
            form.addWidget(
                'beitr_gez',
                ttk.Entry(
                    self.frmPersJuEinzelDaten,
                    width=6,
                    justify='right',
                    validate='key',
                    validatecommand=(self.valInt, '%P')
                    ),
                'int',
                label='Bez.'
                )
            Tooltip(form.beitr_gez, 'TN-Beitrag, der\ntatsächlich gezahlt\nund schon verbucht wurde')
            form.lbl_beitr_gez.grid(column=4, row=13, sticky=tk.E)
            form.beitr_gez.grid(column=5, row=13, sticky=tk.W)
            
            form.addWidget(
                'beitr_dat',
                ttk.Entry(
                    self.frmPersJuEinzelDaten,
                    width=6,
                    validate='focusout',
                    validatecommand=(self.valDate, '%P'),
                    invalidcommand=(self.invalidHoldFocus, '%W')
                    ),
                'date',
                label='Datum'
                )
            Tooltip(form.beitr_dat, 'Wann der TN-Beitrag\nbezahlt wurde')
            form.lbl_beitr_dat.grid(column=4, row=14, sticky=tk.E)
            form.beitr_dat.grid(column=5, row=14, sticky=tk.W)
            
            form.addWidget(
                'status',
                ComboboxValueLabel(
                    self.frmPersJuEinzelDaten,
                    width=20,
                    state='readonly'
                    ),
                'text',
                label='Status'
                )
            Tooltip(form.status, 'Anmelde-Status')
            form.lbl_status.grid(column=0, row=15, sticky=tk.W)
            form.status.grid(column=0, row=16, sticky=tk.W)
            
            form.addWidget(
                'status_gesetzt_am',
                ttk.Entry(self.frmPersJuEinzelDaten, width=15, state=tk.DISABLED),
                'date',
                label='... gesetzt am'
                )
            form.status_gesetzt_am.grid(column=0, row=17, sticky=tk.W)
            
            form.addWidget(
                'anm_am_um',
                ttk.Entry(self.frmPersJuEinzelDaten, width=20, state=tk.DISABLED),
                'datetime',
                label='Anm. am/um'
                )
            form.lbl_anm_am_um.grid(column=0, row=18, sticky=tk.W)
            form.anm_am_um.grid(column=0, row=19, sticky=tk.W)
            
            form.addWidget(
                'nachricht',
                scrolledtext.ScrolledText(self.frmPersJuEinzelDaten, width=35, height=6),
                'text',
                label=ttk.Label(self.frmPersJuEinzelDaten, text='Nachricht')
                )
            Tooltip(form.nachricht, 'Nachricht des TN\naus der Online-Anmeldung')
            form.lbl_nachricht.grid(column=1, row=15, columnspan=3, sticky=tk.W)
            form.nachricht.grid(column=1, row=16, columnspan=3, rowspan=4, sticky=tk.W)
            
            form.addWidget(
                'bemerkung',
                scrolledtext.ScrolledText(self.frmPersJuEinzelDaten, width=35, height=6),
                'text',
                label=ttk.Label(self.frmPersJuEinzelDaten, text='Bemerkung')
                )
            Tooltip(form.bemerkung, 'Bemerkung(en) des TB')
            form.lbl_bemerkung.grid(column=4, row=15, columnspan=3, sticky=tk.W)
            form.bemerkung.grid(column=4, row=16, columnspan=3, rowspan=4, sticky=tk.W)
            
            bearbVonAm = BearbVonAm(self.frmPersJuEinzelDaten)
            bearbVonAm.grid(column=0, row=20, columnspan=3, sticky=tk.W)
            bearbVonAm.connectToForm(form)
        #
        # Personen Anmeldestatus
        def FactoryPersonStatusListe():
            form = Form()
            #
            # Navi herstellen und einsetzen
            navi = NaviForm(self.frmPersonenStatusListeInhalt.innerFrame, elemente=('save', 'delete'))
            form.setNavi(navi)
            #
            # Navi konfigurieren
            navi.connectToModell(
                PersonStatus,
                selects=('status',))
            #
            # Widgets
            form.addWidget(
                'id',
                ttk.Entry(
                    self.frmPersonenStatusListeInhalt.innerFrame,
                    state=tk.DISABLED,
                    width=6),
                'int',
                label='ID')
            form.addWidget(
                'status',
                ComboboxValueLabel(
                    self.frmPersonenStatusListeInhalt.innerFrame,
                    width=10),
                'text',
                label='Status')
            form.addWidget(
                'name',
                ttk.Entry(
                    self.frmPersonenStatusListeInhalt.innerFrame,
                    state=tk.DISABLED,
                    width=12),
                'text',
                label='Name')
            form.addWidget(
                'vorname',
                ttk.Entry(
                    self.frmPersonenStatusListeInhalt.innerFrame,
                    state=tk.DISABLED,
                    width=12),
                'text',
                label='Vorname')
            form.addWidget(
                'gebdat',
                ttk.Entry(
                    self.frmPersonenStatusListeInhalt.innerFrame,
                    state=tk.DISABLED,
                    width=12),
                'date',
                label='Geb.-Dat.')
            form.addWidget(
                'geschlecht',
                ComboboxValueLabel(
                    self.frmPersonenStatusListeInhalt.innerFrame,
                    state=tk.DISABLED,
                    width=12),
                'text',
                label='Geschlecht'
                )
            form.getWidget('geschlecht').fill((
                ('m', 'männlich'),
                ('w', 'weiblich'),
                ('d', 'divers'),
                ('?', 'nicht erfasst')
                ))
            form.addWidget(
                'ort',
                ttk.Entry(
                    self.frmPersonenStatusListeInhalt.innerFrame,
                    stat=tk.DISABLED,
                    width=12),
                'text',
                label='Ort')
            form.addWidget(
                'land',
                ttk.Entry(
                    self.frmPersonenStatusListeInhalt.innerFrame,
                    stat=tk.DISABLED,
                    width=10),
                'text',
                label='Land')
            form.addWidget(
                'email',
                ttk.Entry(
                    self.frmPersonenStatusListeInhalt.innerFrame,
                    stat=tk.DISABLED,
                    width=15),
                'text',
                label='eMail')
            form.addWidget(
                'beitr_anm',
                ttk.Entry(
                    self.frmPersonenStatusListeInhalt.innerFrame,
                    stat=tk.DISABLED,
                    justify='right',
                    width=5),
                'int',
                label='Beitr.')
            form.addWidget(
                'nachricht',
                ttk.Entry(
                    self.frmPersonenStatusListeInhalt.innerFrame,
                    stat=tk.DISABLED,
                    width=15),
                'text',
                label='Nachricht')
            #
            # Formular zurückgeben
            return form
                
        with FormListe(self.frmPersonenStatusListeInhalt.innerFrame, FactoryPersonStatusListe) as form:
            glb.formPersonStatusListe = form
            #
            # Navi herstellen und einsetzen
            navi = NaviListe(self.frmPersonenStatusListeNavi)
            form.setNavi(navi)
            #
            # Navi konfigurieren
            P = PersonStatus()
            navi.setGetterDicts(P.FactoryGetterDicts(
                    FilterFelder=('name', 'vorname', 'ort'),
                    Sort='status, name, vorname'))
            #
            # Form Navi packen
            form.getNavi().pack(anchor=tk.W)
        #
        # Personen WS-Anm zuordnen Liste
        def FactoryWSAnmZuordnenListe():
            form = Form()
            #
            # Navi herstellen und einsetzen
            navi = NaviForm(
                self.frmWSAnmZuordnenInhalt.innerFrame,
                elemente=('save', 'delete'))
            form.setNavi(navi)
            #
            # Navi konfigurieren
            navi.connectToModell(AnmWSListe)
            #
            # Widgets
            form.addWidget(
                'id',
                ttk.Entry(self.frmWSAnmZuordnenInhalt.innerFrame,
                    state=tk.DISABLED,
                    justify='right',
                    width=6),
                'int',
                label='ID')
            form.addWidget(
                'tn_id',
                ttk.Entry(self.frmWSAnmZuordnenInhalt.innerFrame,
                    justify='right',
                    width=6),
                'int',
                label='TN-ID')
            form.addWidget(
                'name',
                ttk.Entry(self.frmWSAnmZuordnenInhalt.innerFrame,
                    width=15),
                'text',
                label='Name')
            form.addWidget(
                'vorname',
                ttk.Entry(self.frmWSAnmZuordnenInhalt.innerFrame,
                    width=15),
                'text',
                label='Vorname')
            form.addWidget(
                'email',
                ttk.Entry(self.frmWSAnmZuordnenInhalt.innerFrame,
                    width=25),
                'text',
                label='eMail')
            form.addWidget(
                'ws_a_i',
                ttk.Entry(self.frmWSAnmZuordnenInhalt.innerFrame,
                    width=8),
                'text',
                label='1. Wahl')
            form.addWidget(
                'ws_a_ii',
                ttk.Entry(self.frmWSAnmZuordnenInhalt.innerFrame,
                    width=8),
                'text',
                label='2. Wahl')
            form.addWidget(
                'ws_a_iii',
                ttk.Entry(self.frmWSAnmZuordnenInhalt.innerFrame,
                    width=8),
                'text',
                label='3. Wahl')
            form.addWidget(
                'nachricht',
                ttk.Entry(self.frmWSAnmZuordnenInhalt.innerFrame,
                    width=25),
                'text',
                label='Nachricht')
            #
            # Formular zurückgeben
            return form
        
        with FormListe(self.frmWSAnmZuordnenInhalt.innerFrame, FactoryWSAnmZuordnenListe) as form:
            glb.formWSAnmZuordnen = form
            #
            # Navi herstellen und einsetzen
            navi = NaviListe(self.frmWSAnmZuordnenNavi)
            form.setNavi(navi)
            #
            # Navi konfigurieren
            W = AnmWSListe()
            navi.setGetterDicts(W.FactoryGetterDicts(
                    FilterFelder=('name', 'vorname', 'ort'),
                    Sort='tn_id, name, vorname'))
            #
            # Form Navi packen
            form.getNavi().pack(anchor=tk.W)
        
        def FactoryWSAnmZuordnenPersonen():
            form = Form()
            #
            # Navi herstellen und einsetzen
            navi = NaviForm(
                self.frmWSAnmZuordnenPersInhalt.innerFrame,
                elemente=('refresh',))
            form.setNavi(navi)
            #
            # Navi konfigurieren
            navi.connectToModell(PersonWSAnmListe)
            #
            # Widgets
            form.addWidget(
                'id',
                ttk.Entry(self.frmWSAnmZuordnenPersInhalt.innerFrame,
                    state=tk.DISABLED,
                    justify='right',
                    width=6),
                'int',
                label='ID')
            form.addWidget(
                'name',
                ttk.Entry(self.frmWSAnmZuordnenPersInhalt.innerFrame,
                    state=tk.DISABLED,
                    width=15),
                'text',
                label='Name')
            form.addWidget(
                'vorname',
                ttk.Entry(self.frmWSAnmZuordnenPersInhalt.innerFrame,
                    state=tk.DISABLED,
                    width=15),
                'text',
                label='Vorname')
            form.addWidget(
                'email',
                ttk.Entry(self.frmWSAnmZuordnenPersInhalt.innerFrame,
                    state=tk.DISABLED,
                    width=25),
                'text',
                label='eMail')
            form.addWidget(
                'ort',
                ttk.Entry(self.frmWSAnmZuordnenPersInhalt.innerFrame,
                    state=tk.DISABLED,
                    width=15),
                'text',
                label='Ort')
            #
            # Formular zurückgeben
            return form
        
        with FormListe(self.frmWSAnmZuordnenPersInhalt.innerFrame, FactoryWSAnmZuordnenPersonen) as form:
            glb.formWSAnmPersonen = form
            #
            # Navi herstellen und einsetzen
            navi = NaviListe(self.frmWSAnmZuordnenPersNavi)
            form.setNavi(navi)
            #
            # Navi konfigurieren
            P = PersonWSAnmListe()
            navi.setGetterDicts(P.FactoryGetterDicts(
                    FilterFelder=('name', 'vorname', 'email', 'ort'),
                    Sort='name, vorname'))
            #
            # Form Navi packen
            form.getNavi().pack(anchor=tk.W)
        #
        # Personen WS festlegen
        def FactoryWSFestlegenListe():
            form = Form()
            #
            # Navi herstellen und einsetzen
            navi = NaviForm(
                self.frmWSFestlegenInhalt.innerFrame,
                elemente=('save', 'delete'))
            form.setNavi(navi)
            #
            # Navi konfigurieren
            navi.connectToModell(PersonWSListe)
            #
            # Widgets
            form.addWidget(
                'id',
                ttk.Entry(self.frmWSFestlegenInhalt.innerFrame,
                    state=tk.DISABLED,
                    justify='right',
                    width=6),
                'int',
                label='ID')
            form.addWidget(
                'name',
                ttk.Entry(self.frmWSFestlegenInhalt.innerFrame,
                    width=15),
                'text',
                label='Name')
            form.addWidget(
                'vorname',
                ttk.Entry(self.frmWSFestlegenInhalt.innerFrame,
                    width=15),
                'text',
                label='Vorname')
            form.addWidget(
                'ort',
                ttk.Entry(self.frmWSFestlegenInhalt.innerFrame,
                    width=15),
                'text',
                label='Ort')
            form.addWidget(
                'ws_a',
                ttk.Entry(self.frmWSFestlegenInhalt.innerFrame,
                    width=8),
                'text',
                label='WS A')
            form.addWidget(
                'ws_b',
                ttk.Entry(self.frmWSFestlegenInhalt.innerFrame,
                    width=8),
                'text',
                label='WS B')
            form.addWidget(
                'ws_c',
                ttk.Entry(self.frmWSFestlegenInhalt.innerFrame,
                    width=8),
                'text',
                label='WS C')
            form.addWidget(
                'ws_d',
                ttk.Entry(self.frmWSFestlegenInhalt.innerFrame,
                    width=8),
                'text',
                label='WS D')
            #
            # Formular zurückgeben
            return form
        
        with FormListe(self.frmWSFestlegenInhalt.innerFrame, FactoryWSFestlegenListe) as form:
            glb.formWSFestlegen = form
            #
            # Navi herstellen und einsetzen
            navi = NaviListe(self.frmWSFestlegenNavi)
            form.setNavi(navi)
            #
            # Navi konfigurieren
            P = PersonWSListe()
            navi.setGetterDicts(P.FactoryGetterDicts(
                    FilterFelder=('name', 'vorname', 'ort'),
                    Sort='name, vorname, ort'))
            #
            # Form Navi packen
            form.getNavi().pack(anchor=tk.W)
        #
        # Personen Finanzen Einzelheiten
        with Form() as form:
            glb.formPersFinanzenEinzel = form
            #
            # Navi herstellen und einsetzen
            navi = NaviForm(self.frmPersFinanzEinzelNavi)
            form.setNavi(navi)
            navi.pack(fill=tk.BOTH, expand=True)
            #
            # Navi konfigurieren
            navi.connectToModell(
                PersonFinanzen,
                selects=('status',),
                keyFeldNavi='id',
                labelFelder=('name', 'vorname', 'id',),
                filterFelder=('name', 'vorname', 'ort',),
                Sort='name, vorname')
            #
            # Widgets herstellen, zeigen und in Formular aufnehmen
            form.addWidget(
                'id',
                ttk.Entry(self.frmPersFinanzEinzelDaten, state=tk.DISABLED, width=6),
                'int',
                label='ID')
            form.lbl_id.grid(column=0, row=0, sticky=tk.W)
            form.id.grid(column=0, row=1, sticky=tk.W)
            
            form.addWidget(
                'name',
                ttk.Entry(self.frmPersFinanzEinzelDaten, state=tk.DISABLED),
                'text',
                label='Name'
                )
            form.lbl_name.grid(column=0, row=2, sticky=tk.W)
            form.name.grid(column=0, row=3, sticky=tk.W)
            
            form.addWidget(
                'vorname',
                ttk.Entry(self.frmPersFinanzEinzelDaten, state=tk.DISABLED),
                'text',
                label='Vorname'
                )
            form.lbl_vorname.grid(column=1, row=2, sticky=tk.W)
            form.vorname.grid(column=1, row=3, sticky=tk.W)
            
            form.addWidget(
                'ort',
                ttk.Entry(self.frmPersFinanzEinzelDaten, state=tk.DISABLED),
                'text',
                label='Ort'
                )
            form.lbl_ort.grid(column=0, row=4, sticky=tk.W)
            form.ort.grid(column=0, row=5, sticky=tk.W)
            
            form.addWidget(
                'land_kurz',
                ttk.Entry(self.frmPersFinanzEinzelDaten, state=tk.DISABLED, width=4),
                'text',
                label='kurz'
                )
            form.lbl_land_kurz.grid(column=1, row=4, sticky=tk.W)
            form.land_kurz.grid(column=1, row=5, sticky=tk.W)
            
            form.addWidget(
                'email',
                ttk.Entry(self.frmPersFinanzEinzelDaten, state=tk.DISABLED, width=40),
                'text',
                label='eMail'
                )
            form.lbl_email.grid(column=0, row=6, columnspan=2, sticky=tk.W+tk.N)
            form.email.grid(column=0, row=7, columnspan=2, sticky=tk.W+tk.N)
            
            ttk.Label(self.frmPersFinanzEinzelDaten, text='TN-Beitrag').grid(
                column=2,
                row=2,
                columnspan=2,
                sticky=tk.W)
            
            form.addWidget(
                'beitr_anm',
                ttk.Entry(
                    self.frmPersFinanzEinzelDaten,
                    state=tk.DISABLED,
                    width=6,
                    justify='right',
                    validate='key',
                    validatecommand=(self.valInt, '%P')
                    ),
                'int',
                label='Bei Anm.:'
                )
            form.lbl_beitr_anm.grid(column=2, row=3, sticky=tk.E)
            form.beitr_anm.grid(column=3, row=3, sticky=tk.W)
            
            form.addWidget(
                'beitr_erm',
                ttk.Entry(
                    self.frmPersFinanzEinzelDaten,
                    width=6,
                    justify='right',
                    validate='key',
                    validatecommand=(self.valInt, '%P')
                    ),
                'int',
                label='Ermäßigt:'
                )
            form.lbl_beitr_erm.grid(column=2, row=4, sticky=tk.E)
            form.beitr_erm.grid(column=3, row=4, sticky=tk.W)
            
            form.addWidget(
                'beitr_gez',
                ttk.Entry(
                    self.frmPersFinanzEinzelDaten,
                    width=6,
                    justify='right',
                    validate='key',
                    validatecommand=(self.valInt, '%P')
                    ),
                'int',
                label='Gezahlt:'
                )
            form.lbl_beitr_gez.grid(column=2, row=5, sticky=tk.E)
            form.beitr_gez.grid(column=3, row=5, sticky=tk.W)
            
            form.addWidget(
                'beitr_dat',
                ttk.Entry(
                    self.frmPersFinanzEinzelDaten,
                    width=8,
                    validate='focusout',
                    validatecommand=(self.valDate, '%P'),
                    invalidcommand=(self.invalidHoldFocus, '%W')
                    ),
                'date',
                label='am:'
                )
            form.lbl_beitr_dat.grid(column=2, row=6, sticky=tk.E)
            form.beitr_dat.grid(column=3, row=6, sticky=tk.W)
            
            form.addWidget(
                'status',
                ComboboxValueLabel(
                    self.frmPersFinanzEinzelDaten,
                    state=tk.DISABLED,
                    width=20
                    ),
                'text',
                label='Status'
                )
            form.lbl_status.grid(column=0, row=8, sticky=tk.W)
            form.status.grid(column=0, row=9, sticky=tk.W)
            
            form.addWidget(
                'bemerkung',
                scrolledtext.ScrolledText(self.frmPersFinanzEinzelDaten, width=35, height=6),
                'text',
                label=ttk.Label(self.frmPersFinanzEinzelDaten, text='Bemerkung')
                )
            form.lbl_bemerkung.grid(column=0, row=10, columnspan=4, sticky=tk.W)
            form.bemerkung.grid(column=0, row=11, columnspan=4, sticky=tk.W)
            
            bearbVonAm = BearbVonAm(self.frmPersFinanzEinzelDaten)
            bearbVonAm.grid(column=0, row=12, columnspan=4, sticky=tk.W)
            bearbVonAm.connectToForm(form)
        #
        # Personen Finanzen als Liste
        def FactoryPersonenFinanzenListe():
            form = Form()
            #
            # Navi herstellen und einsetzen
            navi = NaviForm(
                self.frmPersFinanzListeInhalt.innerFrame,
                elemente=('save', 'delete'))
            form.setNavi(navi)
            #
            # Navi konfigurieren
            navi.connectToModell(
                PersonFinanzenListe,
                selects=('status',))
            #
            # Widgets
            form.addWidget(
                'id',
                ttk.Entry(self.frmPersFinanzListeInhalt.innerFrame,
                    state=tk.DISABLED,
                    width=6),
                'int',
                label='ID')
            form.addWidget(
                'name',
                ttk.Entry(
                    self.frmPersFinanzListeInhalt.innerFrame,
                    width=15,
                    state=tk.DISABLED),
                'text',
                label='Name')
            form.addWidget(
                'vorname',
                ttk.Entry(
                    self.frmPersFinanzListeInhalt.innerFrame,
                    width=15,
                    state=tk.DISABLED),
                'text',
                label='Vorname')
            form.addWidget(
                'ort',
                ttk.Entry(
                    self.frmPersFinanzListeInhalt.innerFrame,
                    width=15,
                    state=tk.DISABLED),
                'text',
                label='Ort')
            form.addWidget(
                'status',
                ComboboxValueLabel(
                    self.frmPersFinanzListeInhalt.innerFrame,
                    state=tk.DISABLED,
                    width=15),
                'text',
                label='Status')
            form.addWidget(
                'beitr_anm',
                ttk.Entry(
                    self.frmPersFinanzListeInhalt.innerFrame,
                    state=tk.DISABLED,
                    width=5,
                    justify='right'),
                'int',
                label='B Anm')
            form.addWidget(
                'beitr_erm',
                ttk.Entry(
                    self.frmPersFinanzListeInhalt.innerFrame,
                    validate='key',
                    validatecommand=(self.valInt, '%P'),
                    width=5,
                    justify='right'),
                'int',
                label='B Erm')
            form.addWidget(
                'beitr_gez',
                ttk.Entry(
                    self.frmPersFinanzListeInhalt.innerFrame,
                    validate='key',
                    validatecommand=(self.valInt, '%P'),
                    width=5,
                    justify='right'),
                'int',
                label='B Gez')
            form.addWidget(
                'beitr_dat',
                ttk.Entry(
                    self.frmPersFinanzListeInhalt.innerFrame,
                    width=12,
                    validate='focusout',
                    validatecommand=(self.valDate, '%P'),
                    invalidcommand=(self.invalidHoldFocus, '%W')
                    ),
                'date',
                label='B Dat'
                )
            form.addWidget(
                'bemerkung',
                scrolledtext.ScrolledText(
                    self.frmPersFinanzListeInhalt.innerFrame,
                    width=20,
                    height=2),
                'text',
                label=ttk.Label(self.frmPersFinanzListeInhalt.innerFrame, text='Bemerkung'))
            #
            # Formular zurückgeben
            return form
                
        with FormListe(self.frmPersFinanzListeInhalt.innerFrame, FactoryPersonenFinanzenListe) as form:
            glb.formPersonenFinanzenListe = form
            #
            # Navi herstellen und einsetzen
            navi = NaviListe(self.frmPersFinanzListeNavi)
            form.setNavi(navi)
            #
            # Navi konfigurieren
            P = PersonFinanzenListe()
            navi.setGetterDicts(P.FactoryGetterDicts(
                    FilterFelder=('name', 'vorname', 'ort'),
                    Sort='beitr_gez, name, vorname, id'))
            #
            # Form Navi packen
            form.getNavi().pack(anchor=tk.W)
        #
        # Veranstaltungen Einzelheiten
        with Form() as form:
            glb.formVAEinzelheiten = form
            #
            # Navi herstellen und einsetzen
            navi = NaviForm(self.frmVAEinzelNavi)
            form.setNavi(navi)
            navi.pack(fill=tk.BOTH, expand=True)
            #
            # Navi konfigurieren
            navi.connectToModell(
                Veranstaltung,
                selects=('art',),
                keyFeldNavi='id',
                labelFelder=('art', 'nr', 'titel'),
                filterFelder=('art', 'titel', 'untertitel'),
                Sort='art, nr')
            #
            # Unterformulare herstellen und an Navi hängen
            #
            # ... für Dozenten
            def FactoryFormVAEinzelDozent():
                uform = Form()
                #
                # Navi herstellen und einsetzen
                unavi = NaviForm(self.frmVAEinzelDozenten, elemente=('save', 'delete'))
                uform.setNavi(unavi)
                #
                # Navi konfigurieren
                unavi.connectToModell(
                    DozentListe,
                    selects=('person_id',))
                #
                # Widgets
                uform.addWidget(
                    'id',
                    ttk.Entry(self.frmVAEinzelDozenten, state=tk.DISABLED, width=4),
                    'int',
                    label='ID')
                uform.addWidget(
                    'veranstaltung_id',
                    ttk.Entry(self.frmVAEinzelDozenten, state=tk.DISABLED, width=5),
                    'int',
                    label='VA-ID')
                uform.addWidget(
                    'person_id',
                    ComboboxValueLabel(
                        self.frmVAEinzelDozenten,
                        width=20,
                        filterEnabled=True),
                    'int',
                    label='Person')
                uform.addWidget(
                    'funktion',
                    ttk.Entry(self.frmVAEinzelDozenten, width=15),
                    'text',
                    label='Funktion')
                #
                # Formular zurückgeben
                return uform
            
            FL = FormListeUnterformular(
                self.frmVAEinzelDozenten,
                FactoryFormVAEinzelDozent,
                linkFeld='veranstaltung_id',
                linkFeldHauptformular='id')
            FL.setGetterDicts(DozentListe().FactoryGetterDicts(
                keyFeld='veranstaltung_id'))
            FL.setHauptformular(form)
            navi.formListen['dozenten'] = FL
            #
            # ... für Raumbelegung
            def FactoryFormVAEinzelRaum():
                uform = Form()
                #
                # Navi herstellen und einsetzen
                unavi = NaviForm(self.frmVAEinzelRaum, elemente=('save', 'delete'))
                uform.setNavi(unavi)
                #
                # Navi konfigurieren
                unavi.connectToModell(
                    RaumbelegungListe,
                    selects=('raum_kurz_bez',))
                #
                # Widgets
                uform.addWidget(
                    'id',
                    ttk.Entry(self.frmVAEinzelRaum, state=tk.DISABLED, width=6),
                    'int',
                    label='ID')
                uform.addWidget(
                    'veranstaltung_id',
                    ttk.Entry(self.frmVAEinzelRaum, state=tk.DISABLED, width=6),
                    'int',
                    label='VA-ID')
                uform.addWidget(
                    'raum_kurz_bez',
                    ComboboxValueLabel(
                        self.frmVAEinzelRaum,
                        width=10),
                    'text',
                    label='Kurz-Bez.')
                uform.addWidget(
                    'datum',
                    ttk.Entry(
                        self.frmVAEinzelRaum,
                        width=10,
                        validate='focusout',
                        validatecommand=(self.valDate, '%P'),
                        invalidcommand=(self.invalidHoldFocus, '%W')
                        ),
                    'date',
                    label='Datum')
                uform.addWidget(
                    'zeit_von',
                    ttk.Entry(
                        self.frmVAEinzelRaum,
                        width=5,
                        justify='right',
                        validate='focusout',
                        validatecommand=(self.valTime, '%P'),
                        invalidcommand=(self.invalidHoldFocus, '%W')
                        ),
                    'time',
                    label='Start')
                uform.addWidget(
                    'zeit_bis',
                    ttk.Entry(
                        self.frmVAEinzelRaum,
                        width=5,
                        justify='right',
                        validate='focusout',
                        validatecommand=(self.valTime, '%P'),
                        invalidcommand=(self.invalidHoldFocus, '%W')
                        ),
                    'time',
                    label='Ende')
                #
                # Formualr zurückgeben
                return uform
            
            FL = FormListeUnterformular(
                self.frmVAEinzelRaum,
                FactoryFormVAEinzelRaum,
                linkFeld='veranstaltung_id',
                linkFeldHauptformular='id')
            FL.setGetterDicts(RaumbelegungListe().FactoryGetterDicts(
                keyFeld='veranstaltung_id'))
            FL.setHauptformular(form)
            navi.formListen['raumbelegung'] = FL
                
            #
            # Widgets
            form.addWidget(
                'id',
                ttk.Entry(self.frmVAEinzelDaten, state=tk.DISABLED),
                'int',
                label='ID')
            form.lbl_id.grid(column=0, row=0, sticky=tk.E)
            form.id.grid(column=0, row=1, sticky=tk.W)
            
            form.addWidget(
                'art',
                ComboboxValueLabel(
                    self.frmVAEinzelDaten,
                    width=25),
                'text',
                label='Art')
            form.lbl_art.grid(column=0, row=10, sticky=tk.W)
            form.art.grid(column=0, row=11, sticky=tk.W)
            
            form.addWidget(
                'nr',
                ttk.Entry(self.frmVAEinzelDaten, width=6),
                'text',
                label='Nr')
            form.lbl_nr.grid(column=1, row=10, sticky=tk.W)
            form.nr.grid(column=1, row=11, sticky=tk.W)
            
            ttk.Label(self.frmVAEinzelDaten, text='TN').grid(column=2, row=11, sticky=tk.W)
            form.addWidget(
                'tn_min',
                ttk.Entry(
                    self.frmVAEinzelDaten,
                    width=6,
                    justify='right',
                    validate='key',
                    validatecommand=(self.valInt, '%P')
                    ),
                'int',
                label='min')
            form.lbl_tn_min.grid(column=2, row=20, sticky=tk.W)
            form.tn_min.grid(column=2, row=21, sticky=tk.W)
            
            form.addWidget(
                'tn_max',
                ttk.Entry(
                    self.frmVAEinzelDaten,
                    width=6,
                    justify='right',
                    validate='key',
                    validatecommand=(self.valInt, '%P')
                    ),
                'int',
                label='max')
            form.lbl_tn_max.grid(column=3, row=20, sticky=tk.W)
            form.tn_max.grid(column=3, row=21, sticky=tk.W)
            
            ttk.Label(self.frmVAEinzelDaten, text='Alter').grid(column=4, row=11, sticky=tk.W)
            form.addWidget(
                'alter_min',
                ttk.Entry(
                    self.frmVAEinzelDaten,
                    width=6,
                    justify='right',
                    validate='key',
                    validatecommand=(self.valInt, '%P')
                    ),
                'int',
                label='min')
            form.lbl_alter_min.grid(column=4, row=20, sticky=tk.W)
            form.alter_min.grid(column=4, row=21, sticky=tk.W)
            
            form.addWidget(
                'alter_max',
                ttk.Entry(
                    self.frmVAEinzelDaten,
                    width=6,
                    justify='right',
                    validate='key',
                    validatecommand=(self.valInt, '%P')
                    ),
                'int',
                label='max')
            form.lbl_alter_max.grid(column=5, row=20, sticky=tk.W)
            form.alter_max.grid(column=5, row=21, sticky=tk.W)
            
            form.addWidget(
                'titel',
                ttk.Entry(self.frmVAEinzelDaten, width=40),
                'text',
                label='Titel')
            form.lbl_titel.grid(column=0, row=20, columnspan=2, sticky=tk.W)
            form.titel.grid(column=0, row=21, columnspan=2, sticky=tk.W)
            
            form.addWidget(
                'untertitel',
                ttk.Entry(self.frmVAEinzelDaten, width=40),
                'text',
                label='Untertitel')
            form.lbl_untertitel.grid(column=0, row=30, columnspan=2, sticky=tk.W)
            form.untertitel.grid(column=0, row=31, columnspan=2, sticky=tk.W)
            
            form.addWidget(
                'sprachen',
                ttk.Entry(self.frmVAEinzelDaten),
                'text',
                label='Sprachen')
            form.lbl_sprachen.grid(column=2, row=30, columnspan=4, sticky=tk.W)
            form.sprachen.grid(column=2, row=31, columnspan=4, sticky=tk.W)
            
            form.addWidget(
                'beschreibung',
                scrolledtext.ScrolledText(self.frmVAEinzelDaten, width=40, height=6),
                'text',
                label=ttk.Label(self.frmVAEinzelDaten, text='Beschreibung'))
            form.lbl_beschreibung.grid(column=0, row=40, columnspan=2, sticky=tk.W)
            form.beschreibung.grid(column=0, row=41, columnspan=2, sticky=tk.W)
            
            form.addWidget(
                'bedingungen',
                scrolledtext.ScrolledText(self.frmVAEinzelDaten, width=40, height=6),
                'text',
                label=ttk.Label(self.frmVAEinzelDaten, text='Bedingungen'))
            form.lbl_bedingungen.grid(column=2, row=40, columnspan=4, sticky=tk.W)
            form.bedingungen.grid(column=2, row=41, columnspan=4, sticky=tk.W)
            
            form.addWidget(
                'anmeldepflicht',
                ttk.Checkbutton(self.frmVAEinzelDaten),
                'bool',
                label='Anm.-Pflicht')
            form.lbl_anmeldepflicht.grid(column=0, row=50, sticky=tk.W)
            form.anmeldepflicht.grid(column=0, row=51, sticky=tk.W)
            
            form.addWidget(
                'honorar',
                ttk.Entry(
                    self.frmVAEinzelDaten,
                    width=6,
                    justify='right',
                    validate='key',
                    validatecommand=(self.valInt, '%P')
                    ),
                'int',
                label='Honorar')
            form.lbl_honorar.grid(column=2, row=50, columnspan=2, sticky=tk.W)
            form.honorar.grid(column=2, row=51, columnspan=2, sticky=tk.W)
            
            form.addWidget(
                'sachkosten',
                ttk.Entry(
                    self.frmVAEinzelDaten,
                    width=6,
                    justify='right',
                    validate='key',
                    validatecommand=(self.valInt, '%P')
                    ),
                'int',
                label='Sachkosten')
            form.lbl_sachkosten.grid(column=4, row=50, columnspan=2, sticky=tk.W)
            form.sachkosten.grid(column=4, row=51, columnspan=2, sticky=tk.W)
            
            form.addWidget(
                'bemerkung',
                scrolledtext.ScrolledText(self.frmVAEinzelDaten, width=60, height=6),
                'text',
                label=ttk.Label(self.frmVAEinzelDaten, text='Bemerkung'))
            form.lbl_bemerkung.grid(column=0, row=60, columnspan=6, sticky=tk.W)
            form.bemerkung.grid(column=0, row=61, columnspan=6, sticky=tk.W)
            
            bearbVonAm = BearbVonAm(self.frmVAEinzelDaten)
            bearbVonAm.grid(column=0, row=70, columnspan=6, sticky=tk.W)
            bearbVonAm.connectToForm(form)
            
        #
        # Räume Einzelheiten
        with Form() as form:
            glb.formRaumEinzelheiten = form
            #
            # Navi herstellen und einsetzen
            navi = NaviForm(self.frmRaumEinzelNavi)
            form.setNavi(navi)
            navi.pack(fill=tk.BOTH, expand=True)
            #
            # Navi konfigurieren
            navi.connectToModell(
                Raum,
                selects=('art',),
                keyFeldNavi='id',
                labelFelder=('kurz_bez', 'bezeichnung'),
                filterFelder=('kurz_bez', 'bezeichnung', 'art'),
                Sort='kurz_bez')
            #
            # Unterformulare herstellen und an Navi hängen
            #
            # ... für Raumbelegung
            def FactoryFormRaumEinzelBelegung():
                uform = Form()
                #
                # Navi herstellen und einsetzen
                unavi = NaviForm(self.frmRaumEinzelBelegung, elemente=('save', 'delete'))
                uform.setNavi(unavi)
                #
                # Navi konfigurieren
                unavi.connectToModell(
                    RaumbelegungListe,
                    selects=('veranstaltung_id',))
                #
                # Widgets
                uform.addWidget(
                    'id',
                    ttk.Entry(self.frmRaumEinzelBelegung, state=tk.DISABLED, width=6),
                    'int',
                    label='ID')
                uform.addWidget(
                    'raum_kurz_bez',
                    ttk.Entry(
                        self.frmRaumEinzelBelegung,
                        state=tk.DISABLED,
                        width=10),
                    'text',
                    label='Raum')
                uform.addWidget(
                    'veranstaltung_id',
                    ComboboxValueLabel(
                        self.frmRaumEinzelBelegung,
                        filterEnabled=True,
                        width=20),
                    'int',
                    label='VA')
                uform.addWidget(
                    'datum',
                    ttk.Entry(
                        self.frmRaumEinzelBelegung,
                        width=10,
                        validate='focusout',
                        validatecommand=(self.valDate, '%P'),
                        invalidcommand=(self.invalidHoldFocus, '%W')
                        ),
                    'date',
                    label='Datum')
                uform.addWidget(
                    'zeit_von',
                    ttk.Entry(
                        self.frmRaumEinzelBelegung,
                        width=5,
                        justify='right',
                        validate='focusout',
                        validatecommand=(self.valTime, '%P'),
                        invalidcommand=(self.invalidHoldFocus, '%W')
                        ),
                    'time',
                    label='Start')
                uform.addWidget(
                    'zeit_bis',
                    ttk.Entry(
                        self.frmRaumEinzelBelegung,
                        width=5,
                        justify='right',
                        validate='focusout',
                        validatecommand=(self.valTime, '%P'),
                        invalidcommand=(self.invalidHoldFocus, '%W')
                        ),
                    'time',
                    label='Ende')
                #
                # Formualr zurückgeben
                return uform
            
            FL = FormListeUnterformular(
                self.frmRaumEinzelBelegung,
                FactoryFormRaumEinzelBelegung,
                linkFeld='raum_kurz_bez',
                linkFeldHauptformular='kurz_bez')
            FL.setGetterDicts(RaumbelegungListe().FactoryGetterDicts(
                keyFeld='raum_kurz_bez'))
            FL.setHauptformular(form)
            navi.formListen['belegung'] = FL
            #
            # Widgets
            form.addWidget(
                'id',
                ttk.Entry(self.frmRaumEinzelDaten, justify='right', width=6, state=tk.DISABLED),
                'int',
                label='ID')
            form.lbl_id.grid(column=0, row=0, sticky=tk.W)
            form.id.grid(column=0, row=1, sticky=tk.W)
            
            form.addWidget(
                'kurz_bez',
                ttk.Entry(self.frmRaumEinzelDaten, width=10),
                'text',
                label='Kurz')
            Tooltip(form.kurz_bez, 'Tagungsinterne Kurz-Bezeichnung,\nsollte "sprechend" sein.')
            form.lbl_kurz_bez.grid(column= 0, row=10, sticky=tk.W)
            form.kurz_bez.grid(column=0, row=11, sticky=tk.W)
            
            form.addWidget(
                'bezeichnung',
                ttk.Entry(self.frmRaumEinzelDaten, width=30),
                'text',
                label='Bezeichnung')
            Tooltip(form.bezeichnung, 'Bezeichnung, Originalnutzung\nz.B. "Klasse 4b"')
            form.lbl_bezeichnung.grid(column=1, row=10, columnspan=2, sticky=tk.W)
            form.bezeichnung.grid(column=1, row=11, columnspan=2, sticky=tk.W)
            
            form.addWidget(
                'art',
                ComboboxValueLabel(
                    self.frmRaumEinzelDaten,
                    filterEnabled=True,
                    width=15),
                'text',
                label='Art')
            form.lbl_art.grid(column=3, row=10, sticky=tk.W)
            form.art.grid(column=3, row=11, sticky=tk.W)
            
            form.addWidget(
                'plaetze_normal',
                ttk.Entry(
                    self.frmRaumEinzelDaten,
                    width=6,
                    justify='right',
                    validate='key',
                    validatecommand=(self.valInt, '%P')),
                'int',
                label='Plätze')
            Tooltip(form.plaetze_normal, 'Plätze bei normaler Bestuhlung')
            form.lbl_plaetze_normal.grid(column=0, row=20, sticky=tk.W)
            form.plaetze_normal.grid(column=0, row=21, sticky=tk.W)
            
            form.addWidget(
                'moebel_variabel',
                ttk.Checkbutton(self.frmRaumEinzelDaten),
                'bool',
                label='variabel')
            Tooltip(form.moebel_variabel, 'Möbel größtenteils beweglich')
            form.lbl_moebel_variabel.grid(column=1, row=20, sticky=tk.W)
            form.moebel_variabel.grid(column=1, row=21, sticky=tk.W)
            
            form.addWidget(
                'qm',
                ttk.Entry(
                    self.frmRaumEinzelDaten,
                    width=6,
                    justify='right',
                    validate='key',
                    validatecommand=(self.valInt, '%P')),
                'int',
                label='Fläche')
            Tooltip(form.qm, 'Fläche in qm')
            form.lbl_qm.grid(column=2, row=20, sticky=tk.W)
            form.qm.grid(column=2, row=21, sticky=tk.W)
            
            form.addWidget(
                'deaktiviert',
                ttk.Checkbutton(self.frmRaumEinzelDaten),
                'bool',
                label='deaktiviert')
            Tooltip(form.deaktiviert, 'Der Raum ist zwar erfasst,\nsoll aber nicht in\nAuswertungen vorkommen.\nSinnvoll v.a. für\nspätere Deaktivierungen.')
            form.lbl_deaktiviert.grid(column=3, row=20, sticky=tk.W)
            form.deaktiviert.grid(column=3, row=21, sticky=tk.W)
            
            form.addWidget(
                'beschreibung',
                scrolledtext.ScrolledText(self.frmRaumEinzelDaten, width=50, height=6),
                'text',
                label=ttk.Label(self.frmRaumEinzelDaten, text='Beschreibung'))
            form.lbl_beschreibung.grid(column=0, row=30, columnspan=4, sticky=tk.W)
            form.beschreibung.grid(column=0, row=31, columnspan=4, sticky=tk.W)
            
            form.addWidget(
                'bemerkung',
                scrolledtext.ScrolledText(self.frmRaumEinzelDaten, width=50, height=6),
                'text',
                label=ttk.Label(self.frmRaumEinzelDaten, text='Bemerkung'))
            form.lbl_bemerkung.grid(column=0, row=40, columnspan=4, sticky=tk.W)
            form.bemerkung.grid(column=0, row=41, columnspan=4, sticky=tk.W)
            
            bearbVonAm = BearbVonAm(self.frmRaumEinzelDaten)
            bearbVonAm.grid(column=0, row=50, columnspan=4, sticky=tk.W)
            bearbVonAm.connectToForm(form)
            
        #
        # Gruppen
        with Form() as form:
            glb.formGruppen = form
            #
            # Navi herstellen und einsetzen
            navi = NaviForm(self.frmGrpNavi)
            form.setNavi(navi)
            navi.pack(fill=tk.BOTH, expand=True)
            #
            # Navi konfigurieren
            navi.connectToModell(
                Gruppe,
                selects=('farbe',),
                keyFeldNavi='id',
                labelFelder=('kurz_bez', 'bez'),
                filterFelder=('kurz_bez', 'bez'),
                Sort='kurz_bez')
            #
            # Widgets herstellen, zeigen und in Formular aufnehmen
            form.addWidget(
                'id',
                ttk.Entry(self.frmGrpDaten, state=tk.DISABLED),
                'int',
                label='ID')
            form.lbl_id.grid(column=0, row=0, sticky=tk.E)
            form.id.grid(column=1, row=0, sticky=tk.W)
            
            form.addWidget(
                'kurz_bez',
                ttk.Entry(self.frmGrpDaten),
                'text',
                label='Kurz.-Bez.')
            form.lbl_kurz_bez.grid(column=0, row=1, sticky=tk.E)
            form.kurz_bez.grid(column=1, row=1, sticky=tk.W)
            
            form.addWidget(
                'bez',
                ttk.Entry(self.frmGrpDaten),
                'text',
                label='Bezeichnung')
            form.lbl_bez.grid(column=0, row=2, sticky=tk.E)
            form.bez.grid(column=1, row=2, sticky=tk.W)
            
            form.addWidget(
                'farbe',
                ttk.Combobox(self.frmGrpDaten),
                'text',
                label='Farbe')
            form.lbl_farbe.grid(column=0, row=3, sticky=tk.E)
            form.farbe.grid(column=1, row=3, sticky=tk.W)
            
            form.addWidget(
                'bemerkung',
                scrolledtext.ScrolledText(self.frmGrpDaten, width=25, height=5),
                'text',
                label=ttk.Label(self.frmGrpDaten, text='Bemerkung'))
            form.lbl_bemerkung.grid(column=0, row=4, sticky=tk.E+tk.N)
            form.bemerkung.grid(column=1, row=4, sticky=tk.W)
            
            bearbVonAm = BearbVonAm(self.frmGrpDaten)
            bearbVonAm.grid(column=0, row=5, columnspan=2, sticky=tk.W)
            bearbVonAm.connectToForm(form)
        #
        # Mail Arten
        with Form() as form:
            glb.formMailart = form
            #
            # Navi herstellen und einsetzen
            navi = NaviForm(self.frmMailartNavi)
            form.setNavi(navi)
            navi.pack(fill=tk.BOTH, expand=True)
            #
            # Navi konfigurieren
            navi.connectToModell(
                Mailart,
                keyFeldNavi='id',
                labelFelder=('kurz_bez', 'bez'),
                filterFelder=('kurz_bez', 'bez'),
                Sort='kurz_bez')
            #
            # Widgets herstellen, zeigen und in Formular aufnehmen
            form.addWidget(
                'id',
                ttk.Entry(self.frmMailartDaten, state=tk.DISABLED),
                'int',
                label='ID')
            form.lbl_id.grid(column=0, row=0, sticky=tk.E)
            form.id.grid(column=1, row=0, sticky=tk.W)
            
            form.addWidget(
                'kurz_bez',
                ttk.Entry(self.frmMailartDaten),
                'text',
                label='Kurz.-Bez.')
            form.lbl_kurz_bez.grid(column=0, row=1, sticky=tk.E)
            form.kurz_bez.grid(column=1, row=1, sticky=tk.W)
            
            form.addWidget(
                'bez',
                ttk.Entry(self.frmMailartDaten, width=40),
                'text',
                label='Bezeichnung')
            form.lbl_bez.grid(column=0, row=2, sticky=tk.E)
            form.bez.grid(column=1, row=2, sticky=tk.W)
            
            form.addWidget(
                'bemerkung',
                scrolledtext.ScrolledText(self.frmMailartDaten, width=60, height=5),
                'text',
                label=ttk.Label(self.frmMailartDaten, text='Bemerkung'))
            form.lbl_bemerkung.grid(column=0, row=4, sticky=tk.E+tk.N)
            form.bemerkung.grid(column=1, row=4, sticky=tk.W)
            
            bearbVonAm = BearbVonAm(self.frmMailartDaten)
            bearbVonAm.grid(column=0, row=5, columnspan=2, sticky=tk.W)
            bearbVonAm.connectToForm(form)
        #
        # Raum Arten
        with Form() as form:
            glb.formRaumart = form
            #
            # Navi herstellen und einsetzen
            navi = NaviForm(self.frmRaumartNavi)
            form.setNavi(navi)
            navi.pack(fill=tk.BOTH, expand=True)
            #
            # Navi konfigurieren
            navi.connectToModell(
                Raumart,
                keyFeldNavi='id',
                labelFelder= ('kurz_bez', 'beschreibung'),
                filterFelder=('kurz_bez', 'beschreibung'),
                Sort='kurz_bez')
            #
            # Widgets herstellen, zeigen und in Formular aufnehmen
            form.addWidget(
                'id',
                ttk.Entry(self.frmRaumartDaten, state=tk.DISABLED),
                'int',
                label='ID')
            form.lbl_id.grid(column=0, row=0, sticky=tk.E)
            form.id.grid(column=1, row=0, sticky=tk.W)
            
            form.addWidget(
                'kurz_bez',
                ttk.Entry(self.frmRaumartDaten),
                'text',
                label='Kurz.-Bez.')
            form.lbl_kurz_bez.grid(column=0, row=1, sticky=tk.E)
            form.kurz_bez.grid(column=1, row=1, sticky=tk.W)
            
            form.addWidget(
                'beschreibung',
                ttk.Entry(self.frmRaumartDaten, width=40),
                'text',
                label='Bezeichnung')
            form.lbl_beschreibung.grid(column=0, row=2, sticky=tk.E)
            form.beschreibung.grid(column=1, row=2, sticky=tk.W)
            
            form.addWidget(
                'bemerkung',
                scrolledtext.ScrolledText(self.frmRaumartDaten, width=60, height=5),
                'text',
                label=ttk.Label(self.frmRaumartDaten, text='Bemerkung'))
            form.lbl_bemerkung.grid(column=0, row=4, sticky=tk.E+tk.N)
            form.bemerkung.grid(column=1, row=4, sticky=tk.W)
            
            bearbVonAm = BearbVonAm(self.frmRaumartDaten)
            bearbVonAm.grid(column=0, row=5, columnspan=2, sticky=tk.W)
            bearbVonAm.connectToForm(form)
        #
        # Veranstaltung Arten
        with Form() as form:
            glb.formVeranstaltungart = form
            #
            # Navi herstellen und einsetzen
            navi = NaviForm(self.frmVeranstaltungartNavi)
            form.setNavi(navi)
            navi.pack(fill=tk.BOTH, expand=True)
            #
            # Navi konfigurieren
            navi.connectToModell(
                Veranstaltungart,
                keyFeldNavi='id',
                labelFelder= ('kurz_bez', 'beschreibung'),
                filterFelder=('kurz_bez', 'beschreibung'),
                Sort='kurz_bez')
            #
            # Widgets herstellen, zeigen und in Formular aufnehmen
            form.addWidget(
                'id',
                ttk.Entry(self.frmVeranstaltungartDaten, state=tk.DISABLED),
                'int',
                label='ID')
            form.lbl_id.grid(column=0, row=0, sticky=tk.E)
            form.id.grid(column=1, row=0, sticky=tk.W)
            
            form.addWidget(
                'kurz_bez',
                ttk.Entry(self.frmVeranstaltungartDaten),
                'text',
                label='Kurz.-Bez.')
            form.lbl_kurz_bez.grid(column=0, row=1, sticky=tk.E)
            form.kurz_bez.grid(column=1, row=1, sticky=tk.W)
            
            form.addWidget(
                'beschreibung',
                ttk.Entry(self.frmVeranstaltungartDaten, width=40),
                'text',
                label='Bezeichnung')
            form.lbl_beschreibung.grid(column=0, row=2, sticky=tk.E)
            form.beschreibung.grid(column=1, row=2, sticky=tk.W)
            
            form.addWidget(
                'bemerkung',
                scrolledtext.ScrolledText(self.frmVeranstaltungartDaten, width=60, height=5),
                'text',
                label=ttk.Label(self.frmVeranstaltungartDaten, text='Bemerkung'))
            form.lbl_bemerkung.grid(column=0, row=4, sticky=tk.E+tk.N)
            form.bemerkung.grid(column=1, row=4, sticky=tk.W)
            
            bearbVonAm = BearbVonAm(self.frmVeranstaltungartDaten)
            bearbVonAm.grid(column=0, row=5, columnspan=2, sticky=tk.W)
            bearbVonAm.connectToForm(form)
        #
        # Gruppen als Liste
        def FactoryGruppeListe():
            form = Form()
            #
            # Navi herstellen und einsetzen
            navi = NaviForm(self.frmGrpListeInhalt.innerFrame, elemente=('save', 'delete'))
            form.setNavi(navi)
            #
            # Navi konfigurieren
            navi.connectToModell(
                GruppeListe,
                selects=('farbe',))
            #
            # Widgets
            form.addWidget(
                'id',
                ttk.Entry(self.frmGrpListeInhalt.innerFrame, state=tk.DISABLED, width=6),
                'int',
                label='ID')
            form.addWidget(
                'kurz_bez',
                ttk.Entry(self.frmGrpListeInhalt.innerFrame, width=10),
                'text',
                label='Kurz.-Bez.')
            form.addWidget(
                'bez',
                ttk.Entry(self.frmGrpListeInhalt.innerFrame, width=20),
                'text',
                label='Bezeichnung')
            form.addWidget(
                'farbe',
                ttk.Combobox(self.frmGrpListeInhalt.innerFrame, width=10),
                'text',
                label='Farbe')
            #
            # Formular zurückgeben
            return form
                
        with FormListe(self.frmGrpListeInhalt.innerFrame, FactoryGruppeListe) as form:
            glb.formGruppenListe = form
            #
            # Navi herstellen und einsetzen
            navi = NaviListe(self.frmGrpListeNavi)
            form.setNavi(navi)
            #
            # Navi konfigurieren
            G = GruppeListe()
            navi.setGetterDicts(G.FactoryGetterDicts(FilterFelder=('kurz_bez', 'bez'), Sort='kurz_bez'))
            #
            # Form Navi packen
            form.getNavi().pack(anchor=tk.W)
        #
        # Farben
        with Form() as form:
            glb.formFarben = form
            #
            # Navi herstellen und einsetzen
            navi = NaviForm(self.frmFarbenNavi)
            form.setNavi(navi)
            navi.pack(fill=tk.BOTH, expand=True)
            #
            # Navi konfigurieren
            navi.connectToModell(
                Farbe,
                keyFeldNavi='id',
                labelFelder=('farbe',),
                filterFelder=('farbe',),
                Sort='farbe')
            #
            # Widgets herstellen, zeigen und in Formular aufnehmen
            form.addWidget(
                'id',
                ttk.Entry(self.frmFarbenDaten, state=tk.DISABLED),
                'int',
                label='ID')
            form.lbl_id.grid(column=0, row=0, sticky=tk.E)
            form.id.grid(column=1, row=0, sticky=tk.W)
            
            form.addWidget(
                'farbe',
                ttk.Entry(self.frmFarbenDaten),
                'text',
                label='Farbe')
            form.lbl_farbe.grid(column=0, row=1, sticky=tk.E)
            form.farbe.grid(column=1, row=1, sticky=tk.W)
            
            bearbVonAm = BearbVonAm(self.frmFarbenDaten)
            bearbVonAm.grid(column=0, row=2, columnspan=2, sticky=tk.W)
            bearbVonAm.connectToForm(form)
            #
            # Info-Widget zu Farben herstellen und zeigen
            infoText = 'Nur Farben aus dem x11names Bereich, s. z.B.\n'
            urlText = 'https://ctan.math.washington.edu/tex-archive/macros/latex/contrib/xcolor/xcolor.pdf'
            wdg = scrolledtext.ScrolledText(
                self.frmFarbenDaten,
                width=70,
                height=4)
            wdg.insert('0.0', urlText)
            wdg.insert('0.0', infoText)
            ttk.Label(self.frmFarbenDaten, text='Info').grid(column=3, row=0, sticky=tk.W)
            wdg.grid(column=3, row=1, rowspan=2, sticky=tk.W)
            wdg.config(state=tk.DISABLED)
            
        #
        # Länder als Liste
        def FactoryLaenderListe():
            form = Form()
            #
            # Navi herstellen und einsetzen
            navi = NaviForm(self.frmLaenderListeInhalt.innerFrame, elemente=('save', 'delete'))
            form.setNavi(navi)
            #
            # Navi konfigurieren
            navi.connectToModell(Laender)
            #
            # Widgets
            form.addWidget(
                'id',
                ttk.Entry(self.frmLaenderListeInhalt.innerFrame, state=tk.DISABLED, width=6),
                'int',
                label='ID')
            form.addWidget(
                'land',
                ttk.Entry(self.frmLaenderListeInhalt.innerFrame, width=40),
                'text',
                label='Land')
            form.addWidget(
                'land_kurz',
                ttk.Entry(self.frmLaenderListeInhalt.innerFrame, width=5),
                'text',
                label='Kurz')
            Tooltip(form.land_kurz, 'Ländercode nach\nhttps://de.wikipedia.org/wiki/ISO-3166-1-Kodierliste')
            form.addWidget(
                'prototyp',
                ttk.Checkbutton(self.frmLaenderListeInhalt.innerFrame),
                'bool',
                label='Prototyp')
            Tooltip(form.prototyp, 'Genau ein Ländereintrag\nmit gleicher Kurz-Bez\nmuss Prototyp sein.')
            #
            # Formular zurückgeben
            return form
                
        with FormListe(self.frmLaenderListeInhalt.innerFrame, FactoryLaenderListe) as form:
            glb.formLaenderListe = form
            #
            # Navi herstellen und einsetzen
            navi = NaviListe(self.frmLaenderListeNavi)
            form.setNavi(navi)
            #
            # Navi konfigurieren
            L = Laender()
            navi.setGetterDicts(L.FactoryGetterDicts(
                      FilterFelder=('land', 'land_kurz'),
                      Sort='land_kurz, land'))
            #
            # Form Navi packen
            form.getNavi().pack(anchor=tk.W)
        #
        # Tagungen
        with Form() as form:
            glb.formTagungen = form
            #
            # Frames für Navi und Formular bauen und in PanedWindow einsetzen
            self.frmTgNavi = ttk.Frame(self.pndTgEinzel)
            self.frmTgDaten = ttk.Frame(self.pndTgEinzel)
            self.pndTgEinzel.add(self.frmTgNavi)
            self.pndTgEinzel.add(self.frmTgDaten)
            #
            # Navi herstellen und einsetzen
            navi = NaviForm(self.frmTgNavi)
            form.setNavi(navi)
            navi.pack(fill=tk.BOTH, expand=True)
            #
            # Navi konfigurieren
            navi.connectToModell(
                Tagung,
                keyFeldNavi='id',
                labelFelder=('kurz_bez',),
                filterFelder=('kurz_bez',),
                Sort='kurz_bez')
            #
            # Widgets herstellen, zeigen und in Formular aufnehmen
            form.addWidget(
                'id',
                ttk.Entry(self.frmTgDaten, state=tk.DISABLED, width=6),
                'int',
                label='ID')
            form.lbl_id.grid(column=0, row=0, sticky=tk.W)
            form.id.grid(column=0, row=1, sticky=tk.W)
            
            form.addWidget(
                'aktiv',
                ttk.Checkbutton(self.frmTgDaten),
                'bool',
                label='Aktiv')
            form.lbl_aktiv.grid(column=1, row=0, sticky=tk.W)
            form.aktiv.grid(column=1, row=1, sticky=tk.W)
            
            form.addWidget(
                'kurz_bez',
                ttk.Entry(self.frmTgDaten, width=40),
                'text',
                label='Kurz-Bez.')
            form.lbl_kurz_bez.grid(column=0, row=2, sticky=tk.W)
            form.kurz_bez.grid(column=0, row=3, sticky=tk.W)
            
            form.addWidget(
                'titel',
                ttk.Entry(self.frmTgDaten),
                'text',
                label='Titel'
                )
            form.lbl_titel.grid(column=1, row=2, sticky=tk.W)
            form.titel.grid(column=1, row=3, sticky=tk.W)
            
            form.addWidget(
                'beschreibung',
                ttk.Entry(self.frmTgDaten),
                'text',
                label='Beschreibung'
                )
            form.lbl_beschreibung.grid(column=2, row=2, stick=tk.W)
            form.beschreibung.grid(column=2, row=3, sticky=tk.W)
            
            form.addWidget(
                'dat_beginn',
                ttk.Entry(
                    self.frmTgDaten,
                    width=15,
                    validate='focusout',
                    validatecommand=(self.valDate, '%P'),
                    invalidcommand=(self.invalidHoldFocus, '%W')
                    ),
                'date',
                label='Beginn'
                )
            form.lbl_dat_beginn.grid(column=0, row=4, sticky=tk.W)
            form.dat_beginn.grid(column=0, row=5, sticky=tk.W)
            
            form.addWidget(
                'dat_ende',
                ttk.Entry(
                    self.frmTgDaten,
                    width=15,
                    validate='focusout',
                    validatecommand=(self.valDate, '%P'),
                    invalidcommand=(self.invalidHoldFocus, '%W')
                    ),
                'date',
                label='Ende'
                )
            form.lbl_dat_ende.grid(column=1, row=4, sticky=tk.W)
            form.dat_ende.grid(column=1, row=5, sticky=tk.W)
            
            form.addWidget(
                'ort',
                ttk.Entry(self.frmTgDaten),
                'text',
                label='Ort'
                )
            form.lbl_ort.grid(column=2, row=4, sticky=tk.W)
            form.ort.grid(column=2, row=5, sticky=tk.W)
            
            form.addWidget(
                'mail_from',
                ttk.Entry(self.frmTgDaten),
                'text',
                label='Mail From')
            form.lbl_mail_from.grid(column=0, row=8, columnspan=2, sticky=tk.W)
            form.mail_from.grid(column=0, row=9, columnspan=2, sticky=tk.W)
            
            form.addWidget(
                'mail_reply',
                ttk.Entry(self.frmTgDaten),
                'text',
                label='Mail Reply')
            form.lbl_mail_reply.grid(column=2, row=8, sticky=tk.W)
            form.mail_reply.grid(column=2, row=9, sticky=tk.W)
            
            form.addWidget(
                'rel_verz',
                ttk.Entry(self.frmTgDaten),
                'text',
                label='Rel. Verz.')
            form.lbl_rel_verz.grid(column=0, row=10, columnspan=2, sticky=tk.W)
            form.rel_verz.grid(column=0, row=11, columnspan=2, sticky=tk.W)
            
            form.addWidget(
                'schema',
                ttk.Entry(self.frmTgDaten),
                'text',
                label='DB Schema')
            form.lbl_schema.grid(column=2, row=10, sticky=tk.W)
            form.schema.grid(column=2, row=11, sticky=tk.W)
            
            bearbVonAm = BearbVonAm(self.frmTgDaten)
            bearbVonAm.grid(column=0, row=12, columnspan=3, sticky=tk.W)
            bearbVonAm.connectToForm(form)
        #
        # Mails
        with Form() as form:
            glb.formMails = form
            #
            # Frames für Navi und Formular bauen und in PanedWindow einsetzen
            self.pndTgMailsNavi = ttk.Frame(self.pndTgMails)
            self.pndTgMailsDaten = ttk.Frame(self.pndTgMails)
            self.pndTgMails.add(self.pndTgMailsNavi)
            self.pndTgMails.add(self.pndTgMailsDaten)
            #
            # Navi herstellen und einsetzen
            navi = NaviForm(self.pndTgMailsNavi)
            form.setNavi(navi)
            navi.pack(fill=tk.BOTH, expand=True)
            #
            # Navi konfigurieren
            navi.connectToModell(
                Mail,
                selects=('art',),
                keyFeldNavi='id',
                labelFelder=('art', 'aktuell', 'id',),
                filterFelder=('art', 'betreff',),
                Sort='art, aktuell desc, id')
            #
            # Widgets herstellen, zeigen und in Formular aufnehmen
            form.addWidget(
                'id',
                ttk.Entry(self.pndTgMailsDaten, state=tk.DISABLED, width=6),
                'int',
                label='ID')
            form.lbl_id.grid(column=0, row=0, sticky=tk.W)
            form.id.grid(column=0, row=1, sticky=tk.W)
            
            form.addWidget(
                'art',
                ComboboxValueLabel(
                      self.pndTgMailsDaten,
                      width=15),
                'text',
                label='Mail-Art')
            form.lbl_art.grid(column=0, row=2, sticky=tk.W)
            form.art.grid(column=0, row=3, sticky=tk.W)
            
            form.addWidget(
                'aktuell',
                ttk.Checkbutton(self.pndTgMailsDaten),
                'bool',
                label='Aktuell')
            Tooltip(form.aktuell, 'Nur eine Mail\nder gleichen Art\ndarf und muss als\naktuell markiert sein')
            form.lbl_aktuell.grid(column=1, row=2, sticky=tk.W)
            form.aktuell.grid(column=1, row=3, sticky=tk.W)
            
            mailsWidth = 25
            mailsHeight = 8
            
            form.addWidget(
                'betreff',
                ttk.Entry(self.pndTgMailsDaten, width=2*mailsWidth),
                'text',
                label='Betreff')
            form.lbl_betreff.grid(column=0, row=4, columnspan=2, sticky=tk.W)
            form.betreff.grid(column=0, row=5, columnspan=2, sticky=tk.W)
            
            form.addWidget(
                'text_vj',
                scrolledtext.ScrolledText(
                    self.pndTgMailsDaten,
                    width=mailsWidth,
                    height=mailsHeight),
                'text',
                label=ttk.Label(self.pndTgMailsDaten, text='Text: Volljährige'))
            Tooltip(form.text_vj, 'Text (ohne Anrede)\nfür volljährige TN')
            form.lbl_text_vj.grid(column=0, row=6, sticky=tk.W)
            form.text_vj.grid(column=0, row=7, sticky=tk.W)
            
            form.addWidget(
                'text_mj',
                scrolledtext.ScrolledText(
                    self.pndTgMailsDaten,
                    width=mailsWidth,
                    height=mailsHeight),
                'text',
                label=ttk.Label(self.pndTgMailsDaten, text='Text: Minderjährige'))
            Tooltip(form.text_mj, 'Text (ohne Anrede)\nfür minderjährige TN')
            form.lbl_text_mj.grid(column=1, row=6, sticky=tk.W)
            form.text_mj.grid(column=1, row=7, sticky=tk.W)
            
            form.addWidget(
                'text_kf',
                scrolledtext.ScrolledText(
                    self.pndTgMailsDaten,
                    width=mailsWidth,
                    height=mailsHeight),
                'text',
                label=ttk.Label(self.pndTgMailsDaten, text='Text: Ki-Tagung'))
            Tooltip(form.text_kf, 'Text (ohne Anrede)\nTN der Kinder-Tagung')
            form.lbl_text_kf.grid(column=2, row=6, sticky=tk.W)
            form.text_kf.grid(column=2, row=7, sticky=tk.W)
            
            form.addWidget(
                'text_kb',
                scrolledtext.ScrolledText(
                    self.pndTgMailsDaten,
                    width=mailsWidth,
                    height=mailsHeight),
                'text',
                label=ttk.Label(self.pndTgMailsDaten, text='Text: Ki-Betreuung'))
            Tooltip(form.text_kb, 'Text (ohne Anrede)\nTN der Kinder-Betreuung')
            form.lbl_text_kb.grid(column=3, row=6, sticky=tk.W)
            form.text_kb.grid(column=3, row=7, sticky=tk.W)
            
            form.addWidget(
                'anhang_vj',
                ttk.Entry(self.pndTgMailsDaten, width=mailsWidth),
                'text',
                label='Anhang: Volljährige')
            Tooltip(form.anhang_vj, 'Anhang für volljährige TN,\ni.d.R. leer')
            form.lbl_anhang_vj.grid(column=0, row=8, sticky=tk.W)
            form.anhang_vj.grid(column=0, row=9, sticky=tk.W)
            
            form.addWidget(
                'anhang_mj',
                ttk.Entry(self.pndTgMailsDaten, width=mailsWidth),
                'text',
                label='Anhang: Minderjährige')
            Tooltip(form.anhang_mj, 'Anhang für minderjährige TN,\ni.d.R. Einverständniserklärung')
            form.lbl_anhang_mj.grid(column=1, row=8, sticky=tk.W)
            form.anhang_mj.grid(column=1, row=9, sticky=tk.W)
            
            form.addWidget(
                'anhang_kf',
                ttk.Entry(self.pndTgMailsDaten, width=mailsWidth),
                'text',
                label='Anhang: Ki-Tagung')
            Tooltip(form.anhang_kf, 'Anhang für TN Kinder-Tagung,\ni.d.R. leer')
            form.lbl_anhang_kf.grid(column=2, row=8, sticky=tk.W)
            form.anhang_kf.grid(column=2, row=9, sticky=tk.W)
            
            form.addWidget(
                'anhang_kb',
                ttk.Entry(self.pndTgMailsDaten, width=mailsWidth),
                'text',
                label='Anhang: Ki-Betreuung')
            Tooltip(form.anhang_kb, 'Anhang für TN Kinder-Betreuung,\ni.d.R. leer')
            form.lbl_anhang_kb.grid(column=3, row=8, sticky=tk.W)
            form.anhang_kb.grid(column=3, row=9, sticky=tk.W)
            
            form.addWidget(
                'bemerkung',
                scrolledtext.ScrolledText(
                    self.pndTgMailsDaten,
                    width=2*mailsWidth,
                    height=mailsHeight),
                'text',
                label=ttk.Label(self.pndTgMailsDaten, text='Bemerkung'))
            Tooltip(form.bemerkung, 'Bemerkung des TB,\nwird nicht mit verschickt.')
            form.lbl_bemerkung.grid(column=0, row=10, columnspan=2, sticky=tk.W)
            form.bemerkung.grid(column=0, row=11, columnspan=2, sticky=tk.W)
            
            bearbVonAm = BearbVonAm(self.pndTgMailsDaten)
            bearbVonAm.grid(column=0, row=12, columnspan=3, sticky=tk.W)
            bearbVonAm.connectToForm(form)
        #
        # Jobs Einzelheiten
        with Form() as form:
            glb.formJobsEinzelheiten = form
            #
            # Navi herstellen und einsetzen
            navi = NaviForm(self.frmJobsEinzelNavi)
            form.setNavi(navi)
            navi.pack(fill=tk.BOTH, expand=True)
            #
            # Navi konfigurieren
            navi.connectToModell(
                Jobs,
                keyFeldNavi='id',
                labelFelder=('titel',),
                filterFelder=('titel', 'kommando'),
                Sort='kommando')
            #
            # Widgets herstellen, zeigen und in Formular aufnehmen
            form.addWidget(
                'id',
                ttk.Entry(self.frmJobsEinzelDaten, state=tk.DISABLED, width=6),
                'int',
                label='ID')
            form.lbl_id.grid(column=0, row=0, sticky=tk.W)
            form.id.grid(column=0, row=1, sticky=tk.W)
            
            form.addWidget(
                'titel',
                ttk.Entry(self.frmJobsEinzelDaten, width=40),
                'text',
                label='Titel')
            form.lbl_titel.grid(column=0, row=2, columnspan=2, sticky=tk.W)
            form.titel.grid(column=0, row=3, columnspan=2, sticky=tk.W)
            
            form.addWidget(
                'kommando',
                ttk.Entry(self.frmJobsEinzelDaten, width=40),
                'text',
                label='Kommando')
            form.lbl_kommando.grid(column=0, row=4, sticky=tk.W)
            form.kommando.grid(column=0, row=5, sticky=tk.W)
            
            form.addWidget(
                'verzeichnis',
                ttk.Entry(self.frmJobsEinzelDaten, width=40),
                'text',
                label='Verzeichnis')
            form.lbl_verzeichnis.grid(column=2, row=4, sticky=tk.W)
            form.verzeichnis.grid(column=2, row=5, sticky=tk.W)
            
            form.addWidget(
                'beschreibung',
                ttk.Entry(self.frmJobsEinzelDaten, width=80),
                'text',
                label='Beschreibung')
            form.lbl_beschreibung.grid(column=0, row=6, columnspan=3, sticky=tk.W)
            form.beschreibung.grid(column=0, row=7, columnspan=3, sticky=tk.W)
            
            form.addWidget(
                'intervall',
                ttk.Entry(
                      self.frmJobsEinzelDaten,
                      width=4,
                      validate='key',
                      validatecommand=(self.valInt, '%P')
                      ),
                'int',
                label='Intervall')
            form.lbl_intervall.grid(column=0, row=8, sticky=tk.E)
            form.intervall.grid(column=0, row=9, sticky=tk.E)
            
            form.addWidget(
                'einheit',
                ComboboxValueLabel(
                      self.frmJobsEinzelDaten,
                      width=12),
                'text',
                label='Einheit')
            form.getWidget('einheit').fill((
                ('mi', 'Minute(n)'),
                ('st', 'Stunde(n)'),
                ('ta', 'Tag(e)'),
                ('mo', 'Monat(e)')
                ))
            form.lbl_einheit.grid(column=1, row=8, sticky=tk.W)
            form.einheit.grid(column=1, row=9, sticky=tk.W)
            
            form.addWidget(
                'aktiv',
                ttk.Checkbutton(self.frmJobsEinzelDaten),
                'bool',
                label='Aktiv')
            form.lbl_aktiv.grid(column=0, row=10, sticky=tk.E)
            form.aktiv.grid(column=1, row=10, sticky=tk.W)
                
            form.addWidget(
                'sofort',
                ttk.Checkbutton(self.frmJobsEinzelDaten),
                'bool',
                label='Sofort')
            form.lbl_sofort.grid(column=0, row=11, sticky=tk.E)
            form.sofort.grid(column=1, row=11, sticky=tk.W)
                
            form.addWidget(
                'gestoppt',
                ttk.Checkbutton(self.frmJobsEinzelDaten),
                'bool',
                label='Gestoppt')
            form.lbl_gestoppt.grid(column=0, row=12, sticky=tk.E)
            form.gestoppt.grid(column=1, row=12, sticky=tk.W)
                
            form.addWidget(
                'selbstzerstoerend',
                ttk.Checkbutton(self.frmJobsEinzelDaten),
                'bool',
                label='Selbstzerstörend')
            form.lbl_selbstzerstoerend.grid(column=0, row=13, sticky=tk.E)
            form.selbstzerstoerend.grid(column=1, row=13, sticky=tk.W)
        #
        # Jobs Liste
        def FactoryJobsListe():
            form = Form()
            #
            # Navi herstellen und einsetzen
            navi = NaviForm(self.frmJobsListeInhalt.innerFrame, elemente=('save', 'delete'))
            form.setNavi(navi)
            #
            # Navi konfigurieren
            navi.connectToModell(JobsListe)
            #
            # Widgets
            form.addWidget(
                'id',
                ttk.Entry(self.frmJobsListeInhalt.innerFrame, state=tk.DISABLED, width=6),
                'int',
                label='ID')
            form.addWidget(
                'titel',
                ttk.Entry(self.frmJobsListeInhalt.innerFrame, width=30),
                'text',
                label='Titel')
            form.addWidget(
                'kommando',
                ttk.Entry(self.frmJobsListeInhalt.innerFrame, width=30),
                'text',
                label='Kommando')
            form.addWidget(
                'intervall',
                ttk.Entry(
                      self.frmJobsListeInhalt.innerFrame,
                      width=8,
                      validate='key',
                      validatecommand=(self.valInt, '%P')
                      ),
                'int',
                label='Interv.')
            form.addWidget(
                'einheit',
                ComboboxValueLabel(
                      self.frmJobsListeInhalt.innerFrame,
                      width=12),
                'text',
                label='Einheit')
            form.getWidget('einheit').fill((
                ('mi', 'Minute(n)'),
                ('st', 'Stunde(n)'),
                ('ta', 'Tag(e)'),
                ('mo', 'Monat(e)')
                ))
            form.addWidget(
                'aktiv',
                ttk.Checkbutton(self.frmJobsListeInhalt.innerFrame),
                'bool',
                label='Aktiv')
            form.addWidget(
                'sofort',
                ttk.Checkbutton(self.frmJobsListeInhalt.innerFrame),
                'bool',
                label='Sofort')
            form.addWidget(
                'gestoppt',
                ttk.Checkbutton(self.frmJobsListeInhalt.innerFrame),
                'bool',
                label='Gestoppt')
            #
            # Formular zurückgeben
            return form
        
        with FormListe(self.frmJobsListeInhalt.innerFrame, FactoryJobsListe) as form:
            glb.formGruppenListe = form
            #
            # Navi herstellen und einsetzen
            navi = NaviListe(self.frmJobsListeNavi)
            form.setNavi(navi)
            #
            # Navi konfigurieren
            J = JobsListe()
            navi.setGetterDicts(J.FactoryGetterDicts(
                    FilterFelder=('titel', 'kommando'),
                    Sort='kommando'))
            #
            # Form Navi packen
            form.getNavi().pack(anchor=tk.W)
        #
        # Status Liste
        def FactoryStatusListe():
            form = Form()
            #
            # Navi herstellen und einsetzen
            navi = NaviForm(self.frmStatusListeInhalt.innerFrame, elemente=('save', 'delete'))
            form.setNavi(navi)
            #
            # Navi konfigurieren
            navi.connectToModell(
                StatusListe,
                selects=('farbe', 'mail_art', 'nachfolge_status'))
            #
            # Widgets
            form.addWidget(
                'id',
                ttk.Entry(self.frmStatusListeInhalt.innerFrame, state=tk.DISABLED, width=6),
                'int',
                label='ID')
            form.addWidget(
                'kurz_bez',
                ttk.Entry(self.frmStatusListeInhalt.innerFrame, width=10),
                'text',
                label='Kurz-Bez.')
            form.addWidget(
                'bez',
                ttk.Entry(self.frmStatusListeInhalt.innerFrame, width=50),
                'text',
                label='Bezeichnung')
            form.addWidget(
                'farbe',
                ttk.Combobox(self.frmStatusListeInhalt.innerFrame, width=8),
                'text',
                label='Farbe')
            form.addWidget(
                'mail_ausloesen',
                ttk.Checkbutton(self.frmStatusListeInhalt.innerFrame),
                'bool',
                label='Mail auslösen')
            form.addWidget(
                'mail_art',
                ttk.Combobox(self.frmStatusListeInhalt.innerFrame, width=8),
                'text',
                label='Art')
            form.addWidget(
                'nachfolge_status',
                ttk.Combobox(self.frmStatusListeInhalt.innerFrame, width=18),
                'text',
                label='Nachfolge-Status')
            #
            # Formular zurückgeben
            return form
        
        with FormListe(self.frmStatusListeInhalt.innerFrame, FactoryStatusListe) as form:
            glb.formStatusListe = form
            #
            # Navi herstellen und einsetzen
            navi = NaviListe(self.frmStatusListeNavi)
            form.setNavi(navi)
            #
            # Navi konfigurieren
            S = StatusListe()
            navi.setGetterDicts(S.FactoryGetterDicts(
                    FilterFelder=('kurz_bez', 'bez'),
                    Sort='kurz_bez'))
            #
            # Form Navi packen
            form.getNavi().pack(anchor=tk.W)
            
    def disableMainNotebook(self):
        """disableMainNotebook - Deaktiviert alle Tabs des Main Notebook
        """
        for index in range(self.nbkMain.index(tk.END)):
            self.nbkMain.tab(index, stat=tk.DISABLED)
                        
    def enableMainNotebook(self):
        """enableMainNotebook - Aktiviert alle Tabs des Main Notebook
        """
        for index in range(self.nbkMain.index(tk.END)):
            self.nbkMain.tab(index, stat=tk.NORMAL)
                        
    def baueLayout(self):
        """baueLayout - Baut das Layout auf, in dem später die Widgets plaziert werden
        
            Notebook-Struktur:
            
                nbkMain
                    nbkPersonen
                        frmJugendEinzelheiten         Personen, relevante Felder für Jugend
                        frmPersonenStatus             Anmelde-Status der Personen
                        frmPersonenFinanzen           Personen: Finanzen
                        frmPersonenFinanzenListe      Personen: Finanzen, als Liste
                        frmAnmWS                      WS-Anm. zuordnen
                    nbkInstitutionen
                        frmInstitutionenJugend        Institutionen, relevante Felder für Jugend
                    nbkQuartier
                        frmQuartiere
                    nbkVeranstaltung
                        frmVeranstaltung
                        frmRaum
                    nbkHelferlein
                        frmGruppen
                        frmGruppenListe
                        frmMailartEinzelheiten
                        frmQuartierartEinzelheiten
                        frmRaumartEinzelheiten
                        frmVeranstaltungsartEinzelheiten
                    nbkVerwaltung
                        frmFarben
                        frmFarbenListe
                        frmTagungenEinzelheiten
                        frmLaenderListe
                        frmJobsListe
                        frmStatus
                        frmStatusListe
                        frmMail
        """
        #
        # Kopfleiste
        with CtxFrame(self) as self.frmTop:
            self.frmTop.pack()
        #
        # Paned Window für Haupt und Fuß Frame
        with CtxPanedWindow(self, orient=tk.VERTICAL) as self.pndHauptUndFuss:
            self.pndHauptUndFuss.pack(expand=tk.YES, fill=tk.BOTH)
            #
            # Haupt Frame
            with CtxFrame(self.pndHauptUndFuss) as self.frmMain:
                # self.frmMain = ttk.Frame(self.pndHauptUndFuss)
                self.pndHauptUndFuss.add(self.frmMain)
                #
                # Haupt-Notebook
                with CtxNotebook(self.frmMain) as self.nbkMain:
                    # self.nbkMain = ttk.Notebook(self.frmMain)
                    self.nbkMain.pack(expand=tk.YES, fill=tk.BOTH)
                    # Notebook Personen
                    with CtxNotebook(self.nbkMain) as self.nbkPersonen:
                        self.nbkMain.add(self.nbkPersonen, text='Personen')
                        # Jugend Einzelheiten
                        with CtxPanedWindow(self.nbkPersonen, orient=tk.HORIZONTAL) as self.pndPersJuEinzel:
                            self.nbkPersonen.add(self.pndPersJuEinzel, text='Jugend: Einzelheiten')
                            # Frames für Navi, Formular und Unterformulare
                            self.frmPersJuEinzelNavi = ttk.Frame(self.pndPersJuEinzel)
                            self.frmPersJuEinzelInhalt = ttk.Frame(self.pndPersJuEinzel)
                            self.pndPersJuEinzel.add(self.frmPersJuEinzelNavi)
                            self.pndPersJuEinzel.add(self.frmPersJuEinzelInhalt)
                            
                            self.frmPersJuEinzelDaten = ttk.Frame(self.frmPersJuEinzelInhalt)
                            self.frmPersJuEinzelUnterformulare = ttk.Frame(self.frmPersJuEinzelInhalt)
                            self.frmPersJuEinzelDaten.pack(side=tk.LEFT, fill=tk.Y, expand=False)
                            ttk.Separator(self.frmPersJuEinzelInhalt, orient=tk.VERTICAL).pack(
                                side=tk.LEFT,
                                fill=tk.Y,
                                expand=False)
                            self.frmPersJuEinzelUnterformulare.pack(
                                side=tk.LEFT,
                                fill=tk.BOTH,
                                expand=True)
                            
                            self.sfrPersJuEinzelGruppen = yScrolledFrame(self.frmPersJuEinzelUnterformulare)
                            self.frmPersJuEinzelGruppen = self.sfrPersJuEinzelGruppen.innerFrame
                            ttk.Label(self.frmPersJuEinzelUnterformulare, text='Gruppen').pack(
                                  side=tk.TOP,
                                  anchor=tk.W)
                            self.sfrPersJuEinzelGruppen.pack(
                                side=tk.TOP,
                                fill=tk.BOTH,
                                expand=True,
                                anchor=tk.W)
                        # Personen Status - Liste
                        with CtxFrame(self.nbkPersonen) as self.frmPersonenStatusListe:
                            self.nbkPersonen.add(self.frmPersonenStatusListe, text='Anm.-Status')
                            # Frames für Navi und Inhalt
                            self.frmPersonenStatusListeNavi = ttk.Frame(self.frmPersonenStatusListe)
                            self.frmPersonenStatusListeInhalt = yScrolledFrame(self.frmPersonenStatusListe)
                            self.frmPersonenStatusListeNavi.pack(
                                side=tk.TOP,
                                anchor=tk.W
                                )
                            self.frmPersonenStatusListeInhalt.pack(
                                side=tk.TOP,
                                expand=tk.YES,
                                fill=tk.BOTH
                                )
                        # Personen WS-Anm. zuordnen - 2 x Liste
                        with CtxFrame(self.nbkPersonen) as self.frmWSAnmZuordnen:
                            self.nbkPersonen.add(self.frmWSAnmZuordnen, text='WS-Anm.')
                            # WS-Anmeldungen
                            with CtxLabelFrame(self.frmWSAnmZuordnen, text = 'WS-Anmeldungen') as frame:
                                frame.pack(side=tk.TOP, expand=tk.YES, fill=tk.BOTH)
                                self.frmWSAnmZuordnenNavi = ttk.Frame(frame)
                                self.frmWSAnmZuordnenInhalt = yScrolledFrame(frame)
                                self.frmWSAnmZuordnenNavi.pack(
                                    side=tk.TOP,
                                    anchor=tk.W
                                    )
                                self.frmWSAnmZuordnenInhalt.pack(
                                    side=tk.TOP,
                                    expand=tk.YES,
                                    fill=tk.BOTH
                                    )
                            # Personen zum Abgleich
                            with CtxLabelFrame(self.frmWSAnmZuordnen, text='Personen') as frame:
                                frame.pack(side=tk.TOP, expand=tk.YES, fill=tk.BOTH)
                                self.frmWSAnmZuordnenPersNavi = ttk.Frame(frame)
                                self.frmWSAnmZuordnenPersInhalt = yScrolledFrame(frame)
                                self.frmWSAnmZuordnenPersNavi.pack(
                                    side=tk.TOP,
                                    anchor=tk.W
                                    )
                                self.frmWSAnmZuordnenPersInhalt.pack(
                                    side=tk.TOP,
                                    expand=tk.YES,
                                    fill=tk.BOTH
                                    )
                        # Personen WS festlegen - Liste
                        with CtxFrame(self.nbkPersonen) as self.frmWSFestlegen:
                            self.nbkPersonen.add(self.frmWSFestlegen, text='WS festlegen')
                            # Frames für Navi und Inhalt
                            self.frmWSFestlegenNavi = ttk.Frame(self.frmWSFestlegen)
                            self.frmWSFestlegenInhalt = yScrolledFrame(self.frmWSFestlegen)
                            self.frmWSFestlegenNavi.pack(
                                side=tk.TOP,
                                anchor=tk.W)
                            self.frmWSFestlegenInhalt.pack(
                                side=tk.TOP,
                                expand=tk.YES,
                                fill=tk.BOTH)
                        # Personen Finanzen - Einzelheiten
                        with CtxPanedWindow(self.nbkPersonen, orient=tk.HORIZONTAL) \
                                as self.pndPersFinanzEinzel:
                            self.nbkPersonen.add(self.pndPersFinanzEinzel, text='Finanzen')
                            # Frames für Navi, Formular und Unterformulare
                            self.frmPersFinanzEinzelNavi = ttk.Frame(self.pndPersFinanzEinzel)
                            self.frmPersFinanzEinzelInhalt = ttk.Frame(self.pndPersFinanzEinzel)
                            self.pndPersFinanzEinzel.add(self.frmPersFinanzEinzelNavi)
                            self.pndPersFinanzEinzel.add(self.frmPersFinanzEinzelInhalt)
                            
                            self.frmPersFinanzEinzelDaten = ttk.Frame(self.frmPersFinanzEinzelInhalt)
                            self.frmPersFinanzEinzelDaten.pack(side=tk.LEFT, fill=tk.Y, expand=False)
                        # Personen Finanzen - Liste
                        with CtxFrame(self.nbkPersonen) as self.frmPersFinanzListe:
                            self.nbkPersonen.add(self.frmPersFinanzListe, text='Finanzen (Liste)')
                            self.frmPersFinanzListeNavi = ttk.Frame(self.frmPersFinanzListe)
                            self.frmPersFinanzListeInhalt = yScrolledFrame(self.frmPersFinanzListe)
                            self.frmPersFinanzListeNavi.pack(
                                side=tk.TOP,
                                anchor=tk.W
                                )
                            self.frmPersFinanzListeInhalt.pack(
                                side=tk.TOP,
                                expand=tk.YES,
                                fill=tk.BOTH
                                )
                    # Notebook Institutionen
                    with CtxNotebook(self.nbkMain) as self.nbkInstitutionen:
                        self.nbkMain.add(self.nbkInstitutionen, text='Institutionen')
                        # Jugend Institutionen - Einzelheiten
                        with CtxPanedWindow(self.nbkInstitutionen, orient=tk.HORIZONTAL) \
                                as self.pndInstitutionenJugend:
                            self.nbkInstitutionen.add(
                                    self.pndInstitutionenJugend,
                                    text='Jugend: Institutionen')
                    # Notebook Quartiere
                    with CtxNotebook(self.nbkMain) as self.nbkQuartiere:
                        self.nbkMain.add(self.nbkQuartiere, text='Quartiere')
                        # Quartiere - Einzelheiten
                        with CtxPanedWindow(self.nbkQuartiere, orient=tk.HORIZONTAL) \
                                as self.pndQuartiere:
                            self.nbkQuartiere.add(self.pndQuartiere, text='Einzelheiten')
                    # Notebook Veranstaltungen (= VA = Veranst)
                    with CtxNotebook(self.nbkMain) as self.nbkVeranst:
                        self.nbkMain.add(self.nbkVeranst, text='Veranstaltungen')
                        # VA - Einzelheiten
                        with CtxPanedWindow(self.nbkVeranst, orient=tk.HORIZONTAL) \
                                as self.pndVeranstEinzel:
                            self.nbkVeranst.add(self.pndVeranstEinzel, text='Einzelheiten')
                            # Frames für Navi, Formular und Unterformulare
                            self.frmVAEinzelNavi = ttk.Frame(self.pndVeranstEinzel)
                            self.frmVAEinzelInhalt = ttk.Frame(self.pndVeranstEinzel)
                            self.pndVeranstEinzel.add(self.frmVAEinzelNavi)
                            self.pndVeranstEinzel.add(self.frmVAEinzelInhalt)
                            
                            self.frmVAEinzelDaten = ttk.Frame(self.frmVAEinzelInhalt)
                            self.frmVAEinzelUnterformulare = ttk.Frame(self.frmVAEinzelInhalt)
                            self.frmVAEinzelDaten.pack(side=tk.LEFT, fill=tk.Y, expand=False)
                            ttk.Separator(self.frmVAEinzelInhalt, orient=tk.VERTICAL).pack(
                                      side=tk.LEFT,
                                      fill=tk.Y,
                                      expand=False)
                            self.frmVAEinzelUnterformulare.pack(
                                      side=tk.LEFT,
                                      fill=tk.BOTH,
                                      expand=True)
                            
                            self.sfrVAEinzelDozenten = yScrolledFrame(self.frmVAEinzelUnterformulare)
                            self.frmVAEinzelDozenten = self.sfrVAEinzelDozenten.innerFrame
                            ttk.Label(self.frmVAEinzelUnterformulare, text='Dozenten').pack(
                                  side=tk.TOP,
                                  anchor=tk.W)
                            self.sfrVAEinzelDozenten.pack(side=tk.TOP, fill=tk.BOTH, expand=True, anchor=tk.W)
                            
                            self.sfrVAEinzelRaum = yScrolledFrame(self.frmVAEinzelUnterformulare)
                            self.frmVAEinzelRaum = self.sfrVAEinzelRaum.innerFrame
                            ttk.Label(self.frmVAEinzelUnterformulare, text='Raum').pack(
                                  side=tk.TOP,
                                  anchor=tk.W)
                            self.sfrVAEinzelRaum.pack(
                                  side=tk.TOP,
                                  fill=tk.BOTH,
                                  expand=True,
                                  anchor=tk.W)        
                    # Notebook Räume
                    with CtxNotebook(self.nbkMain) as self.nbkRaeume:
                        self.nbkMain.add(self.nbkRaeume, text='Räume')
                        # Einzelheiten
                        with CtxPanedWindow(self.nbkRaeume, orient=tk.HORIZONTAL) \
                                as self.frmRaeumeEinzel:
                            self.nbkRaeume.add(self.frmRaeumeEinzel, text='Einzelheiten')
                            # Frames für Navi, Formular und Unterformulare
                            self.frmRaumEinzelNavi = ttk.Frame(self.frmRaeumeEinzel)
                            self.frmRaumEinzelInhalt = ttk.Frame(self.frmRaeumeEinzel)
                            self.frmRaeumeEinzel.add(self.frmRaumEinzelNavi)
                            self.frmRaeumeEinzel.add(self.frmRaumEinzelInhalt)        
                            self.frmRaumEinzelDaten = ttk.Frame(self.frmRaumEinzelInhalt)
                            
                            self.frmRaumEinzelUnterformulare = ttk.Frame(self.frmRaumEinzelInhalt)
                            self.frmRaumEinzelDaten.pack(side=tk.LEFT, fill=tk.Y, expand=False)
                            ttk.Separator(self.frmRaumEinzelInhalt, orient=tk.VERTICAL).pack(
                                      side=tk.LEFT, fill=tk.Y, expand=False)
                            self.frmRaumEinzelUnterformulare.pack(
                                    side=tk.LEFT,
                                    fill=tk.BOTH,
                                    expand=True)
                            
                            self.sfrRaumEinzelBelegung = yScrolledFrame(self.frmRaumEinzelUnterformulare)
                            self.frmRaumEinzelBelegung = self.sfrRaumEinzelBelegung.innerFrame
                            ttk.Label(self.frmRaumEinzelUnterformulare, text='Belegung').pack(
                                  side=tk.TOP,
                                  anchor=tk.W)
                            self.sfrRaumEinzelBelegung.pack(
                                  side=tk.TOP,
                                  fill=tk.BOTH,
                                  expand=True,
                                  anchor=tk.W)        
                    # Notebook Helferlein
                    with CtxNotebook(self.nbkMain) as self.nbkHelferlein:
                        self.nbkMain.add(self.nbkHelferlein, text='Helferlein')
                        # Gruppen - Einzelheiten
                        with CtxPanedWindow(self.nbkHelferlein, orient=tk.HORIZONTAL) \
                                as self.frmGrpEinzel:
                            self.nbkHelferlein.add(self.frmGrpEinzel, text='Gruppen')
                            # Frames für Navi und Daten
                            self.frmGrpNavi = ttk.Frame(self.frmGrpEinzel)
                            self.frmGrpDaten = ttk.Frame(self.frmGrpEinzel)
                            self.frmGrpEinzel.add(self.frmGrpNavi)
                            self.frmGrpEinzel.add(self.frmGrpDaten)
                        # Gruppen - Liste
                        with CtxFrame(self.nbkHelferlein) as self.frmGrpListe:
                            self.nbkHelferlein.add(self.frmGrpListe, text='Gruppen (Liste)')
                            self.frmGrpListeNavi = ttk.Frame(self.frmGrpListe)
                            self.frmGrpListeInhalt = yScrolledFrame(self.frmGrpListe)
                            self.frmGrpListeNavi.pack(
                                side=tk.TOP,
                                anchor=tk.W
                                )
                            self.frmGrpListeInhalt.pack(
                                side=tk.TOP,
                                expand=tk.YES,
                                fill=tk.BOTH
                                )
                        # Mailarten - Einzelheiten
                        with CtxPanedWindow(self.nbkHelferlein, orient=tk.HORIZONTAL) \
                                as self.frmMailartEinzel:
                            self.nbkHelferlein.add(self.frmMailartEinzel, text='Mailarten')
                            # Frames für Navi und Daten
                            self.frmMailartNavi = ttk.Frame(self.frmMailartEinzel)
                            self.frmMailartDaten = ttk.Frame(self.frmMailartEinzel)
                            self.frmMailartEinzel.add(self.frmMailartNavi)
                            self.frmMailartEinzel.add(self.frmMailartDaten)
                        # Quartierarten - Einzelheiten
                        with CtxPanedWindow(self.nbkHelferlein, orient=tk.HORIZONTAL) \
                                as self.frmQuartierartEinzel:
                            self.nbkHelferlein.add(self.frmQuartierartEinzel, text='Quartierarten')
                        # Raumarten - Einzelheiten
                        with CtxPanedWindow(self.nbkHelferlein, orient=tk.HORIZONTAL) \
                                as self.frmRaumartEinzel:
                            self.nbkHelferlein.add(self.frmRaumartEinzel, text='Raumarten')
                            # Frames für Navi und Daten
                            self.frmRaumartNavi = ttk.Frame(self.frmRaumartEinzel)
                            self.frmRaumartDaten = ttk.Frame(self.frmRaumartEinzel)
                            self.frmRaumartEinzel.add(self.frmRaumartNavi)
                            self.frmRaumartEinzel.add(self.frmRaumartDaten)
                        # Veranstaltungsart - Einzelheiten
                        with CtxPanedWindow(self.nbkHelferlein, orient=tk.HORIZONTAL) \
                                as self.frmVeranstArtEinzel:
                            self.nbkHelferlein.add(
                                    self.frmVeranstArtEinzel,
                                    text='Veranstaltungsarten')
                            # Frames für Navi und Daten
                            self.frmVeranstaltungartNavi = ttk.Frame(self.frmVeranstArtEinzel)
                            self.frmVeranstaltungartDaten = ttk.Frame(self.frmVeranstArtEinzel)
                            self.frmVeranstArtEinzel.add(self.frmVeranstaltungartNavi)
                            self.frmVeranstArtEinzel.add(self.frmVeranstaltungartDaten)        
                    # Notebook Verwaltung
                    with CtxNotebook(self.nbkMain) as self.nbkVerwaltung:
                        self.nbkMain.add(self.nbkVerwaltung, text='Verwaltung')
                        # Farben - Einzelheiten
                        with CtxPanedWindow(self.nbkVerwaltung, orient=tk.HORIZONTAL) \
                                as self.pndFarben:
                            self.nbkVerwaltung.add(self.pndFarben, text='Farben')
                            # Frames für Navi und Daten
                            self.frmFarbenNavi = ttk.Frame(self.pndFarben)
                            self.frmFarbenDaten = ttk.Frame(self.pndFarben)
                            self.pndFarben.add(self.frmFarbenNavi)
                            self.pndFarben.add(self.frmFarbenDaten)
                        # Länder
                        with CtxFrame(self.nbkVerwaltung) as self.frmLaenderListe:
                            self.nbkVerwaltung.add(self.frmLaenderListe, text='Länder')
                            # Frames für Navi und Liste
                            self.frmLaenderListeNavi = ttk.Frame(self.frmLaenderListe)
                            self.frmLaenderListeInhalt = yScrolledFrame(self.frmLaenderListe)
                            self.frmLaenderListeNavi.pack(
                                side=tk.TOP,
                                anchor=tk.W)
                            self.frmLaenderListeInhalt.pack(
                                side=tk.TOP,
                                expand=tk.YES,
                                fill=tk.BOTH)
                        # Regelmäßige Aufgaben - Einzelheiten
                        with CtxPanedWindow(self.nbkVerwaltung, orient=tk.HORIZONTAL) \
                                as self.frmJobsEinzel:
                            self.nbkVerwaltung.add(self.frmJobsEinzel, text='Jobs')
                            # Frames für Navi und Formular bauen und in PanedWindow einsetzen
                            self.frmJobsEinzelNavi = ttk.Frame(self.frmJobsEinzel)
                            self.frmJobsEinzelDaten = ttk.Frame(self.frmJobsEinzel)
                            self.frmJobsEinzel.add(self.frmJobsEinzelNavi)
                            self.frmJobsEinzel.add(self.frmJobsEinzelDaten)
                        # Regelmäßige Aufgaben - Liste
                        with CtxFrame(self.nbkVerwaltung) as self.frmJobsListe:
                            self.nbkVerwaltung.add(self.frmJobsListe, text='Jobs (Liste)')
                            # Frames für Navi und Liste
                            self.frmJobsListeNavi = ttk.Frame(self.frmJobsListe)
                            self.frmJobsListeInhalt = yScrolledFrame(self.frmJobsListe)
                            self.frmJobsListeNavi.pack(
                                side=tk.TOP,
                                anchor=tk.W)
                            self.frmJobsListeInhalt.pack(
                                side=tk.TOP,
                                expand=tk.YES,
                                fill=tk.BOTH)
                        # Status - Liste
                        with CtxFrame(self.nbkVerwaltung) as self.frmStatusListe:
                            self.nbkVerwaltung.add(self.frmStatusListe, text='Status (Liste)')
                            # Frames für Navi und Liste
                            self.frmStatusListeNavi = ttk.Frame(self.frmStatusListe)
                            self.frmStatusListeInhalt = yScrolledFrame(self.frmStatusListe)
                            self.frmStatusListeNavi.pack(
                                side=tk.TOP,
                                anchor=tk.W)
                            self.frmStatusListeInhalt.pack(
                                side=tk.TOP,
                                expand=tk.YES,
                                fill=tk.BOTH)
                    # Notebook Tagungen
                    with CtxNotebook(self.nbkMain) as self.nbkTg:
                        self.nbkMain.add(self.nbkTg, text='Tagungen')
                        with CtxPanedWindow(self.nbkTg, orient=tk.HORIZONTAL) as self.pndTgEinzel:
                            self.nbkTg.add(self.pndTgEinzel, text='Stammdaten')
                        with CtxPanedWindow(self.nbkTg, orient=tk.HORIZONTAL) as self.pndTgMails:
                            self.nbkTg.add(self.pndTgMails, text='Mails')
            #
            # Fuß Frame
            with CtxFrame(self.pndHauptUndFuss) as self.frmBottom:
                self.pndHauptUndFuss.add(self.frmBottom)
        
def main():
    configuration()
    
    hauptprogramm = Hauptprogramm()
    hauptprogramm.mainloop()

if __name__ == '__main__':
    main()
