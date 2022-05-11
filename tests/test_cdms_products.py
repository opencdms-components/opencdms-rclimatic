import filecmp
import os

from pandas import DataFrame, read_csv
import pandas

from opencdms_process.process.rinstat import cdms_products

TEST_DIR = os.path.dirname(__file__)
output_path_actual: str = os.path.join(TEST_DIR, "results_actual")


def test_climatic_extremes():
    data_file: str = os.path.join(TEST_DIR, "data", "niger50.csv")
    niger50 = read_csv(
        data_file,
        parse_dates=["date"],
        dayfirst=True,
        na_values="NA",
    )

    # test that max and min are correctly calculated
    actual = cdms_products.climatic_extremes(
        data=niger50,
        date_time="date",
        year="year",
        month="month",
        to="monthly",
        station="station_name",
        elements=["tmax"],
        max_val=True,
        min_val=True,
    )
    assert __is_expected_dataframe(data=actual, file_name="climatic_extremes_actual010.csv")

    # test that Date cols are correctly calculated
    actual = cdms_products.climatic_extremes(
        data=niger50,
        date_time="date",
        year="year",
        month="month",
        to="monthly",
        station="station_name",
        elements=["tmax"],
        max_val=True,
        first_date=True,
        n_dates=True,
        last_date=True,
    )
    assert __is_expected_dataframe(data=actual, file_name="climatic_extremes_actual020.csv")


def test_climatic_missing():
    data_file: str = os.path.join(TEST_DIR, "data", "daily_niger.csv")
    daily_niger = read_csv(
        data_file,
        parse_dates=["date"],
        dayfirst=True,
        na_values="NA",
    )

    # Summarising missing data in the rainfall, temperature, and sun columns
    # climatic_missing(data = daily_niger, date_time = "date",
    #                  elements = c("rain", "tmax", "tmin", "sunh"),
    #                  station_id = "station_name")
    actual = cdms_products.climatic_missing(
        data=daily_niger,
        date_time="date",
        elements=["rain", "tmax", "tmin", "sunh"],
        station_id="station_name",
    )
    assert __is_expected_dataframe(data=actual, file_name="climatic_missing_actual010.csv")


def test_climatic_summary():
    # test approx 29000 row dataframe with missing values
    data_file: str = os.path.join(TEST_DIR, "data", "dodoma.csv")
    dodoma = read_csv(
        data_file,
        parse_dates=["date"],
        dayfirst=True,
        na_values="NA",
    )

    actual = cdms_products.climatic_summary(
        data=dodoma,
        date_time="date",
        elements=["rain", "tmax"],
        summaries={"mean": "mean", "sd": "sd"},
        na_rm=True,
        to="overall",
    )
    assert __is_expected_dataframe(data=actual, file_name="climatic_summary_actual005.csv")

    actual = cdms_products.climatic_summary(
        data=dodoma,
        date_time="date",
        elements=["rain", "tmax"],
        summaries={"mean": "mean", "sd": "sd", "n_na": "naflex::na_n"},
        na_rm=True,
        to="monthly",
    )
    assert __is_expected_dataframe(data=actual, file_name="climatic_summary_actual010.csv")

    # test approx 55000 row dataframe with missing values

    data_file: str = os.path.join(TEST_DIR, "data", "rwanda.csv")
    rwanda = read_csv(
        data_file,
        parse_dates=["date"],
        dayfirst=True,
        na_values="NA",
    )

    actual = cdms_products.climatic_summary(
        data=rwanda,
        date_time="date",
        elements=["precip", "tmp_min"],
        station="station_id",
        summaries={"mean": "mean", "sd": "sd"},
        na_prop=0,
        to="monthly",
    )
    assert __is_expected_dataframe(data=actual, file_name="climatic_summary_actual020.csv")

    # run selection of package `testhat` tests

    data_file: str = os.path.join(TEST_DIR, "data", "niger50.csv")
    niger50 = read_csv(
        data_file,
        parse_dates=["date"],
        dayfirst=True,
        na_values="NA",
    )

    actual = cdms_products.climatic_summary(
        data=niger50,
        date_time="date",
        year="year",
        month="month",
        by="station_name",
        elements=["rain"],
        station="station_name",
        to="monthly",
        summaries={"mean": "mean", "st_dv": "sd", "n_na": "naflex::na_n"},
    )
    assert __is_expected_dataframe(data=actual, file_name="climatic_summary_actual030.csv")

    # test with data used in demo

    data_file: str = os.path.join(TEST_DIR, "data", "observationFinalMinimal.csv")
    observationFinalMinimal = read_csv(
        data_file,
        parse_dates=["obsDatetime"],
        dayfirst=True,
        na_values="NA",
    )
    # climatic_summary(data = obs, date_time = "obsDatetime", station = "ï..recordedFrom", elements = "obsValue",
    #       to = "annual", summaries = c(mean = "mean", max = "max", min = "min"))
    actual = cdms_products.climatic_summary(
        data=observationFinalMinimal,
        date_time="obsDatetime",
        elements=["obsValue"],
        station="recordedFrom",
        to="annual",
        summaries={"mean": "mean", "max": "max", "min": "min"},
    )
    assert __is_expected_dataframe(data=actual, file_name="climatic_summary_actual040.csv")

    # test summaries_params
    actual = cdms_products.climatic_summary(
        data=dodoma,
        date_time="date",
        elements=["rain", "tmax"],
        summaries={"mean": "mean", "sd": "sd"},
        na_rm=True,
        to="overall",
        summaries_params={"mean": {"trim": 0.5}},
    )
    assert __is_expected_dataframe(data=actual, file_name="climatic_summary_actual050.csv")


