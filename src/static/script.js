$(document).ready(load);





function load() {
    url = window.location.pathname;
    if (url == '/') {
        url = '/About'
    }
}


function fillContent(data) {
    $("#Content").empty();
    $("#Content").append(data);
//   history.pushState({},path,path);
}

function fillNews(data) {
    $("#Posts").append(data);

}

function changePage(path) {
    $.get("/Pages"+path,fillContent);
    
}
