from flask import Flask, render_template, request, redirect, url_for, jsonify,session
from twilio.rest import Client
import psycopg2
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__, static_url_path='/static')

# Database connection configuration
conn = psycopg2.connect(
    host="localhost",
    port=5432,
    database="postgres",
    user="",
    password=""
)
cursor = conn.cursor()

TWILIO_ACCOUNT_SID = "sid"
TWILIO_AUTH_TOKEN = "token"
TWILIO_PHONE_NUMBER = 'tnum'


client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/book', methods=['POST'])
def book():
    # Placeholder logic for handling the booking form submission
    passenger_name = request.form.get('passenger_name')
    pickup_location = request.form.get('pickup_location')
    destination = request.form.get('destination')
    travel_date = request.form.get('travel_date')

    # Placeholder logic to send an SMS notification to the driver
    send_booking_notification(passenger_name, pickup_location, destination, travel_date)

    # Pass a message to the confirmation template
    confirmation_message = "Thank you for booking! Your driver will be notified shortly."
    return render_template('confirmation.html', message=confirmation_message)

def send_booking_notification(passenger_name, pickup_location, destination, travel_date):
    driver_phone_number = "+91"  # Replace with the actual driver's phone number

    message_body = f"New booking details:\nPassenger: {passenger_name}\nPickup: {pickup_location}\nDestination: {destination}\nTravel Date: {travel_date}"

    message = client.messages.create(
        body=message_body,
        from_=TWILIO_PHONE_NUMBER,
        to=driver_phone_number
    )

    print(f"SMS Notification Sent to {driver_phone_number}. SID: {message.sid}")

    return jsonify({"message_sid": message.sid})

@app.route('/track')
def track():
    # Display tracking page
    return render_template('track.html')

@app.route('/login')
def login():
    # Display tracking page
    return render_template('login.html')


@app.route('/register')
def Register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password == confirm_password:
            hashed_password = generate_password_hash(password, method='sha256')

            cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hashed_password))
            conn.commit()

            return redirect(url_for('login'))

    return render_template('register.html')

if __name__ == '__main__':
    app.run(debug=True)
