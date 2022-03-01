from cmath import nan
from io import BytesIO
from typing import Dict, List

import PIL.Image as Image
from numpy import integer
from pandas import DataFrame
from rpy2.robjects import NULL as r_NULL
from rpy2.robjects import conversion, default_converter, packages, pandas2ri
from rpy2.robjects.vectors import StrVector


def climatic_summary(
    data: DataFrame,
    date_time: str,
    station: str = None,
    elements: List = [],
    year: str = None,
    month: str = None,
    dekad=None, #TODO add type
    pentad=None, #TODO add type
    to: str = "hourly",
    by=None, #TODO add type
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

    #  convert Python objects to R objects:
    with conversion.localconverter(default_converter + pandas2ri.converter):
        r_data = conversion.py2rpy(data)

    r_summaries = StrVector(list(summaries.values()))
    r_summaries.names = list(summaries.keys())

    station = r_NULL if station is None else station
    year = r_NULL if year is None else year
    month = r_NULL if month is None else month
    dekad = r_NULL if dekad is None else dekad
    pentad = r_NULL if pentad is None else pentad
    by = r_NULL if by is None else by
    doy = r_NULL if doy is None else doy
    na_prop = r_NULL if na_prop is None else na_prop
    na_n = r_NULL if na_n is None else na_n
    na_consec = r_NULL if na_consec is None else na_consec
    na_n_non = r_NULL if na_n_non is None else na_n_non

    # execute R function
    r_cdms_products = packages.importr("cdms.products")
    r_data_returned = r_cdms_products.climatic_summary(
        data=r_data,
        date_time=date_time,
        station=station,
        elements=StrVector(elements),
        year=year,
        month=month,
        dekad=dekad,
        pentad=pentad,
        to=to,
        by=by,
        doy=doy,
        doy_first=doy_first,
        doy_last=doy_last,
        summaries=r_summaries,
        na_rm=na_rm,
        na_prop=na_prop,
        na_n=na_n,
        na_consec=na_consec,
        na_n_non=na_n_non,
        first_date=first_date,
        n_dates=n_dates,
        last_date=last_date,
        # summaries_params: r_summaries_params, TODO convert to R type 'list of lists'
        names=names,
    )

    # convert R data frame to pandas data frame
    with conversion.localconverter(default_converter + pandas2ri.converter):
        data_returned = conversion.rpy2py(r_data_returned)

    return data_returned


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
