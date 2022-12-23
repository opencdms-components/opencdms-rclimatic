# =================================================================
#
# Authors: IDEMS International, Stephen Lloyd
#
# Copyright (c) 2022, OpenCDMS Project
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation
# files (the "Software"), to deal in the Software without
# restriction, including without limitation the rights to use,
# copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following
# conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.
#
# =================================================================
"""Provides a set of wrapper functions for the `cdms.products` R package.

This module provides access to the `cdms.products` R package
(https://github.com/IDEMSInternational/cdms.products).
It communicates with the R environment using the `rpy2` package.
Access is provided through a set of wrapper functions.
Each wrapper function:
  - Allows the equivalent R function to be called from Python, using Python
    data types.
  - Has a parameter list that is  as close as possible to the equivalent R
    function's parameter list.
  - Returns it's result as a platform independent object, typically a Python
    pandas data frame, or a link to a JPEG file.
  - Has a similar structure. First it converts the Python parameters (as
    needed) into R equivalent data types used by `rpy2`. It calls the R
    function. If needed, it converts the returned result into a Python data
    type.
"""
from pathlib import Path
from typing import Dict, List, Union

from numpy import integer
from pandas import DataFrame, to_datetime
from rpy2.robjects import NULL as r_NULL
from rpy2.robjects import (NA_Character, NA_Logical, conversion,
                           default_converter, globalenv, packages, pandas2ri,
                           r)
from rpy2.robjects.vectors import DataFrame as RDataFrame
from rpy2.robjects.vectors import FloatVector, ListVector, StrVector

from .enums import (DateTimeFormats, FacetBy, FileTypes, GGThemes, Position,
                    TimeseriesPlotType, Timespan)

r_cdms_products = packages.importr("cdms.products")
r_ggplot2 = packages.importr("ggplot2")


def climatic_extremes(
    data: DataFrame,
    date_time: str,
    elements: List[str] = None,
    station: str = None,
    year: str = None,
    month: str = None,
    dekad: str = None,
    pentad: str = None,
    to: DateTimeFormats = DateTimeFormats.HOURLY,
    by: List[str] = None,
    doy: str = None,
    doy_first: integer = 1,
    doy_last: integer = 366,
    max_val: bool = True,
    min_val: bool = False,
    first_date: bool = False,
    n_dates: bool = False,
    last_date: bool = False,
    na_rm: bool = False,
    na_prop: integer = None,
    na_n: integer = None,
    na_consec: integer = None,
    na_n_non: integer = None,
    names="{.fn}_{.col}",
) -> DataFrame:
    """Calculate extremes from climatic data.

    Returns a data table displaying the minimum and/or maximum values for
    elements in a given time period. This can be provided by station.

    Args:
        data: The data frame to calculate from.
        date_time: The name of the date column in 'data'.
        elements: The name of the elements column in 'data' to  apply the
          function to.
        station: The name of the station column in 'data', if the data are
          for multiple stations.
        year: The name of the year column in 'data'.
        month: The name of the month column in 'data'.
        dekad: The name of the dekad column in 'data'.
        pentad: The name of the pentad column in 'data'.
        to: The date-time format to put the data into.
        by: The name of columns in 'data' to group the summary data by.
        doy: The name of the day of the year (1-366) column in 'data'.
          If 'None' it will be created using 'lubridate::year(data[[doy]])'.
        doy_first: The first day of the year.
        doy_last: The last day of the year.
        max_val: If True the extreme maximum is calculated.
        min_val: If True the extreme minimum is calculated.
        first_date: If True the first instance of 'date_time' when the value
          equals the summary value is included. Generally only used for extreme
          summaries i.e. first 'date_time' when the maximum occurred.
        n_dates: If True the number of 'date_time' points when the value
          equals the summary value is included. Generally only used for
          extreme summaries i.e. number of days in which the minimum occurred.
        last_date: If True the last instance of 'date_time' when the value
          equals the summary value is included. Generally only used for
          extreme summaries i.e. last 'date_time' whenthe maximum occurred.
        na_rm: If True all 'na_ parameters are ignored and missing values are
          removed. If 'False' missing values are not
          removed unless any 'na_ parameters are specified.
        na_prop: Max proportion of missing values allowed.
        na_n: Max number of missing values allowed.
        na_consec: Max number of consecutive missing values allowed.
        na_n_non: Min number of non-missing values required.
        names: Format of column names. Passed to '.names' in 'dplyr::across'.

    Returns:
        A summary data frame containing minimum/maximum values for element(s).
    """
    # If dates in data frame do not include timezone data, then set to UTC
    data[date_time] = to_datetime(data[date_time], utc=True)
    if not elements:
        elements = StrVector([])
    r_params: Dict = __get_r_params(locals())
    r_data_frame: RDataFrame = r_cdms_products.climatic_extremes(**r_params)
    return __get_data_frame(r_data_frame)


def climatic_missing(
    data: DataFrame,
    date_time: str,
    elements: List[str],
    station_id: str = None,
    start: bool = True,
    end: bool = False,
) -> DataFrame:
    """Summarise missing data in a data frame.

     Returns a data frame displaying the number and
     percentage of missing values for an element (and station) in a
     given time period. The total number of full years are also given.

    Args:
        data: The data frame to calculate from.
        date_time: The name of the date column in 'data'.
        elements: The name of the column in 'data' to apply the function to.
        station_id: The name of the station column in 'data', if the data are
          for multiple station, then the calculations are performed separately
          for each station.
        start: If 'True' start date as ...
        end: If 'True' set end date as ...

    Returns:
        Data frame summarising the missing data.
    """
    # If dates in data frame do not include timezone data, then set to UTC
    data[date_time] = to_datetime(data[date_time], utc=True)

    if not elements:
        elements = StrVector([])

    r_params: Dict = __get_r_params(locals())
    r_data_frame: RDataFrame = r_cdms_products.climatic_missing(**r_params)
    return __get_data_frame(r_data_frame)


