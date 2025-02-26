import unittest

import pandas as pd
from heagVehicleLivedataUtils.analyze.plot import VehicleDataPlotter
from heagVehicleLivedataUtils.analyze.data import DataAnalysis
from heagVehicleLivedataUtils.vehicleInformation import encode_line_name
from heagVehicleLivedataUtils.vehicleDataUtils.read import verify_vehicledata_format

class TestRead(unittest.TestCase):
    def test_regular_read_and_plot(self):
        da = VehicleDataPlotter(vehicledata_path="../test/vehicleInfo_test/")

        # test if working with data does not throw errors
        da.plot_number_of_trams_in_service(sample_time="15Min",show_plot=False)
        da.plot_all_trams_in_service(sample_time="15Min",show_plot=False)
        da.plot_electric_buses_in_service(sample_time="15Min",show_plot=False)

        da.get_tram_journeys()
        da.get_tram_journeys()

        # check if dataframe is formated to expected spec
        self.assertTrue(verify_vehicledata_format(da.get_vehicledata()))


    # TODO: what about ill formed data?/ -> error handling
    def test_special_read(self):
        da = VehicleDataPlotter(vehicledata_path="../test/vehicleInfo_test_special_cases/") # TODO seems to have problems with "6E" and such lines
        vehicle_data = da.get_vehicledata()

        timestamp = pd.Timestamp("2024-11-09T09:29:49+0100")

        # bus line as category 1(tram)
        self.assertEqual(vehicle_data.loc[(timestamp, 444),'category'],1)

        # added offset to vehicleid
        self.assertEqual(vehicle_data.loc[(timestamp, 4284), 'lineid'], encode_line_name("L"))

        # line name that can be read as float
        self.assertEqual(vehicle_data.loc[(timestamp, 430), 'lineid'], encode_line_name("4E"))

        # tram vehicleid on bus line
        self.assertEqual(vehicle_data.loc[(timestamp, 112), 'lineid'], encode_line_name("WE2"))


        timestamp = pd.Timestamp("2024-11-09T23:04:49+0100")

        # line name that can be read as float
        self.assertEqual(vehicle_data.loc[(timestamp, 69), 'lineid'], encode_line_name("8E"))

        # switched category
        self.assertEqual(vehicle_data.loc[(timestamp, 114), 'category'], 5)


        timestamp = pd.Timestamp("2024-11-09T23:39:49+0100")

        self.assertEqual(vehicle_data.loc[(timestamp, 405), 'lineid'], encode_line_name("8"))

        self.assertEqual(vehicle_data.loc[(timestamp, 68), 'lineid'], encode_line_name("6E"))



if __name__ == '__main__':
    unittest.main()
