"""
methods for working with collection of vehicle data.
"""

import pandas as pd

from ..vehicleInformation import get_tram_number, st12Numbers, st13Numbers, st14Numbers, \
    st15Numbers
from .read import vehicledata_index_timestamp,vehicledata_index_vehicleid

def remove_duplicated_index(df: pd.DataFrame) -> pd.DataFrame:
    """removes entries with duplicated index

    Args:
        df: pandas dataframe

    Returns:
        dataframe where only fist occurrence of each index is kept
        """
    return df[~df.index.duplicated(keep='first')]


def trams_in_service(vehicledata_df: pd.DataFrame, columns:list|None=None, vehicles:list|None =None) -> pd.DataFrame:
    """ list the lines the trams are in service on, based on the presented vehicleData

    differet methond from busses_in_service because this also adds the prefix to the vehicle id

    Args:
        vehicledata_df: dataFrame as given by vehicleData_from_jsonFiles
        columns: columns to be included in return
        vehicles: the trams to be included in return

    Returns:
        DataFrame: DataFrame indexed by timestamps and columns are the give mulitindexed with trams
    """
    trams = vehicledata_df[vehicledata_df['category'] == 1]

    # remove duplicated index
    trams = remove_duplicated_index(trams)

    if columns is not None:
        trams = trams.reindex(columns=columns)
    else:
        columns = trams.columns
    # TODO: maybe geht hier auch schon die vehicles zu filtern?

    if trams.empty:
        raise ValueError('empty Dataframe, cannot pivot')

    trams_in_service_df = trams.reset_index().pivot(index=vehicledata_index_timestamp,
                                                    columns=vehicledata_index_vehicleid)
    trams_in_service_df.columns = trams_in_service_df.columns.map(lambda x: (x[0], get_tram_number(x[1])))

    if vehicles is not None:
        new_columns = pd.MultiIndex.from_product((columns,vehicles))
        trams_in_service_df = trams_in_service_df.reindex(columns=new_columns)
        # TODO: maybe geht das hier auch über nen drop columns?

    return  trams_in_service_df


def number_of_trams_in_service(trams_in_service_df: pd.DataFrame) -> pd.DataFrame:
    """
    counts the number of trams in each class, that are in servie for at each timestamp
    TODO: ahh grammar

    Args:
        trams_in_service_df: the service dataframe, formated like return of trams_in_service

    Returns: dataframe containing the counts per class at each timestamp

    """
    tram_class_number_tuples=[("ST12", st12Numbers), ("ST13", st13Numbers), ("ST14", st14Numbers), ("ST15", st15Numbers)]
    number_of_trams_in_service_series_list_by_class: list[pd.Series] = []
    visited_columns: list[str] = []

    for tram_class_tuple in tram_class_number_tuples:
        number_of_trams_of_class_series = (trams_in_service_df.reindex(columns=tram_class_tuple[1])
                                           .fillna(0).map(lambda x: x > 0).sum(axis=1)) # adds one for every tram in service
        number_of_trams_of_class_series.name = tram_class_tuple[0]
        number_of_trams_in_service_series_list_by_class.append(number_of_trams_of_class_series)

        visited_columns.extend(tram_class_tuple[1])

    other_trams = trams_in_service_df.columns.difference(visited_columns)
    number_of_other_trams_in_service = trams_in_service_df.reindex(columns=other_trams).fillna(0).map(lambda x: x > 0).sum(axis=1)
    number_of_other_trams_in_service.name="other"
    number_of_trams_in_service_series_list_by_class.append(number_of_other_trams_in_service)

    return pd.concat(number_of_trams_in_service_series_list_by_class,axis=1)


def buses_in_service(vehicledata_df: pd.DataFrame, columns:list|None=None, vehicles:list|None =None) -> pd.DataFrame:
    """ list the lines the buses are in service on, based on the presented vehicleData

    Args:
        vehicledata_df (DataFrame): dataFrame as given by vehicleData_from_jsonFiles
        columns: columns to be included in return
        vehicles: the buses to be included in return

    Returns:
        DataFrame: DataFrame indexed by timestamps that contains the line the selected buses are in service on
    """
    buses = vehicledata_df[vehicledata_df['category'] == 5]

    buses = remove_duplicated_index(buses)

    if columns is not None:
        buses = buses.reindex(columns=columns)
    else:
        columns = buses.columns
    # TODO: maybe geht hier auch schon die vehicles zu filtern?

    if buses.empty:
        raise ValueError('empty Dataframe, cannot pivot')
    buses_in_service_df = buses.reset_index().pivot(index=vehicledata_index_timestamp,
                                                    columns=vehicledata_index_vehicleid)
    buses_in_service_df.columns = buses_in_service_df.columns.map(lambda x: (x[0],str(x[1]))) # make sure that we index with stings

    if vehicles is not None:
        new_columns = pd.MultiIndex.from_product((columns,vehicles))
        buses_in_service_df = buses_in_service_df.reindex(columns=new_columns)
        # TODO: maybe geht das hier auch über nen drop columns?

    return  buses_in_service_df
