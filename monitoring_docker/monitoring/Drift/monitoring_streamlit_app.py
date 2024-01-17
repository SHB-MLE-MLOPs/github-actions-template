# import library to build web application
import streamlit as st
# import library to make multi pages on the web application
from streamlit_option_menu import option_menu

from Drift.app_pages.About_Drift import about_page
from Drift.app_pages.Concept_or_Model import concept_drift_test
from Drift.app_pages.Data_or_Feature_or_Covariate import feature_drift_test
from Drift.app_pages.Data_or_Target_or_Covariate import target_drift_test
from Drift.app_pages.Prior_probability_or_Target import \
    prior_probability_drift_test

# set the title of our main app page
st.set_page_config(
    page_title="Monitoring",
)


# class for create multi app pages
class MultiApp:
    # function to create a liste of app page (list witch is empty at the begening)
    def __init__(self):
        self.apps = []

    # function to add another app page
    def add_app(self, title, func):
        self.apps.append({"title": title, "function": func})

    # function to run app page
    def run(self):
        # create app sidebar where you can navigate through off pages
        # app = st.sidebar(
        with st.sidebar:
            app = option_menu(
                # set the sidebar title
                menu_title="Monitoring",
                # set the name of all page witch will be visible in the sidebar
                options=[
                    "Feature Data",
                    "ML model",
                    "Target Data",
                    "Prior Probability",
                    "about",
                ],
                # set the icon of all page witch will be visible in the sidebar
                icons=[
                    "house-fill",
                    "person-circle",
                    "trophy-fill",
                    "chat-fill",
                    "info-circle-fill",
                ],
                # set the icon of sidebar title witch will be visible in the sidebar
                menu_icon="chat-text-fill",
                default_index=1,
                styles={
                    # style and color for interior of sidebar
                    "container": {
                        "padding": "5!important",
                        "background-color": "black",
                    },
                    # style and color for icon
                    "icon": {"color": "white", "font-size": "23px"},
                    # style and color for icon don't select in sidebar when we navigate
                    "nav-link": {
                        "color": "white",
                        "font-size": "20px",
                        "text-align": "left",
                        "margin": "0px",
                        "--hover-color": "blue",
                    },
                    # style and color for selected icon in sidebar when we navigate
                    "nav-link-selected": {"background-color": "#02ab21"},
                },
            )

        # run only home app page
        if app == "Feature Data":
            # home_page.app()
            feature_drift_test.app()
        # run only test app page
        if app == "ML model":
            # test_page.app()
            concept_drift_test.app()
        # run only trending app page
        if app == "Target Data":
            # trending_page.app()
            target_drift_test.app()
        # run only your_posts app page
        if app == "Prior Probability":
            # your_posts_page.app()
            prior_probability_drift_test.app()
        # run only about app page
        if app == "about":
            about_page.app()


# run the main app page
if __name__ == "__main__":
    monitoring_app = MultiApp()
    monitoring_app.run()
