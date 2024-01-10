import json
from typing import Any

import numpy as np
import pandas as pd
from classification_model import __version__ as model_version
from classification_model.new_prediction_with_model_trained import predict
from fastapi import APIRouter, HTTPException, Request
from fastapi.encoders import jsonable_encoder
from fastapi.responses import HTMLResponse
from loguru import logger

from building_fastapi_api import __version__, config_fastapi_api
from building_fastapi_api.schemas import \
    settings_endpoint  # , save_userdata_endpoint
from building_fastapi_api.schemas import predict_endpoint

# from building_fastapi_api.pipelines_building import pipelines

# Create a default APIRouter named root_router
root_router = APIRouter()


# To define one API GET endpoint within root_router.
@root_router.get("/")
def html_response(request: Request) -> Any:
    """Basic HTML response."""
    body = (
        "<html>"
        "<body style='padding: 10px;'>"
        "<h1>Welcome to the API</h1>"
        "<div>"
        "Check the docs: <a href='/docs'>here</a>"
        "</div>"
        "</body>"
        "</html>"
    )

    return HTMLResponse(content=body)


# Create a default APIRouter named api_router (This will be associated with our API interface)
api_router = APIRouter()


# To define one API GET endpoint within api_router.
@api_router.get(
    "/settings",
    response_model=settings_endpoint.SettingsGetEndpoint,
    status_code=200,
)
def settings() -> dict:
    """Root Get"""

    api_settings = settings_endpoint.SettingsGetEndpoint(
        name=config_fastapi_api.settings.PROJECT_NAME,
        api_version=__version__,
        model_version=model_version,
    )

    return api_settings.dict()


# to define an API POST endpoint within api_router.
@api_router.post(
    "/prediction",
    response_model=predict_endpoint.PredictionResultsPostEndpoint,
    status_code=200,
)
async def prediction(input_data: predict_endpoint.MultipleTitanicDataInputs) -> Any:
    """Make titanic survived predictions with the TID classification model"""

    # to return Python objects (dataframe here) as JSON format before sending them as responses
    # from your FastAPI endpoints
    input_df = pd.DataFrame(jsonable_encoder(input_data.inputs))

    # Advanced: You can improve performance of your API by rewriting the
    # `make prediction` function to be async and using await here.
    logger.info(f"Making prediction on inputs: {input_data.inputs}")
    results = predict.make_prediction(input_data=input_df.replace({np.nan: None}))

    if results["errors"] is not None:
        logger.warning(f"Prediction validation error: {results.get('errors')}")
        raise HTTPException(status_code=400, detail=json.loads(results["errors"]))

    logger.info(f"Prediction results: {results.get('predictions')}")

    return results


# # To define one API POST endpoint within api_router.
# @api_router.post(
#     "/persist",
#     response_model=save_userdata_endpoint.SaveUserdataGetEndpoint,
#     status_code=200,
# )
# async def save_userdata(
#     input_data: save_userdata_endpoint.MultipleTitanicAllDataInputAndOutput
# ) -> dict:
#     """Persist Get"""

#     # to return Python objects (dataframe here) as JSON format before sending them as responses
#     # from your FastAPI endpoints
#     input_df = pd.DataFrame(jsonable_encoder(input_data.inputs))
#     # Replace nan value by None in input data
#     data_to_save = input_df.replace({np.nan: None})
#     data_to_save0 = input_df.replace({np.nan: None})
#     # persist data into database (api_user_server)
#     pipe_pud = pipelines.persist_user_data_in_apiuserserver_by_Endpoint_pipe
#     pipe_pud.fit_transform(data_to_save)
#     # persist data into database (new_drift_server)
#     pipe_pud = pipelines.persist_user_data_in_newdriftserver_by_Endpoint_pipe
#     pipe_pud.fit_transform(data_to_save0)

#     api_save_userdata = save_userdata_endpoint.SaveUserdataGetEndpoint(
#         name=config_fastapi_api.settings.PROJECT_NAME,
#         api_version=__version__,
#         model_version=model_version,
#         data_row_and_columns=[
#             num for num in data_to_save.shape
#         ]
#     )

#     return api_save_userdata
