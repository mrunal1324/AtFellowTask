from flask import Flask, request, jsonify, send_from_directory, session
import sqlite3
import jwt
import datetime
import random
import numpy as np
import requests
import openai
from flask_babelex import Babel
from langdetect import detect
from sklearn.cluster import KMeans
from forex_python.converter import CurrencyRates
from forex_python.converter import RatesNotAvailableError
from dotenv import load_dotenv
import os
from functools import wraps

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your_secret_key')
app.config['BABEL_DEFAULT_LOCALE'] = 'en'
babel = Babel(app)
openai.api_key = os.getenv('OPENAI_API_KEY')

# JWT Authentication Wrapper
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('x-access-token')
        if not token:
            return jsonify({'message': 'Token is missing!'}), 403
        try:
            jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired!'}), 403
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Token is invalid!'}), 403
        return f(*args, **kwargs)
    return decorated

@babel.localeselector
def get_locale():
    """Detect the language from the user's request."""
    return detect(request.headers.get('Accept-Language')) or 'en'

# Serve index.html at the root URL
@app.route('/')
def index():
    return send_from_directory('', 'index.html')

# Serve static files like CSS and JS
@app.route('/<path:path>')
def serve_static_files(path):
    return send_from_directory('', path)

# Database connection
def get_db_connection():
    conn = sqlite3.connect('itineraries.db')
    conn.row_factory = sqlite3.Row
    return conn

# Generate a token (JWT Authentication)
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if data['username'] == 'admin' and data['password'] == 'admin':
        token = jwt.encode({
            'user': data['username'],
            'exp': datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=30)
        }, app.config['SECRET_KEY'])
        return jsonify({'token': token})
    return jsonify({'message': 'Invalid Credentials!'}), 403

# AI-Powered Itinerary Optimization
def optimize_itinerary(itinerary, attractions_data, travel_time_matrix):
    best_times = np.array([attractions_data[attraction]['best_visit_time'] for attraction in itinerary])
    num_clusters = min(len(itinerary), 3)  # For simplicity, group into 3 clusters
    kmeans = KMeans(n_clusters=num_clusters)
    clusters = kmeans.fit_predict(travel_time_matrix)
    
    cluster_itineraries = []
    for cluster in range(num_clusters):
        cluster_attractions = [itinerary[i] for i in range(len(itinerary)) if clusters[i] == cluster]
        sorted_attractions = sorted(cluster_attractions, key=lambda x: attractions_data[x]['best_visit_time'])
        cluster_itineraries.extend(sorted_attractions)
    
    return cluster_itineraries

# Expense Tracking & Budget Analysis
def track_expenses(data, base_currency='USD'):
    c = CurrencyRates()
    total_expense = 0

    for item in data:
        try:
            amount = item['amount']
            currency = item['currency']
            total_expense += c.convert(currency, base_currency, amount)
        except RatesNotAvailableError:
            return "Currency rates are not available at this time."
        except Exception as e:
            return f"An error occurred: {str(e)}"
    return total_expense

def budget_analysis(total_expense, budget):
    if total_expense > budget:
        return f"Over budget by {total_expense - budget} {budget.currency}"
    return f"Within budget with {budget - total_expense} {budget.currency} remaining"

# Collaborative Itinerary Planning
def add_collaborator(itinerary_id, collaborator_email):
    user_id = session.get('user_id')
    if user_id is None:
        return jsonify({'message': 'User not logged in!'}), 403
    conn = get_db_connection()
    conn.execute('INSERT INTO collaborators (itinerary_id, user_id) VALUES (?, ?)', (itinerary_id, user_id))
    conn.commit()

def get_shared_itineraries(user_id):
    conn = get_db_connection()
    itineraries = conn.execute('SELECT * FROM itineraries WHERE user_id=? OR id IN (SELECT itinerary_id FROM collaborators WHERE user_id=?)', 
                               (user_id, user_id)).fetchall()
    return itineraries

# User Reviews and Ratings
def submit_review(user_id, activity_id, rating, review_text):
    conn = get_db_connection()
    conn.execute('INSERT INTO reviews (user_id, activity_id, rating, review) VALUES (?, ?, ?, ?)', 
                 (user_id, activity_id, rating, review_text))
    conn.commit()

def get_reviews(activity_id):
    conn = get_db_connection()
    reviews = conn.execute('SELECT * FROM reviews WHERE activity_id=?', (activity_id,)).fetchall()
    avg_rating = conn.execute('SELECT AVG(rating) FROM reviews WHERE activity_id=?', (activity_id,)).fetchone()
    return reviews, avg_rating

# Weather-Driven Dynamic Itineraries
def adjust_for_weather(itinerary, destination, travel_dates):
    api_key = os.getenv('OPENWEATHER_API_KEY')
    api_url = f"http://api.openweathermap.org/data/2.5/forecast?q={destination}&appid={api_key}"

    response = requests.get(api_url).json()
    weather_data = response.get('list', [])

    adjusted_itinerary = []
    for activity in itinerary:
        for forecast in weather_data:
            if activity['time'] == forecast['dt_txt']:
                if forecast['weather'][0]['main'] != 'Rain':
                    adjusted_itinerary.append(activity)
    return adjusted_itinerary

