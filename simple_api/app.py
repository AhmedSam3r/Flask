from flask import Flask, json, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import UUID
import uuid
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://databaseUsername:databasePassword@portName:portNumber/databaseName'
db = SQLAlchemy(app)
auth = HTTPBasicAuth()


class User(db.Model):
    user_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = db.Column(db.String(120), unique=True, nullable=False)
    accounts = db.relationship('Account', backref = 'user', lazy= True)
        
    def __repr__(self):
        return f'Id = {self.user_id}, username= {self.username}'


class Account(db.Model):
    account_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    balance = db.Column(db.Float, nullable=False)
    currency = db.Column(db.String(3), nullable=False, default='EGP')
    user_id_fk = db.Column(UUID(as_uuid=True),db.ForeignKey('user.user_id'), nullable=False)
    
    def __repr__(self):
        return f'currency = {self.currency}'




@app.route("/home", methods=['GET','POST'])
def testing_uuid():
    return uuid.uuid4().hex

@app.route('/user/balance', methods=['POST'])
def userBalance():
    if request.method == 'POST':
        user_uuid = request.get_json()
        accounts = Account.query.filter_by(user_id_fk = user_uuid['user_id'])
        tuple_of_account = list()
        for account in accounts:
            tuple_of_account.append((account.account_id, account.balance))
        return jsonify(tuple_of_account)

'''we should here consider all possible scenarios
function needs refactoring to consider future scenarios like multiple currencies rather than egp and usd
command design pattern could work'''
def calculateAmountScenarios(amount, currency, source, destination):
    src_amount = amount
    dst_amount = amount
    if currency == 'USD':
        if source.currency == 'EGP':
            src_amount *=  15.75 
        if destination.currency == 'EGP':
            dst_amount *= 15.75 
    
    elif currency == 'EGP':
        if source.currency == 'USD':
            src_amount /=  15.75 
        if destination.currency == 'USD':
            dst_amount /= 15.75 
        
    return src_amount, dst_amount

user_data = {
    "ahmed":generate_password_hash("ahmedahmed")
}


@auth.verify_password
def verify_password(username, password):
    if username in user_data and \
            check_password_hash(user_data.get(username), password):
        return username




@app.route('/user/transfer', methods = ['POST'])
@auth.login_required
def userTransfer():
        if request.method == 'POST':
            transfer_request = request.get_json()
            source_account= Account.query.filter_by(user_id_fk = transfer_request['src_id']).first()
            destination_account = Account.query.filter_by(user_id_fk = transfer_request['dst_id']).first()
            #calculate the actual amount to be transferred
            actual_amount_src, actual_amount_dst = calculateAmountScenarios(transfer_request['amount'], transfer_request['currency'], source_account, destination_account)
            
            if source_account.balance >= actual_amount_src :
                source_account.balance = source_account.balance - actual_amount_src
                destination_account.balance = destination_account.balance + actual_amount_dst
                db.session.commit()
                return jsonify("The process has succeeded"), 200
        
            return jsonify("The process has failed, Balance isn't enough to complete this transaction"), 405

            



if __name__ == '__main__':
    app.run()