def test_export_cdt():
    data_file: str = os.path.join(TEST_DIR, "data", "daily_summary_data.csv")
    daily_summary_data = read_csv(
        data_file,
        parse_dates=["date"],
        na_values="NA",
    )

    data_file = os.path.join(TEST_DIR, "data", "stations_niger.csv")
    stations_niger = read_csv(
        data_file,
        dayfirst=True,
        na_values="NA",
    )

    # export_cdt(data = daily_summary_data, station = "station_name",
    #            element = "sum", latitude = "lat", longitude = "long",
    #            altitude = "alt", type =  "daily", date_time = "date",
    #            metadata = stations_niger,
    #            file_path = "C:\\Users\\steph\\OneDrive\\Desktop\\FirefoxDownloads\\export_cdt_expected010.csv")
    output_file_actual: str = os.path.join(
        TEST_DIR, "results_actual", "export_cdt_actual010.csv"
    )
    cdms_products.export_cdt(
        data=daily_summary_data,
        station="station_name",
        element="sum",
        latitude="lat",
        longitude="long",
        altitude="alt",
        type="daily",
        date_time="date",
        metadata=stations_niger,
        file_path=output_file_actual,
    )
    assert __is_expected_file("export_cdt_actual010.csv")


def test_export_cdt_daily():
    pass


def test_export_cdt_dekad():
    pass


def test_export_climat_messages():
    pass


def test_export_climdex():
    pass


def test_export_geoclim():
    pass


def test_export_geoclim_dekad():
    pass


def test_export_geoclim_month():
    pass


def test_export_geoclim_pentad():
    pass