# AI Chatbot Travel Assistant
def chatbot_assistant(prompt, model="gpt-3.5-turbo", temperature=0.7, max_tokens=150):
    """
    Function to interact with OpenAI's GPT-based chatbot.

    Parameters:
    - prompt (str): The input message to send to the chatbot.
    - model (str): The model to use (default: "gpt-4").
    - temperature (float): Sampling temperature, controls creativity of responses (0.7 default).
    - max_tokens (int): Maximum number of tokens to generate (default: 150).

    Returns:
    - response (str): The chatbot's response to the input prompt.
    """
    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt},
            ],
            temperature=temperature,
            max_tokens=max_tokens,
        )
        # Extracting and returning the chatbot's reply
        return response['choices'][0]['message']['content']
    
    except Exception as e:
        return f"Error: {str(e)}"

# Sustainable Travel Suggestions
def calculate_carbon_footprint(distance, mode_of_transport):
    emission_factors = {
        'car': 0.12,    # kg CO2 per km
        'plane': 0.15,
        'train': 0.05,
        'bus': 0.03
    }
    return distance * emission_factors.get(mode_of_transport, 0.12)

def suggest_sustainable_options(transport_modes):
    sustainable_modes = [mode for mode in transport_modes if mode in ['train', 'bus']]
    return sustainable_modes if sustainable_modes else 'No eco-friendly options available'

# Custom Day Plans and To-Do Lists
def create_day_plan(user_id, date, activities):
    conn = get_db_connection()
    conn.execute('INSERT INTO day_plans (user_id, date, activities) VALUES (?, ?, ?)', 
                 (user_id, date, ','.join(activities)))
    conn.commit()

def get_day_plan(user_id, date):
    conn = get_db_connection()
    day_plan = conn.execute('SELECT activities FROM day_plans WHERE user_id=? AND date=?', (user_id, date)).fetchone()
    return day_plan['activities'].split(',') if day_plan else []

# Create a new itinerary
@app.route('/itinerary', methods=['POST'])
@token_required
def create_itinerary():
    data = request.get_json()
    user_id = data.get('user_id')
    destination = data.get('destination')
    duration = data.get('duration')
    budget = data.get('budget')
    interests = data.get('interests')

    if not all([user_id, destination, duration, budget, interests]):
        return jsonify({'message': 'All fields are required!'}), 400

    places = ['Museum', 'Park', 'Monument', 'Shopping Center']
    itinerary = [random.choice(places) for _ in range(int(duration))]

    # Sample attraction data
    attractions_data = {
        'Museum': {'best_visit_time': 2},
        'Park': {'best_visit_time': 1},
        'Monument': {'best_visit_time': 1},
        'Shopping Center': {'best_visit_time': 3}
    }

    # Sample travel time matrix
    travel_time_matrix = np.random.rand(len(itinerary), len(itinerary))

    optimized_itinerary = optimize_itinerary(itinerary, attractions_data, travel_time_matrix)

    try:
        conn = get_db_connection()
        conn.execute('INSERT INTO itineraries (user_id, destination, duration, budget, interests, itinerary) VALUES (?, ?, ?, ?, ?, ?)', 
                     (user_id, destination, duration, budget, interests, ', '.join(optimized_itinerary)))
        conn.commit()
    except sqlite3.OperationalError as e:
        return jsonify({'message': 'Database error: ' + str(e)}), 500
    finally:
        conn.close()

    return jsonify({'itinerary': optimized_itinerary})

# Track expenses
@app.route('/track-expense', methods=['POST'])
def track_expense():
    data = request.get_json()
    amount = data.get('amount')
    currency = data.get('currency')
    total_expense = track_expenses([data], base_currency='USD')
    return jsonify({'total_expense': total_expense})

# Submit a review
@app.route('/submit-review', methods=['POST'])
@token_required
def submit_review_route():
    data = request.get_json()
    user_id = data.get('user_id')
    activity_id = data.get('activity_id')
    rating = data.get('rating')
    review_text = data.get('review_text')

    if not all([user_id, activity_id, rating, review_text]):
        return jsonify({'message': 'All fields are required!'}), 400

    submit_review(user_id, activity_id, rating, review_text)
    return jsonify({'message': 'Review submitted successfully!'})

# AI Chatbot Interaction
@app.route('/chatbot', methods=['POST'])
def chatbot():
    data = request.get_json()
    query = data.get('query')
    response = chatbot_assistant(query)
    return jsonify({'response': response})

# Initialize the database
def init_db():
    conn = get_db_connection()
    conn.execute('''CREATE TABLE IF NOT EXISTS itineraries (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT NOT NULL,
                    destination TEXT NOT NULL,
                    duration INTEGER NOT NULL,
                    budget INTEGER NOT NULL,
                    interests TEXT NOT NULL,
                    itinerary TEXT NOT NULL)''')
    conn.execute('''CREATE TABLE IF NOT EXISTS reviews (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT NOT NULL,
                    activity_id TEXT NOT NULL,
                    rating INTEGER NOT NULL,
                    review TEXT)''')
    conn.execute('''CREATE TABLE IF NOT EXISTS day_plans (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT NOT NULL,
                    date TEXT NOT NULL,
                    activities TEXT NOT NULL)''')
    conn.execute('''CREATE TABLE IF NOT EXISTS collaborators (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    itinerary_id INTEGER NOT NULL,
                    user_id TEXT NOT NULL)''')
    conn.close()

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
