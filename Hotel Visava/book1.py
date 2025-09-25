from flask import Flask, request, redirect
import sqlite3

app = Flask(__name__)

# Initialize the database with an additional 'date' field
def init_db():
    conn = sqlite3.connect('bookings.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            contact TEXT NOT NULL,
            email TEXT NOT NULL,
            address TEXT,
            rooms INTEGER NOT NULL,
            date TEXT NOT NULL  -- New 'date' column
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/', methods=['GET'])
def booking_form():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Hotel Visava Booking</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background: linear-gradient(to bottom, #00ffcc 20%, #003300 100%);
                margin: 0;
                padding: 0;
            }
            .container {
                max-width: 500px;
                margin: 4rem auto;
                background: white;
                padding: 2rem;
                border-radius: 10px;
                box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
            }
            h1 {
                text-align: center;
                color: #333;
            }
            form {
                display: flex;
                flex-direction: column;
            }
            label {
                margin-top: 1rem;
                font-weight: bold;
            }
            input, textarea {
                padding: 0.7rem;
                border: 1px solid #ccc;
                border-radius: 5px;
            }
            textarea {
                resize: vertical;
                min-height: 80px;
            }
            .btn {
                margin-top: 1.5rem;
                padding: 0.8rem;
                background-color: #c59d5f;
                color: white;
                border: none;
                border-radius: 5px;
                cursor: pointer;
                font-weight: bold;
            }
            .btn:hover {
                background-color: #b48b4e;
            }
            .success {
                text-align: center;
                color: green;
                font-weight: bold;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Hotel Visava Booking</h1>
            <form action="/submit" method="post">
                <label for="name">Full Name:</label>
                <input type="text" id="name" name="name" required>

                <label for="contact">Contact Number:</label>
                <input type="text" id="contact" name="contact" required>

                <label for="email">Email Address:</label>
                <input type="email" id="email" name="email" required>

                <label for="address">Address:</label>
                <textarea id="address" name="address"></textarea>

                <label for="rooms">Number of Rooms:</label>
                <input type="number" id="rooms" name="rooms" min="1" required>

                <label for="date">Booking Date:</label>
                <input type="date" id="date" name="date" required>

                <button type="submit" class="btn">Book Now</button>
            </form>
        </div>
    </body>
    </html>
    '''

@app.route('/submit', methods=['POST'])
def submit_form():
    name = request.form['name']
    contact = request.form['contact']
    email = request.form['email']
    address = request.form['address']
    rooms = request.form['rooms']
    date = request.form['date']  # Capture the date field from the form

    # Insert booking data into the database
    conn = sqlite3.connect('bookings.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO bookings (name, contact, email, address, rooms, date)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (name, contact, email, address, rooms, date))  # Insert the date into the DB
    conn.commit()
    conn.close()

    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Booking Confirmed</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #f4f4f4;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
            }
            .message {
                background: white;
                padding: 2rem;
                border-radius: 10px;
                box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
                text-align: center;
            }
            .message h2 {
                color: green;
            }
            a {
                display: inline-block;
                margin-top: 1rem;
                text-decoration: none;
                color: #c59d5f;
                font-weight: bold;
            }
        </style>
    </head>
    <body>
        <div class="message">
            <h2>Booking Successful!</h2>
            <p>Thank you for booking with Hotel Visava.</p>
            <a href="/">Back to Booking Page</a>
        </div>
    </body>
    </html>
    '''

if __name__ == '__main__':
    init_db()  # Initialize the database when the app starts
    app.run(debug=True)
