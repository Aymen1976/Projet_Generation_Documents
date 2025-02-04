document.getElementById('fileInput').addEventListener('change', function(event) {
    const file = event.target.files[0];

    if (!file) {
        alert("Aucun fichier n’a été sélectionné");
        return;
    }

    console.log("Fichier sélectionné :", file.name);
    alert("Fichier sélectionné : " + file.name);

    // Afficher le nom du fichier sélectionné
    document.getElementById('fileNameDisplay').textContent = "Fichier sélectionné : " + file.name;

    const output = document.getElementById('output');
    const canvas = document.getElementById('pdfCanvas');
    const context = canvas.getContext('2d');

    // Lecture et affichage d'un fichier PDF (nouvelle version améliorée)
    if (file.type === 'application/pdf') {
        const fileReader = new FileReader();
        fileReader.onload = function() {
            const typedarray = new Uint8Array(this.result);
            
            pdfjsLib.getDocument(typedarray).promise.then(function(pdf) {
                console.log("📂 PDF chargé avec succès :", pdf);

                pdf.getPage(1).then(function(page) {
                    console.log("📄 Affichage de la première page du PDF");
                    const scale = 1.5;
                    const viewport = page.getViewport({ scale: scale });

                    // Ajuster la taille et afficher le canvas
                    canvas.height = viewport.height;
                    canvas.width = viewport.width;
                    canvas.style.display = 'block';

                    // Rendu de la page PDF
                    const renderContext = {
                        canvasContext: context,
                        viewport: viewport
                    };
                    page.render(renderContext);
                }).catch(function(error) {
                    console.error("❌ Erreur lors de l'affichage de la page PDF :", error);
                    alert("Impossible d'afficher ce PDF.");
                });

            }).catch(function(error) {
                console.error("❌ Erreur de lecture du PDF :", error);
                alert("Erreur lors de l'affichage du PDF.");
            });
        };
        fileReader.readAsArrayBuffer(file);

    // Lecture et affichage d'un fichier Word
    } else if (file.type === 'application/vnd.openxmlformats-officedocument.wordprocessingml.document') {
        const reader = new FileReader();
        reader.onload = function(event) {
            mammoth.convertToHtml({arrayBuffer: event.target.result})
                .then(function(result) {
                    output.innerHTML = result.value || "Le document Word est vide ou non lisible.";
                    canvas.style.display = 'none';
                })
                .catch(function(err) {
                    console.error("❌ Erreur de lecture Word :", err);
                    output.innerHTML = "Erreur lors de la lecture du fichier Word.";
                });
        };
        reader.readAsArrayBuffer(file);
    } else {
        alert("Veuillez sélectionner un fichier PDF ou Word.");
    }
});

// Fonction pour générer un PDF
function generatePDF() {
    if (!window.jspdf || !window.jspdf.jsPDF) {
        alert("Erreur : jsPDF n'est toujours pas chargé !");
        return;
    }

    const { jsPDF } = window.jspdf;
    const doc = new jsPDF();

    // Récupérer le texte personnalisé de l'utilisateur
    const userText = document.getElementById('customText')?.value || "Exemple de Contenu PDF";

    // Ajouter du texte au PDF
    doc.text(userText, 10, 10);

    // Créer un blob et générer un lien de téléchargement
    const blob = doc.output("blob");
    const link = document.createElement("a");
    link.href = URL.createObjectURL(blob);
    link.download = "exemple.pdf";

    // Ajouter le lien au DOM et simuler un clic
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);

    // Ouvrir automatiquement le fichier après téléchargement
    setTimeout(() => {
        window.open(link.href);
    }, 1000); // Ouvre le fichier après 1 seconde
}

// Fonction pour générer un fichier Word
function generateWord() {
    // Récupérer le texte de l'utilisateur
    const userText = document.getElementById('customText')?.value || "Exemple de Contenu Word";
    
    const blob = new Blob([userText], {
        type: "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    });

    const link = document.createElement('a');
    link.href = window.URL.createObjectURL(blob);
    link.download = 'exemple.docx';
    link.click();
}