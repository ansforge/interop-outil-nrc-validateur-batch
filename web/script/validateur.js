// Comportements d'interface uniquement : le traitement est géré par app.py
(function () {
    var form = document.getElementById("form");
    var checkOptions = document.getElementById("checkOptions");
    var snapshotFile = document.getElementById("snapshotFile");
    var snapshotLabel = document.getElementById("snapshotLabel");

    // Affiche les fichiers sélectionnés dans le libellé du champ
    function updateFileLabel(input) {
        var label = input.nextElementSibling;
        var files = input.files;
        if (!files || files.length === 0) {
            label.textContent = label.dataset.placeholder;
        } else if (input.webkitdirectory) {
            label.textContent = files[0].webkitRelativePath.split("/")[0]
                + " (" + files.length + " fichiers)";
        } else if (files.length === 1) {
            label.textContent = files[0].name;
        } else {
            label.textContent = files.length + " fichiers sélectionnés";
        }
    }

    // Les paramètres de vérification ne sont utiles qu'en mode vérification
    function updateMode() {
        var isCheck = form.elements.mode.value === "check";
        checkOptions.hidden = !isCheck;
        checkOptions.disabled = !isCheck;
    }

    // Bascule le sélecteur de la release entre archive ZIP et dossier
    function updateSnapshotSource() {
        var isDir = form.elements.snapshotSource.value === "dir";
        snapshotFile.value = "";
        snapshotFile.webkitdirectory = isDir;
        if (isDir) {
            snapshotFile.removeAttribute("accept");
        } else {
            snapshotFile.setAttribute("accept", ".zip");
        }
        snapshotLabel.firstChild.textContent = isDir
            ? "Dossier de la release RF2 de l'édition FR "
            : "Release RF2 de l'édition FR ";
        updateFileLabel(snapshotFile);
    }

    // Le formulaire n'est jamais envoyé : le traitement est déclenché par app.py
    form.addEventListener("submit", function (event) { event.preventDefault(); });
    form.querySelectorAll(".custom-file-input").forEach(function (input) {
        input.addEventListener("change", function () { updateFileLabel(input); });
    });
    form.querySelectorAll("[name=mode]").forEach(function (radio) {
        radio.addEventListener("change", updateMode);
    });
    form.querySelectorAll("[name=snapshotSource]").forEach(function (radio) {
        radio.addEventListener("change", updateSnapshotSource);
    });
    form.addEventListener("reset", function () {
        // Attendre que le navigateur ait réinitialisé les champs
        setTimeout(function () {
            form.querySelectorAll(".custom-file-input").forEach(updateFileLabel);
            updateMode();
            updateSnapshotSource();
        });
    });

    updateMode();
})();
