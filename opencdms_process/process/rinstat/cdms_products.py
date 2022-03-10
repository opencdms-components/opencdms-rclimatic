from cmath import nan
import copy
from io import BytesIO
from typing import Dict, List, Tuple

import PIL.Image as Image
from numpy import integer
from pandas import DataFrame
from rpy2.robjects import NULL as r_NULL
from rpy2.robjects import conversion, default_converter, packages, pandas2ri, globalenv
from rpy2.robjects.vectors import StrVector
from rpy2.robjects.vectors import DataFrame as RDataFrame
from rpy2.robjects import r


r_cdms_products = packages.importr("cdms.products")


def climatic_summary(
    data: DataFrame,
    date_time: str,
    station: str = None,
    elements: List = [],
    year: str = None,
    month: str = None,
    dekad=None,  # TODO add type
    pentad=None,  # TODO add type
    to: str = "hourly",
    by=None,  # TODO add type
    doy: str = None,
    doy_first: integer = 1,
    doy_last: integer = 366,
    summaries: Dict = {"n": "dplyr::n"},
    na_rm: bool = False,
    na_prop: integer = None,
    na_n: integer = None,
    na_consec: integer = None,
    na_n_non: integer = None,
    first_date: bool = False,
    n_dates: bool = False,
    last_date: bool = False,
    summaries_params: List = [],
    names: str = "{.fn}_{.col}",
) -> DataFrame:
    """TODO 'to' parameter must be one of ("hourly", "daily", "pentad", "dekadal",
    "monthly", "annual-within-year",
    "annual", "longterm-monthly",
    "longterm-within-year", "station",
    "overall")"""

    r_params = _get_r_params(locals())
    r_data_frame: RDataFrame = r_cdms_products.climatic_summary(
        data=r_params["data"],
        date_time=r_params["date_time"],
        station=r_params["station"],
        elements=r_params["elements"],
        year=r_params["year"],
        month=r_params["month"],
        dekad=r_params["dekad"],
        pentad=r_params["pentad"],
        to=r_params["to"],
        by=r_params["by"],
        doy=r_params["doy"],
        doy_first=r_params["doy_first"],
        doy_last=r_params["doy_last"],
        summaries=r_params["summaries"],
        na_rm=r_params["na_rm"],
        na_prop=r_params["na_prop"],
        na_n=r_params["na_n"],
        na_consec=r_params["na_consec"],
        na_n_non=r_params["na_n_non"],
        first_date=r_params["first_date"],
        n_dates=r_params["n_dates"],
        last_date=r_params["last_date"],
        # summaries_params: r_summaries_params, TODO convert to R type 'list of lists'
        names=r_params["names"],
    )

    return _get_data_frame(r_data_frame)


def export_geoclim_month(
    data: DataFrame,
    year,
    month,
    element: str,
    station_id,
    latitude,
    longitude,
    metadata=None,
    join_by=None,
    add_cols=None,
    file_path: str = None,
    **kwargs
) -> str:
    # TODO if file_path is None then set it to "GEOCLIM-" + element + ".csv"
    # TODO convert `kwargs`` to R parameters
    pass


def inventory_table(
    data: DataFrame,
    date_time: str,
    elements: List,
    station: str = None,
    year: str = None,
    month: str = None,
    day: str = None,
    missing_indicator: str = "M",
    observed_indicator: str = "X",
) -> DataFrame:

    r_params = _get_r_params(locals())

    # convert any 'POSIXt' type data in the data frame to the R 'Date' type
    globalenv['df'] = r_params["data"]
    df = r('data.frame(lapply(df, function(x) { if (inherits(x, "POSIXt")) as.Date(x) else x }))')

    r_data_frame: RDataFrame = r_cdms_products.inventory_table(
        data=df,
        date_time=r_params["date_time"],
        elements=r_params["elements"],
        station=r_params["station"],
        year=r_params["year"],
        month=r_params["month"],
        day=r_params["day"],
        missing_indicator=r_params["missing_indicator"],
        observed_indicator=r_params["observed_indicator"],
    )
    return _get_data_frame(r_data_frame)


def timeseries_plot(
    path: str,
    file_name: str,
    data: DataFrame,
    date_time: str,
    elements: str,
    station: str = None,
    facet_by: str = "stations",
    type: str = "line",
    add_points: bool = False,
    add_line_of_best_fit: bool = False,
    se: bool = True,
    add_path: bool = False,
    add_step: bool = False,
    na_rm: bool = False,
    show_legend: bool = nan,
    title: str = "Timeseries Plot",
    x_title: str = None,
    y_title: str = None,
):
    # TODO ensure show_legend nan converted to R NA
    # TODO this function returns a ggplot2 object. How can we convert this into a type that is useful in Python and JS?
    # TODO `facet_by` must be one of ("stations", "elements", "stations-elements", "elements-stations", "none")
    # TODO `type` must be one of ("line", "bar")

    station = r_NULL if station is None else station
    x_title = r_NULL if x_title is None else x_title
    y_title = r_NULL if y_title is None else y_title
    with conversion.localconverter(default_converter + pandas2ri.converter):
        r_data = conversion.py2rpy(data)

    r_cdms_products = packages.importr("cdms.products")
    r_plot = r_cdms_products.timeseries_plot(
        data=r_data,
        date_time=date_time,
        elements=elements,
        station=station,
        facet_by=facet_by,
    )

    r_ggplot2 = packages.importr("ggplot2")
    r_ggplot2.ggsave(filename=file_name, plot=r_plot, device="jpeg", path=path)


def _get_r_params(params: Dict) -> Dict:
    r_params: Dict = params.copy()

    for key in r_params:
        if r_params[key] is None:
            r_params[key] = r_NULL
        elif isinstance(r_params[key], List):
            r_params[key] = StrVector(r_params[key])
        elif isinstance(r_params[key], Dict):
            names: List = list(r_params[key].keys())
            r_params[key] = StrVector(list(r_params[key].values()))
            r_params[key].names = names
        elif isinstance(r_params[key], DataFrame):
            with conversion.localconverter(default_converter + pandas2ri.converter):
                r_params[key] = conversion.py2rpy(r_params[key])

    return r_params


def _get_data_frame(r_data_frame: RDataFrame) -> DataFrame:
    # convert R data frame to pandas data frame
    with conversion.localconverter(default_converter + pandas2ri.converter):
        data_frame: DataFrame = conversion.rpy2py(r_data_frame)
    return data_frame
