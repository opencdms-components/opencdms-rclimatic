import os

import pandas
from pandas import DataFrame, read_csv

from opencdms_process.process.rinstat import cdms_products

TEST_DIR = os.path.dirname(__file__)


def test_climatic_summary():
    """# test 1000 row dataframe with no missing values
    data_file: str = os.path.join(TEST_DIR, "data", "dodoma_short_no_NA.csv")
    data = read_csv(
        data_file,
        parse_dates=["date"],
        dayfirst=True,
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
        str(actual.head())
        == "   mean_rain   sd_rain  mean_tmax   sd_tmax\n1     1.2605  6.143391    27.3309  7.297193"
    )

    # test 1000 row dataframe with missing values
    data_file: str = os.path.join(TEST_DIR, "data", "dodoma_short.csv")
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
        str(actual.head())
        == "   mean_rain   sd_rain  mean_tmax   sd_tmax\n1   1.386689  6.430281   29.13742  2.019636"
    )
    """
    """ test approx 29000 row dataframe with missing values
    """
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

    output_file_expected: str = os.path.join(
        TEST_DIR, "results_expected", "climatic_summary_expected010.csv"
    )
    # actual.to_csv(output_file_expected, index = False)
    expected_from_csv: pandas.DataFrame = read_csv(output_file_expected)

    # Writing the expected results to csv changed the column headings and index numbers.
    # So we write/read actual to/from csv, and compare the expected with that.
    output_file_actual: str = os.path.join(
        TEST_DIR, "results_actual", "climatic_summary_actual010.csv"
    )
    actual.to_csv(output_file_actual, index=False)
    actual_from_csv: pandas.DataFrame = read_csv(output_file_actual)
    diffs: DataFrame = actual_from_csv.compare(expected_from_csv)
    assert diffs.empty

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

    output_file_expected: str = os.path.join(
        TEST_DIR, "results_expected", "climatic_summary_expected020.csv"
    )
    # actual.to_csv(output_file_expected, index=False)
    expected_from_csv: pandas.DataFrame = read_csv(output_file_expected)

    output_file_actual: str = os.path.join(
        TEST_DIR, "results_actual", "climatic_summary_actual020.csv"
    )
    actual.to_csv(output_file_actual, index=False)
    actual_from_csv: pandas.DataFrame = read_csv(output_file_actual)
    diffs: DataFrame = actual_from_csv.compare(expected_from_csv)
    assert diffs.empty


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
