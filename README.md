# WBI-Docu-Assist

Lokaler Webassistent zur Erstellung von WBI-WIVIO-Dokumenten in den Formaten Word (.docx), Excel (.xlsx) und PowerPoint (.pptx) – basierend auf echten WBI-Vorlagen.

## Überblick

Dieses Repository enthält den **WBI Dokumentations-Assistenten**, eine Flask-Webanwendung, die es ermöglicht, strukturierte Office-Dokumente auf Basis der WBI-Vorlagen zu generieren. Die optionale KI-Unterstützung bei der Kapitelgenerierung unterstützt mehrere Provider (OpenAI, Azure OpenAI, Anthropic Claude).

## Projektstruktur

```
wbi-docu-assist/
└── wbi-doku/              # Hauptanwendung (Flask-Server)
    ├── app.py             # Einstiegspunkt
    ├── config.py          # Konfigurationsmanagement
    ├── requirements.txt   # Python-Abhängigkeiten
    ├── start.bat          # Windows-Schnellstart
    ├── ai_providers/      # KI-Provider-Integration
    ├── generator/         # Dokumentgeneratoren (Word, Excel, PPTX)
    ├── templates/         # HTML-Frontend
    └── vorlagen/          # WBI-Vorlagendateien (manuell befüllen)
```

## Schnellstart

Detaillierte Einrichtungsanweisungen befinden sich in [`wbi-doku/README.md`](wbi-doku/README.md).

```bash
cd wbi-doku
pip install -r requirements.txt
python app.py
```

Der Browser öffnet sich automatisch unter **http://localhost:5000**.

## Voraussetzungen

- Python 3.9 oder neuer
- WBI-Vorlagendateien aus dem WBI-System (in `wbi-doku/vorlagen/` ablegen)

## Lizenz

Internes Werkzeug – alle Rechte vorbehalten.
