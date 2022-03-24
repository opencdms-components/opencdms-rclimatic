from cmath import nan
import copy
from io import BytesIO
from typing import Dict, List, Tuple

from numpy import integer
from pandas import DataFrame
from rpy2.robjects import NULL as r_NULL
from rpy2.robjects import conversion, default_converter, packages, pandas2ri, globalenv
from rpy2.robjects.vectors import FloatVector, ListVector, StrVector
from rpy2.robjects.vectors import DataFrame as RDataFrame
from rpy2.robjects import r


r_cdms_products = packages.importr("cdms.products")


def climatic_extremes(
    data: DataFrame,
    date_time: str,
    elements: List[str] = [],
    station:str=None,
    year: str = None,
    month: str = None,
    dekad=None,  # TODO add type
    pentad=None,  # TODO add type
    to: str = "hourly",
    by=None,  # TODO add type
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
    pass


def climatic_missing(
    data: DataFrame, 
    date_time: str, 
    elements: List[str], 
    stations:str, 
    start: bool = True, 
    end: bool = False,
) -> DataFrame:
    pass


def climatic_summary(
    data: DataFrame,
    date_time: str,
    station: str = None,
    elements: List[str] = [],
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

    r_params = _get_r_params(locals())

    names: List = list(r_params["summaries"].keys())
    r_params["summaries"] = StrVector(list(r_params["summaries"].values()))
    r_params["summaries"].names = names

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


def export_cdt(
    data: DataFrame,
    station: str,
    element: str,
    latitude: str,
    longitude: str,
    altitude: str,
    type: str = "dekad",
    date_time: str = None,
    year: str = None,
    month: str = None,
    dekad: str = None,
    metadata:DataFrame=None,
    file_path: str = None,
    *args,
    **kwargs
):
    # TODO file_path = paste0("CDT-", element, ".csv")
    pass


def export_cdt_daily(
    data: DataFrame,
    station: str,
    element: str,
    date_time: str,
    latitude: str,
    longitude: str,
    altitude: str,
    metadata: DataFrame=None,
    file_path: str = None,
    *args,
    **kwargs
):
    # TODO file_path = paste0("CDT-", element, ".csv")
    pass


def export_cdt_dekad(
    data: DataFrame,
    station: str,
    element: str,
    date_time: str,
    latitude: str,
    longitude: str,
    altitude: str,
    year: str = None,
    month: str = None,
    dekad: str = None,
    metadata: DataFrame=None,
    file_path: str = None,
    *args,
    **kwargs
):
    # TODO file_path = paste0("CDT-", element, ".csv")
    pass


def export_climat_messages(
    data: DataFrame,
    date_time: str,
    station_id:str,
    year:str=None,
    month:str=None,
    mean_pressure_station:str=None,
    mean_pressure_reduced:str=None,
    mean_temp:str=None,
    mean_max_temp:str=None,
    mean_min_temp:str=None,
    mean_vapour_pressure:str=None,
    total_precip:str=None,
    total_sunshine:str=None,
    total_snow_depth:str=None,
    max_ws:str=None,
    min_h_vis:str=None,
    folder:str = None,
):
    #TODO folder=getwd()
    pass


def export_climdex(
    data: DataFrame,
    prcp:str,
    tmax:str,
    tmin:str,
    date:str=None,
    year:str=None,
    month:str=None,
    day:str=None,
    file_type:str= "csv",
    file_path: str = None,
    *args,
    **kwargs
):
    # TODO file_path = paste0("climdex-", Sys.Date())
    pass


def export_geoclim(
    data: DataFrame,
    year:str,
    type_col:str,
    element: str,
    station_id: str,
    latitude:str,
    longitude:str,
    type: str = "dekad",
    metadata:DataFrame=None,
    join_by:List[str]=None,
    add_cols:List[str]=None,
    file_path: str = None,
    *args,
    **kwargs
):
    # TODO file_path = paste0("GEOCLIM-", element, ".csv")
    pass


def export_geoclim_dekad(
    data: DataFrame,
    year:str,
    dekad:str,
    element: str,
    station_id: str,
    latitude:str,
    longitude:str,
    metadata:DataFrame=None,
    join_by:List[str]=None,
    add_cols:List[str]=None,
    file_path: str = None,
    *args,
    **kwargs
):
    # TODO file_path = paste0("GEOCLIM-", element, ".csv")
    pass


def export_geoclim_month(
    data: DataFrame,
    year:str,
    month:str,
    element: str,
    station_id: str,
    latitude:str,
    longitude:str,
    metadata:DataFrame=None,
    join_by:List[str]=None,
    add_cols:List[str]=None,
    file_path: str = None,
    *args,
    **kwargs
):
    # TODO file_path = paste0("GEOCLIM-", element, ".csv")
    pass


def export_geoclim_pentad(
    data: DataFrame,
    year:str,
    pentad:str,
    element: str,
    station_id: str,
    latitude:str,
    longitude:str,
    metadata:DataFrame=None,
    join_by:List[str]=None,
    add_cols:List[str]=None,
    file_path: str = None,
    *args,
    **kwargs
):
    # TODO file_path = paste0("GEOCLIM-", element, ".csv")
    pass


def histogram_plot(
    data: DataFrame,
    date_time: str,
    elements: List[str],
    station:str=None,
    facet_by:str = "stations",
    position: str="identity",
    colour_bank:str=None,
    plot_type: str="histogram",
    na_rm: bool = False,
    orientation:str=None,
    show_legend:bool=None,
    width:int=None,
    facet_nrow:int=None,
    facet_ncol:int=None,
    title:str="Histogram Plot",
    x_title:str=None,
    y_title:str=None,
):
    #TODO orientation=NA,
    #TODO show_legend=NA,

    pass


def inventory_plot(
    path: str,
    file_name: str,
    data: DataFrame,
    date_time: str,
    elements: List[str] = [],
    station: str = None,
    year: str = None,
    doy: str = None,
    year_doy_plot: bool = False,
    facet_by: str = None,
    facet_x_size: int = 7,
    facet_y_size: int = 11,
    title: str = "Inventory Plot",
    plot_title_size:int=None,
    plot_title_hjust:float=0.5,
    x_title:str=None,
    y_title:str=None,
    x_scale_from:int=None,
    x_scale_to:int=None,
    x_scale_by:int=None,
    y_date_format:str=None,
    y_date_scale_by:str=None, #TODO clarify type
    y_date_scale_step:int=1,
    facet_scales: str = "fixed",
    facet_dir: str = "h",
    facet_x_margin: List[int]=None,
    facet_y_margin: List[int]=None,
    facet_nrow: int = None,
    facet_ncol: int = None,
    missing_colour: str = "red",
    present_colour: str = "grey",
    missing_label: str = "Missing",
    present_label: str = "Present",
    display_rain_days: bool = False,
    rain: str = None,
    rain_cats: Dict[str, list] = {
        "breaks": [0, 0.85, float("inf")],
        "labels": ["Dry", "Rain"],
        "key_colours": ["tan3", "blue"],
    },
    coord_flip: bool = False,
):

    r_params = _get_r_params(locals())
    r_params["data"] = _convert_posixt_to_r_date(r_params["data"])

    # TODO facet_by \code{character(1)} Whether to facet by stations, elements, or both. Options are \code{"stations"}, \code{"elements"}, \code{"station-elements"}, \code{"elements-stations"}.
    #   In \code{"station-elements"}, stations are given as rows and elements as columns. In \code{"elements-stations"}, elements are given as rows and stations as columns.

    # TODO facet_scales \code{character(1)} Are scales shared across all facets (the default, \code{"fixed"}),
    #   or do they vary across rows (\code{"free_x"}), columns (\code{"free_y"}), or both rows and columns (\code{"free"})?

    # TODO translate none null facet margin parameters to R ggplot margin types
    r_ggplot2 = packages.importr("ggplot2")
    if r_params["facet_x_margin"] == r_NULL:
        r_params["facet_x_margin"] = r_ggplot2.margin(1, 0, 1, 0)
    if r_params["facet_y_margin"] == r_NULL:
        r_params["facet_y_margin"] = r_ggplot2.margin(1, 0, 1, 0)

    # convert the dictionary of R lists, into a named R list of R lists
    #   e.g. with format like 'list(breaks = c(0, 0.85, Inf), labels = c("Dry", "Rain"), key_colours = c("tan3", "blue"))'
    r_rain_cats: Dict[str, list] = {}
    for key in rain_cats:
        # TODO add check for empty list; add check that list is all strings or all floats
        key_list: List = list(rain_cats[key])
        if isinstance(key_list[0], str):
            r_rain_cats[key] = StrVector(key_list)
        else:
            r_rain_cats[key] = FloatVector(key_list)
    r_params["rain_cats"] = ListVector(r_rain_cats)

    r_plot = r_cdms_products.inventory_plot(
        data=r_params["data"],
        date_time=r_params["date_time"],
        elements=r_params["elements"],
        station=r_params["station"],
        year=r_params["year"],
        doy=r_params["doy"],
        year_doy_plot=r_params["year_doy_plot"],
        facet_by=r_params["facet_by"],
        facet_x_size=r_params["facet_x_size"],
        facet_y_size=r_params["facet_y_size"],
        title=r_params["title"],
        plot_title_size=r_params["plot_title_size"],
        plot_title_hjust=r_params["plot_title_hjust"],
        x_title=r_params["x_title"],
        y_title=r_params["y_title"],
        x_scale_from=r_params["x_scale_from"],
        x_scale_to=r_params["x_scale_to"],
        x_scale_by=r_params["x_scale_by"],
        y_date_format=r_params["y_date_format"],
        y_date_scale_by=r_params["y_date_scale_by"],
        y_date_scale_step=r_params["y_date_scale_step"],
        facet_scales=r_params["facet_scales"],
        facet_dir=r_params["facet_dir"],
        facet_x_margin=r_params["facet_x_margin"],
        facet_y_margin=r_params["facet_y_margin"],
        facet_nrow=r_params["facet_nrow"],
        facet_ncol=r_params["facet_ncol"],
        missing_colour=r_params["missing_colour"],
        present_colour=r_params["present_colour"],
        missing_label=r_params["missing_label"],
        present_label=r_params["present_label"],
        display_rain_days=r_params["display_rain_days"],
        rain=r_params["rain"],
        rain_cats=r_params["rain_cats"],
        coord_flip=r_params["coord_flip"],
    )

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
    elements: List[str] = [],
    station: str = None,
    year: str = None,
    month: str = None,
    day: str = None,
    missing_indicator: str = "M",
    observed_indicator: str = "X",
) -> DataFrame:

    r_params = _get_r_params(locals())

    # convert any 'POSIXt' type data in the data frame to the R 'Date' type
    globalenv["df"] = r_params["data"]
    df = r(
        'data.frame(lapply(df, function(x) { if (inherits(x, "POSIXt")) as.Date(x) else x }))'
    )

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


def output_CPT(
    data: DataFrame,
    lat_lon_data: DataFrame,
    station_latlondata:str,
    latitude:str,
    longitude:str,
    station: str,
    year:str,
    element: str,
    long_data: bool = True,
    na_code:int=-999,
) -> DataFrame:
    pass


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


def windrose(
    data: DataFrame,
    speed:List[float],
    direction:List[float],
    facet_by:List[str]=None,
    n_directions:int=12,
    n_speeds:int=5,
    speed_cuts: List[float] = [],
    col_pal:str="GnBu",
    ggtheme:str="grey",
    legend_title="Wind Speed",
    calm_wind:float=0,
    variable_wind:float=990,
    n_col:int=None,
):
    # TODO speed_cuts = NA
    pass


def _get_r_params(params: Dict) -> Dict:
    r_params: Dict = params.copy()

    for key in r_params:
        if r_params[key] is None:
            r_params[key] = r_NULL
        elif isinstance(r_params[key], List):
            # TODO add support for float vectors, needed for windrose speed_cuts parameter
            r_params[key] = StrVector(r_params[key])
        # elif isinstance(r_params[key], Dict):
        # TODO replace with single line like 'x = robjects.ListVector({'a': 1, 'b': 2, 'c': 3})', see https://rpy2.github.io/doc/v3.4.x/html/vector.html#creating-vectors
        # r_params[key] = ListVector(r_params[key])

        # names: List = list(r_params[key].keys())
        # r_params[key] = StrVector(list(r_params[key].values()))
        # r_params[key].names = names
        elif isinstance(r_params[key], DataFrame):
            with conversion.localconverter(default_converter + pandas2ri.converter):
                r_params[key] = conversion.py2rpy(r_params[key])

    return r_params


def _get_data_frame(r_data_frame: RDataFrame) -> DataFrame:
    # convert R data frame to pandas data frame
    with conversion.localconverter(default_converter + pandas2ri.converter):
        data_frame: DataFrame = conversion.rpy2py(r_data_frame)
    return data_frame


def _convert_posixt_to_r_date(r_data):
    globalenv["df"] = r_data
    return r(
        'data.frame(lapply(df, function(x) { if (inherits(x, "POSIXt")) as.Date(x) else x }))'
    )
