"""
This module contains constants regarding operations 

TODO: das ordentlich beschreiben, ie. hier sind vorallem betreibsnummber der Fahrzeuge und ne colormap für die liniennummern ihre farbe zuordent
"""

from matplotlib.colors import ListedColormap


def tram_class_prefix(vehicle_id: int) -> str:
    """ gives the class prefix for the vehicle number of the given tram

    Args:
        vehicle_id: the (TODO: vehicleID) of a tram without the class prefix

    Returns:
        string: the class prefix of that tram

    """

    # sort of divide & conquer to avoid elif chains
    if vehicle_id >= 75:
        if vehicle_id <= 92:
            return '07'
        elif vehicle_id <= 125:
            return '22'
        else:
            return ''  # not in range of current numbers
    else:
        if vehicle_id >= 55:
            return '98'
        elif vehicle_id <= 25:
            # modern hight floor tram
            if vehicle_id >= 15:
                return '91'
            elif vehicle_id >= 9:
                return '82'
            else:
                return '76'
        else:
            return ''  # trailers are not shown as vehicles, others have no prefix


def get_tram_number(vehicle_id: int) -> str:
    """ gives the full id number of the tram vehicle

    Args:
        vehicle_id: the vehicle Id number of the tram whose full id number is to be returned.

    Returns:
        str: the full id number of the tram vehicle
    """
    return tram_class_prefix(vehicle_id) + str(vehicle_id)


# the vehicle numbers of the differnet classes of trams
st12Numbers: list[str] = [f'91{i:0>2}' for i in range(15, 25)]
st13Numbers: list[str] = [f'98{i:0>2}' for i in range(55, 75)]
st14Numbers: list[str] = [f'07{i:0>2}' for i in range(75, 93)]
st15Numbers: list[str] = [f'221{i:0>2}' for i in range(1, 26)]
tinaNumbers: list[str] = st15Numbers
st7Numbers: list[str] = ['31']

modern_tram_numbers: list[str] = st12Numbers + st13Numbers + st14Numbers + tinaNumbers
usual_tram_numbers: list[str] = st7Numbers + modern_tram_numbers

# Betriebsnummern of the busses in operation
setra_s531_dt_numbers = ['291','292','298','299'] # double decker (2019-2021)

citaro_c2_o530_le_numbers = [f'31{i:0>1}' for i in range(7,10)] # standard diesel (2017)

lions_city_18C_numbers = [f'4{i:0>2}' for i in range(7,15)] # articulated diesel (2020)
lions_city_g_ng_323_A23_numbers = ([f'26{i:0>1}' for i in range(1,6)] # articulated diesel (2010-2018)
                                   + [f'40{i:0>1}' for i in range(1,6)]
                                   + [f'3{i:0>2}' for i in range(51,65)]
                                   + [f'3{i:0>2}' for i in range(72,84)])
citaro_c2_o530_G_numbers = [f'3{i:0>2}' for i in range(65,72)] # articulated diesel (2017)

eCitaro_numbers = [f'3{i:0>2}' for i in range(27,44)] # standard battery (2020-2021)
eCitaro_G_numbers = [f'4{i:0>2}' for i in range(15,28)] + [f'4{i:0>2}' for i in range(37,47)]  # articulated battery (2021-2024)
lions_city_18E_numbers = [f'4{i:0>2}' for i in range(28,37)] # articulated battery (2024)

electric_bus_numbers = eCitaro_numbers + eCitaro_G_numbers + lions_city_18E_numbers
articlated_bus_numbers = (citaro_c2_o530_G_numbers
                          + lions_city_g_ng_323_A23_numbers
                          + lions_city_18C_numbers
                          + eCitaro_G_numbers
                          + lions_city_18E_numbers)

# colormap to assign (tram)line numbers their official color (as given on the Lininenetzplan) 
# when applied to values ranging from [0,10], where 0 indicates no line at all
heagLineColormap: ListedColormap = ListedColormap(
    ['#ffffff', '#eb6d8c', '#00a650', '#f2bc17', '#3871c1', '#50ade5', '#ec6d1f', '#ec008c', '#e02828', '#74c933',
     '#8d198f'])

# offset to separate numerical line identifiers from utf-8 encodings of other line identifiers
lineId_offset: int = 10000 #TODO: maybe 10^4 better suited?


def encode_line_name(line_name: str) -> int:
    """ encodes the string representation of the line identifier into a unique int

    Args: lineName: the line identifier as a string

    Returns:
        int: the encoded line identifier
    """
    if line_name.isnumeric():
        return int(line_name)

    return int.from_bytes(line_name.encode(), 'big') + lineId_offset


def decode_line_id(line_id: int) -> str:
    """ decodes the sting representation of the line identifier encoded in the lineId

    Args:
        line_id: the encoded line identifier, as given by mapLineName

    Returns:
        str: sting representation of the line name
    """
    if line_id < lineId_offset:
        return str(line_id)

    # line name is encoded
    name_representation = line_id - lineId_offset
    byte_representation = name_representation.to_bytes((name_representation.bit_length() + 7) // 8, 'big')
    return byte_representation.decode('utf-8')
