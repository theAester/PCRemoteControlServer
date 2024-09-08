window.onload = function () {
    document.getElementsByClassName('expand')[0].addEventListener('click', function () {
        var elems = document.getElementsByClassName('expanded');
        for(var i =0; i < elems.length; i++){
            elems[i].classList.toggle("hide");
        }
        if (this.innerText.indexOf("Less") != -1) {
            this.innerHTML = "------- More Details &darr; -------";
        } else {
            this.innerHTML = "------- Less Details &uarr; -------";
        }
    });
}