function savePost() {
	var title = document.getElementById("title").value;
	var content = document.getElementById("content").value;
	var keywords = document.getElementById("keywords").value;
	var releasable = document.getElementById("releasable").checked;

	var xhr = new XMLHttpRequest();
	xhr.open("POST", `http://127.0.0.1:5000/newpost?title=${title}&content=${content}&keywords=${keywords}&releasable=${releasable}`, true);
	xhr.send();
}
function saveChatSettings() {
	var title = document.getElementById("title").value == ""?"IKA313": document.getElementById("title").value;
	var my_message_out = document.getElementById("my_message_out").value.split("#")[1];
	var my_message_in = document.getElementById("my_message_in").value.split("#")[1];
	var other_message_out = document.getElementById("other_message_out").value.split("#")[1];
	var other_message_in = document.getElementById("other_message_in").value.split("#")[1];
	var viewMembers = document.getElementById("viewMembers").checked == true?"1": "0";
	var viewAdmins = document.getElementById("viewAdmins").checked == true?"1": "0";
	var sendMessage = document.getElementById("sendMessage").checked == true?"1": "0";
	var deleteMessages = document.getElementById("deleteMessages").checked == true?"1": "0";
	var editDetails = document.getElementById("editDetails").checked == true?"1": "0";
	var sendSpam = document.getElementById("sendSpam").checked == true?"1": "0";
	var sendSwearWords = document.getElementById("sendSwearWords").checked == true?"1": "0";

	var xhr = new XMLHttpRequest();
	xhr.open("GET", `http://127.0.0.1:5000/admin/edit?db=chats&action=edit&title=${title}&my_message_out=${my_message_out}&my_message_in=${my_message_in}&other_message_out=${other_message_out}&other_message_in=${other_message_in}&viewMembers=${viewMembers}&viewAdmins=${viewAdmins}&sendMessage=${sendMessage}&deleteMessages=${deleteMessages}&editDetails=${editDetails}&sendSpam=${sendSpam}&sendSwearWords=${sendSwearWords}`, true);
	xhr.send();
}
function saveAdminSettings(action, args) {
	var xhr = new XMLHttpRequest();
	if (action == "new" || action == "permissions") {
		xhr.open("GET", `http://127.0.0.1:5000/admin/edit?db=admins&action=${action}&ID=${args[0]}&accessToPosts=${args[1]}&accessToChats=${args[2]}&accessToUsers=${args[3]}&accessToAdmins=${args[4]}&attribute=${args[5]}`, true);
	} else if (action == "deactivate") {
		xhr.open("GET", `http://127.0.0.1:5000/admin/edit?db=admins&action=${action}&ID=${args[0]}`, true);
	}
	xhr.send();
}
function saveUserSettings(id, DorP, arg) {
	var key = arg.split("=")[0];
	var val = eval(arg.split("=")[1]);

	var xhr = new XMLHttpRequest();
	xhr.open("GET", `http://127.0.0.1:5000/admin/edit?db=users&action=${DorP}&ID=${id}&key=${key}&value=${val}`, true);
	xhr.send();
}