def climatic_summary(
    data: DataFrame,
    date_time: str,
    station: str = None,
    elements: List[str] = None,
    year: str = None,
    month: str = None,
    dekad: str = None,
    pentad: str = None,
    to: DateTimeFormats = DateTimeFormats.HOURLY,
    by: List[str] = None,
    doy: str = None,
    doy_first: integer = 1,
    doy_last: integer = 366,
    summaries: Dict[str, str] = None,
    na_rm: bool = False,
    na_prop: integer = None,
    na_n: integer = None,
    na_consec: integer = None,
    na_n_non: integer = None,
    first_date: bool = False,
    n_dates: bool = False,
    last_date: bool = False,
    summaries_params: Dict[str, Dict] = None,
    names: str = "{.fn}_{.col}",
) -> DataFrame:
    """Calculate summaries from climatic data.

    Returns a data table displaying summary statistics for element(s)
    (and for each station) in a given time period.

    Args:
        data: The data frame to calculate from.
        date_time: The name of the date column in 'data'.
        station: The name of the station column in 'data', if the data are
          for multiple stations.
        elements: The name of the elements column in 'data'
         to apply the function to..
        year: The name of the year column in 'data'.
        month: The name of the month column in 'data'.
        dekad: The name of the dekad column in 'data'.
        pentad: The name of the pentad column in 'data'.
        to: The date-time format to put the data into.
        by: The name of columns in 'data' to group the summary data by.
        doy: The name of the day of the year (1-366) column in 'data'.
          If 'NULL' it will be created using 'lubridate::year(data[[doy]])'.
        doy_first: The first day of the year.
        doy_last: The last day of the year.
        summaries: A named character vector of summary functions. The names are
          used as the column names in the results. The values can be any
          function name as a string or a function call as a formula.
          e.g. {"mean" = "mean", "st_dv" = "sd", "n = "~dplyr::n()"}.
        na_rm: If True all 'na_ parameters are ignored and missing values are
          removed. If 'False' missing values are not
          removed unless any 'na_ parameters are specified.
        na_prop: Max proportion of missing values allowed.
        na_n: Max number of missing values allowed.
        na_consec: Max number of consecutive missing values allowed.
        na_n_non: Min number of non-missing values required.
        first_date: If True the first instance of 'date_time' when the value
          equals the summary value is included. Generally only used for extreme
          summaries i.e. first 'date_time' when the maximum occurred.
        n_dates: If True the number of 'date_time' points when the value
          equals the summary value is included. Generally only used for
          extreme summaries i.e. number of days in which the minimum occurred.
        last_date: If True the last instance of 'date_time' when the value
          equals the summary value is included. Generally only used for
          extreme summaries i.e. last 'date_time' whenthe maximum occurred.
        summaries_params: Additional parameters to pass to 'summaries'. Must be
          a list of lists with the same names as 'summaries'.
        names: Format of column names. Passed to '.names' in 'dplyr::across'.

    Returns:
        A summary data frame for selected element(s) in climatic data.
    """
    # If dates in data frame do not include timezone data, then set to UTC

    if not elements:
        elements = StrVector([])

    if not by:
        by = StrVector([])

    if not summaries:
        summaries = {"n": "~dplyr::n()"}

    if not summaries_params:
        summaries_params = {}

    data[date_time] = to_datetime(data[date_time], utc=True)

    r_params: Dict = __get_r_params(locals())

    r_params["summaries"] = StrVector(list(summaries.values()))
    r_params["summaries"].names = list(summaries.keys())

    # summaries_params: convert to a 2-level deep R-type:
    #   one list item for each summary function, and one list of parameters for
    #   each summary function e.g. 'list(mean = list(trim = 0.5))'
    r_summaries_params: Dict[str, ListVector] = {}
    for key in summaries_params:
        r_summaries_params[key] = ListVector(summaries_params[key])
        r_summaries_params[key].names = list(summaries_params[key].keys())
    r_params["summaries_params"] = ListVector(r_summaries_params)
    r_params["summaries_params"].names = list(summaries_params.keys())

    r_data_frame: RDataFrame = r_cdms_products.climatic_summary(**r_params)
    return __get_data_frame(r_data_frame)


