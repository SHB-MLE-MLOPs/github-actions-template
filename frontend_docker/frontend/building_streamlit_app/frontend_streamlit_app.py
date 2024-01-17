import numpy as np
import pandas as pd
import requests
import streamlit as st
from classification_model.configuration import core

# ===== SET THE CONFIGURATION OF THE INTERFACE OF DASHBOARD =====
# all streamlit icon or emoji shortcodes supported by Streamlit can be found in this link :
# https://streamlit-emoji-shortcodes-streamlit-app-gwckff.streamlit.app/

# setup of the interface of dashboard
st.set_page_config(
    page_title="A simple frontend prototyping app",
    page_icon=":bar_chart:",
    layout="wide",
)

# set the title of the page icon
st.title(":bar_chart: A simple frontend app for ML model")
# push the page icon and it's title at top of page
st.markdown(
    "<style>div.block-container{padding-top:1rem;}</style>", unsafe_allow_html=True
)


# Simple decription of app goal's
st.write(
    """This application is used as a prototyping tool for deployment of
     machine learning model in production
"""
)


# App sidebar to enter manually features
st.sidebar.header("Inlet parameter for prediction")


# Function to set sidebar of app
def user_manual_input():
    pclass_attrib = st.sidebar.slider(
        label="pclass", min_value=1, max_value=10, value=2
    )
    name_attrib = st.sidebar.selectbox(
        "name", ("Anael Amadji", "Ken Damaguo", "Mobile Phone")
    )
    sex_attrib = st.sidebar.selectbox("sex", ("female", "male"))
    age_attrib = st.sidebar.slider(label="age", min_value=18, max_value=100, value=29)
    sibsp_attrib = st.sidebar.slider(label="sibsp", min_value=1, max_value=10, value=7)
    parch_attrib = st.sidebar.slider(label="parch", min_value=1, max_value=10, value=9)
    ticket_attrib = st.sidebar.slider(
        label="ticket", min_value=1, max_value=100000, value=25897
    )
    homedest_attrib = st.sidebar.selectbox(
        "homedest", ("St Louis, MO", "Nelson Mandela, SGP", "Agoe Nyive, QNY")
    )
    cabin_attrib = st.sidebar.selectbox("cabin", ("D29 C26", "A29 F26", "Z129"))
    embarked_attrib = st.sidebar.selectbox("embarked", ("S", "O", "N"))
    boat_attrib = st.sidebar.slider(
        label="boat", min_value=1, max_value=1000, value=25478
    )
    body_attrib = st.sidebar.slider(label="body", min_value=1, max_value=10, value=6)
    fare_attrib = st.sidebar.slider(label="fare", min_value=1, max_value=10, value=3)
    data = {
        "pclass": pclass_attrib,
        "name": name_attrib,
        "sex": sex_attrib,
        "age": age_attrib,
        "sibsp": sibsp_attrib,
        "parch": parch_attrib,
        "ticket": ticket_attrib,
        "fare": fare_attrib,
        "cabin": cabin_attrib,
        "embarked": embarked_attrib,
        "boat": boat_attrib,
        "body": body_attrib,
        "homedest": homedest_attrib,
    }
    data_df = pd.DataFrame(data, index=[0])
    return data_df


# Data uploaded by user
user_upload_file = st.file_uploader(
    ":file_folder: Upload a file", type=(["csv", "txt", "xlsx", "xls"])
)


# Data recorded manually by user
user_manual_file = user_manual_input()


st.text("")
# st.markdown('#')
# st.markdown('##')


