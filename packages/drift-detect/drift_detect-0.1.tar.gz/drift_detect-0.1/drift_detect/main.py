
import numpy as np
import pandas as pd
from scipy.stats import ks_2samp, chi2_contingency ,false_discovery_control  , fisher_exact


# TODO add post-hoc analysis where feasible 

def hello_datadrift():
    util_str = '''
    drift-detect is a Python package that helps detect distributional drift between two datasets.
     
    Class : 
        DetectDrift

    Init Args:\n
        data1 (pd.DataFrame): The first dataset\n
        data2 (pd.DataFrame): The second dataset\n
        numerical_cols (List[str]): List of numerical column names\n
        categorical_cols (List[str]): List of categorical column names\n
        correction_type (str, optional): The method for multiple hypothesis correction ('FDR' or 'Bon'). Defaults to 'FDR'\n
        alpha (float, optional): The significance level. Defaults to 0.05\n

    Method:
        detect_drift(): Performs drift detection and prints the results.
    
    Returns:
        bool: True if drift is detected , False otherwise 
    '''

    print(util_str)


class DetectDrift :
    """
    A class to detect distributional drift between two datasets for both numerical and categorical features.
 
    Methods:
    detect_drift(): Performs drift detection and prints the results.
    """

    def __init__(self , data1 : pd.DataFrame, data2 : pd.DataFrame,
                  numerical_cols : list[str], categorical_cols : list[str] , 
                  correction_type : str = 'FDR', alpha : float = 0.05):
        """
        Initializes the DetectDrift class with the given datasets and feature columns\n
        
        Args:\n
        data1 (pd.DataFrame): The first dataset\n
        data2 (pd.DataFrame): The second dataset\n
        numerical_cols (List[str]): List of numerical column names\n
        categorical_cols (List[str]): List of categorical column names\n
        correction_type (str, optional): The method for multiple hypothesis correction ('FDR' or 'Bon'). Defaults to 'FDR'\n
        alpha (float, optional): The significance level. Defaults to 0.05\n
        """
        self.data1 = data1
        self.data2 = data2
        self.numerical_cols = numerical_cols
        self.categorical_cols = categorical_cols
        self.correction_type = correction_type
        self.alpha = alpha 
        self.DRIFT_FLAG = False
        self.__validate_input()
    
    def __validate_input(self):
        """
        Validates the input parameters, including column existence and correction type.
        
        Raises:
        ValueError: If the correction type is not 'FDR' or 'Bon', or if any columns are missing from the datasets.
        """
        try:
            assert (self.correction_type in ['FDR', 'Bon'])
        except AssertionError:
            raise ValueError("Only Bonferroni (Bon) or the False Discovery Rate (FDR) correction is supported.")

        missing_columns_data1 , missing_columns_data2 = [],[]

        # Iterate through all the columns
        for col in self.numerical_cols + self.categorical_cols:
            if col not in self.data1.columns:
                missing_columns_data1.append(col)
            if col not in self.data2.columns:
                missing_columns_data2.append(col)

        # Raise an error if any columns are missing
        if missing_columns_data1 or missing_columns_data2:
            missing_columns_msg = "Columns missing in data1 : {} & data2 : {}".format(','.join(missing_columns_data1) ,','.join(missing_columns_data2) )
            raise ValueError(missing_columns_msg)

    def detect_drift(self)-> bool:
        # TODO make sure this method only runs once 
        """
        Detects drift in the features between the two datasets. It tests both numerical and categorical features
        for drift using hypothesis testing. Results are adjusted for multiple testing using the specified correction 
        method (Bonferroni or FDR).
        Returns:
        bool: True if drift is detected , False otherwise 
        """
        h0 = 'There is not enough evidence to suggest different distributions'
        h1 = 'The two samples come from different distributions.'
        p_values = {}
        num_tests = len(self.numerical_cols) + len(self.categorical_cols)

        for col in self.numerical_cols : 
            p_value = self.__numerical_feature_test(col)
  
            p_values[col ] = float(p_value)
    
            if self.data1[col].isna().sum() > 0 or self.data2[col].isna().sum() > 0:
                num_tests += 1
                p_value_nullcheck = self.__numerical_feature_null_test(col)
                p_values[col + '_nullcheck'] = float (p_value_nullcheck)
           

        for col in self.categorical_cols:
            p_value = self.__categorical_feature_test(col )
            p_values[col ] = float(p_value)
          
        # process the correction for multiple-tests 
        if self.correction_type =='Bon':
            self.alpha= self.__bonferroni_correction(num_tests)
            p_values_adjusted = p_values
        else: # self.correction_type =='FDR':
            p_values_adjusted = self.__FDR_correction(list(p_values.values()))


        for k , p in zip(p_values.keys(), p_values_adjusted) :
            if p < self.alpha:
                self.DRIFT_FLAG = True
                if 'null' in k :
                    col_name = k.replace('_nullcheck', '')
                    print('The distribution of NULLs in Feature : {} is statistically diffrent across the two datasets'.format(col_name))
                else:
                    print('The distribution of Feature : {} is statistically diffrent across the two datasets'.format(k))
        print('*' * 50)
        if self.DRIFT_FLAG :
            print('Reject Null Hypothesis - {}'.format(h1)) 
            print('*' * 50)
            return True
      
        print('Failed to Reject Null Hypothesis - {}'.format(h0))
        print('*' * 50)
        return False
    def __numerical_feature_null_test(self, col : str) -> float :
        """
        Compares the distributions of NULL values of a numerical feature in the two datasets.
        
        Args:
        col (str): The numerical column name.

        Returns:
        float: The p-value from Fisher's Exact test. 
        """
        p_value_nullcheck = self.__fisher_exact_test(col)
        return p_value_nullcheck
    
    def __numerical_feature_test(self, col :str ) ->  float:
        """
        Performs the Kolmogorov-Smirnov test to compare the distributions of a numerical feature in the two datasets.
        
        Args:
        col (str): The numerical column name.
        
        Returns:
        float: The p-value for  the Kolmogorov-Smirnov test.
        """
        sample1 , sample2 = self.data1[col].dropna() , self.data2[col].dropna()
        ks_stat, p_value = ks_2samp(sample1, sample2)
        assert p_value <=1 and p_value >= 0
        # distribution of null v/s non-null values could be statistically diffrent 
        return  p_value
    
    def __fisher_exact_test(self,col:str) -> float:
        """
        Performs Fisher's Exact test to compare the distribution of NULL values between the two datasets.
        
        Args:
        col (str): The column name to test for NULL value distribution.
        
        Returns:
        float: The p-value from Fisher's Exact test.
        """
        sample1_isnull , sample2_isnull= self.data1[col].isna().value_counts().astype(str).reset_index() , self.data2[col].isna().value_counts().astype(str).reset_index()
        contingency_table = sample1_isnull.merge(sample2_isnull, how ='outer', on=col,suffixes=('_1', '_2')).fillna(0).T
        contingency_table = np.array(contingency_table)
        odd_ratio, p_value = fisher_exact(contingency_table) 

        assert p_value <=1 and p_value >= 0
        return p_value
    
    def __categorical_feature_test(self, col : str ) -> float:
        """
        Performs the Chi-squared test to compare the distributions of a categorical feature in the two datasets.
        
        Args:
        col (str): The categorical column name.
        
        Returns:
        float: The p-value from the Chi-squared test.
        """
        # TODO chisq not good for high cardinality, find another test - https://stats.stackexchange.com/questions/388240/will-chi-square-test-work-for-high-number-of-categories
        sample1 , sample2 = self.data1[col].fillna('empty'), self.data2[col].fillna('empty')
        sample1 = self.data1[col].value_counts().astype(int).reset_index()
        sample2 = self.data2[col].value_counts().astype(int).reset_index()
        contingency_table = sample1.merge(sample2, how ='outer', on=col,suffixes=('_1', '_2')).fillna(0)
        contingency_table = np.array(contingency_table[['count_1', 'count_2']])
        ret = chi2_contingency(contingency_table) 
        p_value = ret.pvalue
        assert p_value <=1 and p_value >= 0
        return ret.pvalue

    def __bonferroni_correction(self, num_tests : int ) -> float:
        """
        Performs False Discovery Rate (FDR) correction for multiple hypothesis testing using Benjamini-Hochberg procedure.
        
        Args:
        p_values (list): The list of p-values to adjust.
        
        Returns:
        np.array: The adjusted p-values after applying FDR correction.
        """
        return num_tests/self.alpha

    def __FDR_correction(self, p_values : list)-> np.array:
        """
        Returns a string representation of the DetectDrift instance.
        """
        return false_discovery_control(p_values)
    