def export_cdt(
    data: DataFrame,
    station: str,
    element: str,
    latitude: str,
    longitude: str,
    altitude: str,
    file_path: str,
    type: Timespan = Timespan.DEKAD.value,
    date_time: str = None,
    year: str = None,
    month: str = None,
    dekad: str = None,
    metadata: DataFrame = None,
):
    """Export daily or dekadal data in the format for CDT.

    Rearranges a data frame using 'prepare_cdt' to a format suitable for use in
    CDT. The data frame is then written to a file or connection.

    Args:
        data: Data frame of daily or dekadal climatic data in tidy format
          i.e. one row per time point (per station) and one column per element.
        station: Name of the station identifying column in 'data'.
        element: Name of the element column in 'data'.
        latitude: Name of the latitude column in 'metadata'.
        longitude: Name of the longitude column in 'metadata'.
        altitude: Name of the altitude column in 'metadata'.
        file_path: The file path and file name to export.
        type: The type of data, either 'dekad' or 'daily'.
        date_time: Name of the date column in 'data'. If 'type' is 'daily',
          then required. If 'type' is 'dekad', then this is only needed if
          'year', 'month', and 'dekad' are not specified.
        year: Name of the year column in 'data'. Only needed if 'type' is
          'dekad'. If 'None' it will be created using
          'lubridate::year(data[[date_time]])'.
        month: Name of the month column in 'data'. Only needed if 'type' is
          'dekad'. If 'None' it will be created using
          'lubridate::year(month[[date_time]])'.
        dekad: Name of the dekad column in 'data'. Only needed if 'type' is
          'dekad'. If 'None' it will be created using the 'dekad' function.
        metadata: Data frame of station metadata. Use this if the station
          details are in a separate data.frame with one row per station. If
          specified, 'latitude, 'longitude and 'altitude' are assumed to be in
          'metadata' and 'station' must be in both 'data' and 'metadata' to
          facilitate joining.

    Returns:
        Nothing.
    """
    # If dates in data frame do not include timezone data, then set to UTC
    data[date_time] = to_datetime(data[date_time], utc=True)

    r_params: Dict = __get_r_params(locals())
    r_params["data"] = __convert_posixt_to_r_date(r_params["data"])

    r_cdms_products.export_cdt(**r_params)


def export_cdt_daily(
    data: DataFrame,
    station: str,
    element: str,
    date_time: str,
    latitude: str,
    longitude: str,
    altitude: str,
    file_path: str,
    metadata: DataFrame = None,
):
    """Export daily data in the format for CDT.

    Takes a data frame with daily data. This data frame is then rearranged
    using 'prepare_cdt_daily' to a format suitable for use in CDT, and then
    written to a file or connection.

    Args:
        data: Data frame of daily climatic data in tidy format
          i.e. one row per day (per station) and one column per element.
        station: Name of the station identifying column in 'data'.
        element: Name of the element column in 'data'.
        date_time: Name of the date column in 'data'.
        latitude: Name of the latitude column in 'metadata'.
        longitude: Name of the longitude column in 'metadata'.
        altitude: Name of the altitude column in 'metadata'.
        file_path: The file path and file name to export.
        metadata: Data frame of station metadata. Use this is the
          station details are in a separate data.frame with one row per
          station. If specified, 'latitude, 'longitude and 'altitude'
          are assumed to be in 'metadata' and 'station' must be in both
          'data' and 'metadata' to facilitate joining.

    Returns:
        Nothing.
    """
    # If dates in data frame do not include timezone data, then set to UTC
    data[date_time] = to_datetime(data[date_time], utc=True)

    r_params: Dict = __get_r_params(locals())
    r_params["data"] = __convert_posixt_to_r_date(r_params["data"])

    r_cdms_products.export_cdt_daily(**r_params)


def export_cdt_dekad(
    data: DataFrame,
    station: str,
    element: str,
    date_time: str,
    latitude: str,
    longitude: str,
    altitude: str,
    file_path: str,
    year: str = None,
    month: str = None,
    dekad: str = None,
    metadata: DataFrame = None,
):
    """Export dekad data in CDT format.

    Takes a data frame that has elements summarised by dekad. This data frame
    is then rearranged using 'prepare_cdt_dekad' to a format suitable for use
    in CDT, and then written to a file or connection.

    Args:
        data: Data frame of dekadal climatic data in tidy
          format i.e. one row per dekad (per station) and one column
          per element.
        station: Name of the station identifying column in 'data'.
        element: Name of the element column in 'data'.
        date_time: Name of the date column in 'data'. If 'type' is 'daily',
          then required. If 'type' is 'dekad', then this is only needed if
          'year', 'month', and 'dekad' are not specified.
        latitude: Name of the latitude column in 'metadata'.
        longitude: Name of the longitude column in 'metadata'.
        altitude: Name of the altitude column in 'metadata'.
        year: Name of the year column in 'data'. Only needed if 'type' is
          'dekad'. If 'None' it will be created using
          'lubridate::year(data[[date_time]])'.
        month: Name of the month column in 'data'. Only needed if 'type' is
          'dekad'. If 'None' it will be created using
          'lubridate::year(month[[date_time]])'.
        dekad: Name of the dekad column in 'data'. Only needed if 'type' is
          'dekad'. If 'None' it will be created using the 'dekad' function.
        metadata: Data frame of station metadata. Use this if the station
          details are in a separate data.frame with one row per station. If
          specified, 'latitude, 'longitude and 'altitude' are assumed to be in
          'metadata' and 'station' must be in both 'data' and 'metadata' to
          facilitate joining.
        file_path: The file path and file name to export.

    Returns:
        Nothing.
    """
    # If dates in data frame do not include timezone data, then set to UTC
    data[date_time] = to_datetime(data[date_time], utc=True)

    r_params: Dict = __get_r_params(locals())
    r_params["data"] = __convert_posixt_to_r_date(r_params["data"])

    r_cdms_products.export_cdt_dekad(**r_params)


