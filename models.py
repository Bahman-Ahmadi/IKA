from json import loads,dumps
from hashlib import sha256

class User:
	users = loads(open('static/DB/users.json').read().strip())
	ids = [i.get("ID").lower() for i in users]

	def __init__(self, details):
		if not details.get("ID") in User.ids:
			User.users.append(details)
			details["password"] = sha256(details.get("password").encode()).hexdigest()
			details["avatar"] = "assets/profile.jpg"
			details["followings"], details["followers"] = [],[]
			open('static/DB/users.json',"w").write(dumps(User.users,indent=4))
			User.ids.append(details.get("ID"))
		else:
			raise TypeError('id is exist')

	@staticmethod
	def getUser(ID):
		if ID.lower() in User.ids:
			return User.users[User.ids.index(ID.lower())]
		else:
			raise TypeError('id is wrong')

	@staticmethod
	def edit(ID,key,value):
		if key == "password": User.users[User.ids.index(ID)]["password"] = sha256(value.encode()).hexdigest()
		else: User.users[User.ids.index(ID)][key] = value
		open('static/DB/users.json',"w").write(dumps(User.users,indent=4))

	@staticmethod
	def editPermissions(ID, key, value):
		User.users[User.ids.index(ID)]["permissions"][key] = value
		open('static/DB/users.json',"w").write(dumps(User.users,indent=4))


class Admin():
	admins = loads(open("static/DB/admins.json").read())
	ids = [i.get("ID") for i in admins]

	def __init__(self, ID, password, permissions):
		self.account     = User.getUser(ID)
		self.permissions = permissions

	@staticmethod
	def get(ID, prop):
		return Admin.admins[Admin.ids.index(ID)].get(prop)

	@staticmethod
	def edit(ID, key, value):
		if key == "password": Admin.admins[Admin.ids.index(ID)][key] = sha256(value.encode()).hexdigest()
		else: Admin.admins[Admin.ids.index(ID)][key] = value
		open('static/DB/admins.json',"w").write(dumps(Admin.admins,indent=4))

	@staticmethod
	def editPermissions(ID, key, value):
		print(ID,key,value)
		print(Admin.ids.index(ID),Admin.admins[Admin.ids.index(ID)])
		Admin.admins[Admin.ids.index(ID)]["permissions"][key] = value
		open('static/DB/admins.json',"w").write(dumps(Admin.admins,indent=4))

	@staticmethod
	def new(account, permissions):
		Admin.admins.append({"attribute": account.get("attribute"), "ID": account.get("ID"), "password": account.get("password"), "permissions":permissions})
		Admin.ids.append(account.get("ID"))
		open('static/DB/admins.json',"w").write(dumps(Admin.admins,indent=4))

	@staticmethod
	def deactivate(ID):
		Admin.admins.remove(Admin.admins[Admin.ids.index(ID)])
		Admin.ids.remove(ID)
		open('static/DB/admins.json',"w").write(dumps(Admin.admins,indent=4))


class Post():
	posts = loads(open('static/DB/posts.json').read())
	slugs = [i.get("slug") for i in posts]
	def __init__(self,details):
		from requests import get
		details["ID"], details["slug"] = len(Post.posts), details.get("title").replace(" ","-")
		link = "127.0.0.1:5000/p/"+details["slug"]
		try:
			details["link"] = get("https://rizy.ir/st?api=64f7450caf6800c3d29f3f627137ebc65b1828b2&url="+link).text
		except:
			details["link"] = link
		Post.posts.append(details)
		open('static/DB/posts.json',"w").write(dumps(Post.posts,indent=4))

	@staticmethod
	def getPost(slug):
		return Post.posts[Post.slugs.index(slug)]

	@staticmethod
	def edit(ID,key,value):
		Post.posts[ID-1][key] = value
		open('static/DB/posts.json',"w").write(Post.posts)

	@staticmethod
	def delete(ID):
		Post.posts.remove(Post.posts[ID-1])
		open("static/DB/posts.json","w").write(Post.posts)


class Settings():
	settings = loads(open('static/DB/settings.json').read())
	def __init__(self,key,value):
		'''this method (constructor) is to edit a setting'''
		Settings.settings[key] = value
		open('static/DB/settings.json',"w").write(dumps(Settings.settings,indent=4))

	@staticmethod
	def read(key):
		return Settings.get(key)


class Chat():
	def __init__(self):
		self.chats = loads(open('static/DB/chats.json').read()).get("messages")
		self.IDs = [int(i.get("ID")) for i in self.chats]

	def get(self,ID):
		return self.chats[self.IDs.index(ID)]

	@staticmethod
	def new(TYPE, FROM, REPLIED, DETAILS, CONTENT):
		file = loads(open('static/DB/chats.json').read()).get("messages")
		sender = User.getUser(FROM).get
		senderRank = "admin" if FROM in [i.get("ID") for i in loads(open("static/DB/admins.json").read())] else "user"
		data = {
			"type":TYPE,
			"from":{
					"name":sender("name"),
					"ID":FROM,
					"avatar":sender("avatar"),
					"rank": {
					"title": senderRank,
					"status": None if senderRank == "user" else {
						"attribute":Admin.get(FROM,"attribute"),
						"permissions": {
							"posts":Admin.get(FROM,"permissions").get("posts"),
							"chats":Admin.get(FROM,"permissions").get("chats"),
							"users":Admin.get(FROM,"permissions").get("users"),
							"admins":Admin.get(FROM,"permissions").get("admins")
						}
					}
				}
			},
			"replied":REPLIED,
			"replies":[],
			"details":DETAILS,
			"ID":len(loads(open('static/DB/chats.json').read())),
			"content": CONTENT,
			"status": {
				"sent": True
			}
		}
		file.append(data)
		open('static/DB/chats.json',"w").write(dumps({"messages":file},indent=4))

	def edit(self,ID, key, value):
		datas = loads(open('static/DB/chats.json').read())
		if type(key) == str: datas[ID][key] = value
		else:
			keys = ["["+i+"]" for i in key]
			exec(f"datas[{ID}]{''.join(keys)} = {value}")
		open('static/DB/chats.json',"w").write(dumps(datas),indent=4)