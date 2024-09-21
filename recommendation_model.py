import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

# Simulated data
places_data = pd.DataFrame([
    {'place': 'Eiffel Tower', 'culture': 5, 'adventure': 1, 'relaxation': 2, 'food': 1},
    {'place': 'Phi Phi Islands', 'culture': 1, 'adventure': 5, 'relaxation': 3, 'food': 2},
])

def recommend_places(user_preferences):
    user_pref_df = pd.DataFrame([user_preferences])
    similarities = cosine_similarity(user_pref_df, places_data.drop('place', axis=1))
    recommended_place_idx = similarities.argmax()
    return places_data.iloc[recommended_place_idx]['place']

# Example usage
user_preferences = {'culture': 5, 'adventure': 2, 'relaxation': 3, 'food': 1}
recommended_place = recommend_places(user_preferences)
print(f"Recommended place: {recommended_place}")
