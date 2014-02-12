function inject(url) {
    var ajaxRq = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject("Msxml2.XMLHTTP");
    ajaxRq.open("GET", url, false);
    ajaxRq.send(null);
    document.write(ajaxRq.responseText);
}