from flask import Flask, render_template, jsonify, request
import mysql.connector

app = Flask(__name__)

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="hostel_database"
    )

# Route to serve HTML page
@app.route('/')
def home():
    return render_template('addremoveView.html')

@app.route('/get_hostellers', methods=['GET'])
def get_hostellers():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM enrolled_hostellers")
    hostellers = cursor.fetchall()
    conn.close()
    return jsonify(hostellers)

@app.route('/add_hosteller', methods=['POST'])
def add_hosteller():
    data = request.get_json()
    conn = get_db_connection()
    cursor = conn.cursor()
    query = """
        INSERT INTO enrolled_hostellers (name, room_no, hostel_name, contact_no, email)
        VALUES (%s, %s, %s, %s, %s)
    """
    cursor.execute(query, (data['name'], data['room_no'], data['hostel_name'], data['contact_no'], data['email']))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Hosteller added successfully'}), 201

@app.route('/delete_hosteller/<int:id>', methods=['DELETE'])
def delete_hosteller(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM enrolled_hostellers WHERE hosteller_id = %s", (id,))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Hosteller deleted successfully'})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5002, debug=True)
