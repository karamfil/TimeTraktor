from flask import Flask, render_template
from engine import Engine

app	= Flask(__name__)
db	= Engine()

USER = 'karamfil'


@app.route('/')
def index():
	return render_template('index.html', **{
		'name'			: USER,
		'top'			: db.get_top_all_time(USER),
		'top_week'		: db.get_top_week(USER),
		'top_today'		: db.get_top_today(USER),
		'top_name'		: db.get_top_name_all_time(USER),
		'top_name_week'	: db.get_top_name_week(USER),
		'top_name_today': db.get_top_name_today(USER),
	})


if __name__ == '__main__':
	app.debug = True
	app.run()