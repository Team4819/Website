$(document).ready(load);





function load() {
    url = window.location.pathname;
    if (url == '/') {
        url = '/About'
    }
    $.get("/Content"+url,fillContent);
}


function fillContent(data) {
    $("#Content").empty();
    $("#Content").append(data);
}

function fillNews(data) {
    $("#Posts").append(data);

}

function changePage(path) {
    $.get("/Content"+path,fillContent);
    history.pushState({},path,path);
}