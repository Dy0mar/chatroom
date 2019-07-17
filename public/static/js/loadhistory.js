$(function() {
    let socket = create_socket('loadhistory');

    let lastMessageId = $("#last_message_id");
    let loadOldMessages = $("#load_old_messages");

    socket.onmessage = function(message) {

        let data = JSON.parse(message.data);
        let new_messages = data.messages;
        let last_id = data.previous_id;

        if(last_id === -1){
            loadOldMessages.remove();
            lastMessageId.text(last_id);
            if(new_messages.length === 0){
                return;
            }
        }
        else{
            lastMessageId.text(last_id)
        }

        let chat = $("#chat");

        for(let i=new_messages.length - 1; i>=0; i--){
            let el = $('<li class="list-group-item"></li>');

            el.append('<strong>'+new_messages[i]['user']+'</strong> : ');
            el.append(new_messages[i]['message']);
            chat.prepend(el)
        }
    };

    loadOldMessages.on("click", function() {
        let message = {
            last_message_id: lastMessageId.text()
        };
        socket.send(JSON.stringify(message));
        return false;
    });
});
