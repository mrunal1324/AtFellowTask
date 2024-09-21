
# Personalized Travel Itinerary Generator

The **Personalized Travel Itinerary Generator** is a Flask-based web application designed to help users create personalized travel itineraries based on their preferences such as destination, budget, duration, and interests. The application integrates several advanced features like AI-powered itinerary optimization, expense tracking, group collaboration, reviews and ratings, and an AI chatbot assistant.

## Features

### 1\. **JWT Authentication**

*   Users are authenticated using JSON Web Tokens (JWT). A valid token is required for accessing most features.
*   Token expiration is set to 30 minutes.
*   Example endpoint: `/login` (POST)

### 2\. **AI-Powered Itinerary Optimization**

*   The itinerary is optimized based on user interests and best visiting times for attractions. K-means clustering is used to group nearby attractions for better planning.
*   The system generates a sequence of activities that are optimized based on travel time and visiting hours.
*   Example endpoint: `/itinerary` (POST)

### 3\. **Multi-language Support**

*   Automatic detection of the user's preferred language using the `langdetect` library.
*   Currently, the default language is English, but support for other languages can be added based on user requests.
*   Example: Detection occurs through `Accept-Language` headers.

### 4\. **Expense Tracking & Budget Analysis**

*   Users can track their travel expenses in different currencies. The app converts currencies to a base currency (USD) using the `forex-python` library.
*   Provides budget analysis to ensure that users stay within their defined budgets.
*   Example endpoint: `/track-expense` (POST)

### 5\. **Collaborative Itinerary Planning**

*   Users can invite collaborators to participate in planning the itinerary. Itineraries can be shared with others, making group travel planning easier.
*   Collaborators can view and edit shared itineraries.
*   Example endpoint: `/add-collaborator` (POST)

### 6\. **User Reviews and Ratings**

*   Users can submit reviews and ratings for activities included in their itineraries.
*   Other users can view these reviews and see the average rating for activities to help them make better decisions.
*   Example endpoints: `/submit-review` (POST), `/get-reviews` (GET)

### 7\. **Weather-Driven Dynamic Itineraries**

*   The app adjusts itineraries based on weather conditions in the destination using the OpenWeather API.
*   If bad weather is expected during a scheduled activity, the system suggests alternate plans.
*   Example endpoint: `/adjust-itinerary-for-weather` (POST)

### 8\. **AI Chatbot Travel Assistant**

*   Users can ask the AI-powered chatbot for travel suggestions, tips, or any other queries they might have about their trip.
*   The chatbot is powered by OpenAI's GPT model.
*   Example endpoint: `/chatbot` (POST)

### 9\. **Sustainable Travel Suggestions**

*   The system provides eco-friendly travel suggestions and calculates the carbon footprint of different transportation methods (car, plane, train, etc.).
*   Users are encouraged to choose sustainable options where possible.
*   Example endpoint: `/carbon-footprint` (POST)

### 10\. **Custom Day Plans and To-Do Lists**

*   Users can create personalized day plans for their trips, allowing them to schedule activities in advance.
*   These plans can be shared with collaborators or used as a personal reference during the trip.
*   Example endpoint: `/day-plan` (POST)

### 11\. **Real-time Flight and Hotel Deals**

*   Integration with external APIs like Skyscanner and Booking.com allows users to get the best deals on flights and accommodations.
*   Example endpoint: `/get-deals` (POST)

### 12\. **Offline Itinerary Mode**

*   Users can download their itineraries in offline mode for easy access when traveling without internet access.
*   Example endpoint: `/download-itinerary` (GET)

### 13\. **Personalized Notifications**

*   The app sends personalized notifications such as trip reminders, flight status updates, and weather alerts for the destination.
*   Example endpoint: `/get-notifications` (GET)

### 14\. **Advanced Filtering and Search**

*   Users can search for specific activities, events, or destinations with advanced filtering options like category, price range, and popularity.
*   Example endpoint: `/search-activities` (GET)

### 15\. **Weather-Driven Dynamic Itineraries**

*   The app modifies travel plans based on the weather forecast, adjusting outdoor activities if rain is expected.
*   Example endpoint: `/adjust-for-weather` (POST)

- - -

## Installation

### Prerequisites

*   Python 3.8+
*   Flask
*   SQLite3
*   OpenAI API Key
*   OpenWeather API Key
*   [forex\-python](https://forex-python.readthedocs.io/en/latest/)

### Steps to Run the Application

1.  **Clone the Repository**
    
    bash
    
    Copy code
    
    `git clone https://github.com/your-repo/personalized-travel-itinerary.git cd personalized-travel-itinerary`
    
2.  **Create a Virtual Environment**
    
    bash
    
    Copy code
    
    `` python3 -m venv venv source venv/bin/activate  # On Windows use `venv\Scripts\activate` ``
    
3.  **Install Dependencies**
    
    bash
    
    Copy code
    
    `pip install -r requirements.txt`
    
4.  **Set Up Environment Variables**
    
    *   Create a `.env` file and add the following keys:
        
        makefile
        
        Copy code
        
        `SECRET_KEY=your_flask_secret_key OPENAI_API_KEY=your_openai_api_key OPENWEATHER_API_KEY=your_openweather_api_key`
        
5.  **Initialize the Database**
    
    bash
    
    Copy code
    
    `flask shell from app import init_db init_db() exit()`
    
6.  **Run the Flask Application**
    
    bash
    
    Copy code
    
    `flask run`
    
7.  **Access the Application** Open your browser and go to: `http://127.0.0.1:5000/`
    

- - -

## Usage

1.  **User Login**
    
    *   First, log in using the `/login` endpoint to receive a JWT token.
    *   Example Request:
        
        bash
        
        Copy code
        
        `POST /login {   "username": "admin",   "password": "admin" }`
        
2.  **Create Itinerary**
    
    *   Use the `/itinerary` endpoint to create a personalized travel itinerary.
    *   Example Request:
        
        bash
        
        Copy code
        
        `POST /itinerary {   "user_id": "admin",   "destination": "Paris",   "duration": 5,   "budget": 1000,   "interests": "museums, parks" }`
        
3.  **Track Expenses**
    
    *   Use the `/track-expense` endpoint to track travel expenses.
    *   Example Request:
        
        bash
        
        Copy code
        
        `POST /track-expense {   "amount": 100,   "currency": "EUR" }`
        
4.  **Chatbot Assistant**
    
    *   Ask the AI Chatbot any travel-related question.
    *   Example Request:
        
        bash
        
        Copy code
        
        `POST /chatbot {   "query": "What are the best places to visit in Paris?" }`
        
5.  **Collaborate on Itineraries**
    
    *   Share itineraries and collaborate with other users by adding them as collaborators.
    *   Example Request:
        
        bash
        
        Copy code
        
        `POST /add-collaborator {   "itinerary_id": 1,   "collaborator_email": "user@example.com" }`
        

- - -

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request or open an issue for any suggestions or improvements.

- - -

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

- - -