def test_histogram_plot():
    data_file: str = os.path.join(TEST_DIR, "data", "niger50.csv")
    niger50 = read_csv(
        data_file,
        parse_dates=["date"],
        dayfirst=True,
        na_values="NA",
    )

    data_file: str = os.path.join(TEST_DIR, "data", "agades.csv")
    agades = read_csv(
        data_file,
        parse_dates=["date"],
        dayfirst=True,
        na_values="NA",
    )

    # test_that("single element facet by station graphs are correct", {
    #   t1 <- histogram_plot(data = niger50, date_time = "date", elements = "tmax",
    #                         station = "station_name", facet_by = "stations")
    file_name_actual: str = "histogram_plot_actual010.jpg"
    cdms_products.histogram_plot(
        path=output_path_actual,
        file_name=file_name_actual,
        data=niger50,
        date_time="date",
        elements=["tmax"],
        station="station_name",
        facet_by="stations",
    )
    assert __is_expected_file(file_name_actual)

    # test_that("single element single station graphs are correct", {
    #   t1 <- histogram_plot(data = agades, date_time = "date", elements = "tmax",
    #                         facet_by = "none")
    file_name_actual: str = "histogram_plot_actual020.jpg"
    cdms_products.histogram_plot(
        path=output_path_actual,
        file_name=file_name_actual,
        data=agades,
        date_time="date",
        elements=["tmax"],
        facet_by="none",
    )
    assert __is_expected_file(file_name_actual)

    # test_that("single element colour by station no facet graphs are correct", {
    #   t1 <- histogram_plot(data = niger50, date_time = "date", elements = "tmax",
    #                         station = "station_name", facet_by = "none")
    file_name_actual: str = "histogram_plot_actual030.jpg"
    cdms_products.histogram_plot(
        path=output_path_actual,
        file_name=file_name_actual,
        data=niger50,
        date_time="date",
        elements=["tmax"],
        station="station_name",
        facet_by="none",
    )
    assert __is_expected_file(file_name_actual)

    # test_that("multiple element single station graphs are correct", {
    #   t1 <- histogram_plot(data = agades, date_time = "date",
    #                         elements = c("tmin", "tmax"),
    #                         facet_by = "none")
    file_name_actual: str = "histogram_plot_actual040.jpg"
    cdms_products.histogram_plot(
        path=output_path_actual,
        file_name=file_name_actual,
        data=agades,
        date_time="date",
        elements=["tmin", "tmax"],
        facet_by="none",
    )
    assert __is_expected_file(file_name_actual)

    # test_that("multiple element single station facet by elements graphs are correct", {
    #   t1 <- histogram_plot(data = agades, date_time = "date",
    #                         elements = c("tmin", "tmax"),
    #                         facet_by = "elements")
    file_name_actual: str = "histogram_plot_actual050.jpg"
    cdms_products.histogram_plot(
        path=output_path_actual,
        file_name=file_name_actual,
        data=agades,
        date_time="date",
        elements=["tmin", "tmax"],
        station="station_name",
        facet_by="elements",
    )
    assert __is_expected_file(file_name_actual)

    # test_that("multiple element & multiple stations with both as facet_by graphs are correct", {
    #   t1 <- histogram_plot(data = niger50, date_time = "date",
    #                         station = "station_name",
    #                         elements = c("tmin", "tmax"),
    #                         facet_by = "stations-elements")
    file_name_actual: str = "histogram_plot_actual060.jpg"
    cdms_products.histogram_plot(
        path=output_path_actual,
        file_name=file_name_actual,
        data=niger50,
        date_time="date",
        station="station_name",
        elements=["tmin", "tmax"],
        facet_by="stations-elements",
    )
    assert __is_expected_file(file_name_actual)

    # test_that("multiple element & multiple stations facet by elements graphs are correct", {
    #   t1 <- histogram_plot(data = niger50, date_time = "date",
    #                         station = "station_name",
    #                         elements = c("tmin", "tmax"),
    #                         facet_by = "elements")
    file_name_actual: str = "histogram_plot_actual070.jpg"
    cdms_products.histogram_plot(
        path=output_path_actual,
        file_name=file_name_actual,
        data=niger50,
        date_time="date",
        station="station_name",
        elements=["tmin", "tmax"],
        facet_by="elements",
    )
    assert __is_expected_file(file_name_actual)

    # test_that("multiple element & multiple stations facet by stations graphs are correct", {
    #   t1 <- histogram_plot(data = niger50, date_time = "date",
    #                         station = "station_name",
    #                         elements = c("tmin", "tmax"),
    #                         facet_by = "stations")
    file_name_actual: str = "histogram_plot_actual080.jpg"
    cdms_products.histogram_plot(
        path=output_path_actual,
        file_name=file_name_actual,
        data=niger50,
        date_time="date",
        station="station_name",
        elements=["tmin", "tmax"],
        facet_by="stations",
    )
    assert __is_expected_file(file_name_actual)

    # test_that("multiple element & multiple stations no facet graphs are correct", {
    #   t1 <- histogram_plot(data = niger50, date_time = "date",
    #                         station = "station_name",
    #                         elements = c("tmin", "tmax"),
    #                         facet_by = "none")
    file_name_actual: str = "histogram_plot_actual090.jpg"
    cdms_products.histogram_plot(
        path=output_path_actual,
        file_name=file_name_actual,
        data=niger50,
        date_time="date",
        station="station_name",
        elements=["tmin", "tmax"],
        facet_by="none",
    )
    assert __is_expected_file(file_name_actual)

    # TODO the 'add_*' parameters do not exist, these calls fail in Python wrapper and RStudio
    # test_that("points, LOBF, path and step are correctly added", {
    #   t1_points <- histogram_plot(data = agades, date_time = "date",
    #                                facet_by = "none",
    #                                elements = "tmin", add_points = TRUE)
    #   t1_lobf <- histogram_plot(data = agades, date_time = "date",
    #                              facet_by = "none",
    #                              elements = "tmin", add_line_of_best_fit = TRUE)
    #   t1_path <- histogram_plot(data = agades, date_time = "date",
    #                              facet_by = "none",
    #                              elements = "tmin", add_path = TRUE)
    #   t1_step <- histogram_plot(data = agades, date_time = "date",
    #                              facet_by = "none",
    #                              elements = "tmin", add_step = TRUE)

    # test_that("facet warning is displayed", {
    #   expect_warning(histogram_plot(data = niger50, date_time = "date", elements = "tmax",
    #                                  facet_by = "stations"))
    # TODO


