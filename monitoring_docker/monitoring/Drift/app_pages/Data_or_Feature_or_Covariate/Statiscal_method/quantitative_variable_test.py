# import necessary packages
import numpy as np
import pandas as pd
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


# A Z-test for reduced deviation (also known as Z-test for skewness or Z-test for asymmetry) is
# a statistical test used to assess whether the skewness of a sample is significantly different
# from that of a normal distribution
def z_test_for_skewness(data1, data2):
    # Calculate skewness of the datasets
    skewness1 = scipy.stats.skew(data1)
    skewness2 = scipy.stats.skew(data2)

    # Calculate standard errors of skewness
    se_skewness1 = np.sqrt(6 / len(data1))
    se_skewness2 = np.sqrt(6 / len(data2))

    # Calculate Z-score for the difference in skewness
    z_score = (skewness1 - skewness2) / np.sqrt(se_skewness1**2 + se_skewness2**2)

    # Calculate p-value
    p_value = 2 * scipy.stats.norm.cdf(-np.abs(z_score))

    return z_score, p_value


def z_test_for_matched_samples(data1, data2):
    # Calculate the differences between matched pairs
    differences = data1 - data2

    # Calculate the mean and standard deviation of the differences
    mean_diff = np.mean(differences)
    std_diff = np.std(differences, ddof=1)

    # Calculate the standard error of the mean difference
    se_mean_diff = std_diff / np.sqrt(len(differences))

    # Perform the Z-test
    z_score = mean_diff / se_mean_diff

    # Calculate p-value
    p_value = 2 * scipy.stats.norm.cdf(-np.abs(z_score))

    return z_score, p_value


# independance test between 2 quantitative variables
def Independance(
    *,
    reference_data: pd.DataFrame,
    new_data: pd.DataFrame,
    normality_test_threshold: float,
) -> pd.DataFrame:
    # test to ensure type of input data
    if not isinstance(reference_data, pd.DataFrame):
        raise ValueError("reference data (reference_data) should be a dataframe")
    if not isinstance(new_data, pd.DataFrame):
        raise ValueError("new data (new_data) should be a dataframe")

    # Get the list of all column names from reference_data and new_data
    column_reference_data = reference_data.columns.values.tolist()
    column_new_data = new_data.columns.values.tolist()

    # Test to ensure that we have the same variable in 2 data set
    if column_reference_data != column_new_data:
        raise ValueError(
            "variable in 2 data set should be the same for independance test"
        )

    # Creating Empty DataFrame with Column Names and empty list
    p_value_list = []

    for var in column_reference_data:
        # Normal law test
        # Kolmogoro-Smirinov
        KS_result = scipy.stats.ks_2samp(
            data1=reference_data[var],
            data2=new_data[var],
            alternative="two-sided",
            method="auto",
        )

        # Lilliefors
        # reference_ksstat, reference_pvalue = sm.stats.diagnostic.lilliefors(reference_data[var])
        # new_ksstat, new_pvalue  = sm.stats.diagnostic.lilliefors(new_data[var])

        # if (
        #     reference_pvalue >= normality_test_threshold and  \
        #     new_pvalue >= normality_test_threshold
        # ):
        if KS_result.pvalue >= normality_test_threshold:
            # variable do not follow normal law or we do not know the law
            if reference_data.shape[0] == new_data.shape[0]:
                # Bravais-Pearson correlation test works very well for
                # 2 variables wich have the same size
                pr_result = scipy.stats.pearsonr(
                    reference_data[var],
                    new_data[var],
                    alternative="two-sided",
                    method=None,
                )
                p_value_list.append(pr_result.pvalue)
            else:
                # Covariance matrix method to calculate the correlation
                # create new columns name for reference and new data
                ref_var = var + "_ref"
                new_var = var + "_new"
                # create new dataframe with new columns name
                ref_frame_concat = pd.DataFrame(
                    reference_data[var].values.tolist(), columns=[ref_var]
                )
                new_frame_concat = pd.DataFrame(
                    new_data[var].values.tolist(), columns=[new_var]
                )
                # concatenate new dataframe horizontaly
                reference_and_new_frame = pd.concat(
                    [ref_frame_concat, new_frame_concat], axis=1
                )
                # Calculate the correlation matrix
                cor_matrix_frame = reference_and_new_frame.corr()
                # append pvalue obtained into plist value
                p_value_list.append(cor_matrix_frame.loc[ref_var][new_var])
        # variable we do not know the law, we perform non-parametric test like Spearman rs
        else:
            if reference_data.shape[0] == new_data.shape[0]:
                sr_result = scipy.stats.spearmanr(
                    reference_data[var],
                    new_data[var],
                    axis=0,
                    nan_policy="propagate",
                    alternative="two-sided",
                )
                p_value_list.append(sr_result.pvalue)
            else:
                # Covariance matrix method to calculate the correlation
                # create new columns name for reference and new data
                ref_var = var + "_ref"
                new_var = var + "_new"
                # create new dataframe with new columns name
                ref_frame_concat = pd.DataFrame(
                    reference_data[var].values.tolist(), columns=[ref_var]
                )
                new_frame_concat = pd.DataFrame(
                    new_data[var].values.tolist(), columns=[new_var]
                )
                # concatenate new dataframe horizontaly
                reference_and_new_frame = pd.concat(
                    [ref_frame_concat, new_frame_concat], axis=1
                )
                # Calculate the correlation matrix
                cor_matrix_frame = reference_and_new_frame.corr()
                # append pvalue obtained into plist value
                p_value_list.append(cor_matrix_frame.loc[ref_var][new_var])

    # Using append to add the p_value_list to p_value_frame
    p_value_frame = pd.DataFrame([p_value_list], columns=column_reference_data)

    return p_value_frame


