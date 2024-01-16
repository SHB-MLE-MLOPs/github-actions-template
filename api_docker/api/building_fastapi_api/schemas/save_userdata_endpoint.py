from typing import List, Optional

from classification_model.processing import new_predict_data_preparation
from pydantic import BaseModel


# to specify config type of elements witch will be in the setting of API,
# witch will also be the first get endpoint of api
class SaveUserdataGetEndpoint(BaseModel):
    name: str
    api_version: str
    model_version: str
    data_row_and_columns: Optional[List[float]]

    # to specify that there are no protected namespaces for class SettingsGetEndpoint,
    # which should resolve the conflict with the "model_version" field in pydantic library
    class Config:
        protected_namespaces = ()


# to specify dictionary of data the api will set or receive in order to provide prediction as result
class MultipleTitanicAllDataInputAndOutput(BaseModel):
    inputs: List[new_predict_data_preparation.TitanicAllDataInputAndOutputSchema]

    class Config:
        json_schema_extra = {
            "example": {
                "inputs": [
                    {
                        "pclass": 20,
                        "name": "Allen, Miss. Elisabeth Walton",
                        "sex": "female",
                        "age": 30,
                        "sibsp": 2,
                        "parch": 2,
                        "ticket": 24160,
                        "fare": 151.55,
                        "cabin": "C22 C26",
                        "embarked": "S",
                        "boat": 11,
                        "body": 135,
                        "homedest": "New York, NY",
                        "pclass_mi": 1.0,
                        "age_mi": 0.79,
                        "sibsp_mi": 0.0,
                        "parch_mi": 0.0,
                        "fare_mi": 0.23,
                        "age_na_mi": 0.0,
                        "fare_na_mi": 0.0,
                        "age_outliers_mi": 0.0,
                        "sibsp_outliers_mi": 0.0,
                        "parch_outliers_mi": 0.0,
                        "fare_outliers_mi": 0.0,
                        "sex_female_mi": 0.0,
                        "cabin_Rare_mi": 1.0,
                        "cabin_Missing_mi": 0.0,
                        "cabin_B_mi": 0.0,
                        "embarked_S_mi": 1.0,
                        "embarked_Q_mi": 0.0,
                        "title_Mrs_mi": 0.0,
                        "title_Miss_mi": 0.0,
                        "title_Mr_mi": 0.0,
                        "survived": 1,
                    }
                ]
            }
        }
