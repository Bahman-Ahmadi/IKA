from flask import Flask, render_template, request, redirect, flash
from werkzeug.utils import secure_filename
from datetime import datetime
from langlib1 import Persian
from json import loads,dumps
from hashlib import sha256
import urllib.request, os
from models import *


app = Flask(__name__)
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = "static/uploads/"
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

USER,ADMIN,ALLOWED_EXTENSIONS = None,None,set(['png','jpg','jpeg','gif'])
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS


#****************** Blog ******************#
@app.route('/')
def index():
	Post.post = loads(open("static/DB/posts.json").read())
	Post.slugs = [i.get("slug") for i in Post.posts]
	return render_template('index.html', account=USER, articles=Post.posts, Post=Post, commentsLengths=[len(i.get("comments")) for i in Post.posts])


@app.route('/',methods=['POST'])
@app.route("/api")
def api(): return str({"posts":loads(open("static/DB/posts.json").read())})


@app.route('/p/<slug>')
def postDetails(slug):
	Post.post = loads(open("static/DB/posts.json").read())
	Post.sluge = [i.get("slug") for i in Post.posts]
	try:
		post = Post.getPost(slug)
		post["align"], post["direction"] = "right" if Persian(post["content"][0]) else "left", "rtl" if Persian(post["content"][0]) else "ltr"
		return render_template("post.html", post=post)
	except IndexError: return "404-not found"


#****************** User ******************#
@app.route("/<ID>")
def userDetails(ID):
	if len(ID.split("/")) == 1:
		try:
			isAdmin = ID.lower() in [i.get("ID").lower() for i in loads(open("static/DB/admins.json").read())]
			return render_template("userDetails.html",user=User.getUser(ID),posts=loads(open("static/DB/posts.json").read()), isAdmin=isAdmin)
		except Exception as e:
			print(e)
		return redirect("/")


@app.route('/signup')
def signup(): return render_template('loginsignup.html',login=False)


@app.route('/signedup',methods=['POST'])
def signedup():
	result = []
	for i in request.form:
		result.append(request.form[i])
	account = User({'name':result[0],'password':result[1],'ID':result[2],'phone':result[3],'email':result[4],'birthdate':result[5],'joindate':datetime.now().strftime('%Y-%m-%d %H:%M'),'permissions':{'post': True,'chat': True},'isbanned':False})
	return redirect('/login')


@app.route('/login')
def login(): return render_template('loginsignup.html',login=True)


@app.route('/loggedin',methods=['POST'])
def loggedin():
	global USER
	file = loads(open('static/DB/users.json').read().strip())
	users, passwords, isbanneds, result = [i.get("ID") for i in file],[j.get("password") for j in file],[m.get("isbanned") for m in file],[request.form[i] for i in request.form]
	if result[0] in users and sha256(result[1].encode()).hexdigest() == passwords[users.index(result[0])] and not isbanneds[users.index(result[0])]:
		USER=User.getUser(request.form.get("id"))
		return redirect("/user")
	else: return 'wrong username or password; please try again!'


@app.route('/user')
def userPanel():
	User.users = loads(open('static/DB/users.json').read())
	global USER
	try:
		return render_template("user.html", user=User.getUser(USER.get("ID")), posts=loads(open('static/DB/posts.json').read()))
	except AttributeError:
		return redirect("/login")


@app.route("/user/newpost")
def user_newpost(): return render_template("userAddPost.html")


@app.route("/user/newpost", methods=["POST"])
def user_savepost():
	global USER
	result, file = [request.form[i] for i in request.form], request.files['file']
	if file and allowed_file(file.filename):
		filename = str(datetime.now())+"."+file.filename.split(".")[-1]
		file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
		print(filename,result)
		Post({
			"thumbnail":f"uploads/{filename}",
			"title":result[0],
			"preview":result[1][:30],
			"content":result[1],
			"author":USER.get("ID"),
			"likes":0,
			"comments":[],
			"keywords":result[2].split(" "),
			"released":False
		})
		flash("post successfully sent to admin panel")
	else:
		flash("Allowed image types are : png, jpg, jpeg, gif")

	return redirect("/user")


@app.route('/user/edit',methods=['POST'])
def editUser():
	global USER
	if USER != None:
		result = [request.form[i] for i in request.form]
		receivedData = {"name":result[0],"oldPassword":result[1],"newPassword":result[2],"repeatPassword":result[3],"phone":result[4],"email":result[5]}

		if sha256(receivedData.get("oldPassword").encode()).hexdigest != USER.get("password") or receivedData.get("newPassword") != receivedData.get("repeatPassword"):
			if sha256(receivedData.get("oldPassword").encode()).hexdigest != USER.get("password"):
				flash("your entered old password is not equal with really old password!")

			if receivedData.get("newPassword") != receivedData.get("repeatPassword"):
				flash("new password is not equal with repeat of that!")

			return render_template("user.html", user=USER, posts=loads(open('static/DB/posts.json').read()))

		else:
			flash("details edited successful!")
			if receivedData.get("name"): User.edit(USER.ID,"name",receivedData.get("name"))
			if receivedData.get("newPassword"): User.edit(USER.ID,"password",sha256(receivedData.get("newPassword").encode()).hexdigest())
			if receivedData.get("phone"): User.edit(USER.ID,"phone",receivedData.get("phone"))
			if receivedData.get("email"): User.edit(USER.ID,"email",receivedData.get("email"))
			return render_template("user.html", user=USER, posts=loads(open('static/DB/posts.json').read()))

	else:
		return redirect("/login")
	

