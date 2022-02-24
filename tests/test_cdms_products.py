from opencdms_process.process.rinstat import cdms_products
from pandas import read_csv


def test_climatic_summary():
    df = read_csv(
        "/home/stephen/opencdms/processes/opencdms-process/tests/data/dodoma_short_no_NA.csv",
        parse_dates=["date"],
        dayfirst=True,
    )

    actual = cdms_products.climatic_summary(
        data=df,
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
