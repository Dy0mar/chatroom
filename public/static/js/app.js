$(function() {
    $('#all_messages').scrollTop($('#all_messages')[0].scrollHeight);

    let ws_scheme = window.location.protocol === "https:" ? "wss" : "ws";
    let host = ws_scheme + '://' + window.location.host + "/chat/";
    let socket = new WebSocket(host);

    socket.onmessage = function(message) {
        let no_messages = $("#no_messages");
        if(no_messages.length){
            no_messages.remove();
        }

        let data = JSON.parse(message.data);

        if(data.type === "presence"){
            //update looker count
            console.log(data.payload);
            let lookers = data.payload.lookers;
            let looker_el = document.getElementById("looker-count");
            looker_el.innerText = lookers;

            //update logged in users list
            let user_list = data.payload.members;
            document.getElementById("loggedin-users-count").innerText = user_list.length;
            let user_list_obj = document.getElementById("user-list");
            user_list_obj.innerText = "";

            //alert(user_list);
            for(let i = 0; i < user_list.length; i++ ){
                let user_el = document.createElement('li');
                user_el.setAttribute('class', 'list-group-item');
                user_el.innerText = user_list[i];
                user_list_obj.append(user_el);
            }

            return;
        }

        let chat = $("#chat");
        let el = $('<li class="list-group-item"></li>');
        
        el.append('<strong>'+data.user+'</strong> : ');
        
        el.append(data.message);
        
        chat.append(el);
        $('#all_messages').scrollTop($('#all_messages')[0].scrollHeight);
    };

    $("#chatform").on("submit", function(event) {
        let elMessage = $('#message');
        let message = {
            message: elMessage.val()
        };
        socket.send(JSON.stringify(message));
        elMessage.val('').focus();
        return false;
    });

    setInterval(
        function() {
            socket.send(JSON.stringify("heartbeat"));
        },
        10000
    );
});