st.button("Reset", type="primary")
if st.button("Get Prediction from manual data"):
    # st.write()
    # Treatment of case when user recorded manually the features
    if user_manual_file is not None:
        # Subtitle for paragraph bellow
        st.subheader("data recorded manually and prediction")
        c1, c2 = st.columns(2)

        # Get
        user_file_df = user_manual_file

        # Get input data for api POST endpoint, replace nan in the data
        # and transform data from dataframe to dictionnary
        payload = {
            # ensure pydantic plays well with np.nan
            "inputs": user_file_df.replace({np.nan: None}).to_dict(orient="records")
        }

        # # FOR LOCAL MACHINE RUNNING
        # # Make a request to api POST endpoint
        # req_via_post = requests.post(
        #    "http://localhost:8001/api/titanic.survived.predict/v1/prediction",
        #    json=payload,
        # )

        # # FOR RUNNING WITH Dockerfile AND 2 OR MULTIPLES CONTAINERS
        # # Make a request to api endpoint POST from docker container
        # # 172.17.0.2:8001 means that we connect docker container (container where we have
        # # frontend app already running) to port 8001 exposed in API Dockerfile
        # # We connect docker container using it IP adress and it can be found
        # # with the following command "docker inspect container_ID"
        # req_via_post = requests.post(
        #    "http://172.17.0.3:8001/api/titanic.survived.predict/v1/prediction",
        #    json=payload,
        # )

        # FOR RUNNING WITH docker-compose WHEN WE SPECIFY EACH CONTAINER IP ADRESS
        req_via_post = requests.post(
            "http://192.168.1.3:8001/api/titanic.survived.predict/v1/prediction",
            json=payload,
        )

        # Make assert test to ensure that everything is going very well in request
        assert req_via_post.status_code == 200

        # Extract prediction, version and error from response of api POST endpoint
        results = req_via_post.json()

        # Make assert test for result variable
        assert results["predictions"]
        assert results["errors"] is None

        # Get result from post request
        model_input_data = results["ml_input_data"]
        pred_res = results["predictions"]
        vers_res = results["version"]
        erro_res = results["errors"]

        # Convert input data of model from list to dataframe
        model_input_data_df = pd.DataFrame(
            model_input_data, columns=core.config.mod_config.ml_input_features_for_db
        )

        # Convert prediction from list to dataframe
        pred_res_df = pd.DataFrame(pred_res, columns=[core.config.mod_config.target])

        # Concatenate of inlet feature and prediction
        feat_pred = pd.concat([user_file_df, pred_res_df], axis=1)
        db_data = pd.concat([user_file_df, model_input_data_df, pred_res_df], axis=1)

        # Get input data for api GET endpoint, replace nan in the data
        # and transform data from dataframe to dictionnary
        payload = {
            # ensure pydantic plays well with np.nan
            "inputs": db_data.replace({np.nan: None}).to_dict(orient="records")
        }

        # # FOR LOCAL MACHINE RUNNING
        # # Make a request to api POST endpoint
        # #req_via_post = requests.post(
        # #    "http://localhost:8001/api/titanic.survived.predict/v1/persist",
        # #    json=payload,
        # #)

        # ## FOR RUNNING WITH Dockerfile AND 2 OR MULTIPLES CONTAINERS
        # # Make a request to api endpoint POST from docker container
        # # 172.17.0.2:8001 means that we connect docker container (container where we have
        # # frontend app already running) to port 8001 exposed in API Dockerfile
        # # We connect docker container using it IP adress and it can be found
        # # with the following command "docker inspect container_ID"
        # req_via_post = requests.post(
        #    "http://172.17.0.3:8001/api/titanic.survived.predict/v1/persist",
        #    json=payload,
        # )

        # FOR RUNNING WITH docker-compose WHEN WE SPECIFY EACH CONTAINER IP ADRESS
        req_via_post = requests.post(
            "http://192.168.1.3:8001/api/titanic.survived.predict/v1/persist",
            json=payload,
        )

        # Make assert test to ensure that everything is going very well in request
        assert req_via_post.status_code == 200

        # Extract prediction, version and error from response of api POST endpoint
        results = req_via_post.json()

        # Make assert test for result variable
        assert results["data_row_and_columns"]
        assert len(results["data_row_and_columns"]) == 2

        # 1st printing of feature and prediction
        c1.write(user_file_df)
        c2.write(pred_res_df)

        # 2nd printing of feature and prediction
        st.write(feat_pred)

    st.text("")
    # st.markdown('#')
    # st.markdown('##')


