function play(){
    var aud = document.getElementById('aud')
    var audio = new Audio(aud.value);
    audio.play()
    console.log(aud.value)
}
function hyperlink(w){
    ar = w.split(" ")
    if (ar.length == 1){
        window.location.href = "/link/"+w
    }
}