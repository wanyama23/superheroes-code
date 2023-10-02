from flask import Flask, make_response, jsonify, request
from flask_migrate import Migrate

from models import db, Hero, Power, hero_powers

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def home():
    return make_response(jsonify({"msg": "Welcome to Hero/Power api"}), 200)

#Get heroes
@app.route("/heroes")
def heroes():
    heroes = [hero.to_dict() for hero in Hero.query.all()]
    return make_response(jsonify({"heroes": heroes}), 200)

# Get heroes by id
@app.route("/heroes/<int:id>")
def heroes_by_id(id):
    hero = Hero.query.filter_by(id=id).first()
    if not hero:
        return make_response(jsonify({"error": "Hero not found"}), 404)
    else:
        return make_response(jsonify(hero.to_dict()), 200)

# get powers
@app.route("/powers")
def powers():
    powers = [power.to_dict() for power in Power.query.all()]
    return make_response(jsonify({"powers": powers}), 200)   

# get powers by id
@app.route("/powers/<int:id>", methods=["GET", "PATCH"])
def powers_by_id(id):
    power = Power.query.filter_by(id=id).first()
    if not power:
        return make_response(jsonify({"error": "Power not found"}), 404)
    else:
        if request.method == "GET":
            return make_response(jsonify(power.to_dict()), 200)
        
        # update description
        elif request.method == "PATCH":
            description = request.form.get("description")
            if description and len(description) < 20:
                return make_response(jsonify({"error":"[validation errors]"}), 400)
            
            setattr(power, "description", description)
            db.session.add(power)
            db.session.commit()
            return make_response(jsonify(power.to_dict()), 200)

# post hero_powers
@app.route("/hero_powers", methods=["POST"])
def create_hero_power():
        
        if request.method == "POST":
            # validate if strength is in the given strengths
            if request.form.get("strength") not in ["Strong", "Weak", "Average"]:
                return make_response(jsonify({"errors": ["validation errors"]}),400)
            
            # if it is, post the strength
            strength = request.form.get("strength")
            power_id = request.form.get("power_id")
            hero_id =  request.form.get("hero_id")

            new_hp = hero_powers.insert().values(
                strength = strength ,
                power_id= power_id,
                hero_id = hero_id,
            )
            db.session.execute(new_hp)
            db.session.commit()
            

            updated_hero = Hero.query.filter_by(id=hero_id).first()
            response_data = {
                "id": updated_hero.id,
                "name": updated_hero.name,
                "super_name": updated_hero.super_name,
                "powers": [power.to_dict() for power in updated_hero.powers]
            }

            return make_response(jsonify(response_data), 201)

if __name__ == '__main__':
    app.run(port=5555)