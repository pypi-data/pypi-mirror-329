"""
Methods for reading vehiclelivedata from json
"""
from os import walk
from os.path import join

from pathlib import Path

import pandas as pd
import json

from ..vehicleInformation import encode_line_name

vehicledata_columns = ["lineid", "category", "direction", "status", "latitude", "longitude", "bearing", "type"]
vehicledata_index_timestamp = 'timestamp'
vehicledata_index_vehicleid = 'vehicleid'
vehicledata_index_names = [vehicledata_index_timestamp, vehicledata_index_vehicleid]

def verify_vehicledata_format(dataframe: pd.DataFrame) -> bool:
    """
    checks if dataframe contains a valid vehicle data format
    Args:
        dataframe: dataframe to check

    Throws: Value error if dataframe is not formatted correctly

    """

    expected_columns = set(vehicledata_columns) # is set so that order does not matter -> TODO: is that necessary?
    if not expected_columns <= set(dataframe.columns):
        raise ValueError("dataframe columns do not contain expected columns")

    expected_index_names = set(vehicledata_index_names)
    if not expected_index_names == set(dataframe.index.names):
        raise ValueError("dataframe index names do not match expected names")

    return True

## data reading
def vehicledata_from_dict(vehicledata_dict: dict, *, file_path: str = None)-> pd.DataFrame:
    """ extracts service information of public transport vehicles into a Dataframe

    Args:
        vehicledata_dict (JSON dict): data structured like vehicleData from HEAG vehicleLivedata api
        file_path: used in error messages. If vehicledata_dict is taken from a json file, use its path, otherwise leave empty

    Returns:
        DataFrame: contains the information from the vehicleData, indexed with timestamp and vehicleId
    """
    if not {'timestamp', 'vehicles'} <= vehicledata_dict.keys():
        raise ValueError(
            f"json file {file_path} is not formatted correctly. Missing keys 'timestamp' and/or 'vehicles' ")

    vehicledata_df = pd.DataFrame.from_dict(vehicledata_dict['vehicles'])

    # lowercase colums work better with database
    vehicledata_df.columns = vehicledata_df.columns.str.lower()

    expected_entries_names = set(vehicledata_columns + [vehicledata_index_vehicleid])
    if not expected_entries_names <= set(vehicledata_df.columns):
        if file_path is None:
            message_begin = "vehicledata_dict"
        else:
            message_begin = f"json file {file_path}"

        missing_entries = expected_entries_names - set(vehicledata_df.columns)
        raise ValueError(message_begin + f"was not formatted correctly. Missing entries {missing_entries} in vehicles")

    # use timestamp vehicleId multiindex -> TODO: überlege ob das sinvoll ist (bei db sollte alles in colums stehen, sonnst ist vllt anders praktisch), ist jetzt aba alles darauf ausgelegt
    vehicledata_df.index = pd.MultiIndex.from_product(
                                            [[pd.Timestamp(vehicledata_dict['timestamp'])],
                                                    vehicledata_df[vehicledata_index_vehicleid]],
                                                    names= vehicledata_index_names )

    vehicledata_df['lineid'] = vehicledata_df['lineid'].map(encode_line_name)

    # make sure columns are the expected ones
    vehicledata_df = vehicledata_df.reindex(columns = vehicledata_columns)

    return vehicledata_df

# TODO: | PathLike[str] as well??
def vehicledata_from_dir(path_to_dir: str|Path, max_recursion_depht: int =0, follow_links:bool = False) -> pd.DataFrame:
    """
    returns the vehicledata found in dir
    Args:
        path_to_dir: where to search for vehicledata
        max_recursion_depht: deprecated

    Returns:
        vehicledata found in dir, returned as dataframe
    """

    vehicledata_df_list = []
    for dirpath, dirname, filenames in walk(path_to_dir,follow_links):
        for filename in filenames:
            with open(join(dirpath, filename)) as json_file:
                vehicledata_df_list.append(vehicledata_from_dict(json.load(json_file)))

    if len(vehicledata_df_list) == 0:
        raise ValueError("No vehicledata found in directory")

    return pd.concat(vehicledata_df_list)