def test_inventory_plot():
    data_file: str = os.path.join(TEST_DIR, "data", "daily_niger.csv")
    daily_niger = read_csv(
        data_file,
        parse_dates=["date"],
        dayfirst=True,
        na_values="NA",
    )

    # Create an inventory plot with two elements and by station
    file_name_actual: str = "inventory_plot_actual010.jpg"
    actual = cdms_products.inventory_plot(
        path=output_path_actual,
        file_name=file_name_actual,
        data=daily_niger,
        station="station_name",
        elements=["tmax", "tmin"],
        date_time="date",
    )
    assert __is_expected_file(file_name_actual)

    # Create an inventory plot by year and day of year
    # TODO Python plot has slightly more data than R plot
    file_name_actual: str = "inventory_plot_actual020.jpg"
    actual = cdms_products.inventory_plot(
        path=output_path_actual,
        file_name=file_name_actual,
        data=daily_niger,
        station="station_name",
        elements=["tmax", "tmin"],
        date_time="date",
        year_doy_plot=True,
    )
    assert __is_expected_file(file_name_actual)

    # Can add in rainy/dry days into the plot
    file_name_actual: str = "inventory_plot_actual030.jpg"
    actual = cdms_products.inventory_plot(
        path=output_path_actual,
        file_name=file_name_actual,
        data=daily_niger,
        station="station_name",
        elements=["tmax", "tmin"],
        date_time="date",
        rain="rain",
        display_rain_days=True,
    )
    assert __is_expected_file(file_name_actual)


def test_inventory_table():

    # test with data that has invalid format for date column, should trigger exception
    data_file: str = os.path.join(TEST_DIR, "data", "daily_niger.csv")
    daily_niger = read_csv(
        data_file,
        # parse_dates=["date"],
        dayfirst=True,
        na_values="NA",
    )

    try:
        actual = cdms_products.inventory_table(
            data=daily_niger,
            date_time="date",
            elements=["rain"],
            station="station_name",
            year="year",
            month="month",
            day="day",
        )
        assert False  # exception should have been thrown
    except Exception as err:
        actual: str = err.args[0]
        expected: str = (
            "Error in (function (data, date_time, elements, station = NULL, "
            "year = NULL,  : \n  Assertion on 'data[[date_time]]' failed: Must be of class "
            "'Date', not 'character'.\n"
        )
        assert actual == expected

    # read in correctly formatted data
    daily_niger = read_csv(
        data_file,
        parse_dates=["date"],
        dayfirst=True,
        na_values="NA",
    )

    # Functions output for one element (rain) for day
    actual = cdms_products.inventory_table(
        data=daily_niger,
        date_time="date",
        elements=["rain"],
        station="station_name",
        year="year",
        month="month",
        day="day",
    )
    assert __is_expected_dataframe(data=actual, file_name="inventory_table_actual010.csv")

    # Functions output for all elements for day
    actual = cdms_products.inventory_table(
        data=daily_niger,
        date_time="date",
        elements=["tmax", "tmin", "rain", "hmax", "hmin", "sunh", "ws", "wd"],
        station="station_name",
        year="year",
        month="month",
        day="day",
    )
    assert __is_expected_dataframe(data=actual, file_name="inventory_table_actual020.csv")

    # Functions output for one element (rain) for doy
    actual = cdms_products.inventory_table(
        data=daily_niger,
        date_time="date",
        elements=["rain"],
        station="station_name",
        year="year",
        month="month",
        day="doy",
    )
    assert __is_expected_dataframe(data=actual, file_name="inventory_table_actual030.csv")

    # Functions output for all elements for doy
    actual = cdms_products.inventory_table(
        data=daily_niger,
        date_time="date",
        elements=["tmax", "tmin", "rain", "hmax", "hmin", "sunh", "ws", "wd"],
        station="station_name",
        year="year",
        month="month",
        day="doy",
    )
    assert __is_expected_dataframe(data=actual, file_name="inventory_table_actual040.csv")


