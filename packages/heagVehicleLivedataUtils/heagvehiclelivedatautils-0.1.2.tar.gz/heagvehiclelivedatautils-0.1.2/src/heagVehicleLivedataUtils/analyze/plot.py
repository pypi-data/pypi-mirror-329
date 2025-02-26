"""
TODO: stuff for ploting data
"""

from io import BytesIO

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from .data import DataAnalysis
from ..vehicleInformation import decode_line_id, heagLineColormap, modern_tram_numbers, usual_tram_numbers, \
    electric_bus_numbers


def _plot_vehicle_service_timeseries(vehicle_service_timeseries: pd.DataFrame,
                                      *,
                                      filename: str|BytesIO|None = None,
                                      show_plot: bool= True,
                                      show_line_annotation:bool = False,
                                      datespec: str = '%d.%m.%Y-%H:%M',
                                      sample_time: str|None = None,
                                      title: str = 'Vehicles in service',
                                      figsize: tuple[int,int]|None = None,
                                      time_display_factor:float = .2
                                        ):
    """
    plots the timeseries

    Args:
        vehicle_service_timeseries: dataframe containing timeseries with vehicle service
        show_line_annotation: if true, line Names will also be plotted
        datespec: specifies how timestamp is displayed -> used as argument for pandas strftime
        filename: path of file that is used to save the plot. if left empty, nothing will be saved
        show_plot: true if the plot should be shown
        sample_time: sample size of the plot
        figsize: matplotlib figsize to be used for the plot
        title: title of the plot

    """
    if sample_time is not None:
        vehicle_service_timeseries = vehicle_service_timeseries.fillna(0).resample(sample_time).max()

    # fillna a second time to account for missing timeframe
    vehicle_service_timeseries = vehicle_service_timeseries.fillna(0).astype('int64')

    # format index for plotting
    vehicle_service_timeseries.index = vehicle_service_timeseries.index.strftime(datespec)

    if figsize is not None:
        plt.figure(figsize=figsize)
    else:
        number_of_vehicles = vehicle_service_timeseries.shape[1]
        number_of_entries = vehicle_service_timeseries.shape[0]

        plt.figure(figsize=(3+.2*number_of_vehicles,3+ time_display_factor*number_of_entries))

    if show_line_annotation:
        line_annotation = vehicle_service_timeseries.map(lambda x: f'{decode_line_id(x)}' if x != 0 else '')
        sns.heatmap(vehicle_service_timeseries, annot=line_annotation, fmt='', vmin=0, vmax=10,
                    cmap=heagLineColormap, cbar=False)
    else:
        sns.heatmap(vehicle_service_timeseries, vmin=0, vmax=10, cmap=heagLineColormap, cbar=False)

    plt.title(title)

    plt.tight_layout()

    if filename is not None:
        plt.savefig(filename)
    if show_plot:
        plt.show()
    plt.close()

