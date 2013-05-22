$(document).ready(load);



function reloadContent(){
	$.get("/Pages" + window.location.pathname, fillContent);
}

function load() {
    url = window.location.pathname;
    if (url == '/') {
        url = '/About'
    }
}


function fillContent(data) {
    $("#Content").empty();
    $("#Content").append(data);
    
}

function fillNews(data) {
    $("#Posts").append(data);

}

function changePage(path) {
    $.get("/Pages"+path,fillContent);
    history.pushState({},path,path);
}

function loginPage(){
	changePage("/Login")
}

function login(){
	var data = {};
	data.firstName= $("#firstName")[0].value;
	data.lastName = $("#lastName")[0].value;
	data.Password= $("#Password")[0].value;
	$.post("/python/login",data,loginCallback);
	username = data.firstName
	$("#login").empty();
	$("#login").append("<p>logging in</p>");
}

function loginCallback(data){
	if(data != "InvalidLogin"){
		$("#auth").empty();
		$("#auth").append("<img width='50' src='/static/Nav/id-card-md.png'  /><h3>Welcome, " + data  + "! </br> <a class='link' onclick='logout()'>Log out.</a></h3>");
		changePage("/About");
	}
	else{
		$("#login").empty();
		$("#login").append('<div id="login"><div><p>First Name:</p><input id="firstName" name="firstName"></input></div><div><p>Last Name:</p><input id="lastName" name="lastName"></input></div><div><p>Password:</p><input id="Password" name="Password" type="password"></input></div></div><a onclick="login()">log in</a><p>invalid login</p>');
	}
}

function logout(){
	$.get("/python/logout", {} , logoutCallback)
	$("#auth").empty();
	$("#auth").append("<h3>Logging Out</h3>");
}

function logoutCallback(data){
	$("#auth").empty();
	$("#auth").append('<a class="link" onclick="loginPage()"><img width="50" src="/static/Nav/id-card-md.png"  /><h3>Sign in</h3></a>');
	reloadContent();
}
