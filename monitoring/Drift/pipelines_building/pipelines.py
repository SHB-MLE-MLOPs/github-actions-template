# import necessary library or module
from processing import house_preprocessors_v1 as h_pp
from sklearn.pipeline import Pipeline

# set up the pipeline
# using Feature-engine open source Library for building transformers
n_sample_to_fetch = 5

# ===== BUILDING PIPELINES TO PERSIST USER DATA =====
# download reference data
download_reference_data_pipe = Pipeline(
    [
        # == SAVE USER DATA AND PREDICTION INTO MYSQL DATA BASE  ====
        (
            "Fetch data from MySQL data base",
            h_pp.ExtractDataFromMySQLDatabase(
                size=n_sample_to_fetch,
                schema_name="db_for_ref_driftanalysis",
                table_name="data_no_drift",
                db_host="192.168.1.8",
                user="root",
                password="root_password",
            ),
        ),
    ]
)

# download new data
download_new_data_pipe = Pipeline(
    [
        # == SAVE USER DATA AND PREDICTION INTO MYSQL DATA BASE  ====
        (
            "Fetch data from MySQL data base",
            h_pp.ExtractDataFromMySQLDatabase(
                size=n_sample_to_fetch,
                schema_name="db_for_new_driftanalysis",
                table_name="data_from_tsp_model",
                db_host="192.168.1.9",
                user="root",
                password="root_password",
            ),
        ),
    ]
)

# save into reference database : for data wich not drift after drift analysis
save_into_reference_db_pipe = Pipeline(
    [
        # == SAVE USER DATA AND PREDICTION INTO MYSQL DATA BASE  ====
        (
            "Save User data into MySQL data base",
            h_pp.SaveIntoMySQLDatabasebyEndpoint(
                schema_name="db_for_ref_driftanalysis",
                table_name="data_no_drift",
                db_host="192.168.1.8",
                user="root",
                password="root_password",
            ),
        ),
    ]
)

# save into retrain database : data to use to retrain model after drift analysis
save_into_retrain_db__pipe = Pipeline(
    [
        # == SAVE USER DATA AND PREDICTION INTO MYSQL DATA BASE  ====
        (
            "Save User data into MySQL data base",
            h_pp.SaveIntoMySQLDatabasebyEndpoint(
                schema_name="db_for_retrain_mlmodel",
                table_name="data_drift",
                db_host="192.168.1.6",
                user="root",
                password="root_password",
            ),
        ),
    ]
)


# download real target data
download_real_data_pipe = Pipeline(
    [
        # == SAVE USER DATA AND PREDICTION INTO MYSQL DATA BASE  ====
        (
            "Save User data into MySQL data base",
            h_pp.ExtractDataFromMySQLDatabase(
                size=n_sample_to_fetch,
                schema_name="db_for_new_driftanalysis",
                table_name="data_from_tsp_model",
                db_host="192.168.1.9",
                user="root",
                password="root_password",
            ),
        ),
    ]
)
