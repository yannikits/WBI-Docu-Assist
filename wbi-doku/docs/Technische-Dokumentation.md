# WBI Dokumentations-Assistent - Technische Dokumentation

---

## Inhaltsverzeichnis

- [1. Architektur](#1-architektur)
- [2. Projektstruktur](#2-projektstruktur)
- [3. Konfiguration](#3-konfiguration)
- [4. Backend – Flask-Server](#4-backend--flask-server)
- [5. KI-Provider-System](#5-ki-provider-system)
- [6. Generator – Word](#6-generator--word)
- [7. Generator – Excel](#7-generator--excel)
- [8. Generator – PowerPoint](#8-generator--powerpoint)
- [9. Frontend](#9-frontend)
- [10. Datenmodell](#10-datenmodell)
- [11. Serverbetrieb](#11-serverbetrieb)
- [12. Neue Vorlage hinzufügen](#12-neue-vorlage-hinzufügen)
- [13. Neuen KI-Provider hinzufügen](#13-neuen-ki-provider-hinzufügen)
- [14. Abhängigkeiten](#14-abhängigkeiten)

---

## 1. Architektur

```
Browser (localhost:5000 oder SERVER-IP:5000)
    │
    │  GET  /            → index.html ausliefern
    │  GET  /api/config  → KI-Status abfragen
    │  POST /generate    → Office-Dokument generieren
    │  POST /ai-generate → KI-Inhalt generieren
    │
    ▼
Flask + waitress (app.py)
    │
    ├── config.py                      Konfigurationsverwaltung
    │
    ├── generator/
    │   ├── word_generator.py          python-docx
    │   ├── excel_generator.py         openpyxl
    │   └── pptx_generator.py          python-pptx
    │
    ├── ai_providers/
    │   ├── base.py                    Abstrakte Basisklasse + Factory
    │   ├── openai_provider.py         OpenAI / ChatGPT
    │   ├── anthropic_provider.py      Anthropic Claude
    │   └── azure_openai_provider.py   Azure OpenAI
    │
    └── vorlagen/                      WBI-Vorlagendateien
```

**Ablauf Dokumenterstellung:**

1. Nutzer füllt Frontend aus → klickt „Dokument erstellen"
2. `POST /generate` mit JSON-Payload
3. Flask wählt Generator, öffnet Vorlage, befüllt sie
4. Fertige Datei als Download-Response

**Ablauf KI-Generierung:**

1. Nutzer gibt Beschreibung ein → klickt „Mit KI generieren"
2. `POST /ai-generate` mit JSON-Payload
3. Flask ruft konfigurierten Provider auf
4. Provider sendet Prompt an KI-API
5. Markdown-Antwort wird ans Frontend zurückgegeben
6. Frontend lädt Markdown in Editor → Nutzer prüft und erstellt Dokument

---

## 2. Projektstruktur

```
wbi-doku/
├── app.py                        Flask-Einstiegspunkt, alle Routen
├── config.py                     Konfigurationsverwaltung
├── config.ini                    Aktive Konfiguration (nicht im ZIP)
├── config.ini.example            Vorlage mit allen Optionen und Kommentaren
├── requirements.txt              Python-Abhängigkeiten
├── start.bat                     Einzelplatz-Start (Browser öffnet sich)
├── start_server.bat              Serverbetrieb (kein Browser)
│
├── generator/
│   ├── __init__.py
│   ├── word_generator.py
│   ├── excel_generator.py
│   └── pptx_generator.py
│
├── ai_providers/
│   ├── __init__.py
│   ├── base.py                   AIProvider-Basisklasse + get_provider()
│   ├── openai_provider.py
│   ├── anthropic_provider.py
│   └── azure_openai_provider.py
│
├── vorlagen/                     WBI-Vorlagendateien (manuell befüllen)
│
├── templates/
│   └── index.html                Jinja2-Template + Frontend-SPA
│
└── docs/
    ├── Benutzerhandbuch.md
    ├── Technische-Dokumentation.md
    └── Kurzreferenz.md
```

---

## 3. Konfiguration

### 3.1 config.ini

Die Datei `config.ini` (aus `config.ini.example` kopieren) steuert Server und KI:

```ini
[server]
host = 127.0.0.1      # 0.0.0.0 für Serverbetrieb
port = 5000
debug = false
open_browser = true   # false für Serverbetrieb

[ai]
enabled = false        # true zum Aktivieren
provider = openai      # openai | anthropic | azure_openai
openai_api_key =
openai_model = gpt-4o
anthropic_api_key =
anthropic_model = claude-sonnet-4-20250514
azure_api_key =
azure_endpoint =
azure_deployment = gpt-4o
azure_api_version = 2024-02-01
```

### 3.2 Umgebungsvariablen

Alle `config.ini`-Werte können über Umgebungsvariablen überschrieben werden. Schema: `WBI_SECTION_KEY`, z.B.:

```
WBI_AI_OPENAI_API_KEY=sk-proj-...
WBI_SERVER_PORT=8080
```

Nützlich für Docker-Deployments oder CI/CD-Pipelines ohne `config.ini`.

### 3.3 config.py

`config.py` liest `config.ini` und stellt typisierte Getter bereit:

```python
cfg.get_server_config()   # dict mit host, port, debug, open_browser
cfg.get_ai_config()       # dict mit allen KI-Einstellungen
cfg.ai_enabled()          # bool – True wenn KI aktiv und API-Key vorhanden
```

---

## 4. Backend – Flask-Server

### 4.1 Routen

| Route | Methode | Beschreibung |
|-------|---------|-------------|
| `/` | GET | index.html mit `ai_enabled`-Flag ausliefern |
| `/api/config` | GET | `{"ai_enabled": true/false}` |
| `/generate` | POST | Office-Dokument generieren, als Download zurückgeben |
| `/ai-generate` | POST | KI-Inhalt generieren, Markdown zurückgeben |

### 4.2 /generate – Payload

```json
{
  "format": "word",
  "template": "intern",
  "titleSubject": "M365",
  "titleTopic": "Konfiguration Entra ID Sync",
  "aushang": false,
  "chapters": [
    {"name": "Voraussetzungen", "subs": ["Lizenzen", "Berechtigungen"]},
    {"name": "Konfiguration", "subs": []}
  ],
  "refs": [{"num": "12345", "name": "Partnervertrag"}],
  "markdownContent": "# M365 - Konfiguration...\n\n..."
}
```

### 4.3 /ai-generate – Payload

```json
{
  "description": "Schritt-für-Schritt-Anleitung zur Einrichtung...",
  "title": "M365 - Konfiguration Entra ID Sync",
  "format": "word",
  "template": "intern",
  "chapters": [...],
  "aushang": false,
  "refs": [...]
}
```

Antwort: `{"markdown": "# M365 - Konfiguration...\n\n..."}`

### 4.4 Fehlerbehandlung

| HTTP-Code | Ursache |
|-----------|---------|
| 400 | Unbekanntes Format |
| 403 | KI nicht aktiviert |
| 404 | Vorlagendatei fehlt |
| 500 | Generierungsfehler (Traceback in Konsole) |

### 4.5 Server-Modus

```python
# Produktivbetrieb (waitress)
from waitress import serve
serve(app, host=host, port=port, threads=8)

# Entwicklung (Flask Dev-Server)
app.run(host=host, port=port, debug=True)
```

---

## 5. KI-Provider-System

### 5.1 Abstrakte Basisklasse (ai_providers/base.py)

```python
class AIProvider(ABC):
    @abstractmethod
    def generate_document(self, description, title, fmt, template_id,
                          chapters, aushang, refs) -> str:
        """Gibt fertiges Markdown zurück."""
        ...

    def _build_prompt(self, ...) -> str:
        """Gemeinsamer WBI-Prompt für alle Provider."""
        ...
```

### 5.2 Provider-Factory

```python
from ai_providers.base import get_provider

provider = get_provider(cfg.get_ai_config())
markdown = provider.generate_document(...)
```

`get_provider()` wählt anhand von `config["provider"]` den richtigen Provider.

### 5.3 KI-Prompt-Struktur

Der gemeinsame Prompt in `_build_prompt()` enthält:

- Dokumenttyp und Vorlagenname
- Titel
- Optionale Kapitelstruktur als Vorgabe
- Optionale Mitgeltende Unterlagen
- Aushang-Hinweis
- Formatierungsregeln (Markdown-Struktur, WBI-Konventionen)
- Anweisung: nur Markdown zurückgeben, keine Erklärungen

### 5.4 Verfügbare Provider

| Provider | Klasse | Paket |
|----------|--------|-------|
| OpenAI | `OpenAIProvider` | `openai` |
| Azure OpenAI | `AzureOpenAIProvider` | `openai` |
| Anthropic | `AnthropicProvider` | `anthropic` |

---

## 6. Generator – Word

**Datei:** `generator/word_generator.py` | **Bibliothek:** `python-docx`

### 6.1 Stil-Erkennung

WBI-Vorlagen verwenden deutsche Stilnamen (`Überschrift 3` statt `Heading 3`). Der Generator erkennt automatisch welche Stilnamen in der Vorlage vorhanden sind:

```python
_STYLE_CANDIDATES = {
    'heading1': ['Heading 1', 'Überschrift 1', 'Title'],
    'heading2': ['Heading 2', 'Überschrift 2'],
    ...
}

def _build_style_map(doc) -> dict:
    # Prüft welche Kandidaten im Dokument vorhanden sind
    # Gibt Mapping zurück: {'heading1': 'Überschrift 1', ...}
```

Wenn kein passender Stil gefunden wird: direkte Formatierung als Fallback (Schriftgröße, Farbe, Fettschrift).

### 6.2 TOC-Erhalt

Das Inhaltsverzeichnis-Feld der Vorlage wird vor dem Leeren gesichert und danach wiederhergestellt:

```python
toc_elements = _clear_body_keep_toc(doc)
# ... Inhalt schreiben ...
_reinsert_toc(doc, toc_elements)
```

Unterstützt sowohl SDT-basierte als auch Feld-basierte TOCs (ältere und neuere Word-Versionen). In Word einmal `F9` drücken um das TOC zu aktualisieren.

### 6.3 Bild-Einbettung

Base64-kodierte Bilder aus dem Markdown werden als echte Word-Bilder eingefügt:

```python
def _try_insert_image(doc, line) -> bool:
    # Erkennt: ![alt](data:image/png;base64,...)
    # Dekodiert Base64, fügt über run.add_picture() ein
    # Breite: max. 14 cm
```

### 6.4 Markdown-Parsing

`_add_markdown_content()` verarbeitet beim Import:

- Erste `# H1` überspringen (Titel bereits gesetzt)
- `## Inhaltsverzeichnis` und Boilerplate-Abschnitte überspringen
- Markdown-Links `[Text](url)` in Klartext umwandeln (aber `![Bild]()` nicht)
- Tabellen, Listen, Warnhinweise, Überschriften korrekt konvertieren

---

## 7. Generator – Excel

**Datei:** `generator/excel_generator.py` | **Bibliothek:** `openpyxl`

Die Vorlage wird komplett geladen (inkl. aller Sheets). Je nach Template-ID:

- `netzwerk`: Info-Sheet mit Kundenname und Datum befüllen, alle 13 Sheets bleiben erhalten
- `brief`: Datum und Betreff eintragen
- Alle anderen: Aktives Sheet leeren und Dokumentstruktur aufbauen

---

## 8. Generator – PowerPoint

**Datei:** `generator/pptx_generator.py` | **Bibliothek:** `python-pptx`

Generierte Folien:

| Folie | Inhalt |
|-------|--------|
| 1 | Titelfolie (blauer Hintergrund, Titel + Datum) |
| 2 | Agenda mit allen Kapiteln |
| 3–N | Eine Inhaltsfolie pro Kapitel |
| N+1 | Abschlussfolie |

Alle Textboxen werden als neue Shapes eingefügt (layout-unabhängig).

---

## 9. Frontend

**Datei:** `templates/index.html` | Single-Page-Application, Vanilla JavaScript

### 9.1 State-Objekt

```javascript
const S = {
  step: 1,              // 1 | 2 | 3
  mode: '',             // 'import' | 'ai' | 'manual'
  format: '',           // 'word' | 'excel' | 'ppt'
  template: '',
  titleSubject: '',
  titleTopic: '',
  aushang: false,
  chapters: [{name:'', subs:['']}],
  refs: [{num:'', name:''}],
  aiDescription: '',    // KI-Eingabetext
  aiLoading: false,     // Ladezustand KI
  aiError: '',
  markdownContent: '',  // Editorinhalt
  importedFile: '',
  imgCounter: 0,
  error: ''
};
```

### 9.2 KI-Modus im Frontend

```javascript
async function runAI() {
  S.aiLoading = true; S.step = 3; render(); // Ladescreen
  const resp = await fetch('/ai-generate', { ... });
  S.markdownContent = data.markdown;        // In Editor laden
  S.aiLoading = false; render();
}
```

Der `AI_ENABLED`-Wert wird per Jinja2-Template-Variable vom Backend gesetzt:

```html
const AI_ENABLED = {{ 'true' if ai_enabled else 'false' }};
```

Wenn `false`: Modus-Kacheln werden nicht angezeigt, Ablauf ist immer manuell.

### 9.3 Render-Zyklus

```
render()
  └── renderHdr()      // Header mit Badges
  └── renderStepBar()  // Schrittanzeige (Titel je nach Modus)
  └── renderS1()       // Import + Modus-Wahl + Format
      renderS2()       // Basisdaten + ggf. KI-Beschreibung
      renderS3()       // Editor (oder KI-Ladescreen)
      └── attach()     // Event-Listener neu registrieren
```

---

## 10. Datenmodell

```typescript
interface Chapter {
  name: string;
  subs: string[];
}

interface Ref {
  num: string;
  name: string;
}

interface GeneratePayload {
  format: 'word' | 'excel' | 'ppt';
  template: string;
  titleSubject: string;
  titleTopic: string;
  aushang: boolean;
  chapters: Chapter[];
  refs: Ref[];
  markdownContent: string;
}

interface AIGeneratePayload extends GeneratePayload {
  description: string;
  title: string;
}
```

---

## 11. Serverbetrieb

### 11.1 waitress

Der Produktionsserver `waitress` ist ein reiner Python WSGI-Server ohne externe Abhängigkeiten, geeignet für Windows-Produktivbetrieb:

```python
from waitress import serve
serve(app, host='0.0.0.0', port=5000, threads=8)
```

8 Threads bedeutet bis zu 8 gleichzeitige Dokument-Generierungen. Bei höherer Last `threads` in `app.py` anpassen.

### 11.2 Sicherheitshinweise

- `config.ini` mit API-Key niemals in öffentlich zugänglichen Ordnern ablegen
- Bei Serverbetrieb nur im internen Firmennetz betreiben (kein öffentlicher Zugang)
- `debug = false` in Produktivbetrieb immer sicherstellen

---

## 12. Neue Vorlage hinzufügen

**Schritt 1:** Vorlagendatei in `vorlagen/` ablegen.

**Schritt 2:** In `app.py` eintragen:
```python
TEMPLATE_FILES = {
    "meine_vorlage": "Meine_Vorlage.docx",
}
```

**Schritt 3:** In `templates/index.html` eintragen:
```javascript
const TEMPLATES = {
  word: [
    { id: 'meine_vorlage', name: 'Meine Vorlage', desc: 'Beschreibung' }
  ]
};
```

**Schritt 4 (optional):** Spezielle Befüllungslogik in `generator/word_generator.py` ergänzen.

---

## 13. Neuen KI-Provider hinzufügen

**Schritt 1:** Neue Datei `ai_providers/mein_provider.py`:
```python
from ai_providers.base import AIProvider

class MeinProvider(AIProvider):
    def generate_document(self, description, title, fmt,
                          template_id, chapters, aushang, refs) -> str:
        prompt = self._build_prompt(...)  # gemeinsamer WBI-Prompt
        # API-Aufruf
        return markdown_text
```

**Schritt 2:** In `ai_providers/base.py` registrieren:
```python
def get_provider(config):
    if config["provider"] == "mein_provider":
        from ai_providers.mein_provider import MeinProvider
        return MeinProvider(api_key=config["mein_api_key"])
```

**Schritt 3:** In `config.ini.example` dokumentieren.

---

## 14. Abhängigkeiten

| Paket | Version | Verwendung |
|-------|---------|-----------|
| `flask` | ≥ 3.0.0 | Web-Framework |
| `waitress` | ≥ 3.0.0 | Produktionsserver (Multi-User) |
| `python-docx` | ≥ 1.1.0 | Word-Generierung |
| `openpyxl` | ≥ 3.1.0 | Excel-Generierung |
| `python-pptx` | ≥ 0.6.23 | PowerPoint-Generierung |
| `lxml` | ≥ 5.0.0 | XML-Verarbeitung |
| `openai` | ≥ 1.0.0 | OpenAI / Azure OpenAI Provider |
| `anthropic` | ≥ 0.25.0 | Anthropic Claude Provider (optional) |
