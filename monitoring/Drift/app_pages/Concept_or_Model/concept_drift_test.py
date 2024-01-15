# import necessary libriary
import matplotlib.pyplot as mp
import numpy as np
import pandas as pd
import plotly.figure_factory as ff
import seaborn as sns
import streamlit as st

from Drift.app_pages.Concept_or_Model.Statiscal_method import \
    ML_model_performance
from Drift.pipelines_building import pipelines

# set a grey background (use sns.set_theme() if seaborn version 0.11.0 or above)
sns.set(style="darkgrid")


# cred = credentials.Certificate("pondering-5ff7c-c033cfade319.json")
# firebase_admin.initialize_app(cred)
def app():
    st.text("")
    st.markdown("#")
    # st.markdown('##')

    st.button("Reset", type="primary")
    if st.button("get test result with predicted probability"):
        # Specify reference and new data

        # Initialize reference and new data
        reference_data_frame = pd.DataFrame()
        new_data_frame = pd.DataFrame()

        # pipe_drd = pipelines.download_reference_data_pipe
        # reference_data_frame = pipe_drd.fit_transform(reference_data_frame)
        pipe_dnd = pipelines.download_new_data_pipe
        new_data_frame = pipe_dnd.fit_transform(new_data_frame)
        reference_data_frame = new_data_frame.copy().iloc[2:3]

        # # from csv file
        # reference_data_frame = pd.read_csv('./building_monitoring_app/reference_target.csv')
        # new_data_frame = pd.read_csv('./building_monitoring_app/new_target.csv')

        # predicted probability for new and reference data
        drift_threshold = 50.0

        concept_drift_detector_with_probability = (
            ML_model_performance.ConceptDriftDetector_with_PredictedProbability(
                drift_threshold=drift_threshold,
                reference_data_frame=reference_data_frame,
                new_data_frame=new_data_frame,
            )
        )

        (
            new_data_with_concept_drift_statut_frame,
            new_concept_drift_statut_list,
        ) = concept_drift_detector_with_probability.monitor_concept_drift()

        (
            plot_reference_data_frame,
            plot_new_data_frame,
            plot_drift_threshold_frame,
        ) = concept_drift_detector_with_probability.plot_performance()

        # set the title of the page icon
        st.title(":bar_chart: Concept Drift Analysis")
        # push the page icon and it's title at top of page
        st.markdown(
            "<style>div.block-container{padding-top:1rem;}</style>",
            unsafe_allow_html=True,
        )

        # Simple decription of app goal's
        st.write(
            """This application is used as a prototyping tool for deployment of
            machine learning model in production
        """
        )

        # make space between 2 paragraphs
        st.text("")
        # st.markdown('#')
        # st.markdown('##')

        # Subtitle for paragraph bellow
        # st.subheader("New data with prediction, probability prediction and concept drift status")
        st.text("")
        # st.markdown('#')
        # st.markdown('##')

        # ===== TO SEE PARTICULAR COLUMNS DATA NEDDED BY USER =====

        # create title of this section of application
        st.subheader(
            ":point_right: New data with prediction, probability and drift status"
        )

        # create a view panel for dataset
        with st.expander("Summary_Table"):
            df_sample = new_data_with_concept_drift_statut_frame
            fig = ff.create_table(df_sample, colorscale="Cividis")
            st.plotly_chart(fig, use_container_width=True)

        # ===== CREATE CHART =====
        comparison_chart_column, treshold_chart_column = st.columns((2))
        with comparison_chart_column:
            # create title of this section of application
            st.subheader("Probability comparison")

            # creta figure to plot
            fig, ax = mp.subplots()
            sns.scatterplot(
                plot_reference_data_frame,
                x="index",
                y="probability",
                # kind="scatter",
                # hue="time",
                color="r",
                label="referernce",
            )

            sns.scatterplot(
                plot_new_data_frame,
                x="index",
                y="probability",
                # kind="scatter",
                # hue="time",
                color="b",
                label="new",
            )

            # set x and y labels
            mp.xlabel("Data")
            mp.ylabel("probability")

            # add plot to column
            st.pyplot(fig)

        with treshold_chart_column:
            # create title of this section of application
            st.subheader("Probability and treshold")

            # creta figure to plot
            fig, ax = mp.subplots()
            sns.lineplot(
                data=plot_drift_threshold_frame,
                x="index",
                y="drift_threshold",
                # kind="line",
                # hue="time",
                ax=ax,
                linestyle="solid",
                linewidth=3,
                marker="*",
                markersize=5,
                color="red",
                label="threshold line",
            )

            sns.lineplot(
                data=plot_new_data_frame,
                x="index",
                y="probability",
                # kind="line",
                # hue="time",
                ax=ax,
                linestyle="dashed",
                linewidth=3,
                marker="o",
                markersize=5,
                color="blue",
                label="model preformance (probability)",
            )

            # set x and y labels
            mp.xlabel("Data")
            mp.ylabel("probability")

            # add plot to column
            st.pyplot(fig)

    st.text("")
    st.markdown("#")
    # st.markdown('##')

    st.button("Reset", type="secondary")
    if st.button("get test result with real target"):
        # Specify reference and new data

        # Initialize reference and new data
        reference_data_frame = pd.DataFrame()
        new_data_frame = pd.DataFrame()

        # pipe_drd = pipelines.download_reference_data_pipe
        # reference_data_frame = pipe_drd.fit_transform(reference_data_frame)
        pipe_dnd = pipelines.download_new_data_pipe
        new_data_frame = pipe_dnd.fit_transform(new_data_frame)
        reference_data_frame = new_data_frame.copy().iloc[2:6]

        # # from csv file
        # reference_data_frame = pd.read_csv('./building_monitoring_app/reference_target.csv')
        # new_data_frame = pd.read_csv('./building_monitoring_app/new_target.csv')

        # predicted probability for new and reference data
        drift_threshold = 50.0

        # new_true_target_list = ML_model_performance.get_true_target_from_db()
        new_true_target_list = np.random.randint(
            low=0, high=1, size=(new_data_frame.shape[0], 1)
        )

        concept_drift_detector_with_accuracy = (
            ML_model_performance.ConceptDriftDetector_with_Accuracy(
                drift_threshold=drift_threshold,
                reference_data_frame=reference_data_frame,
                new_data_frame=new_data_frame,
                target_true=new_true_target_list,
            )
        )
        (
            new_data_with_concept_drift_statut_frame,
            new_concept_drift_statut_list,
            new_concept_drift_statut_frame_to_plot,
        ) = concept_drift_detector_with_accuracy.monitor_concept_drift()

        (
            plot_target_predict_frame,
            plot_target_true_frame,
        ) = concept_drift_detector_with_accuracy.plot_performance()

        # set the title of the page icon
        st.title(":bar_chart: Concept Drift Analysis")
        # push the page icon and it's title at top of page
        st.markdown(
            "<style>div.block-container{padding-top:1rem;}</style>",
            unsafe_allow_html=True,
        )

        # Simple decription of app goal's
        st.write(
            """This application is used as a prototyping tool for deployment of
            machine learning model in production
        """
        )

        # make space between 2 paragraphs
        st.text("")
        # st.markdown('#')
        # st.markdown('##')

        # Subtitle for paragraph bellow
        # st.subheader("New data with prediction, probability prediction and concept drift status")
        st.text("")
        # st.markdown('#')
        # st.markdown('##')

        # ===== TO SEE PARTICULAR COLUMNS DATA NEDDED BY USER =====

        # create title of this section of application
        st.subheader(
            ":point_right: New data with prediction, accuracy and drift status"
        )

        # create a view panel for dataset
        with st.expander("Summary_Table"):
            df_sample = new_data_with_concept_drift_statut_frame
            fig = ff.create_table(df_sample, colorscale="Cividis")
            st.plotly_chart(fig, use_container_width=True)

        # ===== CREATE CHART =====
        comparison_chart_column, treshold_chart_column = st.columns((2))
        with comparison_chart_column:
            # create title of this section of application
            st.subheader("Target comparison")

            # creta figure to plot
            fig, ax = mp.subplots()
            sns.scatterplot(
                plot_target_predict_frame,
                x="index",
                y="target_predicted",
                # kind="scatter",
                # hue="time",
                color="red",
                label="predicted",
            )

            sns.scatterplot(
                plot_target_true_frame,
                x="index",
                y="target_true",
                # kind="scatter",
                # hue="time",
                color="blue",
                label="real",
            )

            # set x and y labels
            mp.xlabel("Data")
            mp.ylabel("probability")

            # add plot to column
            st.pyplot(fig)

        with treshold_chart_column:
            # create title of this section of application
            st.subheader("Concept drift statut")

            # 1st printing of feature and prediction
            treshold_chart_column.write(new_concept_drift_statut_frame_to_plot)

            # # creta figure to plot
            # fig, ax = mp.subplots()
            # sns.lineplot(
            #     data=plot_drift_threshold_frame, x="index", y="drift_threshold",
            #     # kind="line",
            #     # hue="time",
            #     ax=ax,
            #     linestyle="solid",
            #     linewidth=3,
            #     marker="*",
            #     markersize=5,
            #     color="red",
            #     label="threshold line"
            # )

            # sns.lineplot(
            #     data=plot_new_data_frame, x="index", y="probability",
            #     # kind="line",
            #     # hue="time",
            #     ax=ax,
            #     linestyle="dashed",
            #     linewidth=3,
            #     marker="o",
            #     markersize=5,
            #     color="blue",
            #     label="model preformance (probability)"
            # )

            # # set x and y labels
            # mp.xlabel("Data")
            # mp.ylabel("probability")

            # # add plot to column
            # st.pyplot(fig)