def export_climat_messages(
    data: DataFrame,
    date_time: str,
    station_id: str,
    folder: str = Path.cwd().resolve().absolute(),
    year: str = None,
    month: str = None,
    mean_pressure_station: str = None,
    mean_pressure_reduced: str = None,
    mean_temp: str = None,
    mean_max_temp: str = None,
    mean_min_temp: str = None,
    mean_vapour_pressure: str = None,
    total_precip: str = None,
    total_sunshine: str = None,
    total_snow_depth: str = None,
    max_ws: str = None,
    min_h_vis: str = None,
):
    """Export CLIMAT messages file(s) from daily data.

    Exports CLIMAT messages file(s) from daily data

    Args:
        data: The data frame to calculate from.
        date_time: The name of the date column in 'data'.
        station_id: The name of the station column in 'data'.
        folder: TODO
        year: The name of the year column in 'data'.
        month: The name of the month column in 'data'.
        mean_pressure_station: TODO
        mean_pressure_reduced: TODO
        mean_temp: TODO
        mean_max_temp: TODO
        mean_min_temp: TODO
        mean_vapour_pressure: TODO
        total_precip: TODO
        total_sunshine: TODO
        total_snow_depth: Daily total snow depth in cm column name
        max_ws: Daily maximum wind speed in m/s column name
        min_h_vis: Daily minimum horizontal visibility in m column name

    Returns:
        Nothing.
    """
    # If dates in data frame do not include timezone data, then set to UTC
    data[date_time] = to_datetime(data[date_time], utc=True)

    r_params: Dict = __get_r_params(locals())
    r_params["data"] = __convert_posixt_to_r_date(r_params["data"])

    r_cdms_products.export_climat_messages(**r_params)


def export_climdex(
    data: DataFrame,
    prcp: str,
    tmax: str,
    tmin: str,
    file_path: str,
    date: str = None,
    year: str = None,
    month: str = None,
    day: str = None,
    file_type: FileTypes = FileTypes.CSV.value,
):
    """Export data in the format for RClimDex.

    Rearranges a data frame using 'prepare_climdex' to a format suitable for
    use in RClimDex. The data frame is then written to a file or connection.

    Args:
        data: Data frame of daily climatic data in tidy format
          i.e. one row per day and one column per element.
        prcp: Name of the precipitation/rainfall column in 'data'.
        tmax: Name of the maximum temperature column in 'data'.
        tmin: Name of the minimum temperature column in 'data'.
        date: Name of the date column in 'data'. This is only needed if 'year',
          'month', and 'day' are not specified.
        year: Name of the year column in 'data'. If 'None' it will be created
          using 'lubridate::year(data[[date]])'.
        month: Name of the month column in 'data'. If 'None' it will be created
          using 'lubridate::month(data[[date]])'.
        day: Name of the day of the month column in 'data'. If 'None' it will
          be created using 'lubridate::day(data[[date]])'.
        file_type: The file type to export as either 'csv' or 'txt'.
        file_path: The file path and file name to export.

    Returns:
        Nothing.
    """
    # If dates in data frame do not include timezone data, then set to UTC
    if date is not None:
        data[date] = to_datetime(data[date], utc=True)

    r_params: Dict = __get_r_params(locals())
    r_params["data"] = __convert_posixt_to_r_date(r_params["data"])

    r_cdms_products.export_climdex(**r_params)


def export_geoclim(
    data: DataFrame,
    year: str,
    type_col: str,
    element: str,
    station_id: str,
    latitude: str,
    longitude: str,
    file_path: str,
    type: Timespan = Timespan.DEKAD.value,
    metadata: DataFrame = None,
    join_by: List[str] = None,
    add_cols: List[str] = None,
):
    """Exports dekad or pentad data in GeoCLIM format.

    Rearranges a data frame using 'prepare_geoclim' to a format suitable for
    use in GeoCLIM. The data frame is then written to a file or connection.

    Args:
        data: The data frame to calculate from.
        year: The name of the year column in 'data'.
        type_col: The name of the dekad or pentad column in 'data'.
        element: Name of the element column in 'data'.
        station_id: The name of the station column in 'metadata', or 'data'
          if 'metadata' is 'None'.
        latitude: The name of the latitude column in 'metadata', or 'data' if
          'metadata' is 'None'.
        longitude: The name of the longitude column in 'metadata', or 'data' if
          'metadata' is 'None'.
        type: Whether the data is in 'dekad' or 'pentad' format.
        metadata: The metadata data frame to calculate from.
        join_by: The variable(s) to merge the 'data' and 'metadata' data frames
        add_cols: Names of additional metadata columns that should be included
          in the output.
        file_path: The file path and file name to export.

    Returns:
        Nothing.
    """
    if not join_by:
        join_by = StrVector([])
    if not add_cols:
        add_cols = StrVector([])

    r_params: Dict = __get_r_params(locals())
    r_cdms_products.export_geoclim(**r_params)


def export_geoclim_dekad(
    data: DataFrame,
    year: str,
    dekad: str,
    element: str,
    station_id: str,
    latitude: str,
    longitude: str,
    file_path: str,
    metadata: DataFrame = None,
    join_by: List[str] = None,
    add_cols: List[str] = None,
):
    """Exports dekad data in GeoCLIM format.

    Takes a data frame that is given by by dekad. This data frame is then
    rearranged using 'prepare_geoclim_dekad' to a format suitable for use in
    GeoCLIM, and then written to a file or connection.

    Args:
        data: The data frame to calculate from.
        year: The name of the year column in 'data'.
        dekad: The name of the dekad column in 'data'.
        element: Name of the element column in 'data'.
        station_id: The name of the station column in 'metadata', or 'data'
          if 'metadata' is 'None'.
        latitude: The name of the latitude column in 'metadata', or 'data' if
          'metadata' is 'None'.
        longitude: The name of the longitude column in 'metadata', or 'data' if
          'metadata' is 'None'.
        file_path: The file path and file name to export.
        metadata: The metadata data frame to calculate from.
        join_by: The variable(s) to merge the 'data' and 'metadata' dataframes
        add_cols: Names of additional metadata columns that should be included
          in the output.

    Returns:
        Nothing.
    """
    if not join_by:
        join_by = StrVector([])
    if not add_cols:
        add_cols = StrVector([])

    r_params: Dict = __get_r_params(locals())
    r_cdms_products.export_geoclim_dekad(**r_params)


