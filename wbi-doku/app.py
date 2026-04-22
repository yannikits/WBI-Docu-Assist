"""WBI Dokumentations-Assistent – Flask Backend"""

import sys, os, threading, webbrowser, time
from flask import Flask, request, jsonify, send_file, render_template

from generator.word_generator import generate_word
from generator.excel_generator import generate_excel
from generator.pptx_generator import generate_pptx
import config as cfg

app = Flask(__name__)
VORLAGEN_DIR = os.path.join(os.path.dirname(__file__), "vorlagen")

TEMPLATE_FILES = {
    "intern":"Internes_Dokument_Vorlage.docx","extern":"Externes_Dokument_Vorlage.docx",
    "kunde":"Kundenanleitung_Vorlage.docx","netzwerk":"Netzwerkdoku_Vorlage.xlsx",
    "intern_xl":"Internes_Dokument_Vorlage.xlsx","extern_xl":"Externes_Dokument_Vorlage.xlsx",
    "kunde_xl":"Kundenanleitung_Vorlage.xlsx","brief":"Briefvorlage.xlsx",
    "praesentation":"Präsentationsvorlage_Vorlage.pptx",
}

def get_template_path(template_id):
    fn = TEMPLATE_FILES.get(template_id)
    if not fn:
        raise ValueError(f"Unbekannte Vorlage: {template_id}")
    path = os.path.join(VORLAGEN_DIR, fn)
    if not os.path.exists(path):
        raise FileNotFoundError(f"Vorlagendatei nicht gefunden: {fn}\nBitte '{fn}' in den Ordner 'vorlagen/' kopieren.")
    return path

@app.route("/")
def index():
    return render_template("index.html", ai_enabled=cfg.ai_enabled())

@app.route("/api/config")
def api_config():
    return jsonify({"ai_enabled": cfg.ai_enabled()})

@app.route("/generate", methods=["POST"])
def generate():
    data = request.get_json(force=True)
    fmt = data.get("format","")
    tid = data.get("template","")
    try:
        tp = get_template_path(tid)
        if fmt == "word":
            buf,fn = generate_word(data,tp)
            mt = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        elif fmt == "excel":
            buf,fn = generate_excel(data,tp)
            mt = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        elif fmt == "ppt":
            buf,fn = generate_pptx(data,tp)
            mt = "application/vnd.openxmlformats-officedocument.presentationml.presentation"
        else:
            return jsonify({"error":f"Unbekanntes Format: {fmt}"}),400
        buf.seek(0)
        return send_file(buf,mimetype=mt,as_attachment=True,download_name=fn)
    except FileNotFoundError as e:
        return jsonify({"error":str(e)}),404
    except Exception as e:
        import traceback; traceback.print_exc()
        return jsonify({"error":str(e)}),500

@app.route("/ai-generate", methods=["POST"])
def ai_generate():
    if not cfg.ai_enabled():
        return jsonify({"error":"KI-Funktionen sind nicht aktiviert (config.ini)."}),403
    data = request.get_json(force=True)
    desc = data.get("description","").strip()
    if not desc:
        return jsonify({"error":"Keine Beschreibung angegeben."}),400
    try:
        from ai_providers.base import get_provider
        provider = get_provider(cfg.get_ai_config())
        md = provider.generate_document(
            description=desc, title=data.get("title",""),
            fmt=data.get("format","word"), template_id=data.get("template","intern"),
            chapters=data.get("chapters",[]), aushang=data.get("aushang",False),
            refs=data.get("refs",[]),
        )
        return jsonify({"markdown": md})
    except Exception as e:
        import traceback; traceback.print_exc()
        return jsonify({"error":str(e)}),500

def run():
    sc = cfg.get_server_config()
    host,port,debug,open_br = sc["host"],sc["port"],sc["debug"],sc["open_browser"]
    url = f"http://{'localhost' if host=='0.0.0.0' else host}:{port}"
    print("="*60)
    print("  WBI Dokumentations-Assistent")
    print(f"  {url}")
    print(f"  KI-Funktionen: {'aktiviert (' + cfg.get_ai_config()['provider'] + ')' if cfg.ai_enabled() else 'deaktiviert'}")
    print("="*60)
    if open_br and not debug:
        def _open():
            time.sleep(1.2); webbrowser.open(url)
        threading.Thread(target=_open,daemon=True).start()
    if debug:
        app.run(host=host,port=port,debug=True)
    else:
        try:
            from waitress import serve
            print(f"  Server läuft (waitress, {8} Threads)")
            serve(app,host=host,port=port,threads=8)
        except ImportError:
            print("  Hinweis: waitress nicht installiert, nutze Flask-Dev-Server.")
            app.run(host=host,port=port,debug=False)

if __name__ == "__main__":
    run()
