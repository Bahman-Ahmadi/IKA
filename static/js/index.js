function goto(link) {
	document.body.innerHTML += `<a href="${link}" id="clickme"></a>`;
	document.getElementById("clickme").click();
}

var elems = document.querySelectorAll('.sidenav');
var instances = M.Sidenav.init(elems);