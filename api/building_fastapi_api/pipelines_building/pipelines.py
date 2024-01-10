from sklearn.pipeline import Pipeline

# from classification_model.configuration import core
from building_fastapi_api.processing import house_preprocessors_v1 as h_pp

# set up the pipeline
# using Feature-engine open source Library for building transformers

# ===== BUILDING PIPELINES TO PERSIST USER DATA =====
persist_user_data_pipe = Pipeline(
    [
        # == SAVE USER DATA AND PREDICTION INTO MYSQL DATA BASE  ====
        (
            "Save User data into MySQL data base",
            h_pp.SaveIntoMySQLDatabase(
                schema_name="user_data",
                table_name="data_conserve",
                db_host="192.168.1.7",
                user="root",
                password="root_password",
            ),
        ),
    ]
)


persist_user_data_in_apiuserserver_by_Endpoint_pipe = Pipeline(
    [
        # == SAVE USER DATA AND PREDICTION INTO MYSQL DATA BASE  ====
        (
            "Save User data into MySQL data base",
            h_pp.SaveIntoMySQLDatabasebyEndpoint(
                schema_name="db_for_api_user",
                table_name="data_from_tsp_model",
                db_host="192.168.1.7",
                user="root",
                password="root_password",
            ),
        ),
    ]
)


persist_user_data_in_newdriftserver_by_Endpoint_pipe = Pipeline(
    [
        # == SAVE USER DATA AND PREDICTION INTO MYSQL DATA BASE  ====
        (
            "Save User data into MySQL data base",
            h_pp.SaveIntoMySQLDatabasebyEndpoint(
                schema_name="db_for_new_driftanalysis",
                table_name="data_from_tsp_model",
                db_host="192.168.1.9",
                user="root",
                password="root_password",
            ),
        ),
    ]
)
