var first = "";
var isPersian = false;
function uppedKey(That) {
	if (first == "") {
		first = That.value;
	}if (That.value == "") {
		first = "";
	}
	if (first == 'a' || first == 'b' || first == 'c' || first == 'd' || first == 'e' || first == 'f' || first == 'g' || first == 'h' || first == 'i' || first == 'j' || first == 'k' || first == 'l' || first == 'm' || first == 'n' || first == 'o' || first == 'p' || first == 'q' || first == 'r' || first == 's' || first == 't' || first == 'u' || first == 'v' || first == 'w' || first == 'x' || first == 'y' || first == 'z' || first == '&' || first == '$' || first == '"' || first == '"' || first == ';' || first == ',' || first == '1' || first == '2' || first == '3' || first == '4' || first == '5' || first == '6' || first == '7' || first == '8' || first == '9' || first == '0' || first == 'A' || first == 'B' || first == 'C' || first == 'D' || first == 'E' || first == 'F' || first == 'G' || first == 'H' || first == 'I' || first == 'J' || first == 'K' || first == 'L' || first == 'M' || first == 'N' || first == 'O' || first == 'P' || first == 'Q' || first == 'R' || first == 'S' || first == 'T' || first == 'U' || first == 'V' || first == 'W' || first == 'X' || first == 'Y' || first == 'Z') {
		That.dir = 'ltr';
		isPersian = false;
	} else {
		That.dir = 'rtl';
		isPersian = true;
	}
}

/*function sendForm() {
	let date = new Date();
	let now = `${date.getHours()}:${(""+date.getMinutes()).length == 1? "0"+date.getMinutes(): date.getMinutes()}`;
	var msgElement = document.getElementsByName("message")[0];
	if (msgElement.value.replace(/\n/g, "").replace(/ /g, "").replace(/‌/g, "").replace(/‍/g, "") == "") {
		msgElement.value = "";
		msgElement.className = "msg-field vibrate";
		setTimeout(function () {
			msgElement.className = msgElement.className.replace("vibrate", "");
		}, 800);
		msgElement.focus();
		return null;
	}
	var first = msgElement.value[0];
	var dir = "rtl";
	if (first == 'a' || first == 'b' || first == 'c' || first == 'd' || first == 'e' || first == 'f' || first == 'g' || first == 'h' || first == 'i' || first == 'j' || first == 'k' || first == 'l' || first == 'm' || first == 'n' || first == 'o' || first == 'p' || first == 'q' || first == 'r' || first == 's' || first == 't' || first == 'u' || first == 'v' || first == 'w' || first == 'x' || first == 'y' || first == 'z' || first == '&' || first == '$' || first == '"' || first == '"' || first == ';' || first == ',' || first == '1' || first == '2' || first == '3' || first == '4' || first == '5' || first == '6' || first == '7' || first == '8' || first == '9' || first == '0' || first == 'A' || first == 'B' || first == 'C' || first == 'D' || first == 'E' || first == 'F' || first == 'G' || first == 'H' || first == 'I' || first == 'J' || first == 'K' || first == 'L' || first == 'M' || first == 'N' || first == 'O' || first == 'P' || first == 'Q' || first == 'R' || first == 'S' || first == 'T' || first == 'U' || first == 'V' || first == 'W' || first == 'X' || first == 'Y' || first == 'Z') {
		dir = "ltr";
	}
	var msgText = msgElement.value;
	if (msgText.length > 30) {
		var cuttedString = msgText.match(/.{30}|.{1,30}/g);
		var result = "";
		for (var i = 0; i < cuttedString.length; i++) {
			result += cuttedString[i]+"<br />";
		}
		msgText = result;
	}

	try {
		document.getElementById("down").remove();
	}catch (e) {}

	document.getElementsByClassName("chats")[0].innerHTML += `<div class="chat my-msg"  style="${document.getElementsByClassName("chat")[document.getElementsByClassName("chat").length-1].className == "chat my-msg" ? "margin-top: 3px;": "margin-top: 10px;"} ; ${dir == "rtl" ? "direction: rtl; text-align: right;": "direction: ltr; text-align: left;" }">
	${msgText.replace(/\n/g, "<br />")}
	<br />
	<span class="details" dir="ltr">${now} - √√</span>
	</div>`;

	document.getElementsByClassName("chats")[0].innerHTML += "<a href='#down' id='down'></a>";
	document.getElementById('down').click();

	msgElement.value = "";
	msgElement.dir = "ltr";
	msgElement.focus();
}*/