st.button("Reset", type="secondary")
if st.button("Get Prediction from data in file uploded"):
    # st.write()
    # Treatment of case when user uploded file contains features
    if user_upload_file is not None:
        # Subtitle for paragraph bellow
        st.subheader("data from file uploded and prediction")
        c1, c2 = st.columns(2)

        # Get the name of file uploded by user and write it
        filename = user_upload_file.name
        st.write(filename)

        # Convert data uploaded by user into dataframe
        user_file_df = pd.read_csv(user_upload_file, encoding="ISO-8859-1")

        # Get input data for api POST endpoint, replace nan in the data
        # and transform data from dataframe to dictionnary
        payload = {
            # ensure pydantic plays well with np.nan
            "inputs": user_file_df.replace({np.nan: None}).to_dict(orient="records")
        }

        # # FOR LOCAL MACHINE RUNNING
        # # Make a request to api endpoint POST from your local host
        # # (localhost=127.0.0.1):8001 means that we connect localhost (where we have
        # # frontend app already running) to port 8001 exposed in Dockerfile
        # req_via_post = requests.post(
        #    "http://localhost:8001/api/titanic.survived.predict/v1/prediction",
        #    json=payload,
        # )

        # # FOR RUNNING WITH Dockerfile AND 2 OR MULTIPLES CONTAINERS
        # # Make a request to api endpoint POST from docker container
        # # 172.17.0.2:8001 means that we connect docker container (container where we have
        # # frontend app already running) to port 8001 exposed in API Dockerfile
        # # We connect docker container using it IP adress and it can be found
        # # with the following command "docker inspect container_ID"
        # req_via_post = requests.post(
        #    "http://172.17.0.3:8001/api/titanic.survived.predict/v1/prediction",
        #    json=payload,
        # )

        # FOR RUNNING WITH docker-compose WHEN WE SPECIFY EACH CONTAINER IP ADRESS
        req_via_post = requests.post(
            "http://192.168.1.3:8001/api/titanic.survived.predict/v1/prediction",
            json=payload,
        )

        # Make assert test to ensure that everything is going very well in request
        assert req_via_post.status_code == 200

        # Extract prediction, version and error from response of api POST endpoint
        results = req_via_post.json()

        # Make assert test for result variable
        assert results["predictions"]
        assert results["errors"] is None

        # Get result from post request
        model_input_data = results["ml_input_data"]
        pred_res = results["predictions"]
        vers_res = results["version"]
        erro_res = results["errors"]

        # Convert input data of model from list to dataframe
        model_input_data_df = pd.DataFrame(
            model_input_data, columns=core.config.mod_config.ml_input_features_for_db
        )

        # Convert prediction from list to dataframe
        pred_res_df = pd.DataFrame(pred_res, columns=[core.config.mod_config.target])

        # Concatenate of inlet feature and prediction
        feat_pred = pd.concat([user_file_df, pred_res_df], axis=1)
        db_data = pd.concat([user_file_df, model_input_data_df, pred_res_df], axis=1)

        # Get input data for api GET endpoint, replace nan in the data
        # and transform data from dataframe to dictionnary
        payload = {
            # ensure pydantic plays well with np.nan
            "inputs": db_data.replace({np.nan: None}).to_dict(orient="records")
        }

        # # FOR LOCAL MACHINE RUNNING
        # # Make a request to api POST endpoint
        # req_via_post = requests.post(
        #    "http://localhost:8001/api/titanic.survived.predict/v1/persist",
        #    json=payload,
        # )

        # # FOR RUNNING WITH Dockerfile AND 2 OR MULTIPLES CONTAINERS
        # # Make a request to api endpoint POST from docker container
        # # 172.17.0.2:8001 means that we connect docker container (container where we have
        # # frontend app already running) to port 8001 exposed in API Dockerfile
        # # We connect docker container using it IP adress and it can be found
        # # with the following command "docker inspect container_ID"
        # req_via_post = requests.post(
        #    "http://172.17.0.3:8001/api/titanic.survived.predict/v1/persist",
        #    json=payload,
        # )

        # FOR RUNNING WITH docker-compose WHEN WE SPECIFY EACH CONTAINER IP ADRESS
        req_via_post = requests.post(
            "http://192.168.1.3:8001/api/titanic.survived.predict/v1/persist",
            json=payload,
        )

        # Make assert test to ensure that everything is going very well for previous request
        assert req_via_post.status_code == 200

        # Extract prediction, version and error from response of api POST endpoint
        results = req_via_post.json()

        # Make assert test for result variable
        assert results["data_row_and_columns"]
        assert len(results["data_row_and_columns"]) == 2

        # 1st printing of feature and prediction
        c1.write(user_file_df)
        c2.write(pred_res_df)

        # 2nd printing of feature and prediction
        st.write(feat_pred)
