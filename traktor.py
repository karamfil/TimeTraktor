# -*- coding: utf-8 -*-

import subprocess, re, MySQLdb
from time import sleep
from engine import Engine

USER = 'karamfil'

def is_idle():
	cmd = None
	
	try:
		cmd = subprocess.check_output(['gnome-screensaver-command', '-q']).strip().split('\n')[0].split(' ')[-1]
	except subprocess.CalledProcessError, e:
		print e
	
	return cmd == 'active'

def get_window_id():
	wid = None
	
	try:
		xprop = subprocess.check_output(['xprop', '-root', '_NET_ACTIVE_WINDOW'])
		wid = xprop.strip().split()[-1]
		
		if wid == '0x0':
			# check why this is 0x0
			print xprop
		
	except subprocess.CalledProcessError, e:
		print e
	
	return wid

def get_window_class():
	wclass = None
	
	try:
		wclass = subprocess.check_output(['xprop', '-id', get_window_id(), 'WM_CLASS']).strip()
		
		try:
			wclass = wclass[20:].split('", "')[1].strip('"')
		except:
			print wclass
	except subprocess.CalledProcessError, e:
		print e
	
	return wclass

db = Engine()

modified = re.compile(r'\*(\])$')
def get_window_title():
	wtitle = None
	
	try:
		wtitle = subprocess.check_output(['xprop', '-id', get_window_id(), 'WM_NAME']).strip()
		wtitle = wtitle.replace('WM_NAME(STRING) = ', '').replace('WM_NAME(COMPOUND_TEXT) = ', '').strip('"').replace(' • ', ' ')
		wtitle = modified.sub(r'\1', wtitle)
	except subprocess.CalledProcessError, e:
		print e
	
	return wtitle

time = 0
last_window_class = get_window_class()
last_window_title = get_window_title()

if __name__ == '__main__':
	print
	while True:
		sleep(1);
		
		if(is_idle()): continue
		
		try:
			window_class = get_window_class()
			window_title = get_window_title()
			
			if window_class != last_window_class or window_title != last_window_title:
				if time > 1:
					print str(time).ljust(6), last_window_class.ljust(30), last_window_title
					
					db.time_add(USER, last_window_class, last_window_title, time)
				
				time = 0
			
			time += 1
			
			last_window_class = window_class
			last_window_title = window_title
		except MySQLdb.OperationalError, e:
			print e
			db.connect()
		except Exception, e:
			print e

print
print
