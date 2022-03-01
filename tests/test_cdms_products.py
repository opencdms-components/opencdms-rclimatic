import os

import pandas
from pandas import DataFrame, read_csv

from opencdms_process.process.rinstat import cdms_products

TEST_DIR = os.path.dirname(__file__)


def test_climatic_summary():
    """test approx 29000 row dataframe with missing values"""
    data_file: str = os.path.join(TEST_DIR, "data", "dodoma.csv")
    data = read_csv(
        data_file,
        parse_dates=["date"],
        dayfirst=True,
        na_values="NA",
    )

    actual = cdms_products.climatic_summary(
        data=data,
        date_time="date",
        elements=["rain", "tmax"],
        summaries={"mean": "mean", "sd": "sd"},
        na_rm=True,
        to="overall",
    )
    assert (
        str(actual.head()) == "   mean_rain   sd_rain  mean_tmax   sd_tmax\n"
        "1   1.574531  6.960521  28.942301  2.188736"
    )

    actual = cdms_products.climatic_summary(
        data=data,
        date_time="date",
        elements=["rain", "tmax"],
        summaries={"mean": "mean", "sd": "sd", "n_na": "naflex::na_n"},
        na_rm=True,
        to="monthly",
    )
    assert __is_expected_csv(data=actual, file_name="climatic_summary_actual010.csv")

    """ test approx 55000 row dataframe with missing values
    """
    data_file: str = os.path.join(TEST_DIR, "data", "rwanda.csv")
    data = read_csv(
        data_file,
        parse_dates=["date"],
        dayfirst=True,
        na_values="NA",
    )

    actual = cdms_products.climatic_summary(
        data=data,
        date_time="date",
        elements=["precip", "tmp_min"],
        station="station_id",
        summaries={"mean": "mean", "sd": "sd"},
        na_prop=0,
        to="monthly",
    )
    assert __is_expected_csv(data=actual, file_name="climatic_summary_actual020.csv")

    """ run selection of package `testhat` tests
    """
    data_file: str = os.path.join(TEST_DIR, "data", "niger50.csv")
    data = read_csv(
        data_file,
        parse_dates=["date"],
        dayfirst=True,
        na_values="NA",
    )

    actual = cdms_products.climatic_summary(
        data=data,
        date_time="date",
        year="year",
        month="month",
        by="station_name",
        elements=["rain"],
        station="station_name",
        to="monthly",
        summaries={"mean": "mean", "st_dv": "sd", "n_na": "naflex::na_n"},
    )
    assert __is_expected_csv(data=actual, file_name="climatic_summary_actual030.csv")


def test_timeseries_plot():
    data_file: str = os.path.join(TEST_DIR, "data", "niger50.csv")
    data = read_csv(
        data_file,
        parse_dates=["date"],
        dayfirst=True,
        na_values="NA",
    )

    output_path_actual: str = os.path.join(TEST_DIR, "results_actual", "")

    actual = cdms_products.timeseries_plot(
        path=output_path_actual,
        file_name="timeseries_plot_actual010.jpg",
        data=data,
        date_time="date",
        elements="tmax",
        station="station_name",
        facet_by="stations",
    )


def __is_expected_csv(data: DataFrame, file_name: str) -> bool:

    # write the actual results to csv file, and then read the results back in again
    # Note:We read the expected results from a csv file. Writing/reading this file may change the
    #      data frame's meta data. Therefore, we must also write/read the actual results to csv so
    #      that we are comparing like with like.
    output_file_actual: str = os.path.join(TEST_DIR, "results_actual", file_name)
    data.to_csv(output_file_actual, index=False)
    actual_from_csv: DataFrame = read_csv(output_file_actual)

    # read the expected reults from csv file
    output_file_expected: str = os.path.join(
        TEST_DIR, "results_expected", file_name.replace("actual", "expected")
    )
    expected_from_csv: DataFrame = read_csv(output_file_expected)

    # return if actual equals expected
    diffs: DataFrame = actual_from_csv.compare(expected_from_csv)
    return diffs.empty
