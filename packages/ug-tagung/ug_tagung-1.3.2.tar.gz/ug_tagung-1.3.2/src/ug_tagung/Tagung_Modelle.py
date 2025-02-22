from ugbib_modell.bibModell import *

#######################################################################
# Modelle Anwendungsübergreifend (Regelmäßige Aufgaben, Länder usw.)
#######################################################################

###   Jobs - Public (regelmäßige Aufgaben, insb. Auswertungen
class Jobs(Modell):
    
    # Tabellen
    _tab = 'tbl_jobs'
    
    # Felder
    _felder = [
        idFeld('id'),
        textFeld('titel'),
        # Angaben zum eigentlichen Programm
        textFeld('kommando'),
        textFeld('verzeichnis'),
        textFeld('beschreibung'),
        # Steuerung
        numFeld('intervall'),
        textFeld('einheit'),
        boolFeld('sofort'),
        boolFeld('aktiv'),
        boolFeld('gestoppt'),
        boolFeld('selbstzerstoerend'),
        ]
    
    keyFeldNavi = 'id'
        
    # Relationen
    _relationen = {}
  
    def __init__(self, id=None, holen=False):
        super().__init__(id=id, holen=holen)

    def __str__(self):
        return '{}'.format(self.titel)

class JobsListe(Modell):
    
    # Tabellen
    _tab = 'tbl_jobs'
    
    # Felder
    _felder = [
        idFeld('id'),
        textFeld('titel'),
        # Steuerung
        textFeld('kommando'),
        numFeld('intervall'),
        textFeld('einheit'),
        boolFeld('sofort'),
        boolFeld('aktiv'),
        boolFeld('gestoppt'),
        ]
    
    keyFeldNavi = 'id'
        
    # Relationen
    _relationen = {}
  
    def __init__(self, id=None, holen=False):
        super().__init__(id=id, holen=holen)

    def __str__(self):
        return '{}'.format(self.titel)

#######################################################################
# Hilfs-Modelle
#######################################################################

###   Tagung - Public
class Tagung(Modell):
    
    # Tabellen
    _tab = 'tbl_tagung'
    
    # Felder
    _felder = [
        idFeld('id'),
        textFeld('kurz_bez'),
        # Kontaktdaten
        textFeld('titel'),
        textFeld('beschreibung'),
        textFeld('ort'),
        dateFeld('dat_beginn'),
        dateFeld('dat_ende'),
        # Weiteres, u.a. zur DB, Mailserver usw.
        boolFeld('aktiv'),
        textFeld('rel_verz'),
        textFeld('mail_from'),
        textFeld('mail_reply'),
        textFeld('schema'),
        # Verwaltung des Datensatzes
        textFeld('bearb_von'),
        datetimeFeld('bearb_am'),
        datetimeFeld('bearb_auto'),
        ]
    
    keyFeldNavi = 'id'
        
    # Relationen
    _relationen = {}
  
    def __init__(self, id=None, holen=False):
        super().__init__(id=id, holen=holen)

    def __str__(self):
        return '{}'.format(self.kurz_bez)

###   Farbe - Public
class Farbe(Modell):
    # Tabellen
    _tab = 'tbl_farben'
    
    # Felder
    _felder = [
        idFeld('id'),
        textFeld('farbe'),
        # Verwaltung des Datensatzes
        textFeld('bearb_von'),
        datetimeFeld('bearb_am'),
        datetimeFeld('bearb_auto'),
        ]
    keyFeldNavi = 'id'
        
    # Relationen
    _relationen = {}
  
    def __init__(self, id=None, holen=False):
        super().__init__(id=id, holen=holen)

    def __str__(self):
        return '{}'.format(self.farbe)

###   Farbe Liste - Public
class FarbeListe(Modell):
    # Tabellen
    _tab = 'tbl_farben'
    
    # Felder
    _felder = [
        idFeld('id'),
        textFeld('farbe'),
        ]
    keyFeldNavi = 'id'
        
    # Relationen
    _relationen = {}
  
    def __init__(self, id=None, holen=False):
        super().__init__(id=id, holen=holen)

    def __str__(self):
        return '{}'.format(self.farbe)

###   Länder - Public
class Laender(Modell):
    # Tabellen
    _tab = 'tbl_laender'
    
    # Felder
    _felder = [
        idFeld('id'),
        textFeld('land'),
        textFeld('land_kurz'),
        boolFeld('prototyp'),
        ]
    keyFeldNavi = 'id'
        
    # Relationen
    _relationen = {}
  
    def __init__(self, id=None, holen=False):
        super().__init__(id=id, holen=holen)

    def __str__(self):
        return '{}: {}'.format(self.land_kurz, self.land)

###   Gruppe - entspricht Rollen
class Gruppe(Modell):
    # Tabelle und Felder
    _tab = 'tbl_gruppen'
    _felder = [
        idFeld('id'),
        textFeld('kurz_bez'),
        textFeld('bez'),
        textFeld('farbe'),
        textFeld('bemerkung'),
        # Verwaltung des Datensatzes
        textFeld('bearb_von'),
        datetimeFeld('bearb_am'),
        datetimeFeld('bearb_auto'),
        ]
    
    keyFeldNavi = 'id'
        
    # Relationen
    R_farbe = Relation('farbe', Farbe, 'farbe')
    R_farbe.setSQLsort('order by farbe')
    _relationen = {'farbe': R_farbe}
    
    def __init__(self, id=None, holen=False):
        super().__init__(id=id, holen=holen)
    
    def __str__(self):
        return '{}: {}'.format(self.kurz_bez, self.bez)

