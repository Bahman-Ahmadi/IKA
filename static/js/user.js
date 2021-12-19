function savePost() {
	var title = document.getElementById("title").value;
	var content = document.getElementById("content").value;
	var keywords = document.getElementById("keywords").value;
	var releasable = document.getElementById("releasable").checked;

	var xhr = new XMLHttpRequest();
	xhr.open("POST", `http://127.0.0.1:5000/user/newpost?title=${title}&content=${content}&keywords=${keywords}&releasable=${releasable}`, true);
	xhr.send();
}