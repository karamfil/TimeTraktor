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
		# print self.cur._last_executed
		
		return self.cur.fetchall()
	
	def time_add(self, USER, window_class, window_title, time):
		self.cur.execute('INSERT INTO timetracking (username, window_class, window_title, time) VALUES (%s, %s, %s, %s)', (USER, window_class, window_title, time))
		# print self.cur._last_executed
		self.db.commit()
	
	def _filter_today(self):
		t		= date.today()
		start	= datetime(t.year, t.month, t.day)
		end		= datetime(t.year, t.month, t.day, 23, 59, 59)
		
		return start.strftime('%F %T'), end.strftime('%F %T')
	
	def _filter_week(self):
		t, w	= date.today(), t.isoweekday()
		start	= (datetime(t.year, t.month, t.day) - timedelta(days = w))
		end		= (datetime(t.year, t.month, t.day, 23, 59, 59) + timedelta(days = 7-w))
		
		return start.strftime('%F %T'), end.strftime('%F %T')
	
	def query_top(self, *params):
		where = 'AND `date` BETWEEN %s AND %s' if params else ''
		
		return self.select('''SELECT window_class, ROUND(SUM(time)/60, 2) AS time, COUNT(id) AS switches
			FROM timetracking
			WHERE username = username {0}
			GROUP BY username, window_class
			ORDER BY time DESC
			LIMIT 10'''.format(where), *params)
	
	def get_top_all_time(self, username):	return self.query_top()
	def get_top_week(self, username):		return self.query_top(*self._filter_week())
	def get_top_today(self, username):		return self.query_top(*self._filter_today())
	
	
	def query_top_title(self, *params):
		where = 'AND `date` BETWEEN %s AND %s' if params else ''
		
		return self.select('''SELECT window_class, window_title, ROUND(SUM(time)/60, 2) AS time, COUNT(id) AS switches
			FROM timetracking
			WHERE username = username {0}
			GROUP BY username, window_class, window_title
			ORDER BY time DESC
			LIMIT 10'''.format(where), *params)
	
	def get_top_title_all_time(self, username):	return self.query_top_title()
	def get_top_title_week(self, username):		return self.query_top_title(*self._filter_week())
	def get_top_title_today(self, username):	return self.query_top_title(*self._filter_today())
	
	# def get_stats_
	
	# def get_stats_today(self):
	# 	self.select('''SELECT window_class, window_title, ROUND(SUM(time)/60, 2) AS time, COUNT(id) AS switches
	# 		FROM timetracking
	# 		WHERE username = username AND `date` BETWEEN %s AND %s
	# 		GROUP BY username, window_class, window_title
	# 		ORDER BY time DESC
	# 		LIMIT 10''', start, end)
		
	# 	return {
	# 		'time'		: ,
	# 		'switches'	: ,
	# 	}