class GruppeListe(Modell):
    # Tabelle und Felder
    _tab = 'tbl_gruppen'
    _felder = [
        idFeld('id'),
        textFeld('kurz_bez'),
        textFeld('bez'),
        textFeld('farbe'),
        ]
    
    keyFeldNavi = 'id'
        
    # Relationen
    R_farbe = Relation('farbe', Farbe, 'farbe')
    R_farbe.setSQLsort('order by farbe')
    _relationen = {'farbe': R_farbe}
    
    def __init__(self, id=None, holen=False):
        super().__init__(id=id, holen=holen)
    
    def __str__(self):
        return '{}: {}'.format(self.kurz_bez, self.bez)

###   Mailart
class Mailart(Modell):
    # Tabelle
    _tab = 'tbl_mail_art'
    
    # Felder
    _felder = [
        idFeld('id'),
        textFeld('kurz_bez'),
        textFeld('bez'),
        textFeld('bemerkung'),
        # Verwaltung des Datensatzes
        textFeld('bearb_von'),
        datetimeFeld('bearb_am'),
        datetimeFeld('bearb_auto'),
        ]
    
    keyFeldNavi = 'id'
        
    # Relationen
    _relationen = {}
  
    def __init__(self, id=None, holen=False):
        super().__init__(id=id, holen=holen)

    def __str__(self):
        return '{} ({})'.format(self.kurz_bez, self.bez)

###   Quartierart
class Quartierart(Modell):
    # Tabelle
    _tab = 'tbl_quartier_art'
    
    # Felder
    _felder = [
        idFeld('id'),
        textFeld('kurz_bez'),
        textFeld('bez'),
        textFeld('bemerkung'),
        # Verwaltung des Datensatzes
        textFeld('bearb_von'),
        datetimeFeld('bearb_am'),
        datetimeFeld('bearb_auto'),
        ]
    
    keyFeldNavi = 'id'
        
    # Relationen
    _relationen = {}
  
    def __init__(self, id=None, holen=False):
        super().__init__(id=id, holen=holen)

    def __str__(self):
        return '{} ({})'.format(self.kurz_bez, self.bez)

###   Raumart
class Raumart(Modell):
    # Tabelle
    _tab = 'tbl_raum_art'
    
    # Felder
    _felder = [
        idFeld('id'),
        textFeld('kurz_bez'),
        textFeld('beschreibung'),
        textFeld('bemerkung'),
        # Verwaltung des Datensatzes
        textFeld('bearb_von'),
        datetimeFeld('bearb_am'),
        datetimeFeld('bearb_auto'),
        ]
    
    keyFeldNavi = 'id'
        
    # Relationen
    _relationen = {}
  
    def __init__(self, id=None, holen=False):
        super().__init__(id=id, holen=holen)

    def __str__(self):
        return '{} ({})'.format(self.kurz_bez, self.bez)

###   Veranstaltungsart
class Veranstaltungart(Modell):
    # Tabelle
    _tab = 'tbl_veranstaltung_art'
    
    # Felder
    _felder = [
        idFeld('id'),
        textFeld('kurz_bez'),
        textFeld('beschreibung'),
        textFeld('bemerkung'),
        # Verwaltung des Datensatzes
        textFeld('bearb_von'),
        datetimeFeld('bearb_am'),
        datetimeFeld('bearb_auto'),
        ]
    
    keyFeldNavi = 'id'
        
    # Relationen
    _relationen = {}
  
    def __init__(self, id=None, holen=False):
        super().__init__(id=id, holen=holen)

    def __str__(self):
        return '{} ({})'.format(self.kurz_bez, self.bez)

###   Status
class Status(Modell):
    # Tabelle
    _tab = 'tbl_status'
    
    # Felder
    _felder = [
        idFeld('id'),
        textFeld('kurz_bez'),
        textFeld('bez'),
        textFeld('farbe'),
        boolFeld('mail_ausloesen'),
        textFeld('mail_art'),
        textFeld('nachfolge_status'),
        textFeld('bemerkung'),
        # Verwaltung des Datensatzes
        textFeld('bearb_von'),
        datetimeFeld('bearb_am'),
        datetimeFeld('bearb_auto'),
        ]
    
    keyFeldNavi = 'id'
    
    # Relationen
    R_farbe = Relation('farbe', Farbe, 'farbe')
    R_farbe.setSQLsort('order by farbe')
    
    R_mail_art = Relation('mail_art', Mailart, 'kurz_bez')
    R_mail_art.setSQLsort('order by kurz_bez')
    
    _relationen = {
        'farbe': R_farbe,
        'mail_art': R_mail_art,
        }
  
    def __init__(self, id=None, holen=False):
        super().__init__(id=id, holen=holen)
    
    def __str__(self):
        return '{}: {}'.format(self.kurz_bez, self.bez)

R_nachfolge_status = Relation('nachfolge_status', Status, 'kurz_bez')
R_nachfolge_status.setSQLsort('order by kurz_bez')
Modell.addRelation(Status, 'nachfolge_status',  R_nachfolge_status)

