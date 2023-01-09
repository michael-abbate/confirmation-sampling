# confirmation-sampling
Web app to perform confirmation sampling for audit procedures.



# How to run on Windows
## First time running the app
1. Open CMD
1. Install virtualenv if you haven't already: `py -m pip3 install --user virtualenv`
1. Change directory to confirmation-sampling folder `cd folder1\folder2\...\confirmation-sampling`
1. Change directory into the \app folder
1. Create virtualenv (venv) within the **\app** folder: `py -m venv venv`
1. Activate the virtualenv: `.\venv\Scripts\activate`. You should now see (venv) on the left side of your CMD.
1. Install all packages required using requirements.txt `pip3 install -r ..\requirements.txt`
1. Back out off the app/ directory into the confirmation-sampling directory: `cd ..`

## After installing necessary packages...
1. Make sure your virtualenv is active (step 6 in First time running the app)
1. Run the following command: FLASK_APP="app/main.py" flask run
1. Input General Ledger Extract
1. Input valid output path *ex. /Users/my_user/Desktop/conf_sampling_output*
1. Click submit. If success you will receive a green flash message confirming files are in the output folder!


# Need help installing venv or running python on your local?
https://medium.com/datacat/a-simple-guide-to-creating-a-virtual-environment-in-python-for-windows-and-mac-1079f40be518