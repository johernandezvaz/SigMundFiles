function toggleDetails(id) {
    // Selecciona todos los contenedores de detalles
    const allDetails = document.querySelectorAll('.details-container');
    
    // Cierra todos los contenedores de detalles
    allDetails.forEach(function(details) {
        details.style.display = 'none';
    });

    // Muestra el contenedor de detalles del paciente seleccionado
    const selectedDetails = document.getElementById('details-' + id);
    if (selectedDetails) {
        selectedDetails.style.display = 'block';
    }
}