###   Status Liste
class StatusListe(Modell):
    # Tabelle
    _tab = 'tbl_status'
    
    # Felder
    _felder = [
        idFeld('id'),
        textFeld('kurz_bez'),
        textFeld('bez'),
        textFeld('farbe'),
        boolFeld('mail_ausloesen'),
        textFeld('mail_art'),
        textFeld('nachfolge_status'),
        ]
    
    keyFeldNavi = 'id'
    
    # Relationen
    R_farbe = Relation('farbe', Farbe, 'farbe')
    R_farbe.setSQLsort('order by farbe')
    
    R_mail_art = Relation('mail_art', Mailart, 'kurz_bez')
    R_mail_art.setSQLsort('order by kurz_bez')
    
    R_nachfolge_status = Relation('nachfolge_status', Status, 'kurz_bez')
    R_nachfolge_status.setSQLsort('order by kurz_bez')
    
    _relationen = {
        'farbe': R_farbe,
        'mail_art': R_mail_art,
        'nachfolge_status': R_nachfolge_status
        }
  
    def __init__(self, id=None, holen=False):
        super().__init__(id=id, holen=holen)
    
    def __str__(self):
        return '{}: {}'.format(self.kurz_bez, self.bez)

#######################################################################
# Haupt-Modelle
#######################################################################

###   Quartier
class Quartier(Modell):
    # Tabelle
    _tab = 'tbl_quartier'
    
    # Felder
    _felder = [
        idFeld('id'),
        # Identität
        numFeld('person_id'),
        numFeld('institution_id'),
        # Beschreibung
        textFeld('quartier_art'),
        numFeld('anzahl'),
        textFeld('beschreibung'),
        # Bemerkung
        textFeld('bemerkung'),
        # Verwaltung des Datensatzes
        textFeld('bearb_von'),
        datetimeFeld('bearb_am'),
        datetimeFeld('bearb_auto'),
        ]
    
    keyFeldNavi = 'id'
    
    # Relationen
    _relationen = {}
  
    def __init__(self, id=None, holen=False):
        super().__init__(id=id, holen=holen)
    
    def __str__(self):
        return '{}, Pers: {}, Inst: {}'.format(self.quartier_art, self.person_id, self.institution_id)

###   Person
class Person(Modell):
    # Tabelle
    _tab = 'tbl_person'
    
    # Felder
    _felder = [
        idFeld('id'),
        # Identität
        textFeld('name'),
        textFeld('vorname'),
        dateFeld('gebdat'),
        textFeld('geschlecht'),
        # Kontaktdaten
        textFeld('strasse'),
        textFeld('plz'),
        textFeld('ort'),
        textFeld('land'),
        textFeld('land_kurz'),
        textFeld('email'),
        textFeld('tel_heimat'),
        textFeld('tel_mobil'),
        # Relevant für Gruppen
        boolFeld('g_ansprechpartner'),
        textFeld('g_beschreibung'),
        numFeld('g_anzahl'),
        numFeld('g_ansprechpartner_id'),
        # Relevant für Kinder
        textFeld('ki_bezugsperson'),
        numFeld('ki_bezugsperson_id'),
        # Relevant für Tagung
        textFeld('aufgabe'),
        textFeld('sprachen'),
        boolFeld('vegetarier'),
        boolFeld('vegan'),
        boolFeld('glutenfrei'),
        boolFeld('lactosefrei'),
        textFeld('ws_a'),
        textFeld('ws_b'),
        textFeld('ws_c'),
        textFeld('ws_d'),
        numFeld('beitr_anm'),
        numFeld('beitr_erm'),
        numFeld('beitr_gez'),
        dateFeld('beitr_dat'),
        textFeld('nachricht'),
        textFeld('bemerkung'),
        # Relevant für Quartiergeber
        textFeld('opnv_anbindung'),
        numFeld('zeit_opnv'),
        boolFeld('auto_vorhanden'),
        numFeld('zeit_auto'),
        # Relevant für Quartiernehmer
        boolFeld('q_wuenscht_vermittlung'),
        textFeld('q_wunsch'),
        numFeld('q_id'),
        numFeld('q_zu_zahlen'),
        numFeld('q_bezahlt'),
        # Anmeldedaten
        datetimeFeld('anm_am_um'),
        textFeld('status'),
        datetimeFeld('status_gesetzt_am'),
        # Verwaltung des Datensatzes
        textFeld('bearb_von'),
        datetimeFeld('bearb_am'),
        datetimeFeld('bearb_auto'),
        ]
    
    keyFeldNavi = 'id'
    
    # Relationen
    R_q_id = Relation('q_id', Quartier, 'id')
    R_q_id.setSQLanzeige("name || ', ' || vorname || '(' || ort || ')'")
    R_q_id.setSQLsort('order by name, vorname')
    
    R_status = Relation('status', Status, 'kurz_bez')
    R_status.setSQLanzeige("kurz_bez || ' (' || bez || ')'")
    R_status.setSQLsort('order by kurz_bez')
    
    _relationen = {
        'q_id': R_q_id,
        'status': R_status
        }
  
    def __init__(self, id=None, holen=False):
        super().__init__(id=id, holen=holen)
    
    def __str__(self):
        return '{}, {} ({})'.format(self.name, self.vorname, self.ort)

R_g_ansprechpartner_id = Relation('g_ansprechpartner_id', Person, 'id')
R_g_ansprechpartner_id.setSQLanzeige("name || ', ' || vorname || '(' || ort || ')'")
R_g_ansprechpartner_id.setSQLsort('order by name, vorname')
Modell.addRelation(Person, 'g_ansprechpartner_id', R_g_ansprechpartner_id)
R_ki_bezugsperson_id = Relation('ki_bezugsperson_id', Person, 'id')
R_ki_bezugsperson_id.setSQLanzeige("name || ', ' || vorname || ' (' || ort || ')'")
R_ki_bezugsperson_id.setSQLsort('order by name, vorname')
Modell.addRelation(Person, 'g_ki_bezugsperson_id', R_ki_bezugsperson_id)

