import React, { useState } from 'react';
import Map from './Map';  // Component for Google Maps
import axios from 'axios';

function App() {
  const [preferences, setPreferences] = useState({
    destination: '',
    budget: '',
    tripDuration: '',
    interests: []
  });

  const [itinerary, setItinerary] = useState(null);

  const handleChange = (e) => {
    setPreferences({ ...preferences, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post('http://localhost:5000/generate-itinerary', preferences);
      setItinerary(response.data);
    } catch (error) {
      console.error("Error generating itinerary:", error);
    }
  };

  return (
    <div>
      <h1>Personalized Travel Itinerary Generator</h1>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          name="destination"
          placeholder="Destination"
          onChange={handleChange}
          required
        />
        <input
          type="number"
          name="budget"
          placeholder="Budget"
          onChange={handleChange}
          required
        />
        <input
          type="number"
          name="tripDuration"
          placeholder="Trip Duration (days)"
          onChange={handleChange}
          required
        />
        <select name="interests" onChange={handleChange} multiple>
          <option value="culture">Culture</option>
          <option value="adventure">Adventure</option>
          <option value="relaxation">Relaxation</option>
          <option value="food">Food</option>
        </select>
        <button type="submit">Generate Itinerary</button>
      </form>

      {itinerary && (
        <div>
          <h2>Your Itinerary for {preferences.destination}</h2>
          <p>Budget: {preferences.budget}</p>
          <p>Duration: {preferences.tripDuration} days</p>
          <h3>Places of Interest</h3>
          <Map places={itinerary.places} />
        </div>
      )}
    </div>
  );
}

export default App;
