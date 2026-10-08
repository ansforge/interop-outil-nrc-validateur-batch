import asyncio
import contextlib
import html
import io as pyio
import os
import os.path as op
import re
import shutil
import traceback
import zipfile

import js
import requests
import requests.sessions
from pyodide.ffi import to_js
from pyscript import document, when

from validateur_batch.main import run

WORK_DIR = "/tmp/validateur"
INPUT_DIR = op.join(WORK_DIR, "input")
OUTPUT_DIR = op.join(WORK_DIR, "output")
SNAPSHOT_DIR = op.join(WORK_DIR, "snapshot")

# Fichiers de la Snapshot lus par `io.read_snapshot`, le groupe 1 correspond au
# chemin du dossier de la release
SNAPSHOT_FILES = re.compile(
    r"^(.*?)/?Snapshot/(Terminology/sct2_Concept_Snapshot_"
    r"|Terminology/sct2_Description_Snapshot-fr_"
    r"|Refset/Language/der2_cRefset_LanguageSnapshot-fr_)[^/]*\.txt$"
)

MIME_TYPES = {".csv": "text/csv;charset=utf-8",
              ".tsv": "text/tab-separated-values;charset=utf-8"}

ALERT_ICONS = {"info": "circle-info", "success": "circle-check",
               "warning": "warning", "error": "circle-cross"}

download_urls = []


# Firefox transmet le User-Agent "python-requests" ajouté par défaut, ce qui impose
# une requête preflight que certains serveurs FHIR (dont le SMT) refusent
_default_headers = requests.sessions.default_headers


def _browser_headers():
    headers = _default_headers()
    del headers["User-Agent"]
    return headers


requests.sessions.default_headers = _browser_headers


class LogWriter:
    """Redirige la sortie standard vers un élément de la page en reproduisant le
    comportement du retour chariot (`\\r`) d'un terminal"""

    def __init__(self, element):
        self.element = element
        self.lines = [""]
        self.carriage_return = False

    def write(self, text: str) -> int:
        for part in re.split(r"(\r|\n)", text):
            if part == "\r":
                self.carriage_return = True
            elif part == "\n":
                self.carriage_return = False
                self.lines.append("")
            elif part:
                if self.carriage_return:
                    self.lines[-1] = ""
                    self.carriage_return = False
                self.lines[-1] += part
        self.element.textContent = "\n".join(self.lines).strip("\n")
        return len(text)

    def flush(self) -> None:
        pass


def icon(name: str) -> str:
    """Renvoie une icône du sprite SVG du Design System ANS"""
    return (f'<svg class="svg-icon svg-{name}" aria-hidden="true" focusable="false">'
            f'<use xlink:href="svg-icons/icon-sprite.svg#{name}"></use></svg>')


def set_status(kind: str, title: str, message: str = "") -> None:
    """Affiche un message du Design System ANS dans la zone de statut"""
    role = "alert" if kind in ("error", "warning") else "status"
    body = f"<p>{html.escape(message)}</p>" if message else ""
    document.getElementById("status").innerHTML = f"""
        <div class="o-alert o-alert--{kind}" role="{role}">
            <div class="o-alert__icon">{icon(ALERT_ICONS[kind])}</div>
            <h2 class="o-alert__title">{html.escape(title)}</h2>
            {body}
        </div>"""


def set_invalid(group_id: str, input_id: str, invalid: bool) -> None:
    """Applique ou retire l'état d'erreur du Design System ANS sur un champ"""
    document.getElementById(group_id).classList.toggle("is-invalid", invalid)
    field = document.getElementById(input_id)
    field.classList.toggle("is-invalid", invalid)
    field.setAttribute("aria-invalid", "true" if invalid else "false")


async def save_file(file, path: str) -> None:
    """Copie un fichier sélectionné dans le navigateur vers le système de fichiers
    de Pyodide"""
    os.makedirs(op.dirname(path), exist_ok=True)
    buffer = await file.arrayBuffer()
    with open(path, "wb") as f:
        f.write(buffer.to_bytes())


async def prepare_snapshot(files, source: str) -> str:
    """Extrait les fichiers utiles de la release RF2 et renvoie le chemin du dossier
    Snapshot reconstitué"""
    found = {}

    if source == "zip":
        archive = files.item(0)
        buffer = await archive.arrayBuffer()
        with zipfile.ZipFile(pyio.BytesIO(buffer.to_bytes())) as zf:
            for name in zf.namelist():
                match = SNAPSHOT_FILES.match(name)
                if match:
                    # Archive sans dossier racine : le nom de l'archive porte la date
                    root = match.group(1) or op.splitext(archive.name)[0]
                    path = op.join(SNAPSHOT_DIR, root,
                                   name[match.end(1):].lstrip("/"))
                    os.makedirs(op.dirname(path), exist_ok=True)
                    with zf.open(name) as src, open(path, "wb") as dst:
                        shutil.copyfileobj(src, dst)
                    found[match.group(2)] = root
    else:
        for file in files:
            match = SNAPSHOT_FILES.match(file.webkitRelativePath)
            if match:
                if not match.group(1):
                    raise ValueError("Sélectionnez le dossier de la release qui "
                                     "contient le dossier Snapshot, et non le "
                                     "dossier Snapshot lui-même")
                await save_file(file, op.join(SNAPSHOT_DIR, file.webkitRelativePath))
                found[match.group(2)] = match.group(1)

    if len(found) < 3:
        raise ValueError("La release ne contient pas les fichiers Snapshot attendus "
                         "(concepts, descriptions FR et language refset FR)")

    return op.join(SNAPSHOT_DIR, next(iter(found.values())), "Snapshot")


