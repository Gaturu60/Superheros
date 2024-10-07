from flask import Flask, jsonify, request, abort
from models import db, Hero, Power, HeroPower
from config import Config
from sqlalchemy.exc import IntegrityError
import logging
from flask_marshmallow import Marshmallow

# Set up logging
logging.basicConfig(level=logging.ERROR)

# Initialize Flask
app = Flask(__name__) 
app.config.from_object(Config)

# Initialize SQLAlchemy
db.init_app(app)

# Initialize Marshmallow
ma = Marshmallow(app)

# Create all tables (inside app context)
with app.app_context():
    db.create_all()

# Error Handling
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Resource not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error", "message": str(error)}), 500

@app.errorhandler(Exception)
def handle_exception(e):
    logging.error(f"An error occurred: {str(e)}")
    return jsonify({"error": "An unexpected error occurred"}), 500

# Marshmallow Schemas
class PowerSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Power

class HeroPowerSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = HeroPower
    power = ma.Nested(PowerSchema)

class HeroSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Hero
    hero_powers = ma.Nested(HeroPowerSchema, many=True)

# Routes
@app.route('/heroes', methods=['GET'])
def get_heroes():
    heroes = Hero.query.all()
    return HeroSchema(many=True).jsonify(heroes)

@app.route('/heroes/<int:id>', methods=['GET'])
def get_hero(id):
    hero = Hero.query.get(id)
    if not hero:
        return jsonify({"error": "Hero not found"}), 404
    return HeroSchema().jsonify(hero)

@app.route('/powers', methods=['GET'])
def get_powers():
    powers = Power.query.all()
    return PowerSchema(many=True).jsonify(powers)

@app.route('/powers/<int:id>', methods=['GET'])
def get_power(id):
    power = Power.query.get(id)
    if not power:
        return jsonify({"error": "Power not found"}), 404
    return PowerSchema().jsonify(power)

@app.route('/powers/<int:id>', methods=['PATCH'])
def update_power(id):
    power = Power.query.get(id)
    if not power:
        return jsonify({"error": "Power not found"}), 404

    data = request.get_json()
    if 'description' not in data or len(data['description']) < 20:
        return jsonify({"errors": ["Validation errors: Description must be at least 20 characters long."]}), 400

    power.description = data['description']
    db.session.commit()
    return PowerSchema().jsonify(power)

@app.route('/hero_powers', methods=['POST'])
def create_hero_power():
    data = request.get_json()
    
    # Validate input data
    if 'strength' not in data or 'hero_id' not in data or 'power_id' not in data:
        return jsonify({"error": "Missing required fields"}), 400

    try:
        hero_power = HeroPower(strength=data['strength'], hero_id=data['hero_id'], power_id=data['power_id'])
        db.session.add(hero_power)
        db.session.commit()
        return HeroPowerSchema().jsonify(hero_power), 201
    except IntegrityError:
        db.session.rollback()  # Roll back the session if an error occurs
        return jsonify({"error": "HeroPower entry already exists"}), 409
    except Exception as e:
        return jsonify({"error": "Database error", "message": str(e)}), 500

# Run the application
if __name__ == '__main__':
    app.run(debug=True)
