# -*- coding: utf-8 -*-

import commands, MySQLdb, re
from time import sleep

USER = 'karamfil'

def db_connect():
	db = MySQLdb.connect(host = 'nakor',  user = 'sites', passwd = 'M0reFun', db = 'test')
	
	return db, db.cursor()

def is_idle():
	cmd = commands.getoutput('gnome-screensaver-command -q').split('\n')[0].split(' ')[-1]
	
	return cmd == 'active'

def get_window_class():
	cmd = commands.getoutput("xprop -id $(xprop -root _NET_ACTIVE_WINDOW | cut -d ' ' -f 5)  WM_CLASS")
	
	try:
		cmd = cmd[20:].split('", "')[1].strip('"')
	except:
		print cmd
		exit()
	
	return cmd

db, c = db_connect()

modified = re.compile(r'\*(\])$')
def get_window_title():
	cmd = commands.getoutput("xprop -id $(xprop -root _NET_ACTIVE_WINDOW | cut -d ' ' -f 5)  WM_NAME")
	cmd = cmd.replace('WM_NAME(STRING) = ', '').replace('WM_NAME(COMPOUND_TEXT) = ', '').strip('"').replace(' • ', ' ')
	cmd = modified.sub(r'\1', cmd)
	
	return cmd

time = 0
last_window_class = get_window_class()
last_window_title = get_window_title()

print
while True:
	sleep(1);
	
	if(is_idle()): continue
	
	window_class = get_window_class()
	window_title = get_window_title()
	
	try:
		if window_class != last_window_class or window_title != last_window_title:
			if time > 4:
				print str(time).ljust(6), last_window_class.ljust(30), last_window_title
				
				c.execute('INSERT INTO timetracking (username, window_class, window_title, time) VALUES (%s, %s, %s, %s)', (USER, window_class, window_title, time))
				# print c._last_executed
				db.commit()
			
			time = 0
		
		time += 1
		
		last_window_class = window_class
		last_window_title = window_title
		
	except MySQLdb.OperationalError:
		db, c = db_connect()

print
print
