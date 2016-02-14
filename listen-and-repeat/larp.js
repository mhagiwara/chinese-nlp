$(document).ready(function(){
    // Initialize
    $("p").click(play_next);
});

function load() {
    // Load one sentence data from JSON and return a deferred object resolved when it's loaded.
    return $.ajax({
        url: "http://localhost:8003/test",
        dataType: "jsonp",
        jsonp: "callback"
    });
}

function show(data) {
    // Show the content of the sentence object.
    $("p#cmn").text(data.cmn);
    $("p#eng").text(data.eng);
    return data;
}

function play(data) {
    // Given the sentence data, play the audio, and return a deferred object which is resolved
    // when the audio metadata was loaded.
    var audio = new Audio(data.audio);
    var dfd = $.Deferred();
    audio.addEventListener('loadedmetadata', function() {
        data.duration = audio.duration * 1000;
        audio.play();
        dfd.resolve(data);
    });
    return dfd;
}

function pause(data) {
    // Given the sentence data, returns a deferred object resolved after duration time.
    var dfd = $.Deferred();
    setTimeout(function() { dfd.resolve(data); }, data.duration);
    return dfd;
}

function play_next() {
    // Play next sentence.
    load()
        .then(show)
        .then(play)
        .then(pause)
        .done(function(data) { console.log(data); });
}
