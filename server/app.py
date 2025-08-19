#!/usr/bin/env python3

from flask import Flask, request, make_response, jsonify
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

@app.route('/')
def home():
    return '<h1>Bakery GET-POST-PATCH-DELETE API</h1>'


# ---------------- GET ROUTES ---------------- #

@app.route('/bakeries')
def bakeries():
    bakeries = [bakery.to_dict() for bakery in db.session.query(Bakery).all()]
    return make_response(bakeries, 200)

@app.route('/bakeries/<int:id>')
def bakery_by_id(id):
    bakery = db.session.get(Bakery, id)
    if not bakery:
        return {"error": "Bakery not found"}, 404
    return make_response(bakery.to_dict(), 200)

@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    baked_goods_by_price = db.session.query(BakedGood).order_by(BakedGood.price.desc()).all()
    baked_goods_by_price_serialized = [bg.to_dict() for bg in baked_goods_by_price]
    return make_response(baked_goods_by_price_serialized, 200)

@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    most_expensive = db.session.query(BakedGood).order_by(BakedGood.price.desc()).first()
    if not most_expensive:
        return {"error": "No baked goods found"}, 404
    return make_response(most_expensive.to_dict(), 200)


# ---------------- POST ROUTE ---------------- #

@app.route('/baked_goods', methods=['POST'])
def create_baked_good():
    name = request.form.get("name")
    price = request.form.get("price")
    bakery_id = request.form.get("bakery_id")

    if not name or not price or not bakery_id:
        return {"error": "Missing required data"}, 400

    new_baked_good = BakedGood(
        name=name,
        price=float(price),
        bakery_id=int(bakery_id)
    )
    db.session.add(new_baked_good)
    db.session.commit()

    return make_response(new_baked_good.to_dict(), 201)


# ---------------- PATCH ROUTE ---------------- #

@app.route('/bakeries/<int:id>', methods=['PATCH'])
def update_bakery(id):
    bakery = db.session.get(Bakery, id)
    if not bakery:
        return {"error": "Bakery not found"}, 404

    name = request.form.get("name")
    if name:
        bakery.name = name

    db.session.commit()
    return make_response(bakery.to_dict(), 200)


# ---------------- DELETE ROUTE ---------------- #

@app.route('/baked_goods/<int:id>', methods=['DELETE'])
def delete_baked_good(id):
    baked_good = db.session.get(BakedGood, id)
    if not baked_good:
        return {"error": "Baked good not found"}, 404

    db.session.delete(baked_good)
    db.session.commit()

    return {"message": "Baked good successfully deleted"}, 200


if __name__ == '__main__':
    app.run(port=5555, debug=True)
