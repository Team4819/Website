$(document).ready(load);



function reloadContent(){
	$.get("/Pages" + window.location.pathname, fillContent);
}

function load() {
	ourl = window.location.pathname
	LoggedIn = ($.cookie("LoginStatus")=="LoggedIn")
	$(window).bind('popstate', function(event) {
	    nurl = window.location.pathname;
	    if(nurl != ourl){
		    if (nurl == '/') {
		        nurl = '/About'
		    }
	    $.get("/Pages"+nurl,fillContent);
	    _gaq.push(['_trackPageview']);
	    }
	    ourl = nurl
	});
	
}

function navigate(e, target){
	changePage(target.getAttribute('href'));
	e.preventDefault()
	
}

function fillContent(data) {
    $("#Content").empty();
    $("#Content").append(data);
    
}

function togglePanel(panelRefrence){
	var panels = $(panelRefrence).siblings()
	for(var i = 0; i < panels.length; i++)
		panels[i].hidden = true
	$(panelRefrence)[0].hidden = !$(panelRefrence)[0].hidden
}

function changePage(path) {
    $.get("/Pages"+path,fillContent);
    url = window.location.pathname;
    if (url == '/') {
        url = '/About'
    }
    history.pushState({"path": url},"",path);
    _gaq.push(['_trackPageview']);
}


function login(){
	var data = {};
	data.firstName= $("#firstName")[0].value;
	data.lastName = $("#lastName")[0].value;
	data.Password= $("#Password")[0].value;
	$.post("/python/login",data,loginCallback);
	togglePanel("#login #loggingInPanel");

}

function loginCallback(data){
	if(data != "InvalidLogin"){
		togglePanel("#auth #welcome");
		$(".username").empty();
		$(".username").append(data);
		changePage("/About");
		if($.cookie("Subscribed")=="True")
			togglePanel("#SubscribedPanel")
		else togglePanel("#SubscribePanel")
		LoggedIn = true;
	}
	else{
		togglePanel("#login #loginPanel");
		$("#invalidLogin")[0].hidden=false;
		}
}

function logout(){
	$.get("/python/logout", {} , logoutCallback);
	togglePanel("#auth #loggingOut");
}

function logoutCallback(data){
	togglePanel("#auth #login")
	togglePanel("#SubscribePanel")
	LoggedIn = false;
	reloadContent();
}

function submitSubscribe(){
	var data = {"email": $("#Subscribe #email")[0].value};
	$.get("/python/subscribe", data, function(data){togglePanel("#SubscribedPanel")});
}