def test_output_CPT():
    data_file: str = os.path.join(TEST_DIR, "data", "yearly_niger.csv")
    yearly_niger = read_csv(
        data_file,
        dayfirst=True,
        na_values="NA",
    )

    data_file = os.path.join(TEST_DIR, "data", "stations_niger.csv")
    stations_niger = read_csv(
        data_file,
        dayfirst=True,
        na_values="NA",
    )

    # Create summary data
    # yearly_niger <- daily_niger %>% dplyr::group_by(station_name, year) %>%
    #     dplyr::summarise(mean_rain = mean(rain))
    # output_CPT(data = yearly_niger, lat_lon_data = stations_niger,
    #            station_latlondata = "station_name", latitude = "lat", longitude = "long",
    #            station = "station_name", year = "year", element = "mean_rain")
    actual = cdms_products.output_CPT(
        data=yearly_niger,
        lat_lon_data=stations_niger,
        station_latlondata="station_name",
        latitude="lat",
        longitude="long",
        station="station_name",
        year="year",
        element="mean_rain",
    )
    assert __is_expected_dataframe(data=actual, file_name="output_CPT_actual010.csv")


def test_timeseries_plot():
    data_file: str = os.path.join(TEST_DIR, "data", "niger50.csv")
    niger50 = read_csv(
        data_file,
        parse_dates=["date"],
        dayfirst=True,
        na_values="NA",
    )

    data_file: str = os.path.join(TEST_DIR, "data", "agades.csv")
    agades = read_csv(
        data_file,
        parse_dates=["date"],
        dayfirst=True,
        na_values="NA",
    )

    # test_that("single element facet by station graphs are correct", {
    #   t1 <- timeseries_plot(data = niger50, date_time = "date", elements = "tmax",
    #                    station = "station_name", facet_by = "stations")
    file_name_actual: str = "timeseries_plot_actual010.jpg"
    actual = cdms_products.timeseries_plot(
        path=output_path_actual,
        file_name=file_name_actual,
        data=niger50,
        date_time="date",
        elements=["tmax"],
        station="station_name",
        facet_by="stations",
    )
    assert __is_expected_file(file_name_actual)

    # test_that("single element single station graphs are correct", {
    #   t1 <- timeseries_plot(data = agades, date_time = "date", elements = "tmax",
    #                    facet_by = "none")
    file_name_actual: str = "timeseries_plot_actual020.jpg"
    actual = cdms_products.timeseries_plot(
        path=output_path_actual,
        file_name=file_name_actual,
        data=agades,
        date_time="date",
        elements=["tmax"],
        facet_by="none",
    )
    assert __is_expected_file(file_name_actual)

    # test_that("single element single station bar graphs are correct", {
    #   t1 <- timeseries_plot(data = agades, date_time = "date", elements = "tmax",
    #                    facet_by = "none", type = "bar")
    file_name_actual: str = "timeseries_plot_actual030.jpg"
    actual = cdms_products.timeseries_plot(
        path=output_path_actual,
        file_name=file_name_actual,
        data=agades,
        date_time="date",
        elements=["tmax"],
        facet_by="stations",
        type="bar",
    )
    assert __is_expected_file(file_name_actual)

    # test_that("single element colour by station no facet graphs are correct", {
    #   t1 <- timeseries_plot(data = niger50, date_time = "date", elements = "tmax",
    #                    station = "station_name", facet_by = "none")
    file_name_actual: str = "timeseries_plot_actual040.jpg"
    actual = cdms_products.timeseries_plot(
        path=output_path_actual,
        file_name=file_name_actual,
        data=niger50,
        date_time="date",
        elements=["tmax"],
        station="station_name",
        facet_by="none",
    )
    assert __is_expected_file(file_name_actual)

    # test_that("multiple element single station graphs are correct", {
    #   t1 <- timeseries_plot(data = agades, date_time = "date",
    #                    elements = c("tmin", "tmax"),
    #                    facet_by = "none")
    file_name_actual: str = "timeseries_plot_actual050.jpg"
    actual = cdms_products.timeseries_plot(
        path=output_path_actual,
        file_name=file_name_actual,
        data=agades,
        date_time="date",
        elements=["tmin", "tmax"],
        facet_by="none",
    )
    assert __is_expected_file(file_name_actual)

    # test_that("multiple element single station facet by elements graphs are correct", {
    #   t1 <- timeseries_plot(data = agades, date_time = "date",
    #                    elements = c("tmin", "tmax"),
    #                    facet_by = "elements")
    file_name_actual: str = "timeseries_plot_actual060.jpg"
    actual = cdms_products.timeseries_plot(
        path=output_path_actual,
        file_name=file_name_actual,
        data=agades,
        date_time="date",
        elements=["tmin", "tmax"],
        facet_by="elements",
    )
    assert __is_expected_file(file_name_actual)

    # test_that("multiple element & multiple stations with both as facet_by graphs are correct", {
    #   t1 <- timeseries_plot(data = niger50, date_time = "date",
    #                    station = "station_name",
    #                    elements = c("tmin", "tmax"),
    #                    facet_by = "stations-elements")
    file_name_actual: str = "timeseries_plot_actual070.jpg"
    actual = cdms_products.timeseries_plot(
        path=output_path_actual,
        file_name=file_name_actual,
        data=niger50,
        date_time="date",
        elements=["tmin", "tmax"],
        station="station_name",
        facet_by="stations-elements",
    )
    assert __is_expected_file(file_name_actual)

    # test_that("multiple element & multiple stations facet by elements graphs are correct", {
    #   t1 <- timeseries_plot(data = niger50, date_time = "date",
    #                    station = "station_name",
    #                    elements = c("tmin", "tmax"),
    #                    facet_by = "elements")
    file_name_actual: str = "timeseries_plot_actual080.jpg"
    actual = cdms_products.timeseries_plot(
        path=output_path_actual,
        file_name=file_name_actual,
        data=niger50,
        date_time="date",
        elements=["tmin", "tmax"],
        station="station_name",
        facet_by="elements",
    )
    assert __is_expected_file(file_name_actual)

    # test_that("multiple element & multiple stations facet by stations graphs are correct", {
    #   t1 <- timeseries_plot(data = niger50, date_time = "date",
    #                    station = "station_name",
    #                    elements = c("tmin", "tmax"),
    #                    facet_by = "stations")
    file_name_actual: str = "timeseries_plot_actual090.jpg"
    actual = cdms_products.timeseries_plot(
        path=output_path_actual,
        file_name=file_name_actual,
        data=niger50,
        date_time="date",
        elements=["tmin", "tmax"],
        station="station_name",
        facet_by="stations",
    )
    assert __is_expected_file(file_name_actual)

    # test_that("multiple element & multiple stations no facet graphs are correct", {
    #   t1 <- timeseries_plot(data = niger50, date_time = "date",
    #                    station = "station_name",
    #                    elements = c("tmin", "tmax"),
    #                    facet_by = "none")
    file_name_actual: str = "timeseries_plot_actual100.jpg"
    actual = cdms_products.timeseries_plot(
        path=output_path_actual,
        file_name=file_name_actual,
        data=niger50,
        date_time="date",
        elements=["tmin", "tmax"],
        station="station_name",
        facet_by="none",
    )
    assert __is_expected_file(file_name_actual)

    # test_that("points, LOBF, path and step are correctly added", {
    #   t1_points <- timeseries_plot(data = agades, date_time = "date",
    #                                facet_by = "none",
    #                                elements = "tmin", add_points = TRUE)
    file_name_actual: str = "timeseries_plot_actual110.jpg"
    actual = cdms_products.timeseries_plot(
        path=output_path_actual,
        file_name=file_name_actual,
        data=agades,
        date_time="date",
        elements=["tmin"],
        facet_by="none",
        add_points=True,
    )
    assert __is_expected_file(file_name_actual)

    #   t1_lobf <- timeseries_plot(data = agades, date_time = "date",
    #                              facet_by = "none",
    #                              elements = "tmin", add_line_of_best_fit = TRUE)
    file_name_actual: str = "timeseries_plot_actual120.jpg"
    actual = cdms_products.timeseries_plot(
        path=output_path_actual,
        file_name=file_name_actual,
        data=agades,
        date_time="date",
        elements=["tmin"],
        facet_by="none",
        add_line_of_best_fit=True,
    )
    assert __is_expected_file(file_name_actual)

    #   t1_path <- timeseries_plot(data = agades, date_time = "date",
    #                              facet_by = "none",
    #                              elements = "tmin", add_path = TRUE)
    file_name_actual: str = "timeseries_plot_actual130.jpg"
    actual = cdms_products.timeseries_plot(
        path=output_path_actual,
        file_name=file_name_actual,
        data=agades,
        date_time="date",
        elements=["tmin"],
        facet_by="none",
        add_path=True,
    )
    assert __is_expected_file(file_name_actual)

    #   t1_step <- timeseries_plot(data = agades, date_time = "date",
    #                              facet_by = "none",
    #                              elements = "tmin", add_step = TRUE)
    file_name_actual: str = "timeseries_plot_actual140.jpg"
    actual = cdms_products.timeseries_plot(
        path=output_path_actual,
        file_name=file_name_actual,
        data=agades,
        date_time="date",
        elements=["tmin"],
        facet_by="none",
        add_step=True,
    )
    assert __is_expected_file(file_name_actual)

    # test_that("facet warning is displayed", {
    #   expect_warning(timeseries_plot(data = niger50, date_time = "date", elements = "tmax",
    #                  facet_by = "stations"))
    file_name_actual: str = "timeseries_plot_actual150.jpg"
    actual = cdms_products.timeseries_plot(
        path=output_path_actual,
        file_name=file_name_actual,
        data=niger50,
        date_time="date",
        elements=["tmax"],
        facet_by="stations",
    )
    assert __is_expected_file(file_name_actual)


