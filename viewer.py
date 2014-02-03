from flask import Flask, render_template

from engine import Engine

from datetime import datetime, timedelta

USER = 'karamfil'

app	= Flask(__name__)

def hours(value, format='%H:%M / %d-%m-%Y'):
	d = datetime(1,1,1) + timedelta(seconds = int(value))
	r = '%02d:%02d' % (d.minute, d.second)
	
	if d.hour > 0:
		r = '%02d:%s' % (d.hour, r)
	
	if d.day > 1:
		r = '%d %s' % (d.day-1, r)
	
	return r

app.jinja_env.filters['hours'] = hours



@app.route('/')
def index():
	db	= Engine()
	
	return render_template('index.html', **{
		'name'				: USER,
		'top'				: db.get_top_all_time(USER),
		'top_week'			: db.get_top_week(USER),
		'top_today'			: db.get_top_today(USER),
		'top_title'			: db.get_top_title_all_time(USER),
		'top_title_week'	: db.get_top_title_week(USER),
		'top_title_today'	: db.get_top_title_today(USER),
		'stats'				: db.get_stats_all_time(USER),
		'stats_week'		: db.get_stats_week(USER),
		'stats_today'		: db.get_stats_today(USER),
	})


if __name__ == '__main__':
	app.debug = True
	app.run()