# variance test between 2 quantitative variables
def variance(
    *,
    reference_data: pd.DataFrame,
    new_data: pd.DataFrame,
    ind_test_pvalue: pd.DataFrame,
    dependance_test_threshold: float,
    normality_test_threshold: float,
) -> pd.DataFrame:
    # test to ensure type of input data
    if not isinstance(reference_data, pd.DataFrame):
        raise ValueError("reference data (reference_data) should be a dataframe")
    if not isinstance(new_data, pd.DataFrame):
        raise ValueError("new data (new_data) should be a dataframe")
    if not isinstance(dependance_test_threshold, float):
        raise ValueError(
            "dependance threshold (dependance_test_threshold) should be a float"
        )

    # Get the list of all column names from reference_data and new_data
    column_reference_data = reference_data.columns.values.tolist()
    column_new_data = new_data.columns.values.tolist()

    # Test to ensure that we have the same variable in 2 data set
    if column_reference_data != column_new_data:
        raise ValueError(
            "variable in 2 data set should be the same for population appartenance test"
        )

    p_value_list = []
    pvalue_c = ind_test_pvalue.copy()

    for var in column_reference_data:
        # Test dependance of each variable
        if pvalue_c[var].tolist()[0] > dependance_test_threshold:
            # variables are independant
            # Normal law test
            # Kolmogoro-Smirinov
            KS_result = scipy.stats.ks_2samp(
                data1=reference_data[var],
                data2=new_data[var],
                alternative="two-sided",
                method="auto",
            )
            if KS_result.pvalue >= normality_test_threshold:
                # variables wich follow normal law
                # Variance equal test
                # Fisher test for variable follow normal law
                ft_statistic, ft_pvalue = f_test(x=reference_data[var], y=new_data[var])
                p_value_list.append(ft_pvalue)
            else:
                # variables do not follow normal law or we do not know the law
                # Variance equal test
                # Barlett test for variable we don't know probability law.
                # you can make this test for any number of variable
                bar_result = scipy.stats.bartlett(
                    data1=reference_data[var], data2=new_data[var]
                )
                # # Levene test for variable we don't know probability law.
                # you can make this test for any number of variable
                # lev_result = scipy.stats.levene(
                # 	data1=reference_data[var],
                #     data2=new_data[var],
                # 	center='median',
                # 	proportiontocut=0.05
                # )
                p_value_list.append(bar_result.pvalue)
        else:
            # variables are not independant
            # Normal law test
            # Kolmogoro-Smirinov
            KS_result = scipy.stats.ks_2samp(
                data1=reference_data[var],
                data2=new_data[var],
                alternative="two-sided",
                method="auto",
            )
            if KS_result.pvalue >= normality_test_threshold:
                # variables wich follow normal law
                # Variance equal test
                # Fisher test for variable follow normal law
                ft_statistic, ft_pvalue = f_test(x=reference_data[var], y=new_data[var])
                p_value_list.append(ft_pvalue)
            else:
                # variables do not follow normal law or we do not know the law
                # Variance equal test
                # Barlett test for variable we don't know probability law.
                # you can make this test for any number of variable
                bar_result = scipy.stats.bartlett(
                    data1=reference_data[var], data2=new_data[var]
                )
                # # Levene test for variable we don't know probability law.
                # # you can make this test for any number of variable
                # lev_result = scipy.stats.levene(
                # 	data1=reference_data[var],
                #     data2=new_data[var],
                # 	center='median',
                # 	proportiontocut=0.05
                # )
                p_value_list.append(bar_result.pvalue)

    # Using append to add the p_value_list to p_value_frame
    pvalue_frame = pd.DataFrame([p_value_list], columns=column_reference_data)

    return pvalue_frame