def test_windrose():
    data_file: str = os.path.join(TEST_DIR, "data", "daily_niger.csv")
    daily_niger = read_csv(
        data_file,
        parse_dates=["date"],
        dayfirst=True,
        na_values="NA",
    )

    # windrose_plot <- windrose(data = daily_niger, speed = "ws", direction = "wd",
    #                           facet_by = "station_name")
    file_name_actual: str = "windrose_actual010.jpg"
    actual = cdms_products.windrose(
        path=output_path_actual,
        file_name=file_name_actual,
        data=daily_niger,
        speed="ws",
        direction="wd",
        facet_by="station_name",
    )
    assert __is_expected_file(file_name_actual)


def __is_expected_dataframe(data: DataFrame, file_name: str) -> bool:
    output_file_actual, output_file_expected = __get_output_file_paths(file_name)

    # write the actual results to csv file, and then read the results back in again
    # Note:We read the expected results from a csv file. Writing/reading this file may change the
    #      data frame's meta data. Therefore, we must also write/read the actual results to csv so
    #      that we are comparing like with like.
    data.to_csv(output_file_actual, index=False)
    actual_from_csv: DataFrame = read_csv(output_file_actual)

    # read the expected reults from csv file
    expected_from_csv: DataFrame = read_csv(output_file_expected)

    # return if actual equals expected
    diffs: DataFrame = actual_from_csv.compare(expected_from_csv)
    return diffs.empty


def __is_expected_file(file_name: str) -> bool:
    output_file_actual, output_file_expected = __get_output_file_paths(file_name)
    return filecmp.cmp(output_file_actual, output_file_expected)


def __get_output_file_paths(file_name: str):
    output_file_actual: str = os.path.join(TEST_DIR, "results_actual", file_name)
    output_file_expected: str = os.path.join(
        TEST_DIR, "results_expected", file_name.replace("actual", "expected")
    )
    return output_file_actual, output_file_expected
