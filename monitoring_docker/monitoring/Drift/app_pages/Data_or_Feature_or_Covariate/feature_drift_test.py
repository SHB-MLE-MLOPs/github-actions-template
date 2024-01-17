# import necessary library and modules
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import streamlit as st
from streamlit_extras.stylable_container import stylable_container

from Drift.app_pages.Data_or_Feature_or_Covariate.Statiscal_method import \
    independance_and_same_population_test
from Drift.pipelines_building import pipelines

# set a grey background (use sns.set_theme() if seaborn version 0.11.0 or above)
sns.set(style="darkgrid")
# pprint(sys.path)


def app():
    st.text("")
    st.markdown("#")
    # st.markdown('##')

    st.button("Reset", type="primary")
    if st.button("get test result"):
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
        # reference_data_frame = pd.read_csv('./building_monitoring_app/reference_data.csv')
        # new_data_frame = pd.read_csv('./building_monitoring_app/new_data.csv')

        # Split reference data into qualitative and quantitative data
        numerical_reference_data_frame = reference_data_frame.select_dtypes(
            include=[np.number]
        )
        # categorical_reference_data_frame = reference_data_frame.select_dtypes(exclude=[np.number])

        # Split new data into qualitative and quantitative data
        numerical_new_data_frame = new_data_frame.select_dtypes(include=[np.number])
        # categorical_new_data_frame = new_data_frame.select_dtypes(exclude=[np.number])

        # Get the list of numerical variable column names from reference_data and new_data
        column_numerical_reference_data = (
            numerical_reference_data_frame.columns.values.tolist()
        )
        column_numerical_new_data = numerical_new_data_frame.columns.values.tolist()

        # Test to ensure that we have the same variable in 2 data set
        if column_numerical_reference_data != column_numerical_new_data:
            raise ValueError(
                "variables or columns name in 2 data set should be the same"
            )

        # Set normality test threshold
        normality_test_threshold = 0.05

        # Set independance test threshold
        dependance_test_threshold = 0.05

        # Set variance equality threshold
        variance_equality_test_threshold = 0.05

        # Apply independance test
        ind_test_result = (
            independance_and_same_population_test.Independance_test_result(
                reference_data=reference_data_frame,
                new_data=new_data_frame,
                normality_test_threshold=normality_test_threshold,
                variance_equality_test_threshold=variance_equality_test_threshold,
            )
        )

        # Apply same population test
        same_pop_test_result = (
            independance_and_same_population_test.same_population_test_result(
                reference_data=reference_data_frame,
                new_data=new_data_frame,
                normality_test_threshold=normality_test_threshold,
                variance_equality_test_threshold=variance_equality_test_threshold,
                dependance_test_threshold=dependance_test_threshold,
            )
        )

        # Get the list of numerical and categorical variable column names
        # from reference_data and new_data in order
        column_categorical = ind_test_result[0].columns.values.tolist()
        column_numerical = ind_test_result[1].columns.values.tolist()

        # ===== SET THE CONFIGURATION OF THE INTERFACE OF DASHBOARD =====
        # all streamlit icon or emoji shortcodes supported by Streamlit can be found in this link :
        # https://streamlit-emoji-shortcodes-streamlit-app-gwckff.streamlit.app/

        # set the title of the page icon
        st.title(":bar_chart: Covariate Drift Analysis")
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
        st.markdown("#")
        # st.markdown('##')

        # Subtitle for paragraph bellow
        st.subheader("numerical data analysis")
        st.text("")
        # st.markdown('#')
        # st.markdown('##')

        # center element in columns with CSS syntax
        with stylable_container(
            key="head_box",
            css_styles=[
                """
                {
                    text-align: center;
                    box-lines: single;
                    width: fit-content;
                    block-size: fit-content;
                }
                """,
            ],
        ):
            # create 7 columns for title of each component of drift analysis
            (
                title_col_1,
                title_col_2,
                title_col_3,
                title_col_4,
                title_col_5,
                title_col_6,
                title_col_7,
            ) = st.columns([4, 5, 5, 5, 5, 6, 8])

            # printing raws of title name
            title_col_1.write(
                """
                              ##### Column
                              """
            )
            title_col_2.write(
                """
                              ##### Distribution
                              """
            )
            title_col_3.write(
                """
                              ##### Ind
                              """
            )
            title_col_4.write(
                """
                              ##### Mean
                              """
            )
            title_col_5.write(
                """
                              ##### Variance
                              """
            )
            title_col_6.write(
                """
                              ##### Data Drift
                              """
            )
            title_col_7.write(
                """
                              ##### Intensity Score (%)
                              """
            )

        for num_var in column_numerical:
            st.text("")
            # st.markdown('#')
            # st.markdown('##')

            # create 7 columns to add value of each component of drift analysis
            (
                value_col_1,
                value_col_2,
                value_col_3,
                value_col_4,
                value_col_5,
                value_col_6,
                value_col_7,
            ) = st.columns([4, 5, 5, 5, 5, 6, 8])

            # printing raws of each drift analysis component value
            with value_col_1:
                # custom streamlit html page with CSS command
                with stylable_container(
                    key="value_col1_box",
                    css_styles=[
                        """
                        {
                            margin: 0;
                            position: absolute;
                            text-align: center;
                            top: 50%;
                            -ms-transform: translateY(50%);
                            transform: translateY(0%);
                        }
                        """,
                    ],
                ):
                    # add value to column
                    st.write(num_var)

            with value_col_2:
                # creta figure to plot
                fig, ax = plt.subplots()
                sns.kdeplot(
                    numerical_reference_data_frame[num_var],
                    fill=True,
                    color="r",
                    label="referernce",
                )
                sns.kdeplot(
                    numerical_new_data_frame[num_var], fill=True, color="b", label="new"
                )
                # custom streamlit html page with CSS command
                with stylable_container(
                    key="plot_image_0",
                    css_styles=[
                        """
                        {
                            margin: auto;
                            text-align: center;
                            left: 10px;
                            top: -10px;
                            width: 100px;
                            height: 100px;
                            padding: 0px;
                        }
                        """,
                    ],
                ):
                    # add plot to column
                    st.pyplot(fig)
                    # pass

            with value_col_3:
                # custom streamlit html page with CSS command
                with stylable_container(
                    key="st_selectbox",
                    css_styles=[
                        """
                        {
                            margin: 0;
                            position: absolute;
                            text-align: center;
                            top: 50%;
                            -ms-transform: translateY(50%);
                            transform: translateY(0%);
                        }
                        """,
                    ],
                ):
                    # add value to column
                    ind_value = ind_test_result[1][num_var].loc[
                        ind_test_result[1].index[0]
                    ]
                    ind_value_format = "{:.2f}".format(ind_value)
                    st.write(ind_value_format)

            with value_col_4:
                # custom streamlit html page with CSS command
                with stylable_container(
                    key="value_col4_box",
                    css_styles=[
                        """
                        {
                            margin: 0;
                            position: absolute;
                            text-align: center;
                            top: 50%;
                            -ms-transform: translateY(50%);
                            transform: translateY(0%);
                        }
                        """,
                    ],
                ):
                    # add value to column
                    mean_value = same_pop_test_result[1][num_var].loc[
                        same_pop_test_result[1].index[0]
                    ]
                    mean_value_format = "{:.2f}".format(mean_value)
                    st.write(mean_value_format)

            with value_col_5:
                # custom streamlit html page with CSS command
                with stylable_container(
                    key="value_col5_box",
                    css_styles=[
                        """
                        {
                            margin: 0;
                            position: absolute;
                            text-align: center;
                            top: 50%;
                            -ms-transform: translateY(50%);
                            transform: translateY(0%);
                        }
                        """,
                    ],
                ):
                    # add value to column
                    var_value = same_pop_test_result[2][num_var].loc[
                        same_pop_test_result[2].index[0]
                    ]
                    var_value_format = "{:.2f}".format(var_value)
                    st.write(var_value_format)

            with value_col_6:
                # custom streamlit html page with CSS command
                with stylable_container(
                    key="value_col6_box",
                    css_styles=[
                        """
                        {
                            margin: 0;
                            position: absolute;
                            text-align: center;
                            top: 50%;
                            -ms-transform: translateY(50%);
                            transform: translateY(0%);
                        }
                        """,
                    ],
                ):
                    # add value to column
                    if mean_value > 0.05 and var_value > 0.05:
                        st.write("Not Detected")
                    else:
                        st.write("Detected")

            with value_col_7:
                # custom streamlit html page with CSS command
                with stylable_container(
                    key="value_col7_box",
                    css_styles=[
                        """
                        {
                            margin: 0;
                            position: absolute;
                            text-align: center;
                            top: 50%;
                            -ms-transform: translateY(50%);
                            transform: translateY(0%);
                        }
                        """,
                    ],
                ):
                    # add value to column
                    score_value = ((mean_value + var_value) / 2) * 100
                    score_value_format = "{:.2f}".format(score_value)

                    st.write(score_value_format)

        # make space between 2 paragraphs
        st.text("")
        st.markdown("#")
        # st.markdown('##')

        # Subtitle for paragraph bellow
        st.subheader("categorical data analysis")
        st.text("")
        # st.markdown('#')
        # st.markdown('##')

        # center element in columns with CSS syntax
        with stylable_container(
            key="head_box",
            css_styles=[
                """
                {
                    text-align: center;
                    box-lines: single;
                    width: fit-content;
                    block-size: fit-content;
                }
                """,
            ],
        ):
            # create 7 columns for title of each component of drift analysis
            (
                title_col_1,
                title_col_2,
                title_col_3,
                title_col_4,
                title_col_5,
                title_col_6,
            ) = st.columns([4, 5, 5, 5, 6, 8])

            # printing raws of title name
            title_col_1.write(
                """
                              ##### Column
                              """
            )
            title_col_2.write(
                """
                              ##### Distribution
                              """
            )
            title_col_3.write(
                """
                              ##### Ind
                              """
            )
            title_col_4.write(
                """
                              ##### Proportion
                              """
            )
            title_col_5.write(
                """
                              ##### Data Drift
                              """
            )
            title_col_6.write(
                """
                              ##### Intensity Score (%)
                              """
            )

        for cat_var in column_categorical:
            st.text("")
            # st.markdown('#')
            # st.markdown('##')

            # create 7 columns to add value of each component of drift analysis
            (
                value_col_1,
                value_col_2,
                value_col_3,
                value_col_4,
                value_col_5,
                value_col_6,
            ) = st.columns([4, 5, 5, 5, 6, 8])

            # printing raws of each drift analysis component value
            with value_col_1:
                # custom streamlit html page with CSS command
                with stylable_container(
                    key="value_col1_box",
                    css_styles=[
                        """
                        {
                            margin: 0;
                            position: absolute;
                            text-align: center;
                            top: 50%;
                            -ms-transform: translateY(50%);
                            transform: translateY(0%);
                        }
                        """,
                    ],
                ):
                    # add value to column
                    st.write(cat_var)

            with value_col_2:
                # creta figure to plot
                categorical_reference_data_plot = reference_data_frame.groupby(
                    by=cat_var
                ).size()
                categorical_new_data_plot = reference_data_frame.groupby(
                    by=cat_var
                ).size()
                fig, ax = plt.subplots()
                sns.kdeplot(
                    categorical_reference_data_plot,
                    fill=True,
                    color="r",
                    label="referernce",
                )
                sns.kdeplot(
                    categorical_new_data_plot, fill=True, color="b", label="new"
                )
                # custom streamlit html page with CSS command
                with stylable_container(
                    key="plot_image_1",
                    css_styles=[
                        """
                        {
                            margin: auto;
                            text-align: center;
                            left: 0px;
                            top: -10px;
                            width: 100px;
                            height: 100px;
                            padding: 0px;
                        }
                        """,
                    ],
                ):
                    # add plot to column
                    st.pyplot(fig)
                    # pass

            with value_col_3:
                # custom streamlit html page with CSS command
                with stylable_container(
                    key="st_selectbox",
                    css_styles=[
                        """
                        {
                            margin: 0;
                            position: absolute;
                            text-align: center;
                            top: 50%;
                            -ms-transform: translateY(50%);
                            transform: translateY(0%);
                        }
                        """,
                    ],
                ):
                    # add value to column
                    ind_value = ind_test_result[0][cat_var].loc[
                        ind_test_result[0].index[0]
                    ]
                    ind_value_format = "{:.2f}".format(ind_value)
                    st.write(ind_value_format)

            with value_col_4:
                # custom streamlit html page with CSS command
                with stylable_container(
                    key="value_col4_box",
                    css_styles=[
                        """
                        {
                            margin: 0;
                            position: absolute;
                            text-align: center;
                            top: 50%;
                            -ms-transform: translateY(50%);
                            transform: translateY(0%);
                        }
                        """,
                    ],
                ):
                    # add value to column
                    freq_value = same_pop_test_result[0][cat_var].loc[
                        same_pop_test_result[0].index[0]
                    ]
                    freq_value_format = "{:.2f}".format(freq_value)
                    st.write(freq_value_format)

            with value_col_5:
                # custom streamlit html page with CSS command
                with stylable_container(
                    key="value_col6_box",
                    css_styles=[
                        """
                        {
                            margin: 0;
                            position: absolute;
                            text-align: center;
                            top: 50%;
                            -ms-transform: translateY(50%);
                            transform: translateY(0%);
                        }
                        """,
                    ],
                ):
                    # add value to column
                    if freq_value > 0.05:
                        st.write("Not Detected")
                    else:
                        st.write("Detected")

            with value_col_6:
                # custom streamlit html page with CSS command
                with stylable_container(
                    key="value_col7_box",
                    css_styles=[
                        """
                        {
                            margin: 0;
                            position: absolute;
                            text-align: center;
                            top: 50%;
                            -ms-transform: translateY(50%);
                            transform: translateY(0%);
                        }
                        """,
                    ],
                ):
                    # add value to column
                    score_value = freq_value * 100
                    score_value_format = "{:.2f}".format(score_value)

                    st.write(score_value_format)

        # make space between 2 paragraphs
        st.text("")
        st.markdown("#")
        # st.markdown('##')

        # Subtitle for paragraph bellow
        st.subheader("numerical and categorical data relationships")
        st.text("")
        # st.markdown('#')
        # st.markdown('##')

        # center element in columns with CSS syntax
        with stylable_container(
            key="head_box",
            css_styles=[
                """
                {
                    text-align: center;
                    box-lines: single;
                    width: fit-content;
                    block-size: fit-content;
                    left: 0px;
                }
                """,
            ],
        ):
            # create 7 columns for title of each component of drift analysis
            title_col_1, title_col_2 = st.columns(2)

            # printing raws of title name
            title_col_1.write(
                """
                              ##### Independance frame
                              """
            )
            title_col_2.write(
                """
                              ##### Independance Score (%)
                              """
            )

        # create 7 columns to add value of each component of drift analysis
        value_col_1, value_col_2 = st.columns(2)

        # printing raws of each drift analysis component value
        with value_col_1:
            # custom streamlit html page with CSS command
            with stylable_container(
                key="value_col1_box",
                css_styles=[
                    """
                    {
                        margin: 0;
                        position: absolute;
                        text-align: center;
                        top: 50%;
                        -ms-transform: translateY(50%);
                        transform: translateY(0%);
                    }
                    """,
                ],
            ):
                # add value to column
                ind_frame = ind_test_result[2]
                ind_frame = np.where(
                    (
                        (ind_test_result[2] > 0.05) & (ind_test_result[3] < 0.05)
                        | (ind_test_result[2] < 0.05) & (ind_test_result[3] > 0.05)
                    ),
                    "Detected",
                    "Not Detected",
                )
                st.write(ind_frame)

        with value_col_2:
            # custom streamlit html page with CSS command
            with stylable_container(
                key="st_selectbox",
                css_styles=[
                    """
                    {
                        margin: 0;
                        position: absolute;
                        text-align: center;
                        top: 50%;
                        -ms-transform: translateY(50%);
                        transform: translateY(0%);
                    }
                    """,
                ],
            ):
                # add value to column
                ind_frame = ind_test_result[2]
                ind_frame = np.where(
                    (
                        (ind_test_result[2] > 0.05) & (ind_test_result[3] < 0.05)
                        | (ind_test_result[2] < 0.05) & (ind_test_result[3] > 0.05)
                    ),
                    (ind_test_result[2] - ind_test_result[3]) * 100,
                    (ind_test_result[2] - ind_test_result[3]) * 100,
                )
                st.write(ind_frame.round(decimals=2))
