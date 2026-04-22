"""
KI-Provider Abstraktion
Alle Provider implementieren dieselbe Schnittstelle.
Neuen Provider hinzufügen: Klasse von AIProvider ableiten und in get_provider() registrieren.
"""

from abc import ABC, abstractmethod


class AIProvider(ABC):
    """Abstrakte Basisklasse für KI-Provider."""

    @abstractmethod
    def generate_document(
        self,
        description: str,
        title: str,
        fmt: str,
        template_id: str,
        chapters: list,
        aushang: bool,
        refs: list,
    ) -> str:
        """
        Generiert ein WBI-Wissensdokument im Markdown-Format.
        Gibt den Markdown-String zurück.
        """
        raise NotImplementedError

    def _build_prompt(
        self,
        description: str,
        title: str,
        fmt: str,
        template_id: str,
        chapters: list,
        aushang: bool,
        refs: list,
    ) -> str:
        """Gemeinsamer System-Prompt für alle Provider."""

        fmt_label = {
            "word": "Word-Dokument (Wissensdokumentation)",
            "excel": "Excel-Tabelle",
            "ppt": "PowerPoint-Präsentation",
        }.get(fmt, "Wissensdokument")

        tpl_label = {
            "intern": "Internes Dokument",
            "extern": "Externes Dokument",
            "kunde": "Kundenanleitung",
            "netzwerk": "Netzwerkdokumentation",
            "praesentation": "Präsentation",
        }.get(template_id, template_id)

        chapter_hint = ""
        valid_chapters = [c for c in chapters if c.get("name", "").strip()]
        if valid_chapters:
            lines = []
            for i, ch in enumerate(valid_chapters, 1):
                lines.append(f"{i}. {ch['name']}")
                for j, sub in enumerate(ch.get("subs", []), 1):
                    if sub.strip():
                        lines.append(f"   {i}.{j} {sub}")
            chapter_hint = f"\n\nVorgegebene Kapitelstruktur:\n" + "\n".join(lines)

        refs_hint = ""
        valid_refs = [r for r in refs if r.get("num") or r.get("name")]
        if valid_refs:
            refs_hint = "\n\nMitgeltende Unterlagen:\n" + "\n".join(
                f"- {r.get('num', '—')}: {r.get('name', '')}" for r in valid_refs
            )

        aushang_hint = "\n\nHinweis: Dieses Dokument wird ausgehängt (Aushang-Abschnitt einbauen)." if aushang else ""

        return f"""Du bist ein technischer Redakteur für das WBI WIVIO Wissensmanagement-System.

Erstelle ein vollständiges {fmt_label} vom Typ "{tpl_label}" auf Deutsch im Markdown-Format.

Dokumenttitel: {title}
{aushang_hint}{chapter_hint}{refs_hint}

Inhalt / Beschreibung:
{description}

Formatierungsregeln:
- Dokumenttitel als # Überschrift
- Kapitelüberschriften als ## N. Kapitelname
- Unterkapitel als ### N.M Unterkapitelname
- Aufzählungen mit - 
- Tabellen im Markdown-Format
- Warnhinweise als > ⚠️ Text
- Inhaltsverzeichnis als ## Inhaltsverzeichnis mit Listeneinträgen
- Aushang als ## 1. Aushang (nur wenn angegeben)
- Mitgeltende Unterlagen als Tabelle (nur wenn vorhanden)
- Kapitel vollständig und fachlich korrekt ausschreiben
- Kein Abschnitt "Hinweise zur Vorlage"
- Nur Markdown ausgeben, keine Erklärungen davor oder danach"""


def get_provider(config: dict) -> "AIProvider":
    """
    Gibt den konfigurierten KI-Provider zurück.
    config erwartet: {"provider": "openai"|"anthropic"|"azure_openai", ...}
    """
    provider_name = config.get("provider", "openai").lower()

    if provider_name == "openai":
        from ai_providers.openai_provider import OpenAIProvider
        return OpenAIProvider(
            api_key=config.get("openai_api_key", ""),
            model=config.get("openai_model", "gpt-4o"),
        )
    elif provider_name == "anthropic":
        from ai_providers.anthropic_provider import AnthropicProvider
        return AnthropicProvider(
            api_key=config.get("anthropic_api_key", ""),
            model=config.get("anthropic_model", "claude-sonnet-4-20250514"),
        )
    elif provider_name == "azure_openai":
        from ai_providers.azure_openai_provider import AzureOpenAIProvider
        return AzureOpenAIProvider(
            api_key=config.get("azure_api_key", ""),
            endpoint=config.get("azure_endpoint", ""),
            deployment=config.get("azure_deployment", "gpt-4o"),
            api_version=config.get("azure_api_version", "2024-02-01"),
        )
    else:
        raise ValueError(f"Unbekannter KI-Provider: {provider_name}")
