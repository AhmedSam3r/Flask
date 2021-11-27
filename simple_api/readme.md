*You must have python3 pre-installed<br>
*pip3 requirements.txt<br>
*connect Class User,Account to a postgress database<br>
for example if local database:

	create database for our api called banking
	app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://databaseUsername:databasePassword@portName:portNumber/databaseName'
	replace databaseUsername with your database username
	replace databasePassword with your database password
	replace portName with your database portName (eg.localhost)
	replace portNumber with your database portNumber(eg. 8080)
*after creating and connect our database<br>
*open simple_api directory in your python IDE<br>
*In terminal:
	>> python
	>> from app import db
	>> db.create_all()
now our database is connected and created with our User, Account classes
	>> user1 = User(email="blabla@gmail.com)
	>> user2 = User(email="blabla22@gmail.com)
	>> db.session.add(user1)
	>> db.session.add(user2)
	>>db.session.commit()
now user1 and user2 are add to our database
	>> account1 = Account(balance = 1000, currency = 'EGP', user_id_fk = user1.user_id)
	>> account2 = Account(balance = 2200, currency = 'EGP', user_id_fk = user2.user_id)
	>> db.session.add(user1)
	>> db.session.add(user2)
	>>db.session.commit()
now account1 and account2 are created and linked to their owners

******for balance api******
our json will be
for example
{
    "user_id" : "c5afe505-7584-4040-bb17-5eef24e3309c"
}
where key is "user_id" and value is uuid value from our database accompanied to user_id column values
it will return json object with all accounts and their balance
{
	(account_id as uuid : account_balance),
	so on ...
}

******for transfer api******
{
    "src_id" : account_id from Account class
    "dst_id" : account_id from Account class,
    "amount" : number,
    "currency": "EGP" or "USD"
}
I added basic authentication to add more security despite its vulnerability
username : ahmed 
password : ahmedahmed
