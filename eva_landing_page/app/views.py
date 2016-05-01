from app import app
from flask import render_template, request,  session, url_for
import os
from werkzeug import secure_filename
import subprocess

ALLOWED_EXTENSIONS = set(['txt', 'csv'])

app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024 * 1024
app.config["UPLOAD_FOLDER"] = os.path.realpath('.') + '/analysis/'
#app.config["UPLOAD_FOLDER"] = 'web-app/analysis/'

"""
    return render_template("dashboard.html", main_ranking="static/fairml_plots/OpenOrd_With_Gephi_Modularity_good.png",\
     iofp = "static/fairml_plots/graph-5.png", lasso="static/fairml_plots/graph-6.png",\
     mrmr="static/fairml_plots/graph-3.png", rf = "static/fairml_plots/graph-4.png")
"""

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/')
@app.route('/index')
def index():
	return render_template("index.html")


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    """Upload a new file."""
    if request.method == 'POST':
    	file = request.files['file']
    	filename = secure_filename(file.filename)
    	if file and allowed_file(file.filename):
    		file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    		#now run the file
    		print "stating "
    		path_to_fairml = app.config["UPLOAD_FOLDER"] + "fairml.py"
    		path_to_input_file = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    		python_command = "python {} --file={} --target=target".format(path_to_fairml, path_to_input_file)
    		subprocess.call(python_command, shell=True)
    		print "finishing "

    		return render_template("dashboard.html", main_ranking="static/img/combined.png",\
    			iofp = "static/img/iofp.png", lasso="static/img/lasso.png",\
    			mrmr="static/img/mrmr.png", rf = "static/img/rf.png")
    	#if the user just clicks the upload file and no file has been selected, then just return to index
    	else:
    		return render_template("index.html")
