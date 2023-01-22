import json
import os
from datetime import datetime, timedelta
import pandas as pd

from flask import (Flask, abort, flash, jsonify, make_response, redirect, render_template, request, session, url_for)
from werkzeug.utils import secure_filename

# from flask_login import (LoginManager, current_user, login_required, login_user, logout_user)

from app import app
# from forms import LoginForm
# from models import Auth, User

from confirmationsampling import determineCutoffThreshold
from scopingreconciliation import scopingRec


UPLOAD_FOLDER = os.path.join('app','uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

__version__ = '0.0.1'
__basedir__ = os.path.abspath(os.path.dirname(__file__))
__rootdir__ = os.path.abspath(os.getcwd())

# login_manager = LoginManager()
# login_manager.init_app(app)
# login_manager.login_view = '.login'
# login_manager.session_protection = 'strong'

# timeout = timedelta(minutes=60)
# app.permanent_session_lifetime = timeout

def removeLocalFile(filepath):
    if os.path.exists(filepath):
        os.remove(filepath)
    else:
        print("The file does not exist")

# Home route
@app.route('/', methods = ['GET', 'POST'])
# @login_required
def home():
    return render_template('index.html', message= "")

@app.route('/test', methods = ['GET', 'POST'])
def test():
    if request.method=="POST":
        try:
            file = request.files["file"]
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            df=pd.read_csv(file_path)
            removeLocalFile(file_path)
            return render_template("test.html", df=df.to_html())
        except Exception as e:
            flash(f"Error, {e}", 'error')
    return render_template('test.html', df= None)

@app.route('/sampling', methods = ['GET', 'POST'])
def sampling():
    if request.method=="POST":
        try:
            file = request.files["file"]
            outputpath = request.form["outputpath"]
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            df=pd.read_csv(file_path)
            removeLocalFile(file_path)
            data_to_save=determineCutoffThreshold(df)
            for data in data_to_save:
                # Update outputs folder to be an option for user
                filename=os.path.join(outputpath,data["data_type"]+"_"+str(data["results"]["Criteria"][0]))                
                df_output=pd.DataFrame(data['results'])
                df_output.to_csv(filename+'.csv', index=False)
                # file.save(os.path.join("outputs",filename))
            flash(f'Success! Files uploaded to {outputpath} folder', 'success')
            return render_template("sampling.html", message="Success!")
        except Exception as e:
            flash(f"Error, {e}", 'error')
    return render_template('sampling.html', message= "")

@app.route('/scoping', methods = ['GET', 'POST'])
# @login_required
def scoping():
    if request.method=="POST":
        try:
            file_1 = request.files['file_1']
            filename_1 = secure_filename(file_1.filename)
            file_path_1 = os.path.join(app.config['UPLOAD_FOLDER'], filename_1)
            file_1.save(file_path_1)

            file_2 = request.files["file_2"]
            filename_2 = secure_filename(file_2.filename)
            file_path_2 = os.path.join(app.config['UPLOAD_FOLDER'], filename_2)
            file_2.save(file_path_2)
            # print('HERE:',file_1)
            outputpath = request.form["outputpath"]
            # df1=pd.read_csv(file_path_1)
            # df2=pd.read_csv(file_path_2)
            data_to_save = scopingRec(file_path_1, file_path_2)
            removeLocalFile(file_path_1)
            removeLocalFile(file_path_2)


            output_file_name = data_to_save['Level 4 -Description'].unique()[0]
            output_filepath=os.path.join(outputpath,output_file_name)                
            data_to_save.to_csv(output_filepath+'.csv', index=False)

            # file.save(os.path.join("outputs",filename))
            flash(f'Success! Files uploaded to {outputpath} folder', 'success')
            return render_template("scoping.html", message="Success!")
        except Exception as e:
            flash(f"Error, {e}", 'error')
    return render_template('scoping.html', message= "")

# @app.context_processor
# def utility_processor():
#     def getEnv(key):
#         return app.config[key]
#     return dict(env=getEnv)


# @login_manager.user_loader
# def load_user(user):
#     user = User(user)
#     if user:
#         return user
#     return None


# @app.route('/login', methods = ['GET', 'POST'])
# def login():
#     if current_user.is_authenticated:
#         return redirect(url_for('home'))

#     auth = Auth()
#     form = LoginForm()

#     if form.validate_on_submit():
#         data = { 'email': form.email.data, 'password': form.password.data }
#         userObj = auth.auth_api_call(data, '/login')
        
#         if 'id' in userObj:
#             session['user'] = userObj
#             session.permanent = False
#             login_user(User(userObj), duration=timeout)
#             return redirect(url_for('home'))
#         else:
#             flash(userObj['message'], userObj['status'])
#             return redirect(url_for('login'))

#     return render_template('login.html', form=form)


# @app.route('/logout')
# @login_required
# def logout():
#     if 'user' in session:
#         session.pop('user', None)
#     logout_user()
#     flash('You were successfully logged out.', 'success')
#     return redirect(url_for('login'))




@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
