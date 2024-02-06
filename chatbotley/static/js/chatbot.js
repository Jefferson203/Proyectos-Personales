

$('#userInput').keypress(function(e){
    if(e.keyCode == 13 && !e.shiftKey) {  // Verifica si la tecla presionada es "Enter" y si "Shift" no está presionado
        e.preventDefault();  // Evita el salto de línea predeterminado en "Enter"
        sendMessage();  // Llama a la función de enviar mensaje
    }
}); 

function sendMessage() {
    var message = $('#userInput').val().trim();  // Aquí se usa .trim() para eliminar los espacios en blanco al inicio y al final del mensaje
    if (message === '') {  // Verifica si el mensaje está vacío
        return;  // Si está vacío, sale de la función y no hace nada más
    }
    $('#chatbox').append('<div class="message user-message"><p>' + message + '</p></div><br>');
    $('#userInput').val('');
    $.ajax({
        url: '/chatbot_ronald_Jefferson',  // Ruta al servidor de tu chatbot
        data: { 'message': message },
        type: 'POST',
        success: function(response) {
            $('#chatbox').append('<div class="message bot-message"><p><b>Chatbot:</b> ' + response + '</p></div><br>');

            $('#chatbox').scrollTop($('#chatbox')[0].scrollHeight);
        },
        error: function(error) {
            console.log(error);
        }
    });
}