###   Person Jugendtagung
class PersonJugend(Modell):
    # Tabelle
    _tab = 'tbl_person'
    
    # Felder
    _felder = [
        idFeld('id'),
        # Identität
        textFeld('name'),
        textFeld('vorname'),
        dateFeld('gebdat'),
        textFeld('geschlecht'),
        # Kontaktdaten
        textFeld('strasse'),
        textFeld('plz'),
        textFeld('ort'),
        textFeld('land'),
        textFeld('land_kurz'),
        textFeld('email'),
        textFeld('tel_heimat'),
        textFeld('tel_mobil'),
        # Relevant für Gruppen
        boolFeld('g_ansprechpartner'),
        textFeld('g_beschreibung'),
        numFeld('g_anzahl'),
        numFeld('g_ansprechpartner_id'),
        # Relevant für Tagung
        textFeld('aufgabe'),
        textFeld('sprachen'),
        boolFeld('vegetarier'),
        boolFeld('vegan'),
        boolFeld('glutenfrei'),
        boolFeld('lactosefrei'),
        textFeld('ws_a'),
        textFeld('ws_b'),
        textFeld('ws_c'),
        textFeld('ws_d'),
        numFeld('beitr_anm'),
        numFeld('beitr_erm'),
        numFeld('beitr_gez'),
        dateFeld('beitr_dat'),
        textFeld('nachricht'),
        textFeld('bemerkung'),
        # Anmeldedaten
        datetimeFeld('anm_am_um'),
        textFeld('status'),
        datetimeFeld('status_gesetzt_am'),
        # Verwaltung des Datensatzes
        textFeld('bearb_von'),
        datetimeFeld('bearb_am'),
        datetimeFeld('bearb_auto'),
        ]
    
    keyFeldNavi = 'id'
    
    # Relationen
    R_status = Relation('status', Status, 'kurz_bez')
    R_status.setSQLanzeige("kurz_bez || ' (' || bez || ')'")
    R_status.setSQLsort('order by kurz_bez')
    
    _relationen = {
        'status': R_status,
        }
  
    def __init__(self, id=None, holen=False):
        super().__init__(id=id, holen=holen)
    
    def __str__(self):
        return '{}, {} ({})'.format(self.name, self.vorname, self.ort)

R_g_ansprechpartner_id = Relation('g_ansprechpartner_id', PersonJugend, 'id')
R_g_ansprechpartner_id.setSQLanzeige("name || ', ' || vorname || '(' || id || ', ' || ort || ')'")
R_g_ansprechpartner_id.setSQLsort('order by name, vorname')
Modell.addRelation(PersonJugend, 'g_ansprechpartner_id', R_g_ansprechpartner_id)

###   Person Status (Zur Bearbeitung des Anmelde-Status)
class PersonStatus(Modell):
    # Tabelle
    _tab = 'tbl_person'
    
    # Felder
    _felder = [
        idFeld('id'),
        # Identität
        textFeld('name'),
        textFeld('vorname'),
        dateFeld('gebdat'),
        textFeld('geschlecht'),
        # Kontaktdaten
        textFeld('ort'),
        textFeld('land'),
        textFeld('email'),
        numFeld('beitr_anm'),
        textFeld('nachricht'),
        # Anmeldedaten
        textFeld('status'),
        ]
    
    keyFeldNavi = 'id'
    
    # Relationen
    R_status = Relation('status', Status, 'kurz_bez')
    R_status.setSQLanzeige("kurz_bez || ' (' || bez || ')'")
    R_status.setSQLsort('order by kurz_bez')
    
    _relationen = {
        'status': R_status
        }
  
    def __init__(self, id=None, holen=False):
        super().__init__(id=id, holen=holen)
    
    def __str__(self):
        return '{}, {} ({})'.format(self.name, self.vorname, self.ort)

###   Person Finanzen (Zur Bearbeitung der Ermäßigungen und Zahlungen)
class PersonFinanzen(Modell):
    # Tabelle
    _tab = 'tbl_person'
    
    # Felder
    _felder = [
        idFeld('id'),
        # Identität
        textFeld('name'),
        textFeld('vorname'),
        # Kontaktdaten
        textFeld('ort'),
        textFeld('land_kurz'),
        textFeld('email'),
        # Relevant für Tagung
        numFeld('beitr_anm'),
        numFeld('beitr_erm'),
        numFeld('beitr_gez'),
        dateFeld('beitr_dat'),
        textFeld('bemerkung'),
        # Anmeldedaten
        textFeld('status'),
        # Verwaltung des Datensatzes
        textFeld('bearb_von'),
        datetimeFeld('bearb_am'),
        datetimeFeld('bearb_auto'),
        ]
    
    keyFeldNavi = 'id'
    
    # Relationen
    R_status = Relation('status', Status, 'kurz_bez')
    R_status.setSQLanzeige("kurz_bez || ' (' || bez || ')'")
    R_status.setSQLsort('order by kurz_bez')
    
    _relationen = {
        'status': R_status
        }
  
    def __init__(self, id=None, holen=False):
        super().__init__(id=id, holen=holen)
    
    def __str__(self):
        return '{}, {} ({})'.format(self.name, self.vorname, self.ort)

