# import necessary packages
import numpy as np
import pandas as pd
import pingouin as pg
import scipy


# define Fisher-test function
def f_test(x, y):
    x = np.array(x)
    y = np.array(y)
    f_statistic = np.var(x, ddof=1) / np.var(y, ddof=1)  # calculate F test statistic
    dfn = x.size - 1  # define degrees of freedom numerator
    dfd = y.size - 1  # define degrees of freedom denominator
    pvalue = 1 - scipy.stats.f.cdf(
        f_statistic, dfn, dfd
    )  # find p-value of F test statistic
    return f_statistic, pvalue


# independance test between qualitative and quantitative variables
def Independance(
    *,
    data: pd.DataFrame,
    normality_test_threshold: float,
    variance_equality_test_threshold: float,
) -> pd.DataFrame:
    # test to ensure type of input data
    if not isinstance(data, pd.DataFrame):
        raise ValueError("data (data) should be a dataframe")
    if not isinstance(normality_test_threshold, float):
        raise ValueError(
            "normality threshold (normality_test_threshold) should be a float"
        )
    if not isinstance(variance_equality_test_threshold, float):
        raise ValueError(
            "variance threshold (variance_equality_test_threshold) should be a float"
        )

    # Split data into qualitative and quantitative data
    categorical_data = data.select_dtypes(exclude=[np.number])
    numerical_data = data.select_dtypes(include=[np.number])

    # Get the list of all column names from data
    column_categorical_data = categorical_data.columns.values.tolist()
    column_numerical_data = numerical_data.columns.values.tolist()

    # Creating Empty DataFrame with Column Names and empty list
    multivariate_list = []
    multivariate_lenght_list = []
    numerical_data_dict_by_catvar = {}

    # Create an empty dictionary to store dataframe
    p_value_dict_by_each_catvar = {}

    # test if variable have 2 or multiples modalities
    for cat_var in column_categorical_data:
        # test for variable wich have 2 modality
        if categorical_data[cat_var].nunique(dropna=False) == 2:
            p_value_list = []
            for num_var in column_numerical_data:
                # Normal law test
                # Kolmogoro-Smirinov
                KS_result = scipy.stats.kstest(
                    *[
                        data[num_var][data[cat_var] == category]
                        for category in data[cat_var].unique()
                    ],
                    alternative="two-sided",
                    method="auto",
                )
                # test if variable follow normal law
                if KS_result.pvalue >= normality_test_threshold:
                    # Variance equal test
                    # Fisher test for variable follow normal law
                    ft_statistic, ft_pvalue = f_test(
                        *[
                            data[num_var][data[cat_var] == category]
                            for category in data[cat_var].unique()
                        ]
                    )
                    # test if variable have same variance
                    if ft_pvalue >= variance_equality_test_threshold:
                        # perform Student Test - takes 2 positional arguments variable for test
                        tst_result = scipy.stats.ttest_ind(
                            *[
                                data[num_var][data[cat_var] == category]
                                for category in data[cat_var].unique()
                            ],
                            axis=0,
                            equal_var=True,
                            random_state=None,
                            alternative="two-sided",
                        )
                        p_value_list.append(tst_result.pvalue)
                    else:
                        # perform Welch’s t-test
                        # (equal to Student Test with parameter equal_var=False)
                        tw_result = scipy.stats.ttest_ind(
                            *[
                                data[num_var][data[cat_var] == category]
                                for category in data[cat_var].unique()
                            ],
                            axis=0,
                            equal_var=False,
                            random_state=None,
                            alternative="two-sided",
                        )
                        p_value_list.append(tw_result.pvalue)
                else:
                    # perform Mann-Whitney U test
                    tmwu_result = scipy.stats.mannwhitneyu(
                        *[
                            data[num_var][data[cat_var] == category]
                            for category in data[cat_var].unique()
                        ],
                        alternative="two-sided",
                        axis=0,
                    )
                    p_value_list.append(tmwu_result.pvalue)
            # dictionnary to persist each categorical variable with his p_value_list
            p_value_dict_by_each_catvar[cat_var] = p_value_list

        # test for variable wich have number of modality higher than 2
        elif categorical_data[cat_var].nunique(dropna=False) > 2:
            p_value_list = []
            for num_var in column_numerical_data:
                # test for variable wich have maximum 4 modality
                if categorical_data[cat_var].nunique(dropna=False) <= 4:
                    # Normal law test
                    # Kolmogoro-Smirinov
                    # test hypothesis : 2<= nombre d'échantillons <=4,
                    # n_sample>=1, n_sample1 et n_sample2 égales ou non
                    KS_result = scipy.stats.kstest(
                        *[
                            data[num_var][data[cat_var] == category]
                            for category in data[cat_var].unique()
                        ],
                        alternative="two-sided",
                        method="auto",
                    )
                    # test if variable follow normal law
                    if KS_result.pvalue >= normality_test_threshold:
                        # Perform one-way ANOVA test
                        faow_result = scipy.stats.f_oneway(
                            *[
                                data[num_var][data[cat_var] == category]
                                for category in data[cat_var].unique()
                            ]
                        )
                        p_value_list.append(faow_result.pvalue)
                    else:
                        # perform kruskal wallis test
                        tkw_result = scipy.stats.kruskal(
                            *[
                                data[num_var][data[cat_var] == category]
                                for category in data[cat_var].unique()
                            ]
                        )
                        p_value_list.append(tkw_result.pvalue)
                # test for variable wich have number of modality higher than 4
                else:
                    # Normal law test
                    # create multivariate dataset based on unique value of categorical variable
                    for uniquevar in data[cat_var].unique():
                        # Extract numerical data for the current category
                        num_data_based_on_cat = data[num_var][
                            data[cat_var] == uniquevar
                        ]
                        # save data into list in order to make pandasframe with those data saved
                        multivariate_list.append(num_data_based_on_cat.values.tolist())
                        # save data lenght into list
                        multivariate_lenght_list.append(
                            len(num_data_based_on_cat.values.tolist())
                        )
                        # save dataframe into dictionnary in order to make
                        # pandasframe with those data saved : better way
                        numerical_data_dict_by_catvar[
                            uniquevar
                        ] = num_data_based_on_cat.values.tolist()
                    # test for variable wich have equal n_sample and n_sample >= 3
                    if all(
                        n_sample >= 3 for n_sample in multivariate_lenght_list
                    ) and multivariate_lenght_list.count(
                        multivariate_lenght_list[0]
                    ) == len(multivariate_lenght_list):
                        # perform the Multivariate Normality Test
                        # This is recommand when number of categorical modality variable > 2
                        # test hypothesis : nombre d'échantillons >= 2,
                        # n_sample>=3, les n_sample de tous les échantillons sont égaux
                        mn_result = pg.multivariate_normality(
                            X=pd.DataFrame(data=numerical_data_dict_by_catvar),
                            alpha=normality_test_threshold,
                        )
                        # test if variable follow normal law
                        if mn_result.pval >= normality_test_threshold:
                            # Perform one-way ANOVA test
                            faow_result = scipy.stats.f_oneway(
                                *[
                                    data[num_var][data[cat_var] == category]
                                    for category in data[cat_var].unique()
                                ]
                            )
                            p_value_list.append(faow_result.pvalue)
                        else:
                            # perform kruskal wallis test
                            tkw_result = scipy.stats.kruskal(
                                *[
                                    data[num_var][data[cat_var] == category]
                                    for category in data[cat_var].unique()
                                ]
                            )
                            p_value_list.append(tkw_result.pvalue)
                    # test for variable wich do not have equal n_sample and n_sample >= 3
                    else:
                        if any(n_sample < 3 for n_sample in multivariate_lenght_list):
                            # print(
                            # 	"checking of dataset is needed",
                            # 	"dataset : num_var samples for a specific cat_var have n_sample "\
                            #   "< 3 for at least one categorical variable",
                            # 	"so pvalue will be set to NaN in this case"
                            # )
                            # pvalueNAN=np.NaN

                            # raise ValueError(
                            #     "checking of dataset is needed",
                            #     "dataset : num_var samples for a specific cat_var have "
                            #     "n_sample < 3 for at least one categorical variable"
                            # )
                            p_value_list.append("Check")
                        elif multivariate_lenght_list.count(
                            multivariate_lenght_list[0]
                        ) != len(multivariate_lenght_list):
                            # print(
                            # 	"checking of dataset is needed",
                            # 	"dataset : num_var samples for a specific cat_var don't equal "\
                            #   "n_sample for all categorical variable",
                            # 	"so pvalue will be set to NaN in this case"
                            # )
                            # pvalueNAN=np.NaN
                            # p_value_list.append(pvalueNAN)

                            # raise ValueError(
                            #     "checking of dataset is needed",
                            #     "dataset : num_var samples for a specific cat_var don't equal to "
                            #     "n_sample for all categorical variable"
                            # )
                            p_value_list.append("Check")

            # dictionnary to persist each categorical variable with his p_value_list
            p_value_dict_by_each_catvar[cat_var] = p_value_list

    # create final pvalue dataframe for test
    pvalue_frame = pd.DataFrame(
        data=p_value_dict_by_each_catvar, index=column_numerical_data
    )

    return pvalue_frame
