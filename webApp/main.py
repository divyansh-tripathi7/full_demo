from distutils.log import debug
from fileinput import filename
from flask import *
app = Flask(__name__)

@app.route('/')
def main():
	return render_template("index.html")

@app.route('/success', methods = ['POST'])
def success():
	if request.method == 'POST':
		f = request.files['file']
		f.save(f.filename)
		return render_template("ack.html", name = f.filename)
	
# @app.route('/query', methods =  ['POST'])
# def query():
# 	if request.method == 'POST':
		

if __name__ == '__main__':
	app.run(debug=True)
