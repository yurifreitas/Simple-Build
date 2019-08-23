from app import db


class Pacote(db.Model):
    __tablename__ = 'pacote'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(77))
    height = db.Column(db.String(77))
    length = db.Column(db.String(77))
    width = db.Column(db.String(77))
    weight = db.Column(db.String(77))
    price = db.Column(db.String(77))

    def __init__(self, name, height, length, width, weight, price):
        self.name = name
        self.height = height
        self.length = length
        self.width = width
        self.weight = weight
        self.price = price

    def __repr__(self):
        return "<pacotes(%s, %s, %s)>" % (
            self.id, self.price, self.name)

    class Meta:
        database = db

db.session.execute('CREATE TABLE IF NOT EXISTS pacote ( name TEXT, height TEXT, length TEXT, width TEXT, weight TEXT, price TEXT)')