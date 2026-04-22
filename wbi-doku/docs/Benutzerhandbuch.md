# WBI Dokumentations-Assistent - Benutzerhandbuch

---

## Inhaltsverzeichnis

- [1. Übersicht](#1-übersicht)
- [2. Voraussetzungen und Installation](#2-voraussetzungen-und-installation)
- [3. Programm starten](#3-programm-starten)
- [4. Schritt 1 – Format, Vorlage und Modus wählen](#4-schritt-1--format-vorlage-und-modus-wählen)
- [5. Schritt 2 – Basisdaten eingeben](#5-schritt-2--basisdaten-eingeben)
- [6. Schritt 3 – Inhalt und Erstellung](#6-schritt-3--inhalt-und-erstellung)
- [7. Markdown-Datei importieren](#7-markdown-datei-importieren)
- [8. Bilder einfügen](#8-bilder-einfügen)
- [9. KI-gestützte Dokumenterstellung](#9-ki-gestützte-dokumenterstellung)
- [10. Serverbetrieb – Mehrere Nutzer gleichzeitig](#10-serverbetrieb--mehrere-nutzer-gleichzeitig)
- [11. Namenskonvention](#11-namenskonvention)
- [12. Fehlerbehebung](#12-fehlerbehebung)

---

## 1. Übersicht

Der WBI Dokumentations-Assistent ist ein lokales Webprogramm zur schnellen Erstellung von Wissensdokumenten für das WBI WIVIO System. Er generiert fertige Dokumente im echten Word-, Excel- oder PowerPoint-Format auf Basis der hinterlegten WBI-Vorlagen.

**Kernfunktionen:**

- Dokumenterstellung in 3 Schritten
- Kapitel- und Unterkapitelstruktur frei konfigurierbar
- Import bestehender Markdown-Dateien mit automatischer Strukturerkennung
- KI-gestützte Inhaltsgenerierung (optional, z.B. über ChatGPT / OpenAI)
- Bilder per Screenshot einfügen (Strg+V) oder Drag & Drop
- Serverbetrieb für mehrere gleichzeitige Nutzer im Netzwerk
- Alle generierten Dokumente basieren direkt auf den WBI-Vorlagendateien

**Unterstützte Dokumenttypen:**

| Format | Vorlagen |
|--------|----------|
| Word (.docx) | Internes Dokument, Externes Dokument, Kundenanleitung |
| Excel (.xlsx) | Netzwerkdokumentation, Internes Dokument, Externes Dokument, Kundenanleitung, Briefvorlage |
| PowerPoint (.pptx) | Präsentation |

---

## 2. Voraussetzungen und Installation

### 2.1 Systemvoraussetzungen

- Windows 10 / 11 (64-Bit)
- Python 3.9 oder neuer ([python.org](https://www.python.org/downloads/))
- Internetzugang bei der Erstinstallation (für Python-Pakete)
- WBI-Vorlagendateien (aus dem WBI WIVIO System exportiert)

### 2.2 Ersteinrichtung

**Schritt 1:** ZIP-Archiv `wbi-doku-assistent.zip` entpacken.

**Schritt 2:** WBI-Vorlagendateien in den Unterordner `vorlagen/` kopieren:

| Dateiname | Beschreibung |
|-----------|-------------|
| `Internes_Dokument_Vorlage.docx` | Word – Internes Dokument |
| `Externes_Dokument_Vorlage.docx` | Word – Externes Dokument |
| `Kundenanleitung_Vorlage.docx` | Word – Kundenanleitung |
| `Netzwerkdoku_Vorlage.xlsx` | Excel – Netzwerkdokumentation |
| `Internes_Dokument_Vorlage.xlsx` | Excel – Internes Dokument |
| `Externes_Dokument_Vorlage.xlsx` | Excel – Externes Dokument |
| `Kundenanleitung_Vorlage.xlsx` | Excel – Kundenanleitung |
| `Briefvorlage.xlsx` | Excel – Briefvorlage |
| `Präsentationsvorlage_Vorlage.pptx` | PowerPoint – Präsentation |

> ⚠️ Die Dateinamen müssen exakt so lauten wie oben angegeben. Groß-/Kleinschreibung beachten.

**Schritt 3:** `config.ini` einrichten (aus `config.ini.example` kopieren und umbenennen). Für den Einzelplatz-Betrieb reichen die Standardwerte.

**Schritt 4:** `start.bat` doppelklicken. Python-Pakete werden beim ersten Start automatisch installiert.

---

## 3. Programm starten

### 3.1 Einzelplatz (lokaler Betrieb)

1. `start.bat` doppelklicken
2. Das Konsolenfenster **offen lassen** – es ist der laufende Server
3. Browser öffnet sich automatisch unter `http://localhost:5000`
4. Zum Beenden: Konsolenfenster schließen oder `Strg+C`

### 3.2 Serverbetrieb (mehrere Nutzer)

Siehe Abschnitt 10.

---

## 4. Schritt 1 – Format, Vorlage und Modus wählen

### 4.1 Bestehendes Dokument importieren (optional)

Oben im ersten Schritt befindet sich eine Import-Zone für bestehende Markdown-Dateien.

- `.md`-Datei per Drag & Drop in die Zone ziehen **oder** auf „Datei auswählen" klicken
- Titel, Kapitel und Unterkapitel werden automatisch erkannt und übernommen
- Der Originalinhalt landet direkt im Editor in Schritt 3

### 4.2 Erstellungsmodus wählen (wenn KI aktiviert)

Wenn die KI-Funktion in der `config.ini` aktiviert ist, erscheinen zwei Kacheln:

| Kachel | Beschreibung |
|--------|-------------|
| Manuell erstellen | Struktur selbst aufbauen, Inhalte direkt eingeben |
| Mit KI erstellen | Dokument per Freitext-Beschreibung automatisch generieren |

Ist die KI nicht aktiviert, entfällt diese Auswahl und der Ablauf ist immer manuell.

### 4.3 Format wählen

- **W – Word:** Textdokumente, Anleitungen, Wissensdokumentationen
- **X – Excel:** Tabellarische Dokumentationen, Netzwerkdokumentation
- **P – PowerPoint:** Präsentationen, Schulungsunterlagen

### 4.4 Vorlage wählen

Nach der Formatauswahl erscheint die Vorlagenliste. Passende Vorlage wählen und auf **„Weiter →"** klicken.

---

## 5. Schritt 2 – Basisdaten eingeben

### 5.1 Dokumenttitel

Der Titel folgt der WBI-Namenskonvention:

```
Themengebiet - Funktion/Thema
```

**Beispiele:**

| Themengebiet | Funktion/Thema |
|-------------|----------------|
| M365 | Konfiguration Entra ID Sync |
| Onboarding | Checkliste neue Mitarbeiter |
| Netzwerk | Firewall Regelwerk |

### 5.2 KI-Beschreibung (nur im KI-Modus)

Im KI-Modus erscheint ein Textfeld für die Inhaltsbeschreibung. Hier wird in freiem Text beschrieben, was das Dokument enthalten soll.

**Tipps für bessere KI-Ergebnisse:**

- Zielgruppe nennen (z.B. „für neue Mitarbeiter ohne Vorkenntnisse")
- Konkrete Inhalte aufzählen (z.B. „enthält Voraussetzungen, Konfigurationsschritte, Fehlerbehebung")
- Ton angeben (z.B. „technisch präzise" oder „verständlich und schrittweise")
- Je detaillierter die Beschreibung, desto besser das Ergebnis

Am Ende des Schritts stehen zwei Buttons:

- **„Mit KI generieren"** – KI erstellt das vollständige Dokument
- **„Ohne KI weiter"** – Weiter zum Editor mit leerem Inhalt

### 5.3 Aushang-Hinweis (nur bei internen Word-Dokumenten)

Der Toggle fügt folgenden Abschnitt ins Dokument ein:

> Dieses Dokument hängt/liegt aus. Die ausgedruckte Version kann veraltet sein – gültig ist immer die digitale Version im WBI-System.

### 5.4 Kapitelstruktur

- **Kapitel hinzufügen:** Auf „+ Kapitel hinzufügen" klicken
- **Unterkapitel hinzufügen:** `+`-Button rechts neben dem Kapitelnamen
- **Entfernen:** `×`-Button neben dem Eintrag
- Im KI-Modus ist die Kapitelstruktur optional – die KI strukturiert auch selbst

### 5.5 Mitgeltende Unterlagen

WBI-Dokumentennummer und Bezeichnung eintragen. Wird als Tabelle ins Dokument übernommen.

---

## 6. Schritt 3 – Inhalt und Erstellung

### 6.1 KI-Ladevorgang

Beim KI-Modus erscheint nach dem Klick auf „Mit KI generieren" ein Ladebildschirm. Die KI generiert das vollständige Dokument (typisch 5–15 Sekunden). Das Ergebnis wird automatisch in den Editor geladen.

### 6.2 Inhaltseditor

Im dritten Schritt erscheint ein Texteditor mit dem Markdown-Inhalt. Hier kann direkt bearbeitet werden:

- KI-generierte Inhalte überprüfen und anpassen
- Platzhaltertexte durch tatsächliche Inhalte ersetzen
- Bilder einfügen (siehe Abschnitt 8)

**Unterstützte Markdown-Formatierungen:**

| Syntax | Ergebnis |
|--------|---------|
| `# Überschrift 1` | Überschrift Ebene 1 |
| `## Überschrift 2` | Überschrift Ebene 2 |
| `### Überschrift 3` | Überschrift Ebene 3 |
| `**fett**` | fett |
| `_kursiv_` | kursiv |
| `> Hinweis` | Eingerückter Warnhinweis |
| `\| Spalte1 \| Spalte2 \|` | Tabelle |
| `- Listenpunkt` | Aufzählungsliste |

### 6.3 Dokument erstellen und herunterladen

Der primäre Button unten rechts erstellt die fertige Office-Datei und startet den Download direkt.

Der Button **„Als .md"** speichert den Editorinhalt als Markdown-Datei für spätere Weiterbearbeitung.

---

## 7. Markdown-Datei importieren

Bestehende `.md`-Dateien können in Schritt 1 importiert werden. Der Assistent erkennt automatisch:

- Dokumenttitel (wird in Themengebiet und Funktion aufgeteilt wenn das Format `X - Y` vorliegt)
- Kapitel (aus `## Überschriften`)
- Unterkapitel (aus `### Überschriften`)

Übersprungen werden automatisch: Inhaltsverzeichnis, Aushang, Mitgeltende Unterlagen, Hinweise zur Vorlage.

---

## 8. Bilder einfügen

Im Editor (Schritt 3) können Bilder auf drei Wegen eingefügt werden:

| Methode | Vorgehen |
|---------|----------|
| Screenshot einfügen | `Win+Shift+S` → in Editor klicken → `Strg+V` |
| Einzeldatei | Bilddatei in den Editor ziehen |
| Ordner | Ordner in den Editor ziehen – alle Bilder werden eingefügt |

Bilder werden als Base64-Daten direkt im Markdown eingebettet und landen so auch im fertigen Word-Dokument.

---

## 9. KI-gestützte Dokumenterstellung

### 9.1 Voraussetzungen

Die KI-Funktion muss in der `config.ini` aktiviert sein:

```ini
[ai]
enabled = true
provider = openai
openai_api_key = sk-proj-...
openai_model = gpt-4o
```

Ein OpenAI-Account mit aktivierter API-Abrechnung ist erforderlich. ChatGPT-Abos (Plus, Team, Enterprise) beinhalten **nicht** automatisch API-Zugang – dieser muss separat unter [platform.openai.com](https://platform.openai.com) mit Guthaben aufgeladen werden.

### 9.2 API-Key erstellen

1. [platform.openai.com](https://platform.openai.com) aufrufen
2. Projekt auswählen oder neu anlegen (z.B. „WBI Assistent")
3. Links auf **API Keys** → **+ Create new secret key**
4. „Owned by" → **Service account** wählen (für Firmenbetrieb)
5. Key sofort kopieren und sicher ablegen (wird nur einmal angezeigt)
6. In `config.ini` eintragen

### 9.3 Unterstützte Provider

| Provider | `provider =` | Einsatz |
|----------|-------------|---------|
| OpenAI / ChatGPT | `openai` | Standard, direkt über OpenAI |
| Azure OpenAI | `azure_openai` | Für Firmen mit Azure/M365-Infrastruktur |
| Anthropic Claude | `anthropic` | Alternative zu OpenAI |

### 9.4 Kosten

Die Kosten entstehen pro Dokumentgenerierung direkt beim gewählten Provider. Mit GPT-4o kostet eine typische Dokumentgenerierung ca. 0,01–0,05 €.

---

## 10. Serverbetrieb – Mehrere Nutzer gleichzeitig

### 10.1 Einrichtung

**Schritt 1:** In `config.ini` den Host anpassen:

```ini
[server]
host = 0.0.0.0
port = 5000
open_browser = false
```

**Schritt 2:** `start_server.bat` auf dem Server ausführen.

**Schritt 3:** Nutzer im Netzwerk rufen den Assistenten über `http://SERVER-IP:5000` auf.

### 10.2 Hinweise zum Serverbetrieb

- Das Programm nutzt `waitress` als Produktionsserver (8 parallele Threads)
- Die Vorlagendateien im `vorlagen/`-Ordner müssen auf dem Server liegen
- Der `config.ini` und der API-Key liegen nur auf dem Server – Nutzer sehen diese nicht
- Empfohlen: Programm-Ordner auf dem Server ablegen, **nicht** im Teams-Freigabeordner (wegen API-Key-Sicherheit)
- Für den Zugriff aus Teams heraus: Shortcut/Link auf `http://SERVER-IP:5000` im Teams-Kanal hinterlegen

### 10.3 Teams-Ordner als Speicherort (ohne Server)

Falls kein Server verfügbar ist, kann das Programm auch aus einem Teams/SharePoint-Ordner heraus gestartet werden – jeder Nutzer startet `start.bat` lokal auf seinem PC. In diesem Fall muss `host = 127.0.0.1` in der `config.ini` bleiben und der API-Key liegt in der geteilten `config.ini`.

> ⚠️ Bei Ablage im Teams-Ordner ist der API-Key für alle Nutzer mit Zugriff sichtbar. Für mehr Sicherheit: Serverbetrieb bevorzugen.

---

## 11. Namenskonvention

```
Themengebiet - Funktion/Thema
```

**Weitere Beispiele:**

| Themengebiet | Funktion/Thema |
|-------------|----------------|
| Windows Server | Active Directory Replikation |
| M365 | Teams Kanal Berechtigungen |
| VMware | vCenter Backup Konfiguration |
| Kunde 10018 | VPN Einrichtung |
| Drucker | Netzwerkdrucker einrichten HP LaserJet |

---

## 12. Fehlerbehebung

| Fehler | Ursache | Lösung |
|--------|---------|--------|
| „Vorlagendatei nicht gefunden" | Datei fehlt im `vorlagen/`-Ordner | Datei kopieren, Dateiname prüfen |
| Seite lädt nicht | Server läuft nicht | `start.bat` erneut ausführen |
| Port 5000 belegt | Anderes Programm nutzt Port | In `config.ini` anderen Port eintragen (z.B. `5001`) |
| „openai-Paket nicht installiert" | Python-Paket fehlt | `pip install openai` ausführen oder `start.bat` neu starten |
| `insufficient_quota` (OpenAI) | Kein Guthaben auf dem Account | Unter platform.openai.com Guthaben aufladen |
| KI-Funktionen erscheinen nicht | `enabled = false` in config.ini | `enabled = true` setzen und Server neu starten |
| Python nicht gefunden | Python nicht installiert | Von python.org installieren, „Add to PATH" aktivieren |