class VehicleDataPlotter (DataAnalysis):
    """
    provides plotting tools
    """

    def plot_number_of_trams_in_service(self,
                                        *,
                                        filename: str|BytesIO|None = None,
                                        show_plot: bool = True,
                                        sample_time: str|None = '10Min',
                                        datespec: str = '%d.%m.%Y-%H:%M',
                                        figsize: tuple[int, int]|None = None,
                                        time_display_factor: float = .2
                                        ):
        """

        Args:
            time_display_factor: scalar for the width of time
            datespec: specififes how timestamp is displayed TODO: was ist da der spec?
            sample_time: sample size of the plot
            figsize:  figsize to be used for the plot
            show_plot: currently only placeholder
            filename: path of file that is used to save the plot. if left empty, nothing will be saved

        """
        number_of_trams_over_time = self.get_number_of_trams_in_service(sample_time)

        if figsize is None:
            number_of_timepoints = number_of_trams_over_time.shape[0]
            figsize = (3 + time_display_factor*number_of_timepoints, 10)

        number_of_trams_over_time.index = number_of_trams_over_time.index.strftime(datespec)

        ax = number_of_trams_over_time.plot(
            kind="bar",
            stacked=True,
            title='HEAG Fahrzeugeinsätzte',
            ylim=(0, 45),
            ylabel="Anzahl Fahrzeuge im Linienbetrieb",
            figsize=figsize,
            width=1)

        plt.tight_layout()

        if filename is not None:
            ax.figure.savefig(filename)
        # TODO: how does this work in the context here?
        #if show_plot:
        #    plt.show()

    def plot_trams_in_servie(self,
                             /,
                             tram_numbers: list[str],
                             *,
                             filename: str|BytesIO|None = None,
                             show_plot: bool= True,
                             show_line_annotation: bool = False, #testing has shown that annotation is what takes most of the runtime
                             datespec: str = '%d.%m.%Y-%H:%M',
                             sample_time: str|None = None,
                             figsize: tuple[int,int]|None = None,
                             time_display_factor:float = .2):
        """
        plots the line assignment for the specifid trams

        Args:
            tram_numbers: list of operational Numbers of the for witch the service status is supposed to be displayed

            time_display_factor: scalar for the height of time
            show_line_annotation: if true, line Names will also be plotted
            datespec: specififes how timestamp is displayed TODO: was ist da der spec?
            filename: path of file that is used to save the plot. if left empty, nothing will be saved
            show_plot: true if the plot should be shown
            sample_time: sample size of the plot
            figsize: figsize to be used for the plot
        """

        _plot_vehicle_service_timeseries(self.get_trams_in_service()['lineid'].reindex(columns=tram_numbers),
                                          title = "Trams in service",
                                          filename=filename,
                                          show_line_annotation=show_line_annotation,
                                          show_plot=show_plot,
                                          datespec=datespec,
                                          sample_time=sample_time,
                                          figsize=figsize,
                                          time_display_factor=time_display_factor)

    def plot_modern_trams_in_service(self,**kwargs):
        """
        like plot_trams_in_servie, but only plots modern trams

        Args:
            Keyword Args: same as plot_trams_in_service except for tram_numbers

        """
        self.plot_trams_in_servie(modern_tram_numbers, **kwargs)

    # das ist eventuell redundent, könnte auch einfach als default wert bei plot_trams_in_servie gemacht werden
    def plot_all_trams_in_service(self, **kwargs):
        """
       like plot_trams_in_servie, but without the ability to specify trams

       Args:
            Keyword Args: same as plot_trams_in_service except for tram_numbers

       """
        self.plot_trams_in_servie(usual_tram_numbers, **kwargs)

    def plot_buses_in_service(self,
                              bus_numbers: list[str],
                               *,
                              filename: str|BytesIO|None = None,
                             show_plot: bool= True,
                             show_line_annotation: bool = True,
                             datespec: str = '%d.%m.%Y-%H:%M',
                             sample_time: str|None = None,
                             figsize: tuple[int,int]|None = None,
                             time_display_factor:float = .2): # TODO columns need to be wider
        """
        plots the line assignment for the electric buses

        Args:
            bus_numbers: list of Betriebsnummber of the buses whose servie is to be plotted

            time_display_factor: scalar for the height of time
            show_line_annotation: if true, line Names will also be plotted
            datespec: specififes how timestamp is displayed TODO: was ist da der spec?
            filename: path of file that is used to save the plot. if left empty, nothing will be saved
            show_plot: true if the plot should be shown
            sample_time: sample size of the plot
            figsize: figsize to be used for the plot
        """

        _plot_vehicle_service_timeseries(self.get_buses_in_service()['lineid'].reindex(columns=bus_numbers),
                                          title="Buses in service",
                                          filename=filename,
                                          show_line_annotation=show_line_annotation,
                                          show_plot=show_plot,
                                          datespec=datespec,
                                          sample_time=sample_time,
                                          figsize=figsize,
                                          time_display_factor=time_display_factor)

    def plot_electric_buses_in_service(self, **kwargs):
        """
        plots the line assignment for the electric buses

        Args:
            Keyword Args: same as plot_buses_in_service except for bus_numbers
        """

        self.plot_buses_in_service(electric_bus_numbers, **kwargs)

