document.addEventListener('DOMContentLoaded', function() {
    const imagenInput = document.getElementById('imagen');
    if (imagenInput) {
        imagenInput.addEventListener('change', function(event) {
            console.log('Evento change detectado');
            const fileInput = event.target;
            const formData = new FormData();
            formData.append('imagen', fileInput.files[0]);

            // Encuentra el div con la clase details-container y extrae el ID
            const detailsContainer = document.querySelector('.details-container');
            const pacienteId = detailsContainer ? detailsContainer.id.split('-')[1] : null;

            console.log(`Paciente ID obtenido: ${pacienteId}`);  // Verifica que se obtiene el ID del paciente correctamente

            if (!pacienteId) {
                alert("No se pudo obtener el ID del paciente");
                return;
            }

            formData.append('paciente_id', pacienteId);

            document.getElementById('loadingIndicator').style.display = 'block';

            fetch('/procesar-imagen-ocr/', {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                }
            })
            .then(response => response.json())
            .then(data => {
                console.log('Respuesta del servidor:', data);
                if (data.texto) {
                    document.getElementById('texto').value = data.texto;
                    document.getElementById('texto').disabled = false;
                    document.getElementById('guardarNotaBtn').disabled = false;
                } else if (data.error) {
                    alert(data.error);
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Ocurrió un error al procesar la imagen.');
            })
            .finally(() => {
                document.getElementById('loadingIndicator').style.display = 'none';
            });
        });
    } else {
        console.error('Elemento con ID "imagen" no encontrado');
    }
});