#****************** Admin ******************#
@app.route('/admin')
def loginadmin(): return render_template('loginadmin.html')


@app.route('/admin',methods=['POST'])
def admin():
	Admin.admins = loads(open("static/DB/admins.json").read())
	Admin.ids = [i.get("ID") for i in Admin.admins]

	global ADMIN
	result = []
	for i in request.form:
		result.append(request.form[i])

	AdminIndex = 0
	for i in Admin.admins:
		if result[0] == i.get("ID"):
			im = Admin.admins[Admin.ids.index(i.get("ID"))]

	if result[0] in [i.get("ID") for i in Admin.admins] and sha256(result[1].encode()).hexdigest() == im.get("password"):
		ADMIN = Admin(result[0],result[1],im['permissions'])
		def getprop(prop): return Admin.get(result[0],prop)
		return render_template('admin.html',User=User,users=loads(open("static/DB/users.json").read()),admins=Admin.admins,admin=getprop,posts=loads(open('static/DB/posts.json').read()))
	else: return 'wrong username or password.<br/>are you sure that you are admin?'


@app.route("/admin/edit")
def editAdmin():
	permissions, result = ["viewMembers","viewAdmins","sendMessage","deleteMessage","editDetails","sendSpam","sendSwearWords"], [request.args[i] for i in request.args]

	if result[0] == "users":
		if result[1] == "details":
			User.edit(result[2], result[3], result[4] == "true")
		elif result[1] == "permissions":
			User.editPermissions(result[2], result[3], result[4] == "true")

	elif result[0] == "admins":
		if result[1] == "deactivate":
			Admin.deactivate(result[2])
		elif result[1] == "permissions":
			Admin.editPermissions(result[2], "posts", result[3]=="true")
			Admin.editPermissions(result[2], "chats", result[4]=="true")
			Admin.editPermissions(result[2], "users", result[5]=="true")
			Admin.editPermissions(result[2], "admins", result[6]=="true")
		elif result[1] == "new":
			Admin.new(result[7], User.getUser(result[2]), {"posts":result[3]=="true","chats":result[4]=="true","users":result[5]=="true","admins":result[6]=="true"})

	elif result[0] == "chats":
		Settings.settings = loads(open('static/DB/settings.json').read().strip())
		Settings.settings["myMessagesColors"]["back"], Settings.settings["myMessagesColors"]["front"], Settings.settings["otherMessagesColors"]["back"], Settings.settings["otherMessagesColors"]["front"] = "#"+result[3], "#"+result[4], "#"+result[5], "#"+result[6]
		open('static/DB/settings.json',"w").write(dumps(Settings.settings,indent=4))
		for i,j in zip(permissions, result[7:]):
			Settings.settings["permissions"][i] = bool(int(j))
		Settings("title",result[2])

	return "200"


@app.route("/admin/newpost")
def admin_newpost(): return render_template("new-post.html")


@app.route("/admin/newpost", methods=["POST"])
def admin_savepost():
	global ADMIN
	result = [request.form[i] for i in request.form]
	Post({
		"thumbnail":"uploads/1.jpg",
		"title":result[0],
		"preview":result[1][:30],
		"content":result[1],
		"author":ADMIN.get("ID"),
		"likes":0,
		"comments":[],
		"keywords":result[2].split(" "),
		"released":result[3]=="true"
	})
	return ""


#****************** Chat ******************#
@app.route('/chat')
def chat():
	global USER
	if USER != None and not USER.get("isbanned"): return render_template("chat.html",settings=loads(open('static/DB/settings.json').read().strip()),users=len([i for i in loads(open('static/DB/users.json').read().strip()) if not i.get("isbanned")]),user=USER)
	else: return "this page can't load, because:<br/>1. you're not logged in to your account<br/>2. your account is ban"


@app.route('/chat/getall')
def getchats(): return open("static/DB/chats.json").read()


@app.route('/getMessage/<ID>')
def getMessage(ID):
	try: return Chat().get(ID)
	except IndexError: return {}


@app.route('/newMessage')
def newMessage():
	result = [request.args[i] for i in request.args]
	Chat().new(
		result[0],
		result[1] if result[1]==USER.get("ID") else None,
		result[2],
		result[3],
		result[4]
	)
	return "ok"


#****************** Other ******************#
@app.route("/static/DB/users.json", methods=["GET","POST"])
@app.route("/static/DB/admins.json", methods=["GET","POST"])
def error(): return "you can't do that, script kid! ;-)"


if __name__ == '__main__':
	app.run(debug=True)