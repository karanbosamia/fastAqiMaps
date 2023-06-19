import models
import requests
import json
from fastapi import FastAPI, Depends, HTTPException
from database import SessionLocal, engine
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder


models.Base.metadata.create_all(bind=engine)

def get_db():
    """
    The get_db function is a helper function that is used to create a database session.
    It will be called when the application needs to access the database, and it will return
    a database session that can be used to query for objects or collections of objects.
    
    :return: A database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI()

@app.get("/")
def read_root():
    """
    The read_root function returns a dictionary with the key &quot;Hello&quot; and value &quot;World&quot;.
    
    
    :return: A dictionary with a single key-value pair
    """
    return {"Hello": "World"}

@app.get("/get/data/{city}/{token}")
async def get_city_aqi(city: str, db:Session=Depends(get_db), token: str):
    """
    The get_city_aqi function takes in a city name and returns the air quality index for that city.
        The function uses the waqi API to get this information.
    
    
    :param city: str: Pass the city name to the function
    :param db:Session: Get the database session from the dependency injection
    :return: A dictionary with the following keys:
    """
    url = f"https://api.waqi.info/feed/{city}?token={token}"
    payload = json.dumps({})
    headers = {
      'Content-Type': 'application/json'
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    
    resp = json.loads(response.text)
    latitude, longitude = None, None
    if resp:
        
        latitude, longitude = resp.get('data', {}).get('city').get('geo')

        aqi_data = models.AirQualityData(
            aqi=resp.get('data', {}).get('aqi', ''),
            latitude=latitude,
            longitude=longitude,
            location_name=resp.get('data', {}).get('city', {}).get('name', '')
        )

        db.add(aqi_data)
        db.commit()
        # db.refresh(aqi_data)
    if latitude and longitude:
        all_aqis = db.query(models.AirQualityData).filter(
            models.AirQualityData.latitude == latitude, models.AirQualityData.longitude == longitude
        )

    return resp



