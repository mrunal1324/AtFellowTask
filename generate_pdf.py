from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def generate_itinerary_pdf(itinerary, file_name):
    c = canvas.Canvas(file_name, pagesize=letter)
    c.drawString(100, 750, f"Travel Itinerary for {itinerary['destination']}")
    
    c.drawString(100, 700, "Places of Interest:")
    for idx, place in enumerate(itinerary['places']):
        c.drawString(100, 680 - idx * 20, f"{place['name']} ({place['type']})")

    c.save()

# Example usage
itinerary = {
    'destination': 'Paris',
    'places': [{'name': 'Eiffel Tower', 'type': 'culture'}]
}
generate_itinerary_pdf(itinerary, 'itinerary.pdf')
