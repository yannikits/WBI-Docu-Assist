# WBI Dokumentations-Assistent - Kurzreferenz

---

## Schnellstart

```
Einzelplatz:  start.bat doppelklicken → http://localhost:5000
Serverbetrieb: start_server.bat + host = 0.0.0.0 in config.ini
```

---

## Erstellungsmodi

| Modus | Wann verwenden |
|-------|---------------|
| Import | Bestehende .md-Datei weiterbearbeiten |
| Manuell | Struktur selbst aufbauen |
| Mit KI | Inhalt per Textbeschreibung generieren lassen |

---

## Namenskonvention

```
Themengebiet - Funktion/Thema

Beispiele:
  M365 - Konfiguration Entra ID Sync
  Netzwerk - Firewall Regelwerk
  Onboarding - Checkliste neue Mitarbeiter
  Kunde 10018 - VPN Einrichtung
```

---

## Verfügbare Vorlagen

| Kürzel | Format | Vorlage |
|--------|--------|---------|
| `intern` | Word | Internes Dokument |
| `extern` | Word | Externes Dokument |
| `kunde` | Word | Kundenanleitung |
| `netzwerk` | Excel | Netzwerkdokumentation (13 Sheets) |
| `intern_xl` | Excel | Internes Dokument |
| `extern_xl` | Excel | Externes Dokument |
| `kunde_xl` | Excel | Kundenanleitung |
| `brief` | Excel | Briefvorlage |
| `praesentation` | PowerPoint | Präsentation |

---

## Markdown-Syntax im Editor

| Syntax | Bedeutung |
|--------|-----------|
| `# Titel` | Dokumenttitel (H1) |
| `## Kapitel` | Kapitelüberschrift (H2) |
| `### Unterkapitel` | Unterkapitel (H3) |
| `**text**` | Fettschrift |
| `_text_` | Kursivschrift |
| `> Hinweis` | Warnhinweis |
| `- Punkt` | Aufzählung |
| `1. Punkt` | Nummerierte Liste |
| `\| A \| B \|` | Tabelle |
| `---` | Trennlinie |

---

## Bilder einfügen

| Methode | Vorgehen |
|---------|----------|
| Screenshot | `Win+Shift+S` → Editor klicken → `Strg+V` |
| Einzeldatei | Bilddatei in Editor ziehen |
| Ordner | Ordner in Editor ziehen (alle Bilder) |

---

## KI-Konfiguration (config.ini)

```ini
[ai]
enabled = true
provider = openai          # openai | anthropic | azure_openai
openai_api_key = sk-proj-...
openai_model = gpt-4o
```

API-Key erstellen: platform.openai.com → API Keys → Service account

---

## Serverbetrieb (config.ini)

```ini
[server]
host = 0.0.0.0     # Alle Netzwerkadressen
port = 5000
open_browser = false
```

Nutzer erreichen den Assistenten unter: `http://SERVER-IP:5000`

---

## Dateien im vorlagen/-Ordner

```
vorlagen/
├── Internes_Dokument_Vorlage.docx
├── Externes_Dokument_Vorlage.docx
├── Kundenanleitung_Vorlage.docx
├── Netzwerkdoku_Vorlage.xlsx
├── Internes_Dokument_Vorlage.xlsx
├── Externes_Dokument_Vorlage.xlsx
├── Kundenanleitung_Vorlage.xlsx
├── Briefvorlage.xlsx
└── Präsentationsvorlage_Vorlage.pptx
```

---

## Häufige Fehler

| Fehler | Lösung |
|--------|--------|
| „Vorlagendatei nicht gefunden" | Datei in `vorlagen/` kopieren |
| Seite lädt nicht | `start.bat` neu starten |
| `insufficient_quota` | OpenAI-Guthaben aufladen |
| „openai-Paket nicht installiert" | `pip install openai` |
| KI-Kachel fehlt | `enabled = true` in config.ini setzen |
| Port belegt | Port in `config.ini` ändern (z.B. 5001) |

---

## Weiterführende Dokumentation

| Dokument | Inhalt |
|----------|--------|
| `docs/Benutzerhandbuch.md` | Vollständige Bedienungsanleitung |
| `docs/Technische-Dokumentation.md` | Entwickler-Dokumentation |
| `config.ini.example` | Alle Konfigurationsoptionen mit Kommentaren |
