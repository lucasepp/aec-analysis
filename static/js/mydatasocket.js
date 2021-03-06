function splitFloats(input) {
   var data = [];
    for (var i = 0; i < input.length; i++) {
        var vals = [];
        var elements = input[i].split(",");
        for (var j = 0; j < elements.length; j++) {
            vals.push(parseFloat(elements[j]));
        }
        data.push(vals);
    }
    return data;
}

$(document).ready(function(){
    namespace = '/data'; // change to an empty string to use the global namespace

    var socket = io.connect('http://' + document.domain + ':' + location.port + namespace);
    socket.on('connect', function() {
        socket.emit('my event', {data: 'I\'m connected!'});
         $('#log').append('<br>connected');
    });

    socket.on('data', function(msg) {
        var channel = msg.channel;
        var data = splitFloats(msg.data);
        $('#' + channel + '_log').append('<br>' + data);
    });

});
