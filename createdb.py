#! /usr/bin/env python
import sqlite3

connect=sqlite3.connect("IIITMK.db")
cursor=connect.cursor()

cursor.execute('create table IIITMKLogin(id integer primary key not null,username varchar(15),password varchar(15),account_type integer)')
cursor.execute('create table UserDetails(id integer primary key not null,username varchar(15),fullname varchar(15),email varchar(15),account_type varchar(15),designation varchar(15),age integer,batch varchar(15),profilepic BLOB)')


cursor.execute('create table OpinionPoll(id integer primary key not null ,topic TEXT,content TEXT,posted_on DATETIME,for_vote integer default 0,against_vote integer default 0 )')

cursor.execute('create table Mailbox(id integer primary key not null,user_id integer,from_adrs varchar(15),to_adrs varchar(15),message TEXT,msgtype varchar(15))')

cursor.execute('create table Friends(id integer primary key not null,user_id integer,friend_id integer,request_status text)')
cursor.execute('create table Discussions(disc_id integer primary key not null,user_id integer,disc_topic text,comment_id integer,discussion text)')

cursor.execute('create table Comments(comment_id integer primary key not null,user_id integer,disc_id integer,comment text)')
cursor.execute('create table News_Events(news_id integer primary key not null,headline text,news_content text,posted_on DATETIME)')

connect.commit()
cursor.close()
