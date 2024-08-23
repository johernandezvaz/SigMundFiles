document.addEventListener("DOMContentLoaded", function() {
    const abrirPopupBtn = document.getElementById('abrirPopup');
    const cerrarPopupBtn = document.getElementById('cerrarPopup');
    const cancelarPopupBtn = document.getElementById('cancelarPopup');
    const agregarNotaPopup = document.getElementById('agregarNotaPopup');
    const imagenInput = document.getElementById('imagen');
    const textoTextarea = document.getElementById('texto');
    const previewImagen = document.getElementById('previewImagen');

    // Abrir el popup
    abrirPopupBtn.addEventListener('click', function() {
        agregarNotaPopup.style.display = 'flex';
    });

    // Cerrar el popup (cerrar y cancelar tienen el mismo comportamiento)
    cerrarPopupBtn.addEventListener('click', function() {
        agregarNotaPopup.style.display = 'none';
    });

    cancelarPopupBtn.addEventListener('click', function() {
        agregarNotaPopup.style.display = 'none';
    });

    // Previsualizar imagen y limpiar textarea
    imagenInput.addEventListener('change', function(event) {
        textoTextarea.value = '';  // Limpiar el textarea
        const file = event.target.files[0];

        if (file) {
            const reader = new FileReader();
            reader.onload = function(e) {
                previewImagen.src = e.target.result;
                previewImagen.style.display = 'block';
            }
            reader.readAsDataURL(file);
        }
    });
});

document.addEventListener('DOMContentLoaded', function() {
    // Mostrar notas al hacer clic en "Ver Notas"
    const verNotasBtns = document.querySelectorAll('.verNotasBtn');
    verNotasBtns.forEach(button => {
        button.addEventListener('click', function() {
            const manuscritoId = this.getAttribute('data-manuscrito-id');
            const notasContainer = document.getElementById(`notasContainer-${manuscritoId}`);
            // Alternar la visibilidad de las notas
            if (notasContainer.style.display === 'none') {
                notasContainer.style.display = 'block';
            } else {
                notasContainer.style.display = 'none';
            }
        });
    });
});