###   Person Finanzen (Zur Bearbeitung der Ermäßigungen und Zahlungen)
class PersonFinanzenListe(Modell):
    # Tabelle
    _tab = 'tbl_person'
    
    # Felder
    _felder = [
        idFeld('id'),
        # Identität
        textFeld('name'),
        textFeld('vorname'),
        # Kontaktdaten
        textFeld('ort'),
        # Relevant für Tagung
        numFeld('beitr_anm'),
        numFeld('beitr_erm'),
        numFeld('beitr_gez'),
        dateFeld('beitr_dat'),
        textFeld('bemerkung'),
        # Anmeldedaten
        textFeld('status'),
        ]
    
    keyFeldNavi = 'id'
    
    # Relationen
    R_status = Relation('status', Status, 'kurz_bez')
    R_status.setSQLanzeige("kurz_bez || ' (' || bez || ')'")
    R_status.setSQLsort('order by kurz_bez')
    
    _relationen = {
        'status': R_status
        }
  
    def __init__(self, id=None, holen=False):
        super().__init__(id=id, holen=holen)
    
    def __str__(self):
        return '{}, {} ({})'.format(self.name, self.vorname, self.ort)

###   Person WS-Anm zuordnen (Zum finden von Personen für WS-Anmeldungen)
class PersonWSAnmListe(Modell):
    # Tabelle
    _tab = 'tbl_person'
    
    # Felder
    _felder = [
        idFeld('id'),
        # Identität
        textFeld('name'),
        textFeld('vorname'),
        # Kontaktdaten
        textFeld('email'),
        textFeld('ort'),
        ]
    
    keyFeldNavi = 'id'
    
    # Relationen
    
    _relationen = {}
  
    def __init__(self, id=None, holen=False):
        super().__init__(id=id, holen=holen)
    
    def __str__(self):
        return '{}, {} ({})'.format(self.name, self.vorname, self.ort)

###   Person WS (Zum festlegen der WSs für Personen)
class PersonWSListe(Modell):
    # Tabelle
    _tab = 'tbl_person'
    
    # Felder
    _felder = [
        idFeld('id'),
        # Identität
        textFeld('name'),
        textFeld('vorname'),
        textFeld('ort'),
        # WSs
        textFeld('ws_a'),
        textFeld('ws_b'),
        textFeld('ws_c'),
        textFeld('ws_d'),
        ]
    
    keyFeldNavi = 'id'
    
    # Relationen
    
    _relationen = {}
  
    def __init__(self, id=None, holen=False):
        super().__init__(id=id, holen=holen)
    
    def __str__(self):
        return '{}, {} ({})'.format(self.name, self.vorname, self.ort)

###   Institution
class Institution(Modell):
    # Tabelle
    _tab = 'tbl_institution'
    
    # Felder
    _felder = [
        idFeld('id'),
        # Identität
        textFeld('bez_i'),
        textFeld('bez_ii'),
        textFeld('ansprechpartner'),
        # Kontaktdaten
        textFeld('strasse'),
        textFeld('plz'),
        textFeld('ort'),
        textFeld('land'),
        textFeld('land_kurz'),
        textFeld('email'),
        textFeld('kontaktdaten'),
        # Bemerkung
        textFeld('nachricht'),
        textFeld('bemerkung'),
        # Relevant für Quartiergeber
        textFeld('opnv_anbindung'),
        numFeld('zeit_opnv'),
        boolFeld('auto_vorhanden'),
        numFeld('zeit_auto'),
        boolFeld('abrechnung_tb'),
        # Verwaltung des Datensatzes
        textFeld('bearb_von'),
        datetimeFeld('bearb_am'),
        datetimeFeld('bearb_auto'),
        ]
    
    keyFeldNavi = 'id'
    
    # Relationen
    _relationen = {}
  
    def __init__(self, id=None, holen=False):
        super().__init__(id=id, holen=holen)
    
    def __str__(self):
        return '{}, {}'.format(self.bez_i, self.bez_ii)

###   Institution Jugend
class InstitutionJugend(Modell):
    # Tabelle
    _tab = 'tbl_institution'
    
    # Felder
    _felder = [
        idFeld('id'),
        # Identität
        textFeld('bez_i'),
        textFeld('bez_ii'),
        textFeld('ansprechpartner'),
        # Kontaktdaten
        textFeld('strasse'),
        textFeld('plz'),
        textFeld('ort'),
        textFeld('land'),
        textFeld('land_kurz'),
        textFeld('email'),
        textFeld('kontaktdaten'),
        # Bemerkung
        textFeld('nachricht'),
        textFeld('bemerkung'),
        # Relevant für Quartiergeber
        textFeld('opnv_anbindung'),
        numFeld('zeit_opnv'),
        boolFeld('auto_vorhanden'),
        numFeld('zeit_auto'),
        boolFeld('abrechnung_tb'),
        # Verwaltung des Datensatzes
        textFeld('bearb_von'),
        datetimeFeld('bearb_am'),
        datetimeFeld('bearb_auto'),
        ]
    
    keyFeldNavi = 'id'
    
    # Relationen
    _relationen = {}
  
    def __init__(self, id=None, holen=False):
        super().__init__(id=id, holen=holen)
    
    def __str__(self):
        return '{}, {}'.format(self.bez_i, self.bez_ii)