# mean test between 2 quantitative variables
def average_mean(
    *,
    reference_data: pd.DataFrame,
    new_data: pd.DataFrame,
    ind_test_pvalue: pd.DataFrame,
    dependance_test_threshold: float,
    normality_test_threshold: float,
    variance_equal_test_threshold: float,
) -> pd.DataFrame:
    # test to ensure type of input data
    if not isinstance(reference_data, pd.DataFrame):
        raise ValueError("reference data (reference_data) should be a dataframe")
    if not isinstance(new_data, pd.DataFrame):
        raise ValueError("new data (new_data) should be a dataframe")
    if not isinstance(dependance_test_threshold, float):
        raise ValueError(
            "dependance threshold (dependance_test_threshold) should be a float"
        )

    # Get the list of all column names from reference_data and new_data
    column_reference_data = reference_data.columns.values.tolist()
    column_new_data = new_data.columns.values.tolist()

    # Test to ensure that we have the same variable in 2 data set
    if column_reference_data != column_new_data:
        raise ValueError(
            "variable in 2 data set should be the same for population appartenance test"
        )

    p_value_list = []
    pvalue_c = ind_test_pvalue.copy()

    for var in column_reference_data:
        # Test dependance of each variable
        if pvalue_c[var].tolist()[0] > dependance_test_threshold:
            # variables are independant
            if reference_data.shape[0] >= 30 and new_data.shape[0] >= 30:
                # A Z-test for reduced deviation
                # (also known as Z-test for skewness or Z-test for asymmetry)
                Z_score, Zp_value = z_test_for_skewness(
                    data1=reference_data[var], data2=new_data[var]
                )
                p_value_list.append(Zp_value)
            else:
                # Normal law test
                # Kolmogoro-Smirinov
                KS_result = scipy.stats.ks_2samp(
                    data1=reference_data[var],
                    data2=new_data[var],
                    alternative="two-sided",
                    method="auto",
                )
                if KS_result.pvalue >= normality_test_threshold:
                    # variables wich follow normal law
                    # Variance equal test
                    # Fisher test for variable follow normal law
                    ft_statistic, ft_pvalue = f_test(
                        x=reference_data[var], y=new_data[var]
                    )
                    if ft_pvalue >= variance_equal_test_threshold:
                        # Variance have the same variance
                        # perform Student Test - takes 2 positional arguments variable for test
                        tst_result = scipy.stats.ttest_ind(
                            a=reference_data[var],
                            b=new_data[var],
                            axis=0,
                            equal_var=True,
                            random_state=None,
                            alternative="two-sided",
                        )
                        p_value_list.append(tst_result.pvalue)
                    else:
                        # Variable have different variance
                        # perform Welch’s t-test
                        # (equal to Student Test with parameter equal_var=False)
                        tw_result = scipy.stats.ttest_ind(
                            *[reference_data[var], new_data[var]],
                            axis=0,
                            equal_var=False,
                            random_state=None,
                            alternative="two-sided",
                        )
                        p_value_list.append(tw_result.pvalue)
                else:
                    # variables wich not follow normal law
                    # perform Mann-Whitney U test
                    tmwu_result = scipy.stats.mannwhitneyu(
                        x=reference_data[var],
                        y=new_data[var],
                        alternative="two-sided",
                        axis=0,
                    )
                    p_value_list.append(tmwu_result.pvalue)
        else:
            # variables are not independant
            if reference_data.shape[0] >= 30 and new_data.shape[0] >= 30:
                # A Z-test for reduced deviation
                # (also known as Z-test for skewness or Z-test for asymmetry)
                Z_score, Zp_value = z_test_for_matched_samples(
                    data1=reference_data[var], data2=new_data[var]
                )
                p_value_list.append(Zp_value)
            else:
                # Normal law test
                # Kolmogoro-Smirinov
                KS_result = scipy.stats.ks_2samp(
                    data1=reference_data[var],
                    data2=new_data[var],
                    alternative="two-sided",
                    method="auto",
                )
                if KS_result.pvalue >= normality_test_threshold:
                    # variables wich follow normal law
                    # Variance equal test
                    # Fisher test for variable follow normal law
                    ft_statistic, ft_pvalue = f_test(
                        x=reference_data[var], y=new_data[var]
                    )
                    if ft_pvalue >= variance_equal_test_threshold:
                        # Variable have the same variance
                        # perform Student Test - takes 2 positional arguments variable for test
                        tst_result = scipy.stats.ttest_ind(
                            a=reference_data[var],
                            b=new_data[var],
                            axis=0,
                            equal_var=True,
                            random_state=None,
                            alternative="two-sided",
                        )
                        p_value_list.append(tst_result.pvalue)
                    else:
                        # Variable have different variance
                        # perform Welch’s t-test
                        # (equal to Student Test with parameter equal_var=False)
                        tw_result = scipy.stats.ttest_ind(
                            *[reference_data[var], new_data[var]],
                            axis=0,
                            equal_var=False,
                            random_state=None,
                            alternative="two-sided",
                        )
                        p_value_list.append(tw_result.pvalue)
                else:
                    # variables wich not follow normal law
                    # perform Wilcoxon non parametric test
                    twil_result = scipy.stats.wilcoxon(
                        x=reference_data[var],
                        y=new_data[var],
                        zero_method="wilcox",
                        correction=False,
                        alternative="two-sided",
                        method="auto",
                        axis=0,
                    )
                    p_value_list.append(twil_result.pvalue)

    # Using append to add the p_value_list to p_value_frame
    pvalue_frame = pd.DataFrame([p_value_list], columns=column_reference_data)

    return pvalue_frame
