$(document).ready(function() {
    var panelOneHeight = $('.form-panel.one').outerHeight(),
        panelTwoHeight = $('.form-panel.two').outerHeight(),
        formContainer = $('.form');

    // Inicializa la altura del contenedor del formulario
    formContainer.css('height', panelOneHeight);

    // Función para abrir el panel de registro
    function openPanelTwo() {
        $('.form-toggle').addClass('visible');
        $('.form-panel.one').addClass('hidden');
        $('.form-panel.two').addClass('active');
        formContainer.stop().animate({
            'height': panelTwoHeight
        }, 300);
    }

    // Evento para abrir el panel de registro
    $('.open-register-panel').on('click', function(e) {
        e.preventDefault();
        if (!$('.form-panel.two').hasClass('active')) {  // Solo abrir si no está ya activo
            openPanelTwo();
        }
    });

    // Evento para cerrar el panel de registro
    $('#close-register').on('click', function(e) {
        e.preventDefault();
        if ($('.form-panel.two').hasClass('active')) {  // Solo cerrar si está activo
            closePanelTwo();
        }
    });

    // Función para cerrar el panel de registro y volver al de inicio de sesión
    function closePanelTwo() {
        formContainer.stop().animate({
            'height': panelOneHeight
        }, 300, function() {
            $('.form-toggle').removeClass('visible');
            $('.form-panel.two').removeClass('active');
            $('.form-panel.one').removeClass('hidden');
        });
    }
});
