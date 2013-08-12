#!/usr/bin/env python
"""
A simple Web Portal for IIITMK Friends
author: Chethana Bhaskaran
website: www.chethanatly.blogspot.com
last modified: August 12 2013
"""
import web
import sys
import Image
import model  	#db functions are defined in this module
import datetime




### Url mappings

urls = ('/' ,'IIITMKIndex',
'/register', 'Register',
'/myHomePage', 'Home',
'/editProfile','EditProfile',
'/myProfile','Profile',
'/viewDiscussionBoard' ,'DiscussionBoard',
'/viewDiscussions' ,'Discussions',
'/postDiscussion' ,'NewDiscussion',
'/addNews&Events','PostNews',
'/viewNews&Events','NewsandEvents',
'/viewMessageBox','Message',
'/composeMessage','compose',
'/viewSentMessages','Sent',
'/viewMembers','Member',
'/listFriends','Friends',
'/addFriend','AddFriend',
'/viewOpinionPolls','ViewPoll',
'/createPoll','NewOpinionPoll',
'/viewsinglepoll/(\d+)','Viewsinglepoll',
'/comment','comment',

'/adminLogin','Admin',
'/approveMembers','Approve',

'/login', 'Login',
'/logout', 'Logout',

)


web.config.debug = False 		#for sessions to work

app=web.application(urls,globals())

### Sessions


if web.config.get('_session') is None:
    session = web.session.Session(app, web.session.DiskStore('sessions'), {'count': 0})
    web.config._session = session
else:
    session = web.config._session

try:
	db=web.database(dbn="sqlite",db="IIITMK.db")
except: 
	print "Could not connect to database"
	sys.exit()

### Templates

render=web.template.render('templates/',globals={'session_user': session})


class IIITMKIndex:
	
	def GET(self):
		return render.loginScreen()
	def POST(self):
		inp=web.input()
		nme=inp.username
		credentials=model.get_Credentials(nme)
		if(credentials):
			for user in credentials:
				if(inp.username==user.username and inp.passwordbox==user.password):
					web.setcookie('username',inp.username)
					name=web.cookies().get('username')
					print '***********SESSION NAME PASSED*****************'
					print name
					return render.myHomePage(name)
				else:
					return render.unAuthorised(name=inp.username)
		else:
			return render.unAuthorised(name=inp.username)

		

class Login:
    def GET(self):
        session.logged_in = True
        raise web.seeother('/')

class Logout:
    def GET(self):
        session.logged_in = False
	web.setcookie('username'," ")
        raise web.seeother('/')

class Register:

	
	def GET(self):
		inp=web.input()
		param=""
       		return render.createProfile(param)

	def POST(self):

		i = web.input()
    		if i.form_action == 'Upload':
         		#Image Upload
			try:
				x = web.input(profile_pic_file={})
				filedir='./static/profilepics' 	#/path/where/you/want/to/save image
				if 'profile_pic_file' in x:
					filepath=x.profile_pic_file.filename.replace('\\','/') # replaces the windows-style slashes with linux ones.
					filename=filepath.split('/')[-1] # splits the / and chooses the last part (the filename with extension)
					fout = open(filedir +'/'+ filename,'w') # creates the file where the uploaded file should be stored
					fout.write(x.profile_pic_file.file.read()) # writes the uploaded file to the newly created file.
					fout.close() # closes the file, upload complete.

					infile = filedir +'/'+filename
					outfile = infile + ".thumbnail"
					im = Image.open(filedir +'/'+filename)
					im.thumbnail((120, 120))
					im.save(outfile, im.format)
				return render.createProfile(outfile)
			except:
				print "Could not upload image;Unexpected error:", sys.exc_info()[0]
				sys.exit()
    		elif i.form_action == 'submit':
         		# Do submit button action
			inp=web.input()
			web.setcookie('username',inp.username)
			inp.profilepic=""
			toLoginTable=db.insert('IIITMKLogin',username=inp.username, password=inp.password,account_type=inp.acc_type);
			toUserdetailsTable=db.insert('UserDetails',username=inp.username,fullname=inp.fullname,email=inp.email,account_type=inp.acc_type,designation=inp.designation,age=inp.age,batch=inp.batch,profilepic=inp.profilepic)
			name=web.cookies().get('username')
			return render.myHomePage(name)
		else:
			"""delete account"""
			name=web.cookies().get('username')
			model.deleteUser(name)


