function create_socket(path){
    let ws_scheme = window.location.protocol === "https:" ? "wss" : "ws";
    let host = ws_scheme + '://' + window.location.host + "/" + path + "/";
    return new WebSocket(host);
}
