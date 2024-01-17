# import necessary library and modules
import numpy as np
import pandas as pd

from Drift.app_pages.Data_or_Feature_or_Covariate.Statiscal_method import (
    qualitative_variable_test, quantitative_and_qualitative_variable_test,
    quantitative_variable_test)


# Independance test
def Independance_test_result(
    *,
    reference_data: pd.DataFrame,
    new_data: pd.DataFrame,
    normality_test_threshold: float,
    variance_equality_test_threshold: float,
) -> pd.DataFrame:
    # test to ensure type of input data
    if not isinstance(reference_data, pd.DataFrame):
        raise ValueError("reference data (reference_data) should be a dataframe")
    if not isinstance(new_data, pd.DataFrame):
        raise ValueError("new data (new_data) should be a dataframe")
    if not isinstance(normality_test_threshold, float):
        raise ValueError(
            "normality threshold (normality_test_threshold) should be a float"
        )
    if not isinstance(variance_equality_test_threshold, float):
        raise ValueError(
            "variance threshold (variance_equality_test_threshold) should be a dataframe"
        )

    # Split reference data into qualitative and quantitative data
    numerical_reference_data = reference_data.select_dtypes(include=[np.number])
    categorical_reference_data = reference_data.select_dtypes(exclude=[np.number])

    # Split new data into qualitative and quantitative data
    numerical_new_data = new_data.select_dtypes(include=[np.number])
    categorical_new_data = new_data.select_dtypes(exclude=[np.number])

    # Get indepandance test result for qualitative variable
    categorical_ind_test_pvalue_frame = qualitative_variable_test.Independance(
        reference_data=categorical_reference_data, new_data=categorical_new_data
    )
    # Get indepandance test result for quantitative variable
    numerical_ind_test_pvalue_frame = quantitative_variable_test.Independance(
        reference_data=numerical_reference_data,
        new_data=numerical_new_data,
        normality_test_threshold=normality_test_threshold,
    )
    # Get indepandance test result between qualitative and quantitative variable for reference data
    numerical_and_categorical_ind_test_pvalue_frame_reference = (
        quantitative_and_qualitative_variable_test.Independance(
            data=reference_data,
            normality_test_threshold=normality_test_threshold,
            variance_equality_test_threshold=variance_equality_test_threshold,
        )
    )
    # Get indepandance test result between qualitative and quantitative variable for reference data
    numerical_and_categorical_ind_test_pvalue_frame_new = (
        quantitative_and_qualitative_variable_test.Independance(
            data=new_data,
            normality_test_threshold=normality_test_threshold,
            variance_equality_test_threshold=variance_equality_test_threshold,
        )
    )

    return (
        categorical_ind_test_pvalue_frame,
        numerical_ind_test_pvalue_frame,
        numerical_and_categorical_ind_test_pvalue_frame_reference,
        numerical_and_categorical_ind_test_pvalue_frame_new,
    )


# same population test
def same_population_test_result(
    *,
    reference_data: pd.DataFrame,
    new_data: pd.DataFrame,
    normality_test_threshold: float,
    variance_equality_test_threshold: float,
    dependance_test_threshold: float,
) -> pd.DataFrame:
    # test to ensure type of input data
    if not isinstance(reference_data, pd.DataFrame):
        raise ValueError("reference data (reference_data) should be a dataframe")
    if not isinstance(new_data, pd.DataFrame):
        raise ValueError("new data (new_data) should be a dataframe")
    if not isinstance(normality_test_threshold, float):
        raise ValueError(
            "normality threshold (normality_test_threshold) should be a float"
        )
    if not isinstance(variance_equality_test_threshold, float):
        raise ValueError(
            "variance threshold (variance_equality_test_threshold) should be a dataframe"
        )

    # Split reference data into qualitative and quantitative data
    numerical_reference_data = reference_data.select_dtypes(include=[np.number])
    categorical_reference_data = reference_data.select_dtypes(exclude=[np.number])

    # Split new data into qualitative and quantitative data
    numerical_new_data = new_data.select_dtypes(include=[np.number])
    categorical_new_data = new_data.select_dtypes(exclude=[np.number])

    # Perform independance test
    ind_test_result = Independance_test_result(
        reference_data=reference_data,
        new_data=new_data,
        normality_test_threshold=normality_test_threshold,
        variance_equality_test_threshold=variance_equality_test_threshold,
    )

    # Same population test result for qualitative data
    categorical_same_proportion_or_frequence_test_pvalue_frame = (
        qualitative_variable_test.proportion_or_frequence(
            reference_data=categorical_reference_data,
            new_data=categorical_new_data,
            ind_test_pvalue=ind_test_result[0],
            dependance_test_threshold=dependance_test_threshold,
        )
    )

    # Same population test result for quantitative data
    # variance test
    numerical_same_variance_test_pvalue_frame = quantitative_variable_test.variance(
        reference_data=numerical_reference_data,
        new_data=numerical_new_data,
        ind_test_pvalue=ind_test_result[1],
        dependance_test_threshold=dependance_test_threshold,
        normality_test_threshold=normality_test_threshold,
    )
    # mean test
    numerical_same_mean_test_pvalue_frame = quantitative_variable_test.average_mean(
        reference_data=numerical_reference_data,
        new_data=numerical_new_data,
        ind_test_pvalue=ind_test_result[1],
        dependance_test_threshold=dependance_test_threshold,
        normality_test_threshold=normality_test_threshold,
        variance_equal_test_threshold=variance_equality_test_threshold,
    )

    return (
        categorical_same_proportion_or_frequence_test_pvalue_frame,
        numerical_same_mean_test_pvalue_frame,
        numerical_same_variance_test_pvalue_frame,
    )
