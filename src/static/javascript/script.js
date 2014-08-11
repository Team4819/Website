$(document).ready(load);



function reloadContent(){
	$.get("/Pages" + window.location.pathname, fillContent);
}

function load() {
	
	ourl = window.location.pathname
	LoggedIn = ($.cookie("LoginStatus")=="LoggedIn")
	$(window).bind('popstate', function(event) {
	    nurl = window.location.pathname;
	    console.log("ourl=" + ourl + " nurl=" + nurl);
	    if(nurl != ourl){
		    if (nurl == '/') {
		        nurl = '/Home'
		    }
	    $.get("/Pages"+nurl,fillContent);
	    _gaq.push(['_trackPageview']);
	    }
	    ourl = nurl
	});
	
}

function navigate(e, target){
	changePage(target.getAttribute('href'));
	e.preventDefault();
}

function fillContent(data) {
    $("#Content").empty();
    $("#Content").append(data);
    $(window).scrollTop();
}

function togglePanel(panelRefrence){
	var panels = $(panelRefrence).siblings().attr("hidden","true");
	if($(panelRefrence).attr("hidden") == "undefined") 
		$(panelRefrence).attr("hidden", "true");
	else 	
		$(panelRefrence).removeAttr("hidden")
}

function changePage(path) {
	console.log("changing to " + path)
    $.get("/Pages"+path,fillContent);
    url = window.location.pathname;
    if (url == '/') {
        url = '/Home'
    }
    history.pushState({"path": url},"",path);
    ourl = path;
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
		changePage("/Home");
		if($.cookie("Subscribed")=="True")
			togglePanel("#SubscribedPanel")
		else togglePanel("#SubscribePanel")
		LoggedIn = true;
		_gaq.push(['_trackEvent', 'Authentication', 'Login', data]);
	}
	else{
		togglePanel("#login #loginPanel");
		$("#invalidLogin").removeAttr("hidden");
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
	_gaq.push(['_trackEvent', 'Authentication', 'Logout']);
	reloadContent();
}

function submitSubscribe(){
	var data = {"email": $("#Subscribe #email")[0].value};
	if(data == "")$.get("/python/subscribe", data, function(data){togglePanel("#SubscribedPanel")});
	else $.get("/python/subscribe", data, function(data){togglePanel("#PublicSubscribedPanel")});
}

function submitUnsubscribe(){
	var data = {"email": $("#Subscribe #email")[0].value};
	$.get("/python/unsubscribe", data, function(data){togglePanel("#SubscribePanel")});
}