class EditProfile:
	
	def GET(self):
		def GET(self):
			"""show profilepage"""
			name=web.cookies().get('username')
			details=model.get_UserDetails(name)
			return render.myProfile(details)


	def POST(self):
		name=web.cookies().get('username')
		inp=web.input()
		inp.profilepic=""
		
		db.update('UserDetails',where="username=$name",vars=locals(),fullname=inp.fullname,email=inp.email,account_type=inp.desig,designation=inp.desig,age=inp.age,batch=inp.batch,profilepic=inp.profilepic)
		print '***********PROFILE UPDATED*****************'
		return render.myHomePage(name)

class Profile:
	def GET(self):
		"""show profilepage"""
		name=web.cookies().get('username')
		details=model.get_UserDetails(name)
		return render.myProfile(details)


class Admin:
	def GET(self):
		return render.adminLogin()
	def POST(self):
		inp=web.input()
		web.setcookie('username',inp.username)
		name=web.cookies().get('username')
		id=1
		alladmin=model.getAdminDetails(int(id))
		for admin in alladmin:
			if(inp.username==admin.username and inp.passwordbox==admin.password):
				return render.adminHome()
			else:
				return render.unAuthorised(name=inp.username)


class Approve:
	def GET(self):
		
		requests=model.get_Requests()
		return render.approveUsers(requests)
	def POST(self):
		inp=web.input()
		id=inp.user

		print '************DEBUUUUUGGGGGG* APPROVE FRIEND**************'
		print id

		if inp.admin_decision=="Approve":
			model.approveUser(int(id))
		else:
			model.rejectUser(int(id))

		requests=model.get_Requests()
		return render.approveUsers(requests)

class Home:
	def GET(self):
		name=web.cookies().get('username')
		return render.myHomePage(name)
			
class AddFriend:
	def GET(self):
		web.seeother('/viewMembers')
	
class NewOpinionPoll:

    form = web.form.Form(
        web.form.Textbox('title', web.form.notnull,size=30,description="Post title:"),
        web.form.Textarea('content', web.form.notnull, rows=10, cols=80,description="Post content:"),
        web.form.Button('Post entry'),)

    def GET(self):
        form = self.form()
        return render.createPoll(form)

    def POST(self):
        form = self.form()
        if not form.validates():
            return render.createPoll(form)
	model.new_post(form.d.title,form.d.content);
	print '***********New Poll Added*****************'
	raise web.seeother('/createPoll')

class ViewPoll:
	def GET(self):
		"""view opinion polls"""
		posts=model.get_posts()
		return render.viewOpinionPolls(posts)

class Viewsinglepoll:
	def GET(self,id):
		""" View single poll """
		post = model.get_post(int(id))
		return render.viewSinglePoll(post)
	def POST(self,id):
		i=web.input()
		poll_id=i.pollid
		
		if i.action_vote=="Vote ^":
			model.addforVote(int(poll_id))
		else:
			model.addagainstVote(int(poll_id))

		print '***********Voted*****************'

		raise web.seeother('/viewOpinionPolls')


class Discussions:
	"""Lists only topics of Discussion"""

	def GET(self):
		discussions=model.get_Discussions();
		return render.viewDiscussions(discussions)

	def POST(self):
		return render.postDiscussion()
		
		

class DiscussionBoard:

	"""Lists Full content of Discussion"""

	def GET(self):
		discussions=model.get_Discussions();
		return render.viewDiscussionBoard(discussions)
	def POST(self):
		inp=web.input()		
		if(inp.discussion_action=="Start New Discussion"):
			return web.seeother('/postDiscussion')	
		else:
			"""Add comment to Discussion"""
#			inp=web.input()
#			name=web.cookies().get('username')
#			userdata = model.get_UserDetails(name)
#			for userid in userdata:
#				user_id=userid.id
#			disc_topic=inp.title
#			dicsussion=inp.content
#			model.new_comment(disc_topic,dicsussion)

			discussions=model.get_Discussions();
			return render.viewDiscussionBoard(discussions)
			


