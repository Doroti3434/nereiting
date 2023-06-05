from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import os

# Инициализируем приложение
app = Flask(__name__)

# Конфигурируем базу данных
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///taxi.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Инициализируем базу данных
db = SQLAlchemy(app)

# Опишем модель данных
class TaxiOrder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    source = db.Column(db.String(100), nullable=False)
    destination = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"TaxiOrder(name='{self.name}', phone='{self.phone}', " + \
               f"source='{self.source}', destination='{self.destination}')"

# Опишем CRUD-операции
@app.route('/orders', methods=['POST'])
def create_order():
    data = request.get_json()
    new_order = TaxiOrder(name=data['name'],
                          phone=data['phone'],
                          source=data['source'],
                          destination=data['destination'])
    db.session.add(new_order)
    db.session.commit()
    return jsonify({'message': 'Order created successfully!'})

@app.route('/orders', methods=['GET'])
def read_orders():
    orders = TaxiOrder.query.all()
    result = []
    for order in orders:
        order_data = {'id': order.id,
                      'name': order.name,
                      'phone': order.phone,
                      'source': order.source,
                      'destination': order.destination}
        result.append(order_data)
    return jsonify(result)

@app.route('/orders/<int:id>', methods=['PUT'])
def update_order(id):
    order = TaxiOrder.query.get_or_404(id)
    data = request.get_json()
    order.name = data['name']
    order.phone = data['phone']
    order.source = data['source']
    order.destination = data['destination']
    db.session.commit()
    return jsonify({'message': 'Order updated successfully!'})

@app.route('/orders/<int:id>', methods=['DELETE'])
def delete_order(id):
    order = TaxiOrder.query.get_or_404(id)
    db.session.delete(order)
    db.session.commit()
    return jsonify({'message': 'Order deleted successfully!'})

# Запускаем приложение
if __name__ == '__main__':
    if not os.path.exists('taxi.db'):
        db.create_all()
    app.run(debug=True)