"""
provides utilities to work with the apis relvant for vehicledata
"""
import pandas as pd
import requests as rq
from .vehicleDataUtils.read import vehicledata_from_dict

vehiclesApi_url = f"https://service.ivanto.de/srs/api/v1/vehiclelivedata?tenant=heag"
stationsApi_url = f"https://service.ivanto.de/srs/api/v1/stations?bundleIdentifier=de.ivanto.heagmobilo&tenant=heag&onlyStations=true&latitude=49.872021&longitude=8.658934&distance=50000"

def get_current_vehicle_data():
    """ request vehicleLiveData form api
    """
    response = rq.get(vehiclesApi_url)

    if response.status_code != rq.codes.ok:
        RuntimeError('Api response status code not ok!')
    
    return response.json()

def get_station_data():
    """ request stationData form api
    """
    response = rq.get(stationsApi_url)

    if response.status_code != rq.codes.ok:
        RuntimeError('Api response status code not ok!')
    
    return response.json()


def get_current_vehicle_data_as_dataframe() -> pd.DataFrame:
    """
    gets current vehiclelivedata from api and  returns it as a dataframe

    Returns: vehicleLiveData form api as pandas dataframe

    """
    return vehicledata_from_dict(get_current_vehicle_data())