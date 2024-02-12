# Importing required modules
import sqlite3
from flask import Flask, jsonify, request
from flask_cors import CORS

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Allow requests from all origins

# Function to initialize the database
def initialize_database():
    connection = sqlite3.connect('ingredients.db')
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS purchased_ingredients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ingredient TEXT NOT NULL,
            quantity INTEGER NOT NULL DEFAULT 0
        )
    ''')
    connection.commit()
    connection.close()

# Initialize the database
initialize_database()

# Route for purchasing ingredients
@app.route('/purchase-ingredient', methods=['POST'])
def purchase_ingredient():
    try:
        data = request.json
        ingredient = data.get('ingredient')
        points = int(data.get('points', 0))  # Ensure points are converted to integers

        # Validate data
        if not ingredient:
            return jsonify({'error': 'Invalid ingredient'}), 400

        # Purchase the ingredient
        connection = sqlite3.connect('ingredients.db')
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM purchased_ingredients WHERE ingredient = ?', (ingredient,))
        existing_ingredient = cursor.fetchone()

        if existing_ingredient:
            # If the ingredient exists, update the quantity
            new_quantity = existing_ingredient[2] + 1
            cursor.execute('UPDATE purchased_ingredients SET quantity = ? WHERE ingredient = ?', (new_quantity, ingredient))
        else:
            # If the ingredient is new, insert it into the table
            cursor.execute('INSERT INTO purchased_ingredients (ingredient, quantity) VALUES (?, ?)', (ingredient, 1))

        connection.commit()
        connection.close()

        return jsonify({'message': f'You have purchased {ingredient} for {points} points.'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Route for retrieving purchased ingredients
@app.route('/purchased-ingredients', methods=['GET'])
def get_purchased_ingredients():
    try:
        connection = sqlite3.connect('ingredients.db')
        cursor = connection.cursor()
        cursor.execute('SELECT ingredient, quantity FROM purchased_ingredients')
        purchased_ingredients = cursor.fetchall()
        connection.close()
        ingredients_data = [{'ingredient': ingredient, 'quantity': quantity} for ingredient, quantity in purchased_ingredients]
        return jsonify(ingredients_data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True, port=8086)