###   Veranstaltung
class Veranstaltung(Modell):
    # Tabelle
    _tab = 'tbl_veranstaltung'
    
    # Felder
    _felder = [
        idFeld('id'),
        # Identität
        textFeld('art'),
        textFeld('nr'),
        # Angaben zur Veranstaltung
        textFeld('titel'),
        textFeld('untertitel'),
        textFeld('beschreibung'),
        numFeld('tn_min'),
        numFeld('tn_max'),
        numFeld('alter_min'),
        numFeld('alter_max'),
        textFeld('sprachen'),
        textFeld('bedingungen'),
        boolFeld('anmeldepflicht'),
        numFeld('honorar'),
        numFeld('sachkosten'),
        # Bemerkung
        textFeld('bemerkung'),
        # Verwaltung des Datensatzes
        textFeld('bearb_von'),
        datetimeFeld('bearb_am'),
        datetimeFeld('bearb_auto'),
        ]
    
    keyFeldNavi = 'id'
    
    # Relationen
    R_art = Relation('art', Veranstaltungart, 'kurz_bez')
    R_art.setSQLanzeige("kurz_bez || ' (' || beschreibung || ')'")
    R_art.setSQLsort('order by kurz_bez')
    
    _relationen = {'art': R_art}
  
    def __init__(self, id=None, holen=False):
        super().__init__(id=id, holen=holen)
    
    def __str__(self):
        return '{} ({})'.format(self.kurz_bez, self.beschreibung)

###   Raum
class Raum(Modell):
    # Tabelle
    _tab = 'tbl_raum'
    
    # Felder
    _felder = [
        idFeld('id'),
        # Identität
        textFeld('kurz_bez'),
        textFeld('bezeichnung'),
        # Angaben zum Raum
        textFeld('art'),
        numFeld('plaetze_normal'),
        boolFeld('moebel_variabel'),
        numFeld('qm'),
        textFeld('beschreibung'),
        boolFeld('deaktiviert'),
        # Bemerkung
        textFeld('bemerkung'),
        # Verwaltung des Datensatzes
        textFeld('bearb_von'),
        datetimeFeld('bearb_am'),
        datetimeFeld('bearb_auto'),
        ]
    
    keyFeldNavi = 'id'
    
    # Relationen
    R_art = Relation('art', Raumart, 'kurz_bez')
    R_art.setSQLanzeige("kurz_bez || ' (' || beschreibung || ')'")
    R_art.setSQLsort('order by kurz_bez')
    
    _relationen = {'art': R_art}
  
    def __init__(self, id=None, holen=False):
        super().__init__(id=id, holen=holen)
    
    def __str__(self):
        return '{} ({})'.format(self.kurz_bez, self.bez)

###   Mail
class Mail(Modell):
    # Tabelle
    _tab = 'tbl_mail'
    
    # Felder
    _felder = [
        idFeld('id'),
        textFeld('art'),
        # Mail
        boolFeld('aktuell'),
        textFeld('betreff'),
        textFeld('text_vj'),    # volljährig
        textFeld('text_mj'),    # minderjährig
        textFeld('text_kf'),    # Kinder-Freizeit
        textFeld('text_kb'),    # Kinder-Betreuung
        textFeld('anhang_vj'),
        textFeld('anhang_mj'),
        textFeld('anhang_kf'),
        textFeld('anhang_kb'),
        # Bemerkung
        textFeld('bemerkung'),
        # Verwaltung des Datensatzes
        textFeld('bearb_von'),
        datetimeFeld('bearb_am'),
        datetimeFeld('bearb_auto'),
        ]
    
    keyFeldNavi = 'id'
    
    # Relationen
    R_art = Relation('art', Mailart, 'kurz_bez')
    R_art.setSQLanzeige("kurz_bez || ' (' || bez || ')'")
    R_art.setSQLsort('order by kurz_bez')
    
    _relationen = {'art': R_art}
  
    def __init__(self, id=None, holen=False):
        super().__init__(id=id, holen=holen)
    
    def __str__(self):
        return '{} ({}): {}'.format(self.art, self.aktuell, self.betreff)

#######################################################################
# Beziehungen (n-n-Relationen)
#######################################################################

###   Person - Gruppe
class PersonGruppe(Modell):
    # Tabelle
    _tab = 'tbl_person_gruppe'
    
    # Felder
    _felder = [
        idFeld('id'),
        numFeld('person_id'),
        textFeld('gruppe_kurz_bez'),
        # Verwaltung des Datensatzes
        textFeld('bearb_von'),
        datetimeFeld('bearb_am'),
        datetimeFeld('bearb_auto'),
        ]
    
    keyFeldNavi = 'id'
        
    # Relationen
    R_person = Relation('person_id', Person, 'id')
    R_person.setSQLanzeige("name || ', ' || vorname")
    R_person.setSQLsort('order by name, vorname')
    
    R_gruppe = Relation('gruppe_kurz_bez', Gruppe, 'kurz_bez')
    R_gruppe.setSQLanzeige("kurz_bez || ': ' || bez")
    R_gruppe.setSQLsort('order by kurz_bez')
    
    _relationen = {
        'person': R_person,
        'gruppe': R_gruppe,
        }
  
    def __init__(self, id=None, holen=False):
        super().__init__(id=id, holen=holen)
    
    def __str__(self):
        return "{}: {}".format(self.person_id, self.gruppe_kurz_bez)

