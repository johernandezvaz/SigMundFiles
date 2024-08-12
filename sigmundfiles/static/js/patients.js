function toggleSection(sectionId) {
    var section = document.getElementById(sectionId);
    if (section.style.display === "none" || section.style.display === "") {
        section.style.display = "block";
    } else {
        section.style.display = "none";
    }
}


document.addEventListener("DOMContentLoaded", function () {
    var fechaNacimientoInput = document.getElementById("id_fecha_nacimiento");
    var edadInput = document.getElementById("id_edad");

    fechaNacimientoInput.addEventListener("change", function () {
        var fechaNacimiento = new Date(fechaNacimientoInput.value);
        var hoy = new Date();
        var edad = hoy.getFullYear() - fechaNacimiento.getFullYear();
        var mes = hoy.getMonth() - fechaNacimiento.getMonth();

        if (mes < 0 || (mes === 0 && hoy.getDate() < fechaNacimiento.getDate())) {
            edad--;
        }

        edadInput.value = edad;
    });
});