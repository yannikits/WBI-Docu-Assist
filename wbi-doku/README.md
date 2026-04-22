# WBI Dokumentations-Assistent

Lokaler Webassistent zur Erstellung von WBI WIVIO Dokumenten im Format
Word (.docx), Excel (.xlsx) und PowerPoint (.pptx) — basierend auf den echten WBI-Vorlagen.

---

## Voraussetzungen

- Python 3.9 oder neuer
- Die WBI-Vorlagendateien (aus dem WBI-System exportiert)

---

## Einrichtung

### 1. Abhängigkeiten installieren

```bash
pip install -r requirements.txt
```

### 2. Vorlagendateien kopieren

Folgende Dateien aus dem WBI-System in den Ordner `vorlagen/` kopieren:

| Dateiname                          | Vorlage für                   |
|------------------------------------|-------------------------------|
| `Internes_Dokument_Vorlage.docx`   | Word – Internes Dokument      |
| `Externes_Dokument_Vorlage.docx`   | Word – Externes Dokument      |
| `Kundenanleitung_Vorlage.docx`     | Word – Kundenanleitung        |
| `Netzwerkdoku_Vorlage.xlsx`        | Excel – Netzwerkdokumentation |
| `Internes_Dokument_Vorlage.xlsx`   | Excel – Internes Dokument     |
| `Externes_Dokument_Vorlage.xlsx`   | Excel – Externes Dokument     |
| `Kundenanleitung_Vorlage.xlsx`     | Excel – Kundenanleitung       |
| `Briefvorlage.xlsx`                | Excel – Briefvorlage          |
| `Präsentationsvorlage_Vorlage.pptx`| PowerPoint – Präsentation     |

### 3. Server starten

```bash
python app.py
```

Der Browser öffnet sich automatisch unter: **http://localhost:5000**

Oder Windows-Schnellstart:
```
start.bat
```

---

## Projektstruktur

```
wbi-doku/
├── app.py                        # Flask-Server (Einstiegspunkt)
├── requirements.txt              # Python-Abhängigkeiten
├── start.bat                     # Windows-Schnellstart
├── vorlagen/                     # WBI-Vorlagendateien (manuell befüllen)
├── generator/
│   ├── word_generator.py         # python-docx Dokumentgenerierung
│   ├── excel_generator.py        # openpyxl Tabellengenerierung
│   └── pptx_generator.py         # python-pptx Präsentationsgenerierung
└── templates/
    └── index.html                # Web-Frontend
```

---

## Workflow

1. **Format & Vorlage** wählen (Word / Excel / PowerPoint + spezifische Vorlage)
2. **Basisdaten** eingeben (Titel nach Namenskonvention `Themengebiet - Funktion`)
3. **Kapitelstruktur** aufbauen (Kapitel + Unterkapitel)
4. Im **Ergebnis-Schritt** optional Inhalte im Markdown-Editor anpassen oder Bilder einfügen
5. **"Dokument erstellen"** klickt → echte Office-Datei wird generiert und heruntergeladen

Alternativ: bestehende `.md`-Datei importieren → Kapitelstruktur wird automatisch erkannt.

---

## Erweiterung in Claude Code

Wenn du Änderungen an den Generatoren vornehmen möchtest:

- `generator/word_generator.py` – Stile, Schriftarten, Absatzformate anpassen
- `generator/excel_generator.py` – Weitere Sheets oder Formatierungen ergänzen
- `generator/pptx_generator.py` – Foliendesign und Layouts anpassen
- `templates/index.html` – Frontend-UI ändern

**Starte Claude Code im Projektordner:**
```bash
cd wbi-doku
claude
```