class PersonGruppeListe(Modell):
    # Tabelle
    _tab = 'tbl_person_gruppe'
    
    # Felder
    _felder = [
        idFeld('id'),
        numFeld('person_id'),
        textFeld('gruppe_kurz_bez'),
        ]
    
    keyFeldNavi = 'id'
        
    # Relationen
    R_person = Relation('person_id', Person, 'id')
    R_person.setSQLanzeige("name || ', ' || vorname")
    R_person.setSQLsort('order by name, vorname')
    
    R_gruppe = Relation('gruppe_kurz_bez', Gruppe, 'kurz_bez')
    R_gruppe.setSQLanzeige("kurz_bez || ': ' || bez")
    R_gruppe.setSQLsort('order by kurz_bez')
    
    _relationen = {
        'person': R_person,
        'gruppe_kurz_bez': R_gruppe,
        }
  
    def __init__(self, id=None, holen=False):
        super().__init__(id=id, holen=holen)
    
    def __str__(self):
        return "{}: {}".format(self.person_id, self.gruppe_kurz_bez)

###   Institution - Gruppe
class InstitutionGruppe(Modell):
    # Tabelle
    _tab = 'tbl_institution_gruppe'
    
    # Felder
    _felder = [
        idFeld('id'),
        numFeld('institution_id'),
        textFeld('gruppe_kurz_bez'),
        # Verwaltung des Datensatzes
        textFeld('bearb_von'),
        datetimeFeld('bearb_am'),
        datetimeFeld('bearb_auto'),
        ]
    
    keyFeldNavi = 'id'
    
    # Relationen
    R_institution = Relation('institution_id', Institution, 'id')
    R_institution.setSQLanzeige("bez_i || ', ' || bez_ii")
    R_institution.setSQLsort('order by bez_i')
    
    R_gruppe = Relation('gruppe_kurz_bez', Gruppe, 'kurz_bez')
    R_gruppe.setSQLanzeige("kurz_bez || ': ' || bez")
    R_gruppe.setSQLsort('order by kurz_bez')
    
    _relationen = {
        'institution_id': R_institution,
        'gruppe':  R_gruppe,
        }
  
    def __init__(self, id=None, holen=False):
        super().__init__(id=id, holen=holen)
    
    def __str__(self):
        return "{}: {}".format(self.institution_id, self.gruppe_kurz_bez)

class InstitutionGruppeListe(Modell):
    # Tabelle
    _tab = 'tbl_institution_gruppe'
    
    # Felder
    _felder = [
        idFeld('id'),
        numFeld('institution_id'),
        textFeld('gruppe_kurz_bez'),
        ]
    
    keyFeldNavi = 'id'
    
    # Relationen
    R_institution = Relation('institution_id', Institution, 'id')
    R_institution.setSQLanzeige("bez_i || ', ' || bez_ii")
    R_institution.setSQLsort('order by bez_i')
    
    R_gruppe = Relation('gruppe_kurz_bez', Gruppe, 'kurz_bez')
    R_gruppe.setSQLanzeige("kurz_bez || ': ' || bez")
    R_gruppe.setSQLsort('order by kurz_bez')
    
    _relationen = {
        'institution_id': R_institution,
        'gruppe':  R_gruppe,
        }
  
    def __init__(self, id=None, holen=False):
        super().__init__(id=id, holen=holen)
    
    def __str__(self):
        return "{}: {}".format(self.institution_id, self.gruppe_kurz_bez)

###   Dozent
class Dozent(Modell):
    # Tabelle
    _tab = 'tbl_dozent'
    
    # Felder
    _felder = [
        idFeld('id'),
        numFeld('person_id'),
        numFeld('veranstaltung_id'),
        textFeld('funktion'),
        textFeld('bemerkung'),
        # Verwaltung des Datensatzes
        textFeld('bearb_von'),
        datetimeFeld('bearb_am'),
        datetimeFeld('bearb_auto'),
        ]
        
    keyFeldNavi = 'id'
    
    # Relationen
    R_person = Relation('person_id', Person, 'id')
    R_person.setSQLanzeige("name || ', ' || vorname")
    R_person.setSQLsort('order by name, vorname')
    
    R_veranstaltung = Relation('veranstaltung_id', Veranstaltung, 'id')
    R_veranstaltung.setSQLanzeige("art || '-' || nr || ': ' || titel")
    R_veranstaltung.setSQLsort('order by art, nr')
    
    _relationen = {
        'person_id': R_person,
        'veranstaltung_id': R_veranstaltung,
        }
  
    def __init__(self, id=None, holen=False):
        super().__init__(id=id, holen=holen)
    
    def __str__(self):
        return "{}/{}: {}".format(self.person_id, self.veranstaltung_id, self.funktion)

###   Dozent Liste
class DozentListe(Modell):
    # Tabelle
    _tab = 'tbl_dozent'
    
    # Felder
    _felder = [
        idFeld('id'),
        numFeld('person_id'),
        numFeld('veranstaltung_id'),
        textFeld('funktion'),
        ]
        
    keyFeldNavi = 'id'
    
    # Relationen
    R_person = Relation('person_id', Person, 'id')
    R_person.setSQLanzeige("name || ', ' || vorname || ' (' || id || ')'")
    R_person.setSQLsort('order by name, vorname')
    
    R_veranstaltung = Relation('veranstaltung_id', Veranstaltung, 'id')
    R_veranstaltung.setSQLanzeige("art || '-' || nr || ': ' || titel")
    R_veranstaltung.setSQLsort('order by art, nr')
    
    _relationen = {
        'person_id': R_person,
        'veranstaltung_id': R_veranstaltung,
        }
  
    def __init__(self, id=None, holen=False):
        super().__init__(id=id, holen=holen)
    
    def __str__(self):
        return "{}/{}: {}".format(self.person_id, self.veranstaltung_id, self.funktion)

