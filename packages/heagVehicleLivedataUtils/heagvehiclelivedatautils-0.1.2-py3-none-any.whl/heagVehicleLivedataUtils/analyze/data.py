"""
provides the DataAnalysis class which provides tools for analyzing the vehicle data

TODO: write more
"""
import pandas as pd

from ..vehicleDataUtils.read import verify_vehicledata_format, vehicledata_from_dir
from ..vehicleDataUtils.process import trams_in_service, number_of_trams_in_service, buses_in_service

# TODO: vllt hier auch weitere optionen?

def _df_changes(df: pd.DataFrame)-> pd.DataFrame:
    """
    returns changes in entires of dataframe

    Args:
        df:

    Returns:
        dataframe of same shape as df, with values True if entries in columns changed. first row will always be True

    """
    return df.ne(df.shift())

def _extract_journeys_for_vehicle(in_service_df:pd.DataFrame, journey_indicators: pd.DataFrame, vehicleid)->pd.DataFrame:
    """
    extracts journeys of specified vehicle
    Args:
        in_service_df: in service dataframe containing information about the vehicle
        journey_indicators: assigns a journey to each row index appearing in in_servie_df. Needs to have a column for vehicleid.
        vehicleid: colum name for the vehicle we want to extract

    Returns:
        dataframe with journeys, with timestamp for begin and end, as well as line number and destination
    """
    time_line_direction_df = in_service_df[[('timestamp', ''), ('lineid',vehicleid), ('direction',vehicleid)]] # in_service_df has mulitinidex columns
    time_line_direction_df.columns = time_line_direction_df.columns.map(lambda x: x[0]) #  removes vehicleid from colum names

    vehicle_journey_indicators = journey_indicators[vehicleid] # we can only group with serial data
    vehicle_journey_indicators.name = 'journey' # we don't want the output index to be named vehicleid

    journeys = time_line_direction_df.groupby(vehicle_journey_indicators)

    return journeys.agg(
        start=pd.NamedAgg(column='timestamp', aggfunc='first'),
        end=pd.NamedAgg(column='timestamp', aggfunc='last'),
        lineid=pd.NamedAgg(column='lineid', aggfunc='first'),
        direction=pd.NamedAgg(column='direction', aggfunc='first')
    )

def _get_vehicle_journeys(in_service_df):
    """

    Args:
        in_service_df: dataaframe formated as returned by trams_in_service

    Returns:
        dataframe with journeys, with timestamp for begin and end, as well as line number and destination.
        index by vehicleid and journeynumber

    """

    # fill empty values, because otherwise NaN != NaN will result in many journeys
    in_service_df['lineid'] = in_service_df['lineid'].fillna(0).astype('int64')
    in_service_df['direction'] = in_service_df['direction'].fillna('')

    # timestamp as column, otherwise it will be lost when grouping
    time_line_destination_df = in_service_df.reset_index()[['timestamp', 'lineid', 'direction']]
    # also needs to happen now, so that the index remains consistent between dataframe and group_indicators

    changes = _df_changes(time_line_destination_df['lineid']) + _df_changes(time_line_destination_df['direction'])

    group_indicators = changes.cumsum() - 1  # first row always indicates a change

    vehicle_ids = time_line_destination_df['lineid'].columns # just grabbing it from here
    vehicle_journeys = [_extract_journeys_for_vehicle(time_line_destination_df, group_indicators, vehicle_id) for
                        vehicle_id in vehicle_ids]

    return pd.concat(vehicle_journeys, axis=0, keys=vehicle_ids)

class DataAnalysis:
    """
    Class to provide tools to analyze given vehicle data.

    TODO: add a bit of detail
    """

    def __init__(self,
                 /,
                 vehicledata: pd.DataFrame = None,
                 *,
                 vehicledata_path: str = None
                 ):
        """


        Args:
            vehicledata: dataframe containing vehicle data. if vehicledata_path or response_paths are specified, this will be disregarded

            vehicledata_path: path to directory where to look for vehicle data json files. if vehicledata is specified, this will be disregarded
        """

        self._vehicledata: pd.DataFrame

        if (vehicledata_path is not None) + (vehicledata is not None) > 1:
            # more than one data sources specified
            Warning("more than one data sources specified, only the fist one will be regarded")


        if vehicledata is not None:
            self.__set_vehicledata_dataframe(vehicledata)
        elif vehicledata_path is not None:
            self.__set_vehicledata_dataframe(vehicledata_from_dir(vehicledata_path))

    def __set_vehicledata_dataframe(self, vehicledata: pd.DataFrame):
        """
        provide vehicledata dataframe directly
        Args:
            vehicledata: dataframe to analyze
        """
        verify_vehicledata_format(vehicledata)

        self._vehicledata = vehicledata

    def get_vehicledata(self) -> pd.DataFrame:
        """

        Returns: the vehicledata dataframe

        """
        return self._vehicledata

    def get_trams_in_service(self, **kwargs) -> pd.DataFrame:
        """
        Args:
            same as process.trams_in_service

        Returns: the dataframe containing the service assignemt of the trams in this analysis

        """
        return trams_in_service(self._vehicledata, **kwargs)

    def get_number_of_trams_in_service(self, sample_time: str|None = None) -> pd.DataFrame:
        """
        Args:
            sample_time: sample size of the vehicledata

        Returns:
            dataframe with numbers of trams in service, index by timestamp.
        """
        number_in_service = number_of_trams_in_service(self.get_trams_in_service()['lineid'])
        if sample_time is not None:
            number_in_service = number_in_service.resample(sample_time).mean()
        return number_in_service

    def get_buses_in_service(self, **kwargs) -> pd.DataFrame:
        """
        Args:
            same as process.buses_in_service

        Returns: the dataframe containing the service assignemt of the buses in this analysis

        """

        return buses_in_service(self._vehicledata, **kwargs)

    def get_tram_journeys(self, vehicles:list|None =None) -> pd.DataFrame:
        """
        extracts journeys of tram vehicles from vehicle data
        Args:
            vehicles: the vehicles for which journeys should be extracted
        Returns:
            dataframe of journeys indexed by vehicleid and journey count
        """
        return _get_vehicle_journeys(self.get_trams_in_service(columns=['lineid', 'direction'], vehicles=vehicles))

    def get_bus_journeys(self, vehicles:list|None =None) -> pd.DataFrame:
        """
        extracts journeys of buses from vehicle data
        Args:
            vehicles: the vehicles for which journeys should be extracted
        Returns:
            dataframe of journeys indexed by vehicleid and journey count
        """
        return _get_vehicle_journeys(self.get_buses_in_service(columns=['lineid', 'direction'], vehicles=vehicles))