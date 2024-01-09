import typing as t

import numpy as np
import pandas as pd

from classification_model import __version__ as _version
from classification_model.configuration import core
from classification_model.processing import data_manager, new_predict_data_preparation

# =====  LOAD PIPELINES TRAINED WITH FILE NAME AND PATH OF DIRECTORY =====
pipeline_dp_file_name = (
    f"{core.config.app_config.data_preparation_pipeline_save_file}{_version}.pkl"
)
pipeline_fe_file_name = (
    f"{core.config.app_config.feature_engineering_pipeline_save_file}{_version}.pkl"
)
pipeline_te_file_name = (
    f"{core.config.app_config.training_estimator_pipeline_dir}{_version}.pkl"
)

pipe_dp = data_manager.load_pipeline(
    directory=core.DATA_PREPARATION_PIPELINE_DIR, file_name=pipeline_dp_file_name
)
pipe_fe = data_manager.load_pipeline(
    directory=core.FEATURES_ENGINEERING_PIPELINE_DIR, file_name=pipeline_fe_file_name
)
pipe_te = data_manager.load_pipeline(
    directory=core.TRAINING_ESTIMATOR_PIPELINE_DIR, file_name=pipeline_te_file_name
)


def make_prediction(*, input_data: t.Union[pd.DataFrame, dict]) -> dict:
    """Make a prediction using a saved model pipeline."""

    # check the type of variable witch will be pass in the function
    if not isinstance(input_data, pd.DataFrame):
        if not isinstance(input_data, dict):
            raise ValueError(
                "variable passed in input_data should be a DataFrame or dictionary type"
            )

    # ========== DATA SET LOADING ==========
    data = pd.DataFrame(input_data).copy()
    validated_data, errors = new_predict_data_preparation.validate_inputs(
        input_data=data
    )
    results = {
        "ml_input_data": np.array([]),
        "predictions": np.array([]),
        "version": _version,
        "errors": errors,
    }

    if not errors:
        # ========== FEATURES ASSIGNMENT ==========
        # assign features we want to have prediction
        validated_data_features = validated_data[
            core.config.mod_config.initial_features
        ]

        # ========== USING OF ANALYSIS AND EXPLORATION PIPELINE ==========
        validated_data_features_dp = pipe_dp.transform(validated_data_features)

        # ========== TARGET DATA TRANSFORMATION ==========
        # Transformation of target --> build pipeline for this step
        # validated_data_target = np.log(validated_data_target)

        # ========== USING FEATURE ENGINEERING PIPELINES ==========
        validated_data_features_fe = pipe_fe.transform(validated_data_features_dp)

        # ========== PERFORM FEATURE SELECTION TO REDUCE DATA SET ==========
        # when we want to perform feature selection
        # validated_data_fe_selected = validated_data_features_fe[
        #     core.config.mod_config.selected_features
        # ]

        # when we don't want to perform feature selection
        validated_data_features_fe_selected = validated_data_features_fe

        # ========== USING PREDICTION PIPELINES ==========
        # let's obtain the prediction
        predictions = pipe_te.predict(
            # extract data of train_features variable in data set
            # X=validated_data_fe_selected[core.config.mod_config.train_features]
            # for data comes directly from feature engineering
            X=validated_data_features_fe_selected
        )

        # ========== CAPTURE THE RESULT WE WANT ==========
        # let's put in results, all result we want from prediction
        results = {
            "ml_input_data": validated_data_features_fe_selected.values.tolist(),
            "predictions": [
                pred for pred in predictions
            ],  # [np.exp(pred) for pred in predictions],  # type: ignore
            "version": _version,
            "errors": errors,
        }

    return results