def export_geoclim_month(
    data: DataFrame,
    year: str,
    month: str,
    element: str,
    station_id: str,
    latitude: str,
    longitude: str,
    file_path: str,
    metadata: DataFrame = None,
    join_by: List[str] = None,
    add_cols: List[str] = None,
):
    """Export monthly data in GeoCLIM format.

    Takes a data frame that is given by month. This data frame is then
    rearranged using 'prepare_geoclim_month' to a format suitable for use in
    GeoCLIM, and then written to a file or connection.

    Args:
        data: The data frame to calculate from.
        year: The name of the year column in 'data'. If 'None' it will be
          created using 'lubridate::year(data[[date_time]])'.
        month: The name of the month column in 'data'. If 'None' it will be
          created using 'lubridate::year(month[[date_time]])'.
        element: Name of the element column in 'data'.
        station_id: The name of the station column in 'metadata', or 'data'
          if 'metadata' is 'None'.
        latitude: The name of the latitude column in 'metadata', or 'data' if
          'metadata' is 'None'.
        longitude: The name of the longitude column in 'metadata', or 'data'
          if 'metadata' is 'None'.
        file_path: The file path and file name to export.
        metadata: The metadata data frame to calculate from.
        join_by: The variable(s) to merge the 'data' and 'metadata' data frames
        add_cols: Names of additional metadata columns that should be included
          in the output.

    Returns:
        Nothing.
    """
    if not join_by:
        join_by = StrVector([])
    if not add_cols:
        add_cols = StrVector([])

    r_params: Dict = __get_r_params(locals())
    r_cdms_products.export_geoclim_month(**r_params)


def export_geoclim_pentad(
    data: DataFrame,
    year: str,
    pentad: str,
    element: str,
    station_id: str,
    latitude: str,
    longitude: str,
    file_path: str,
    metadata: DataFrame = None,
    join_by: List[str] = None,
    add_cols: List[str] = None,
):
    """Export pentad data in GeoCLIM format.

    Takes a data frame that is in a pentad format. This data frame is then
    rearranged using 'prepare_geoclim_pentad' to a format suitable for use in
    GeoCLIM, and then written to a file or connection.

    Args:
        data: The data frame to calculate from.
        year: The name of the year column in 'data'.
        pentad: The name of the pentad column in 'data'.
        element: Name of the element column in 'data'.
        station_id: The name of the station column in 'metadata', or 'data'
          if 'metadata' is 'None'.
        latitude: The name of the latitude column in 'metadata', or 'data' if
          'metadata' is 'None'.
        longitude: The name of the longitude column in 'metadata', or 'data' if
          'metadata' is 'None'.
        file_path: The file path and file name to export.
        metadata: The metadata data frame to calculate from.
        join_by: The variable(s) to merge the 'data' and 'metadata' dataframes
        add_cols: Names of additional metadata columns that should be included
          in the output.

    Returns:
        Nothing.
    """
    if not join_by:
        join_by = StrVector([])
    if not add_cols:
        add_cols = StrVector([])

    r_params: Dict = __get_r_params(locals())
    r_cdms_products.export_geoclim_pentad(**r_params)


def histogram_plot(
    path: str,
    file_name: str,
    data: DataFrame,
    date_time: str,
    elements: List[str],
    station: str = None,
    facet_by: FacetBy = FacetBy.STATIONS.value,
    position: Position = Position.IDENTITY.value,
    colour_bank: str = None,
    na_rm: bool = False,
    orientation: str = NA_Character,
    show_legend: bool = NA_Logical,
    width: int = None,
    facet_nrow: int = None,
    facet_ncol: int = None,
    title: str = "Histogram Plot",
    x_title: str = None,
    y_title: str = None,
):
    """Produce a histogram of elements by station.

    Creates a histogram using 'ggplot2' for each element and station given.
    Takes a data frame as an input and the relevant columns to create the plot.
    Writes the histogram to a JPEG file.

    Args:
        path: The location to write the JPEG output file.
        file_name: The name of the JPEG output file.
        data: The data frame to calculate from.
        date_time: The name of the date column in 'data'.
        elements: The name of the elements column in 'data' to apply the
          function to.
        station: The name of the station column in 'data', if the data are
          for multiple station. Histogram plots are calculated separately
          for each station.
        facet_by: Whether to facet by stations, elements, both, or neither.
          Options are 'stations', 'elements', 'station-elements',
          'elements-stations', or 'none'.
        position: Position adjustment.
        colour_bank: A string denoting colour values if 'position' is 'layer'.
          By default, colours from 'ggplot2::luv_colours' are used.
        na_rm: If False, the default, missing values are
          removed with a warning. If True, missing values are
          silently removed.
        orientation: The orientation of the layer. The default ('NA')
          automatically determines the orientation from the aesthetic
          mapping. In the rare event that this fails it can be given
          explicitly by setting 'orientation' to either "x" or "y".
        show_legend: Should this layer be included in the legends?
          'NA', the default, includes if any aesthetics are mapped.
          False never includes, and True always includes.
        width: Bar width. By default, set to 90% of the resolution of the
          data.
        facet_nrow: Number of rows for the facets if 'facet_by' is one of
          'stations' or 'elements'. Only if 'facet_ncol' is given.
        facet_ncol: Number of rows for the facets if 'facet_by' is one of
          'stations' or 'elements'. Only if 'facet_nrow' is given.
        title: The text for the title.
        x_title: The text for the x-axis.
        y_title: The text for the y-axis.

    Returns:
        Nothing.
    """
    # If dates in data frame do not include timezone data, then set to UTC
    data[date_time] = to_datetime(data[date_time], utc=True)

    r_params: Dict = __get_r_params(
        locals(), exclude={"file_name", "path", "ggtheme"}
    )
    r_plot = r_cdms_products.histogram_plot(**r_params)
    r_ggplot2.ggsave(
        filename=file_name,
        plot=r_plot,
        device="jpeg",
        path=path,
        width=25,
        height=20,
        units="cm",
    )