###   Raumbelegung
class Raumbelegung(Modell):
    # Tabelle
    _tab = 'tbl_raumbelegung'
    
    # Felder
    _felder = [
        idFeld('id'),
        numFeld('veranstaltung_id'),
        textFeld('raum_kurz_bez'),
        dateFeld('datum'),
        timeFeld('zeit_von'),
        timeFeld('zeit_bis'),
        textFeld('bemerkung'),
        # Verwaltung des Datensatzes
        textFeld('bearb_von'),
        datetimeFeld('bearb_am'),
        datetimeFeld('bearb_auto'),
        ]
    
    keyFeldNavi = 'id'
    
    # Relationen
    R_veranstaltung = Relation('veranstaltung_id', Veranstaltung, 'id')
    R_veranstaltung.setSQLanzeige("art || '-' || nr || ': ' || titel")
    R_veranstaltung.setSQLsort('order by art, nr')
    
    R_raum = Relation('raum_kurz_bez', Raum, 'kurz_bez')
    R_raum.setSQLanzeige("kurz_bez")
    R_raum.setSQLsort('order by kurz_bez')
    
    _relationen = {
        'veranstaltung_id': R_veranstaltung,
        'raum_kurz_bez': R_raum,
        }
  
    def __init__(self, id=None, holen=False):
        super().__init__(id=id, holen=holen)
    
    def __str__(self):
        return "{}: {}".format(self.veranstaltung_id, self.raum_kurz_bez)

###   Raumbelegung als Liste
class RaumbelegungListe(Modell):
    # Tabelle
    _tab = 'tbl_raumbelegung'
    
    # Felder
    _felder = [
        idFeld('id'),
        numFeld('veranstaltung_id'),
        textFeld('raum_kurz_bez'),
        dateFeld('datum'),
        timeFeld('zeit_von'),
        timeFeld('zeit_bis'),
        ]
    
    keyFeldNavi = 'id'
    
    # Relationen
    R_veranstaltung = Relation('veranstaltung_id', Veranstaltung, 'id')
    R_veranstaltung.setSQLanzeige("art || '-' || nr || ': ' || titel")
    R_veranstaltung.setSQLsort('order by art, nr')
    
    R_raum = Relation('raum_kurz_bez', Raum, 'kurz_bez')
    R_raum.setSQLanzeige("kurz_bez")
    R_raum.setSQLsort('order by kurz_bez')
    
    _relationen = {
        'veranstaltung_id': R_veranstaltung,
        'raum_kurz_bez': R_raum,
        }
  
    def __init__(self, id=None, holen=False):
        super().__init__(id=id, holen=holen)
    
    def __str__(self):
        return "{}: {}".format(self.veranstaltung_id, self.raum_kurz_bez)

#######################################################################
# Sonstiges
#######################################################################

###   Workshop Anmeldung
class AnmWS(Modell):
    # Tabelle
    _tab = 'tbl_anm_ws'
    
    # Felder
    _felder = [
        idFeld('id'),
        # Teilnehmer
        numFeld('tn_id'),
        textFeld('name'),
        textFeld('vorname'),
        textFeld('email'),
        # WS-Wünsche
        textFeld('ws_a_i'),
        textFeld('ws_a_ii'),
        textFeld('ws_a_iii'),
        textFeld('ws_b_i'),
        textFeld('ws_b_ii'),
        textFeld('ws_b_iii'),
        textFeld('ws_c_i'),
        textFeld('ws_c_ii'),
        textFeld('ws_c_iii'),
        textFeld('ws_d_i'),
        textFeld('ws_d_ii'),
        textFeld('ws_d_iii'),
        textFeld('nachricht'),
        # Verwaltung des Datensatzes
        textFeld('bearb_von'),
        datetimeFeld('bearb_am'),
        datetimeFeld('bearb_auto'),
        ]
        
    keyFeldNavi = 'id'
    
    # Relationen
    R_tn = Relation('tn_id', Person, 'id')
    R_tn.setSQLanzeige("name || ', ' || vorname || '(' || ort || ', ' || email || ')'")
    R_tn.setSQLsort('order by name, vorname, ort')
    
    _relationen = {
        'tn_id': R_tn,
        }
  
    def __init__(self, id=None, holen=False):
        super().__init__(id=id, holen=holen)
    
    def __str__(self):
        return "{}: {}".format(self.veranstaltung_id, self.raum_kurz_bez)

class AnmWSListe(Modell):
    # Tabelle
    _tab = 'tbl_anm_ws'
    
    # Felder
    _felder = [
        idFeld('id'),
        # Teilnehmer
        numFeld('tn_id'),
        textFeld('name'),
        textFeld('vorname'),
        textFeld('email'),
        # WS-Wünsche
        textFeld('ws_a_i'),
        textFeld('ws_a_ii'),
        textFeld('ws_a_iii'),
        textFeld('nachricht'),
        ]
    
    keyFeldNavi = 'id'
    
    # Relationen
    R_tn = Relation('tn_id', Person, 'id')
    R_tn.setSQLanzeige("name || ', ' || vorname || '(' || ort || ', ' || email || ')'")
    R_tn.setSQLsort('order by name, vorname, ort')
    
    _relationen = {
        'tn_id': R_tn,
        }
  
    def __init__(self, id=None, holen=False):
        super().__init__(id=id, holen=holen)
    
    def __str__(self):
        return "{}: {}".format(self.veranstaltung_id, self.raum_kurz_bez)

