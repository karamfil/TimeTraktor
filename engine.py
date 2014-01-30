import MySQLdb, MySQLdb.cursors
from datetime import date, datetime, timedelta

class Engine:
	db	= None
	cur	= None
	
	def __init__(self):
		self.connect()
	
	def connect(self):
		self.db = MySQLdb.connect(host = 'nakor',  user = 'sites', passwd = 'M0reFun', db = 'test', charset = 'utf8', cursorclass = MySQLdb.cursors.DictCursor)
		self.cur = self.db.cursor()
		return self.db, self.cur
	
	def select(self, query, *args):
		self.cur.execute(query, args)
		print self.cur._last_executed
		
		return self.cur.fetchall()
	
	def time_add(self, USER, window_class, window_title, time):
		self.cur.execute('INSERT INTO timetracking (username, window_class, window_title, time) VALUES (%s, %s, %s, %s)', (USER, window_class, window_title, time))
		# print self.cur._last_executed
		self.db.commit()
	
	
	
	def get_top_all_time(self, username):
		return self.select('''SELECT window_class, ROUND(SUM(time)/60, 2) AS time, COUNT(id) AS switches
			FROM timetracking
			WHERE username = username
			GROUP BY username, window_class
			ORDER BY time DESC
			LIMIT 10''')
	
	def get_top_week(self, username):
		t = date.today()
		w = t.isoweekday()
		
		start = (datetime(t.year, t.month, t.day) - timedelta(days = w)).strftime('%F %T')
		end = (datetime(t.year, t.month, t.day, 23, 59, 59) + timedelta(days = 7-w)).strftime('%F %T')
		
		return self.select('''SELECT window_class, ROUND(SUM(time)/60, 2) AS time, COUNT(id) AS switches
			FROM timetracking
			WHERE username = username AND `date` BETWEEN %s AND %s
			GROUP BY username, window_class
			ORDER BY time DESC
			LIMIT 10''', start, end)
	
	def get_top_today(self, username):
		t = date.today()
		
		start = datetime(t.year, t.month, t.day).strftime('%F %T')
		end = datetime(t.year, t.month, t.day, 23, 59, 59).strftime('%F %T')
		
		return self.select('''SELECT window_class, ROUND(SUM(time)/60, 2) AS time, COUNT(id) AS switches
			FROM timetracking
			WHERE username = username AND `date` BETWEEN %s AND %s
			GROUP BY username, window_class
			ORDER BY time DESC
			LIMIT 10''', start, end)
	
	def get_top_name_all_time(self, username):
		return self.select('''SELECT window_class, window_title, ROUND(SUM(time)/60, 2) AS time, COUNT(id) AS switches
			FROM timetracking
			WHERE username = username
			GROUP BY username, window_class, window_title
			ORDER BY time DESC
			LIMIT 10''')
	
	def get_top_name_week(self, username):
		t = date.today()
		w = t.isoweekday()
		
		start = (datetime(t.year, t.month, t.day) - timedelta(days = w)).strftime('%F %T')
		end = (datetime(t.year, t.month, t.day, 23, 59, 59) + timedelta(days = 7-w)).strftime('%F %T')
		
		return self.select('''SELECT window_class, window_title, ROUND(SUM(time)/60, 2) AS time, COUNT(id) AS switches
			FROM timetracking
			WHERE username = username AND `date` BETWEEN %s AND %s
			GROUP BY username, window_class, window_title
			ORDER BY time DESC
			LIMIT 10''', start, end)
	
	def get_top_name_today(self, username):
		t = date.today()
		
		start = datetime(t.year, t.month, t.day).strftime('%F %T')
		end = datetime(t.year, t.month, t.day, 23, 59, 59).strftime('%F %T')
		
		return self.select('''SELECT window_class, window_title, ROUND(SUM(time)/60, 2) AS time, COUNT(id) AS switches
			FROM timetracking
			WHERE username = username AND `date` BETWEEN %s AND %s
			GROUP BY username, window_class, window_title
			ORDER BY time DESC
			LIMIT 10''', start, end)
	