def inventory_plot(
    path: str,
    file_name: str,
    data: DataFrame,
    date_time: str,
    elements: List[str],
    station: str = None,
    year: str = None,
    doy: str = None,
    year_doy_plot: bool = False,
    facet_by: str = None,
    facet_x_size: int = 7,
    facet_y_size: int = 11,
    title: str = "Inventory Plot",
    plot_title_size: int = None,
    plot_title_hjust: float = 0.5,
    x_title: str = None,
    y_title: str = None,
    x_scale_from: int = None,
    x_scale_to: int = None,
    x_scale_by: int = None,
    y_date_format: str = None,
    y_date_scale_by: str = None,
    y_date_scale_step: int = 1,
    facet_scales: str = "fixed",
    facet_dir: str = "h",
    facet_x_margin: List[int] = None,
    facet_y_margin: List[int] = None,
    facet_nrow: int = None,
    facet_ncol: int = None,
    missing_colour: str = "red",
    present_colour: str = "grey",
    missing_label: str = "Missing",
    present_label: str = "Present",
    display_rain_days: bool = False,
    rain: str = None,
    rain_cats: Dict[str, list] = None,
    coord_flip: bool = False,
):
    """Produce an inventory of available and missing data.

    Creates an inventory plot using 'ggplot2' that displays whether a value is
    observed or missing for each element and station given. Takes a data frame
    as an input and the relevant columns to create the plot.
    Writes the plot to a JPEG file.

    Args:
        path: The location to write the JPEG output file.
        file_name: The name of the JPEG output file.
        data: The data frame to calculate from.
        date_time: The name of the date column in 'data'.
        elements: The name of the elements column in 'data' to apply the
          function to.
        station: The name of the station column in 'data', if the data are
          for multiple stations.
        year: The name of the year column in 'data'. If 'None' it will be
          created using 'lubridate::year(data[[date_time]])'.
        doy: The name of the day of the year (1-366) column in 'data'.
          If 'doy' is 'None' then it can be calculated as
          'yday_366(data[[date_time]])' if 'date_time' is provided.
        year_doy_plot: Whether the day of year should be on the y-axis on
          the plot.
        facet_by: Whether to facet by stations, elements, or both. Options are
          'stations', 'elements', 'station-elements', 'elements-stations'. In
          'station-elements', stations are given as rows and elements as
          columns. In 'elements-stations', elements are given as rows and
          stations as columns.
        facet_x_size: Text size for the facets on the x-axis in pts.
        facet_y_size: Text size for the facets on the y-axis in pts.
        title: The text for the title.
        plot_title_size: Text size for the title in pts.
        plot_title_hjust: Horizontal justification for title.
          Value between 0 and 1.
        x_title: The text for the x-axis.
        y_title: The text for the y-axis.
        x_scale_from: The year to display the inventory plot from.
        x_scale_to: The year to display the inventory plot to.
        x_scale_by: The difference, in years, to give the x tick marks between
          from and to.
        y_date_format: TODO
        y_date_scale_by: TODO
        y_date_scale_step: TODO
        facet_scales: Are scales shared across all
            facets (the default, 'fixed'), or do they vary across
            rows ('free_x'), columns ('free_y'), or both
            rows and columns ('free')?
        facet_dir: TODO
        facet_x_margin: Margin width around the text for the x-facets.
        facet_y_margin: Margin width around the text for the y-facets.
        facet_nrow: Number of rows for the facets if 'facet_by' is one of
          'stations' or 'elements'. Only if 'facet_ncol' is given.
        facet_ncol: Number of rows for the facets if 'facet_by' is one of
          'stations' or 'elements'. Only if 'facet_nrow' is given.
        missing_colour: Colour to represent the missing values.
          Default 'red'.
        present_colour: Colour to represent the observed values.
          Default 'grey'.
        missing_label: Label to give in legend for missing values.
          Default 'Missing'.
        present_label: Label to give in legend for observed values.
          Default 'Present'.
        display_rain_days: If 'rain' parameter is not 'None', and 'rain' is not
          an element in the 'elements' parameter, whether to include dry and
          rainy days.
        rain: The name of the rain column in 'data'.
        rain_cats: TODO
        oord_flip: Whether to switch the x and y axes.
        labels: If 'display_rain_days = TRUE', the labels in the key for dry
          and rainy days. By default, 'c("Dry", "Rain")'
        key_colours: If 'display_rain_days = TRUE', the colours for dry and
          rainy days. By default, 'c("tan3", "blue"))'

    Returns:
        Nothing.
    """
    # If dates in data frame do not include timezone data, then set to UTC
    data[date_time] = to_datetime(data[date_time], utc=True)

    if rain_cats is None:
        rain_cats = {
            "breaks": [0, 0.85, float("inf")],
            "labels": ["Dry", "Rain"],
            "key_colours": ["tan3", "blue"],
        }

    r_params: Dict = __get_r_params(
        locals(), exclude={"file_name", "path", "ggtheme"}
    )
    r_params["data"] = __convert_posixt_to_r_date(r_params["data"])

    # translate none null facet margin parameters to R ggplot margin types
    if r_params["facet_x_margin"] == r_NULL:
        r_params["facet_x_margin"] = r_ggplot2.margin(1, 0, 1, 0)
    if r_params["facet_y_margin"] == r_NULL:
        r_params["facet_y_margin"] = r_ggplot2.margin(1, 0, 1, 0)

    # convert the dictionary of R lists, into a named R list of R lists
    #  e.g. with format like 'list(breaks = c(0, 0.85, Inf),
    #  labels = c("Dry", "Rain"), key_colours = c("tan3", "blue"))'
    r_rain_cats: Dict[str, Union[StrVector, FloatVector]] = {}
    for key in rain_cats:
        key_list: List = list(rain_cats[key])
        if len(key_list) > 0:
            if isinstance(key_list[0], str):
                r_rain_cats[key] = StrVector(key_list)
            else:
                r_rain_cats[key] = FloatVector(key_list)
    r_params["rain_cats"] = ListVector(r_rain_cats)

    r_plot = r_cdms_products.inventory_plot(**r_params)

    r_ggplot2.ggsave(
        filename=file_name,
        plot=r_plot,
        device="jpeg",
        path=path,
        width=25,
        height=20,
        units="cm",
    )


