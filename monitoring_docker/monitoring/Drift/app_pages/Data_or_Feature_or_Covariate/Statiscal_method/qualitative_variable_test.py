# import necessary packages
import numpy as np
import pandas as pd
import scipy
import statsmodels.api as sm


# independance test between 2 qualitative variables
def Independance(
    *, reference_data: pd.DataFrame, new_data: pd.DataFrame
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
        # variable witch have 2 modalities, we perform Fisher exact test
        if (
            reference_data[var].nunique(dropna=False) == 2
            and new_data[var].nunique(dropna=False) == 2
        ):
            table = pd.crosstab(reference_data[var].unique(), new_data[var].unique())
            fe_result = scipy.stats.fisher_exact(table, alternative="two-sided")
            p_value_list.append(fe_result.pvalue)
        # variable witch have modality number higher than 2, we perform chi2_contingency test
        else:
            table = pd.crosstab(reference_data[var], new_data[var])
            chi2_result = scipy.stats.chi2_contingency(
                table, correction=True, lambda_=None
            )
            p_value_list.append(chi2_result.pvalue)

    # Using append to add the p_value_list to p_value_frame
    pvalue_frame = pd.DataFrame([p_value_list], columns=column_reference_data)

    return pvalue_frame


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


# proportion or frequence test between 2 qualitative variables
def proportion_or_frequence(
    *,
    reference_data: pd.DataFrame,
    new_data: pd.DataFrame,
    ind_test_pvalue: pd.DataFrame,
    dependance_test_threshold: float,
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
            "variable in 2 data set should be the same population appartenance test"
        )

    p_value_list = []
    pvalue_c = ind_test_pvalue.copy()

    for var in column_reference_data:
        # Test dependance of each variable
        if pvalue_c[var].tolist()[0] > dependance_test_threshold:
            # variables are independant
            if reference_data.shape[0] >= 30 and new_data.shape[0] >= 30:
                # large dataset
                # variable witch have 2 modalities
                if (
                    reference_data[var].nunique(dropna=False) == 2
                    and new_data[var].nunique(dropna=False) == 2
                ):
                    # Fisher exact test
                    table = pd.crosstab(
                        reference_data[var].unique(), new_data[var].unique()
                    )
                    fe_result = scipy.stats.fisher_exact(table, alternative="two-sided")
                    p_value_list.append(fe_result.pvalue)
                else:
                    # Statistique U suit N (0,1)
                    # A Z-test for reduced deviation
                    # (also known as Z-test for skewness or Z-test for asymmetry)
                    Z_score, Zp_value = z_test_for_skewness(
                        data1=reference_data[var], data2=new_data[var]
                    )
                    p_value_list.append(Zp_value)
            else:
                # small dataset : n_sample <= 30
                # variable witch have 2 modalities
                if (
                    reference_data[var].nunique(dropna=False) == 2
                    and new_data[var].nunique(dropna=False) == 2
                ):
                    # Fisher exact test
                    table = pd.crosstab(
                        reference_data[var].unique(), new_data[var].unique()
                    )
                    fe_result = scipy.stats.fisher_exact(table, alternative="two-sided")
                    p_value_list.append(fe_result.pvalue)
                else:
                    # # Chi2 Test
                    # chi2_result = scipy.stats.chisquare(
                    # 	f_obs=reference_data[var],
                    # 	f_exp=new_data[var],
                    # 	ddof=0,
                    # 	axis=0
                    # )
                    # p_value_list.append(chi2_result.pvalue)
                    # Barlett test - suit une loi du Khi² à 1 degré de liberté.
                    # you can make this test for any number of variable
                    bar_result = scipy.stats.bartlett(
                        reference_data[var], new_data[var]
                    )
                    p_value_list.append(bar_result.pvalue)
        else:
            # variables are dependant
            if (
                reference_data[var].nunique(dropna=False) == 2
                and new_data[var].nunique(dropna=False) == 2
            ):
                # variable witch have 2 modalities, we perform McNemar test
                table = pd.crosstab(
                    reference_data[var].unique(), new_data[var].unique()
                )
                Mcn_result = sm.stats.contingency_tables.mcnemar(
                    table=table, exact=False
                )
                p_value_list.append(Mcn_result.pvalue)
            else:
                table = pd.crosstab(reference_data[var], new_data[var])
                chi2_result = scipy.stats.chi2_contingency(
                    table, correction=True, lambda_=None
                )
                p_value_list.append(chi2_result.pvalue)

    # Using append to add the p_value_list to p_value_frame
    pvalue_frame = pd.DataFrame([p_value_list], columns=column_reference_data)

    return pvalue_frame
