from flask import Flask, redirect, url_for, request, session, render_template, flash
from flask_restful import Resource, Api

from dao.db_connection import PostgreDb
from dao.db_model import *
from forms.forms import UserInputForm, SignUpForm
from helper_class import UserPrediction
#import plotly
#import plotly.graph_objs as go
#import json

app = Flask(__name__)
app.secret_key = 'development-key'
api = Api(app)
db = PostgreDb()

@app.route("/", methods = ['GET'])
def root():
    return render_template('index.html')
    
@app.route('/personal_prediction', methods=["GET", "POST"])
def userPrediction():
    form = UserInputForm()
    if form.validate_on_submit():
        to_predict_list = request.form.to_dict()
        loan_status_result = UserPrediction(to_predict_list).FittingData()
        if int(loan_status_result) == 1:
            loan_status_result = 'Yes'
            prediction = 'loan will be approved'
            flash(f'Your prediction: {prediction}', 'success')
        else:
            loan_status_result = 'No'
            prediction = 'loan will not be approved'
            flash(f'Your prediction: {prediction}', 'danger')
        customer = ormCustomer(gender=form.gender.data,
                               married=form.married.data,
                               dependents=form.dependents.data,
                               education=form.education.data,
                               self_employed=form.self_employed.data,
                               applicantincome=form.applicant_income.data,
                               coapplicantincome=form.coapplicant_income.data,
                               loanamount=form.loan_amount.data,
                               loan_amount_term=form.loan_amount_term.data,
                               credit_history=form.credit_history.data,
                               property_area=form.property_area.data,
                               loan_status=loan_status_result)
        db.sqlalchemy_session.add(customer)
        db.sqlalchemy_session.commit()
    return render_template('main_page.html', form=form)

@app.route('/customers', methods=['GET', 'POST'])
def customer_table():
    result = db.sqlalchemy_session.query(ormCustomer).all()
    return render_template('customers.html', customers=result)

if __name__ == "__main__":
        app.run(host='0.0.0.0', debug=True, threaded=True)