def inventory_table(
    data: DataFrame,
    date_time: str,
    elements: List[str] = None,
    station: str = None,
    year: str = None,
    month: str = None,
    day: str = None,
    missing_indicator: str = "M",
    observed_indicator: str = "X",
) -> DataFrame:
    """Create Inventory Table.

    Returns a table for each cell in a climatic data frame with an indicator to
    show whether the corresponding cell value is missing or observed.

    Args:
        data: The data frame to calculate from.
        date_time: The name of the date column in 'data'.
        elements: The name of the elements column in 'data'
          to apply the function to..
        station: The name of the station column in 'data', if the data are
          for multiple stations. The inventory table is
          calculated separately for each station.
        year: The name of the year column in 'data'. If 'None' it will be
          created using 'lubridate::year(data[[date_time]])'.
        month: The name of the month column in 'data'. If 'None' it will be
          created using 'lubridate::year(month[[date_time]])'.
        day: The name of the day column in 'data'. If 'None' it will be
          created using 'lubridate::day(data[[date_time]])'.
        missing_indicator: Indicator to give if the data is missing.
          Default 'M'.
        observed_indicator: Indicator to give if the data is observed.
          Default 'X'.

    Returns:
        A data frame indicating if the value is missing or observed.
    """
    # If dates in data frame do not include timezone data, then set to UTC
    data[date_time] = to_datetime(data[date_time], utc=True)
    if not elements:
        elements = StrVector([])

    r_params: Dict = __get_r_params(locals())
    r_params["data"] = __convert_posixt_to_r_date(r_params["data"])
    r_data_frame: RDataFrame = r_cdms_products.inventory_table(**r_params)
    return __get_data_frame(r_data_frame)


def output_CPT(
    data: DataFrame,
    lat_lon_data: DataFrame,
    station_latlondata: str,
    latitude: str,
    longitude: str,
    station: str,
    year: str,
    element: str,
    long_data: bool = True,
    na_code: int = -999,
) -> DataFrame:
    """Outputs data in the format for the CPT software.

    Returns a data frame to a format suitable for use in the CPT software.

    Args:
        data: The data frame to calculate from.
        lat_lon_data: The name of the metadata to calculate from.
        station_latlondata: The name of the station column in
          'lat_lon_data', or 'data' if 'long_data' is False.
        latitude: The name of the latitude column in 'lat_lon_data', or 'data'
          if 'long_data' is False.
        longitude: The name of the longitude column
            in 'lat_lon_data', or 'data' if 'long_data' is False.
        station: The name of the station column in 'data', if the data are
          for multiple station.
        year: The name of the year column in 'data'.
        element: Name of the element column in 'data'.
        long_data: Whether all columns are in 'data'.
            If all data is in one dataframe
            then must have 'long_data = TRUE'.
        na_code: Indicator for NA values in data.

    Returns:
        A data frame formatted for use in CPT.
    """
    r_params: Dict = __get_r_params(locals())
    r_data_frame: RDataFrame = r_cdms_products.output_CPT(**r_params)
    return __get_data_frame(r_data_frame)


def timeseries_plot(
    path: str,
    file_name: str,
    data: DataFrame,
    date_time: str,
    elements: List[str],
    station: str = None,
    facet_by: FacetBy = FacetBy.STATIONS.value,
    type: TimeseriesPlotType = TimeseriesPlotType.LINE.value,
    add_points: bool = False,
    add_line_of_best_fit: bool = False,
    se: bool = True,
    add_path: bool = False,
    add_step: bool = False,
    na_rm: bool = False,
    show_legend: bool = NA_Logical,
    title: str = "Timeseries Plot",
    x_title: str = None,
    y_title: str = None,
):
    """Produce a timeseries graph.

    Creates a timeseries plot using 'ggplot2' for each element and station
    given. Takes a data frame as an input and the relevant columns to create
    the plot.
    Writes the plot to a JPEG file.

    Args:
        path: The location to write the JPEG output file.
        file_name: The name of the JPEG output file.
        data: The data frame to calculate from.
        date_time: The name of the date column in 'data'.
        elements: The name of the elements column in 'data' to apply
          the function to.
        station: The name of the station column in 'data', if the data are for
          multiple stations. Timeseries plots are calculated separately for
          each station.
        facet_by: Whether to facet by stations, elements, both, or neither.
          Options are 'stations', 'elements', 'station-elements',
          'elements-stations', or 'none'.
        type: The type of plot, either "line" or line graphs or "bar" for bar
          graphs.
        add_points: If True, points are added to the plot using
          'ggplot2::geom_point()'.
        add_line_of_best_fit: If True, points are added to the plot using
          'ggplot2::geom_smooth(method = "lm")'.
        se: If True, the standard error is added to the line of best fit.
          Only works if 'add_line_of_best_fit' is True.
        add_path: If True, paths are added to the plot using
          'ggplot2::geom_path()'.
        add_step: If True, steps are added to the plot using
          'ggplot2::geom_step()'.
        na_rm: If False, the default, missing values are removed with a
          warning. If True, missing values are silently removed.
        show_legend: Should this layer be included in the legends?
          'NA', the default, includes if any aesthetics are mapped.
          False never includes, and True always includes.
        title: The text for the title.
        x_title: The text for the x-axis.
        y_title: The text for the y-axis.

    Returns:
        Nothing.
    """
    # If dates in data frame do not include timezone data, then set to UTC
    data[date_time] = to_datetime(data[date_time], utc=True)

    r_params: Dict = __get_r_params(
        locals(), exclude={"file_name", "path", "ggtheme"}
    )
    r_plot = r_cdms_products.timeseries_plot(**r_params)
    r_ggplot2.ggsave(filename=file_name, plot=r_plot, device="jpeg", path=path)


