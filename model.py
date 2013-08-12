import web, datetime,sys

try:
  db=web.database(dbn="sqlite",db="IIITMK.db")
except: 
	print "Could not connect to database"
	sys.exit()

def getUsers():
	 return db.select('IIITMKLogin')

def get_posts():
    return db.select('OpinionPoll', order='id DESC')

def get_post(id):
    try:
        return db.select('OpinionPoll', where='id=$id', vars=locals())[0]
    except IndexError:
        return None

def new_post(title, text):
    db.insert('OpinionPoll', topic=title, content=text, posted_on=datetime.datetime.utcnow())

def del_post(id):
    db.delete('OpinionPoll', where="id=$id", vars=locals())

def update_post(id, title, text):
    db.update('OpinionPoll', where="id=$id", vars=locals(),topic=title, content=text)

def addforVote(pollid):
	db.update('OpinionPoll', where="id=$pollid", vars=locals(), for_vote = (for_vote) + 1)

def addagainstVote(pollid):
	db.update('OpinionPoll', where="id=$pollid", vars=locals(),against_vote =(against_vote) +1)

def new_event(title,content):

	db.insert('News_Events', headline=title, news_content=content, posted_on=datetime.datetime.utcnow())

def getAdminDetails(id):
	try:
		
		return db.select('IIITMKLogin',vars=locals(),what='username,password',where='account_type=$id')
		
	except IndexError:
		return None

def get_UserDetails(name):
	try:
		return db.select('UserDetails',vars=locals(),where='username=$name')
	except IndexError:
		return None

def get_Credentials(nme):
	return db.select('IIITMKLogin',vars=locals(),where='username=$nme')


def get_Requests():
	return db.select('UserDetails',vars=locals(),where='valid=0')


def approveUser(id):
	try:
		db.update('UserDetails',where="id=$id",vars=locals(),valid=1)
	except IndexError:
		return None

def rejectUser(id):
	try:
		db.update('UserDetails',where="id=$id",vars=locals(),valid=0)
	except IndexError:
		return None
def get_Members():
	return db.select("UserDetails",vars=locals(),what='id,username')

def sendMessage(id,name):
	row=db.select('UserDetails',vars=locals(),where='id=$id')
	for user in row:
		uname=user.username

		fromadrs=name

		msgtype="INBOX"
		reqMessage="Hi..:) I'm "+uname+" Lets be Friends??"
		db.insert('Mailbox',user_id=id, from_adrs=fromadrs,to_adrs=uname,message=reqMessage,msgtype=msgtype)

def composeMessage(fromid,name,to,body):
	msgtype="SENT"
	reqMessage="Hi..:) I'm "+name+" I'm sending you this mail for fun!!"
	db.insert('Mailbox',user_id=fromid, from_adrs=name,to_adrs=to,message=body,msgtype=msgtype)


def get_Messages(uid):
	return db.select('Mailbox',vars=locals(),where='user_id=$uid' )

def get_sentItems(uid):
	return db.select('Mailbox',vars=locals(),where='user_id=$uid and msgtype="SENT"' )

def get_Friends(id):
	
	print '************DEBUUUUUGGGGGG @ model.py***************'
	print id

	return db.query("select UserDetails.username from UserDetails JOIN Friends where UserDetails.id=Friends.friend_id and friend_id IN (select friend_id from Friends where user_id=$id)",vars=locals())

def addFriend(uid,fid):
	db.insert('Friends',user_id=uid,friend_id=fid,request_status="APPROVED");

def get_Discussions():
	return db.select('Discussions')

def add_discussion(user_id,disc_topic,discussion):

	 db.insert('Discussions',user_id=user_id,disc_topic=disc_topic,discussions= discussion)

def new_comment(title, text):
    db.insert('comments', topic=title, content=text, posted_on=datetime.datetime.utcnow())


def add_News(headline,news_content):
	db.insert('News_Events', headline=headline,news_content=news_content, posted_on=datetime.datetime.utcnow())

def get_News():
	return db.select('News_Events')
def deleteUser(name):

	db.delete('UserDetails', where="username=$name")
















		
