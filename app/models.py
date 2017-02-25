from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    categories = db.relationship('Category', backref='owner', lazy='dynamic')
    accounts = db.relationship('Account', backref='owner', lazy='dynamic')

    def __repr__(self):
        return '<User %r>' % (self.nickname)

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Integer, nullable=False)
    date=db.Column(db.DateTime, index=True, nullable=False)
    name=db.Column(db.String(32), index=True, nullable=False)
    detail=db.Column(db.String(120))
    transaction_type=db.Column(db.Enum('spending', 'income', 'transfer'), index=True, nullable=False)
    monthly_budget_id = db.Column(db.Integer, db.ForeignKey('monthly_budget.id'), index=True, nullable=False)
    accounts = db.relationship('Map_Transaction_Account',backref='transaction', lazy='dynamic')
    def __repr__(self):
        return '<Transaction %r>' % (self.name)


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), index=True, unique=True, nullable=False)
    detail = db.Column(db.String(120), nullable=True)
    monthly_budget = db.Column(db.Integer, nullable=False)
    category_type = db.Column(db.Enum('spending', 'saving'), index=True, nullable=False)
    is_active = db.Column(db.Boolean, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), index=True, nullable=False)
    budgets = db.relationship('Monthly_budget', backref='category', lazy='dynamic')

    def __repr__(self):
        return '<Category %r>' % (self.name)


class Monthly_budget(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    initial_amount = db.Column(db.Integer, nullable=False)
    spent_amount = db.Column(db.Integer, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), index=True, nullable=False)
    year = db.Column(db.Integer, index=True, nullable=False)
    month = db.Column(db.Enum('Janvier', 'Fevrier', 'Mars', 'Avril', 'Mai', 'Juin', 'Juillet', 'Aout', 'Septembre', 'Octobre', 'Novembre', 'Decembre'))
    transactions = db.relationship('Transaction', backref='on_budget', lazy='dynamic')

    def __repr__(self):
        return 'Monthly Budget {month} {year}'.format(month=month, year=year)


class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), index=True, unique=True, nullable=False)
    description = db.Column(db.String(120))
    balance = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), index=True, nullable=False)
    transactions = db.relationship('Map_Transaction_Account', backref='account_used', lazy='dynamic')

    def __repr__(self):
        return '<Account %r>' % (self.name)


class Map_Transaction_Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False, index=True)
    transaction_id = db.Column(db.Integer, db.ForeignKey('transaction.id'), nullable=False, index=True)
    direction = db.Column(db.Enum('TO','FROM'), nullable=False, index=True)
    __table_args__ = (db.UniqueConstraint('transaction_id', 'direction'),)
    def __repr__(self):
        return 'Transaction {transac} {tofrom} Account {account}'.format(transac=transaction, tofrom=direction, account=account)
