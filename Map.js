import React, { useEffect, useRef } from 'react';

function Map({ places }) {
  const googleMapRef = useRef(null);

  useEffect(() => {
    const script = document.createElement('script');
    script.src = `https://maps.googleapis.com/maps/api/js?key=YOUR_GOOGLE_MAPS_API_KEY&libraries=places`;
    script.async = true;
    window.document.body.appendChild(script);
    script.addEventListener('load', () => {
      const googleMap = new window.google.maps.Map(googleMapRef.current, {
        zoom: 10,
        center: { lat: places[0].lat, lng: places[0].lng },
      });

      places.forEach(place => {
        new window.google.maps.Marker({
          position: { lat: place.lat, lng: place.lng },
          map: googleMap,
          title: place.name
        });
      });
    });
  }, [places]);

  return <div ref={googleMapRef} style={{ width: '100%', height: '500px' }} />;
}

export default Map;
