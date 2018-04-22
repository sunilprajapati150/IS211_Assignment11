__author__ = 'sunilprajapati'

from flask import Flask, render_template, request, redirect
import pickle
import os.path
import time
import re
app = Flask(__name__)


pickle_path = "todolist.p"
have_pickle = os.path.isfile(pickle_path)

if(have_pickle is True):
	f = open(pickle_path)
	todolist = pickle.load(f)
	f.close()
else:
	todolist = []
	


@app.route('/')
def hello_world():

    return render_template('index.html',todolist = todolist)
	
@app.route('/submit', methods = ['POST'])
def submit():
	if not re.match(r"[^@]+@[^@]+\.[^@]+", request.form['email']):
		print "No email match"
		return redirect('/')
	elif request.form['priority'] not in ("High", "Med", "Low"):
		print "No priority match"
		return redirect('/')
	else:
		todolist.append((request.form['task'],request.form['email'],request.form['priority'],int(time.time())))
		return redirect('/')
	

@app.route('/clear')
def clear_list():
	todolist[:] = []
	return redirect('/')

@app.route('/save')
def save_list():	
	f = open('todolist.p', 'w')
	pickle.dump(todolist,f)
	f.close()
	return redirect('/')

@app.route('/delete')
def delete_item():
	delete_index = None
	delete_id = int(request.args.get('delete_id'))
	for i in enumerate(todolist):
		if(i[1][3] == delete_id):
			delete_index = i[0]
	print delete_index
	del todolist[delete_index]
	return redirect('/')
	

if __name__ == "__main__":
    app.run()