class NewDiscussion:
	def GET(self):
		return render.postDiscussion()
	def POST(self):
		"""Creating new Discussion"""
		inp=web.input()
		name=web.cookies().get('username')
		userdata = model.get_UserDetails(name)
		for userid in userdata:
			user_id=userid.id
		disc_topic=inp.title
		discussion=inp.content
		model.add_discussion(user_id,disc_topic,discussion)
		discussions=model.get_Discussions();
		return render.viewDiscussionBoard(discussions)
			

class comment:
	form = web.form.Form(web.form.Textbox('title', web.form.notnull,size=30,description="Post title:"),web.form.Textarea('content',web.form.notnull, rows=10, cols=80,description="Post content:"),web.form.Button('Post comment'),)

	def GET(self):
		form = self.form()
		return render.comment(form)
	def POST(self):
		form = self.form()
		if not form.validates():
		    return render.comment(form)
		model.new_comment(form.d.title,form.d.content);
		print '***********New comment Added*****************'
		raise web.seeother('/comment')

class NewsandEvents:
	"""Lists only topics of Discussion"""
	def GET(self):
		newslist=model.get_News();
		return render.viewNewsandEvents(newslist)
class PostNews:
	form = web.form.Form(
        web.form.Textbox('title', web.form.notnull,size=30,description="News/Event title:"),
        web.form.Textarea('content', web.form.notnull, rows=10, cols=80,description="Post content:"),
        web.form.Button('Post entry'),)

	def GET(self):
		form = self.form()
		return render.addNews(form)

	def POST(self):
		form = self.form()
		if not form.validates():
		    return render.addNews(form)
		model.new_event(form.d.title,form.d.content);
		print '***********New Event/News Added*****************'
		raise web.seeother('/addNews&Events')
			
class Message:
	def GET(self):
		name=web.cookies().get('username')
		userdata = model.get_UserDetails(name)
		for userid in userdata:
			uid=userid.id
		msginbox=model.get_Messages(uid)

		if(msginbox):
			return render.viewMessageBox(msginbox)
		else:
			return render.viewMessageBox(msginbox="")
	def POST(self):
		i=web.input()
		if i.msgaction=="COMPOSE":
			web.seeother('/composeMessage')
		else:
			web.seeother('/viewSentMessages')

class compose:
	def GET(self):
		return render.composeMessage()
	def POST(self):
		inp=web.input()
		to=inp.toaddress
		body=inp.msgbody
		name=web.cookies().get('username')
		userdata = model.get_UserDetails(name)
		for userid in userdata:
			fromid=userid.id
		model.composeMessage(fromid,name,to,body)
		return web.seeother('/viewSentMessages')

	
class Sent:
	def GET(self):
		name=web.cookies().get('username')
		userdata = model.get_UserDetails(name)
		for userid in userdata:
			uid=userid.id
		msgsent=model.get_sentItems(uid)
		return render.viewSentMessages(msgsent)
class Member:
	def GET(self):
		members=model.get_Members()
		return render.viewMembers(members)
	def POST(self):
		inp=web.input()
		id=inp.member
		name=web.cookies().get('username')

		print '************DEBUUUUUGGGGGG ADD FRIEND***************'
		print id


		fid=inp.member
		userdata = model.get_UserDetails(name)
		for userid in userdata:
			uid=userid.id
		
		model.addFriend(int(uid),int(fid))

		model.sendMessage(int(id),name)
		members=model.get_Members()
		return render.viewMembers(members)

class Friends:
	def GET(self):
		name=web.cookies().get('username')
		userdetails = model.get_UserDetails(name)
		for user in userdetails:
			id=user.id

		print '************DEBUUUUUGGGGGG ID IS RIGHTTT???***************'
		print id

		friends=model.get_Friends(int(id))
		return render.listFriends(friends)
	def POST(self):
		#show profilepage
		i=web.input()
		name=i.friendid
		details=model.get_UserDetails(name)
		return render.myProfile(details)

class Poll:
	def GET(self):
		return render.listOpinionPolls()

	
if __name__=='__main__':
	
	app.run()
