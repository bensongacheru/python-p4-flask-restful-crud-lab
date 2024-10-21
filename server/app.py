from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Plant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    image = db.Column(db.String(200), nullable=False)
    price = db.Column(db.Float, nullable=False)
    is_in_stock = db.Column(db.Boolean, default=True)

@app.route('/plants/<int:id>', methods=['GET'])
def get_plant(id):
    plant = db.session.get(Plant, id)  # Use db.session.get()
    if not plant:
        return jsonify({"error": "Plant not found"}), 404
    return jsonify({
        'id': plant.id,
        'name': plant.name,
        'image': plant.image,
        'price': plant.price,
        'is_in_stock': plant.is_in_stock
    })

@app.route('/plants/<int:id>', methods=['PATCH'])
def update_plant(id):
    plant = db.session.get(Plant, id)
    if not plant:
        return jsonify({"error": "Plant not found"}), 404
    
    data = request.get_json()
    if 'is_in_stock' in data:
        plant.is_in_stock = data['is_in_stock']
    db.session.commit()
    
    return jsonify({
        'id': plant.id,
        'name': plant.name,
        'image': plant.image,
        'price': plant.price,
        'is_in_stock': plant.is_in_stock
    })

@app.route('/plants/<int:id>', methods=['DELETE'])
def delete_plant(id):
    plant = db.session.get(Plant, id)
    if not plant:
        return jsonify({"error": "Plant not found"}), 404

    db.session.delete(plant)
    db.session.commit()
    return jsonify({}), 204

def create_tables():
    with app.app_context():
        db.create_all()

if __name__ == '__main__':
    create_tables()  # Create tables before running the app
    app.run(debug=True)
