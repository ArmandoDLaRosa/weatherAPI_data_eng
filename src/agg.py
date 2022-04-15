"""
Armando De La Rosa - April,2022

This Script purpose is to run and
inject weather data agg
into influxdata.com taking advantage
on how influx deduplicates.
"""
from configparser import ConfigParser
from datetime import datetime

import pytz
import pandas as pd
from influxdb_client import InfluxDBClient, WriteOptions
from pandas import Timestamp


def logger(path: str, job_name: str, message: str, status: bool) -> None:
    """
    path     - File Path where the .txt will be stored
    job_name - Descriptive name for the main.py
    message  - Describe the logged action
    status   - Input = 1, Success
             - Input = 0, Error
    """
    current_time = datetime.now(
        pytz.timezone("America/Mexico_City")
    ).isoformat()
    with open(f"{path}aggs_logs/logs.txt", "a") as file_object:
        file_object.write(
            "\n\n\nJob Name: " + job_name + "\nDate: " + current_time + "\n"
        )

        initial_text = "Success: " if status else "Error: "
        file_object.write(initial_text + message)


def retrieve_data(my_token: str, my_org: str, my_bucket: str):
    """
    my_token - influxdata.com
    my_org - influxdata-com
    """
    with InfluxDBClient(
        url="https://us-east-1-1.aws.cloud2.influxdata.com",
        token=my_token,
        org=my_org,
    ) as client:
        # start 0, brings all available data
        # pivot, structures the influx tables into a single df
        # measurement filter, so that when I add new measures this job isn't
        # affected
        q = f""" from(bucket:"{my_bucket}") 
                |> range(start:0)
                |> filter(fn: (r) => r["_measurement"] == "weather")
                |> pivot(rowKey:["_time"], columnKey: ["_field"], 
                valueColumn: "_value") """
        df_query = client.query_api().query_data_frame(q)
        df_query.drop(
            ["table", "result", "_start", "_stop", "_measurement"],
            inplace=True,
            axis=1,
        )
        client.close()
    return df_query


def main():
    # Variables for the logger
    job_name = "influx agg"
    path = "/home/armando/Github Repos/weatherAPI_data_eng/src/"

    # Load Environment Variables
    try:
        config_object = ConfigParser(interpolation=None)
        config_object.read(f"{path}config.ini")

        influx_db = config_object["DATABASE"]
        my_token = influx_db["token"]
        my_org = influx_db["organization"]
        my_bucket = influx_db["bucket"]
        my_agg = influx_db["agg_bucket"]

        logger(path, job_name, "Env Variables Accesed", True)
    except Exception as e:
        logger(
            path,
            job_name,
            f"Env Variables Not Accessed, exit. {str(e)}",
            False,
        )
        raise e from e

    # Retrieve data stored in influx
    try:
        data_df = retrieve_data(my_token, my_org, my_bucket)
        logger(path, job_name, "Data Retrieved from influx", True)
    except Exception as e:
        logger(
            path,
            job_name,
            f"Data Retrieved from influx, exit. {str(e)}",
            False,
        )
        raise e from e

    # Calculate Aggregations
    try:
        # Create a Date Index so that we can resample the timeseries
        data_df["_time"] = pd.to_datetime(data_df["_time"])
        data_df.set_index("_time", inplace=True)
        data_df.sort_index(inplace=True)

        # For every window, we'll calculate each of the stats in the list
        aggregations_window = (
            "30Min",
            "1H",
            "3H",
            "6H",
            "12H",
            "1D",
            "7D",
            "15D",
        )
        aggregation_function = ("mean", "max", "min", "std")

        df_agg_final = pd.DataFrame()
        for window in aggregations_window:
            for function in aggregation_function:
                df_agg = (
                    data_df.groupby(
                        ("city", "country", "weather_class"), as_index=True
                    )
                    .resample(window)
                    .aggregate(function)
                )

                df_agg.drop(
                    ("city", "country", "weather_class"),
                    axis=1,
                    errors="ignore",
                    inplace=True,
                )
                df_agg["window_time"] = window
                df_agg["agg"] = function
                df_agg_final = pd.concat((df_agg_final, df_agg))

        # Get the dataframe ready for influx
        df_agg_final.reset_index(inplace=True)
        df_agg_final["_time"] = pd.to_datetime(df_agg_final["_time"])
        df_agg_final['time'] = df_agg_final['time'].dt.map(Timestamp.isoformat)
        df_agg_final.set_index("_time", inplace=True)
        logger(path, job_name, "Aggregations", True)
    except Exception as e:
        logger(path, job_name, f"Aggregations, exit. {str(e)}", False)
        raise e from e

    # Store data in influx
    try:
        url_path = "https://us-east-1-1.aws.cloud2.influxdata.com"
        with InfluxDBClient(
            url=url_path, token=my_token, org=my_org
        ) as client:
            with client.write_api(
                write_options=WriteOptions(
                    batch_size=50,
                    flush_interval=10_000,
                    jitter_interval=2_000,
                    retry_interval=5_000,
                    max_retries=5,
                    max_retry_delay=30_000,
                    exponential_base=2,
                )
            ) as write_client:
                write_client.write(
                    my_agg,
                    my_org,
                    record=df_agg_final,
                    data_frame_measurement_name="weather_aggregations",
                    data_frame_tag_columns=[
                        "window_time",
                        "agg",
                        "city",
                        "weather_class",
                        "country",
                    ],
                )
        logger(path, job_name, "Data Stored", True)
    except Exception as e:
        logger(path, job_name, f"Data not Stored, exit. {str(e)}", False)
        raise e from e


if __name__ == "__main__":
    main()