def windrose(
    path: str,
    file_name: str,
    data: DataFrame,
    speed: List[float],
    direction: List[float],
    facet_by: List[str] = None,
    n_directions: int = 12,
    n_speeds: int = 5,
    speed_cuts: List[float] = None,
    col_pal: str = "GnBu",
    ggtheme: GGThemes = "grey",
    legend_title="Wind Speed",
    calm_wind: float = 0,
    variable_wind: float = 990,
    n_col: int = None,
):
    """Produce a windrose graph from the clifro package.

    Creates a windrose plot using 'ggplot2' of wind speed and direction.
    This function is a wrapper of the 'clifro::windrose()' function.
    Writes the plot to a JPEG file.

    Args:
        path: The location to write the JPEG output file.
        file_name: The name of the JPEG output file.
        data: The data frame to calculate from.
        speed: A vector containing wind speeds.
        direction: A vector containing wind direction.
        facet_by: Facets used to plot the various windroses.
        n_directions: The number of direction bins to
            plot (petals on the rose). The number of directions
            defaults to 12.
        n_speeds: The number of equally spaced wind speed bins to plot.
            This is used if speed_cuts is NA (default 5).
        speed_cuts: A vector containing the cut points for the wind speed
            intervals, or NA (default).
        col_pal: String indicating the name of the 'RColorBrewer' colour
            palette to be used for plotting.
        ggtheme: String (partially) matching the 'ggtheme' to be used for
            plotting.
        legend_title: Legend title.
        calm_wind: The upper limit for wind speed that is considered calm
            Default 0.
        variable_wind: Variable winds (if applicable).
        n_col: The number of columns to plot. Default 1.

    Returns:
        Nothing.
    """
    if speed_cuts is None:
        speed_cuts = FloatVector([])

    r_params: Dict = __get_r_params(
        locals(), exclude={"file_name", "path", "ggtheme"}
    )
    r_plot = r_cdms_products.windrose(**r_params)
    r_ggplot2.ggsave(
        filename=file_name,
        plot=r_plot,
        device="jpeg",
        path=path,
        width=25,
        height=20,
        units="cm",
    )


def __get_r_params(params: Dict, exclude: set = None) -> Dict:
    """Returns a dictionary of parameters in R format.

    Converts each Python parameter in 'params' and converts it into an R
    parameter suitable for passing to rpy2. Returns the R parameters as a
    dictionary.

    Args:
        params: A dictionary of Python parameters, normally populated by
          calling `locals()`.

    Returns:
        A dictionary of parameters. Each parameter is in an R format suitable
        for passing to rpy2.
    """
    if exclude is None:
        exclude = set()

    r_params: Dict = {k: v for k, v in params.items() if k not in exclude}

    for key in r_params.keys():
        if r_params[key] is None:
            r_params[key] = r_NULL
        elif isinstance(r_params[key], List):
            if len(r_params[key]) > 0:
                if isinstance(r_params[key][0], str):
                    r_params[key] = StrVector(r_params[key])
                elif isinstance(r_params[key][0], float):
                    r_params[key] = FloatVector(r_params[key])
        elif isinstance(r_params[key], DataFrame):
            with conversion.localconverter(
                default_converter + pandas2ri.converter
            ):
                r_params[key] = conversion.py2rpy(r_params[key])

    return r_params


def __get_data_frame(r_data_frame: RDataFrame) -> DataFrame:
    """Converts an R format data frame into a Python format data frame.

    Converts 'r_data_frame' into a Python data frame and returns it.

    Args:
        r_data_frame: A data frame in rpy2 R format.

    Returns:
        The data frame converted into Python format.
    """
    # convert R data frame to pandas data frame
    with conversion.localconverter(pandas2ri.converter):
        data_frame: DataFrame = conversion.rpy2py(r_data_frame).fillna("")
    return data_frame


def __convert_posixt_to_r_date(r_data_frame: RDataFrame) -> RDataFrame:
    """Converts all Posix dates in a data frame, to 'Date` format.

    Converts all Posix dates in 'r_data_frame' into
    R 'Date' format and returns the updated R data frame.

    Args:
        r_data_frame: A data frame in rpy2 R format.

    Returns:
        The R data frame with all Posix dates converted into 'Date' format.
    """
    globalenv["df"] = r_data_frame
    return r(
        'data.frame(lapply(df, function(x) { if (inherits(x, "POSIXt"))'
        " as.Date(x) else x }))"
    )