def publish_downloads() -> None:
    """Propose au téléchargement les fichiers produits dans le dossier de sortie"""
    downloads = document.getElementById("downloads")
    for name in sorted(os.listdir(OUTPUT_DIR)):
        with open(op.join(OUTPUT_DIR, name), "rb") as f:
            data = f.read()
        mime = MIME_TYPES.get(op.splitext(name)[1], "application/octet-stream")
        blob = js.Blob.new([to_js(data)], to_js({"type": mime},
                                                dict_converter=js.Object.fromEntries))
        url = js.URL.createObjectURL(blob)
        download_urls.append(url)

        item = document.createElement("li")
        item.innerHTML = (
            f'<a class="btn btn--ghost btn--primary btn--icon-before" href="{url}" '
            f'download="{html.escape(name)}">{icon("download")}{html.escape(name)}</a>'
        )
        downloads.append(item)


def validate(form) -> list:
    """Vérifie les champs du formulaire et renvoie la liste des erreurs"""
    errors = []
    is_check = form.elements.mode.value == "check"

    no_batch = form.elements.batchFiles.files.length == 0
    set_invalid("batchGroup", "batchFiles", no_batch)
    if no_batch:
        errors.append("Sélectionnez au moins un fichier batch.")

    endpoint = form.elements.endpoint
    bad_endpoint = is_check and (not endpoint.value or not endpoint.checkValidity())
    set_invalid("endpointGroup", "endpoint", bad_endpoint)
    if bad_endpoint:
        errors.append("Renseignez une URL valide pour le serveur de terminologies.")

    no_snapshot = is_check and form.elements.snapshotFile.files.length == 0
    set_invalid("snapshotGroup", "snapshotFile", no_snapshot)
    if no_snapshot:
        errors.append("Sélectionnez la release RF2 de l'édition FR.")

    return errors


@when("submit", "#form")
def on_submit(event):
    # Un gestionnaire asynchrone serait exécuté trop tard pour bloquer l'envoi
    event.preventDefault()
    asyncio.ensure_future(process())


async def process():
    form = document.getElementById("form")
    submit = document.getElementById("submit")
    log = document.getElementById("log")

    errors = validate(form)
    if errors:
        set_status("error", "Le formulaire contient des erreurs", " ".join(errors))
        return

    submit.disabled = True
    import_mode = form.elements.mode.value == "import"
    set_status("info", "Traitement en cours",
               "La page peut ne plus répondre pendant l'analyse, merci de patienter.")
    for url in download_urls:
        js.URL.revokeObjectURL(url)
    download_urls.clear()
    document.getElementById("downloads").innerHTML = ""
    log.textContent = ""
    document.getElementById("results").hidden = False
    # Laisser le navigateur afficher le statut avant le traitement
    await asyncio.sleep(0.05)

    try:
        shutil.rmtree(WORK_DIR, ignore_errors=True)
        os.makedirs(INPUT_DIR)
        os.makedirs(OUTPUT_DIR)

        for file in form.elements.batchFiles.files:
            await save_file(file, op.join(INPUT_DIR, file.name))

        snapshot = None
        endpoint = None
        if not import_mode:
            log.textContent = "Lecture de la release RF2..."
            await asyncio.sleep(0.05)
            snapshot = await prepare_snapshot(form.elements.snapshotFile.files,
                                              form.elements.snapshotSource.value)
            endpoint = form.elements.endpoint.value.rstrip("/")

        with contextlib.redirect_stdout(LogWriter(log)):
            run(INPUT_DIR, OUTPUT_DIR, import_mode, endpoint, snapshot)

        publish_downloads()
        set_status("success", "Traitement terminé",
                   "Les fichiers produits sont disponibles ci-dessous.")
    except requests.exceptions.RequestException as e:
        log.textContent += "\n\n" + traceback.format_exc()
        set_status("error", "Erreur de communication avec le serveur de terminologies",
                   f"{e}. Vérifiez l'endpoint et que le serveur autorise les requêtes "
                   "cross-origin (CORS) depuis ce site.")
    except Exception as e:
        log.textContent += "\n\n" + traceback.format_exc()
        set_status("error", "Le traitement a échoué", str(e))
    finally:
        submit.disabled = False


document.getElementById("status").innerHTML = ""
document.getElementById("submit").disabled = False
