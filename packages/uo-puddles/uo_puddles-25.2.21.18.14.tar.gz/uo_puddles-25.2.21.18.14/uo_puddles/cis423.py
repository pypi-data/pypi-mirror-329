#for cis 423 class use

pypi_version = '1.67'

import datetime
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.model_selection import ParameterGrid
from sklearn.pipeline import Pipeline
import pandas as pd
pd.set_option('mode.chained_assignment', None)  #https://pandas.pydata.org/pandas-docs/stable/user_guide/indexing.html#returning-a-view-versus-a-copy
import numpy as np
import warnings
from sklearn.model_selection import train_test_split
from sklearn.impute import KNNImputer  #chapter 6
from sklearn.experimental import enable_halving_search_cv
from sklearn.model_selection import HalvingGridSearchCV
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import precision_score, recall_score, f1_score, accuracy_score, roc_auc_score
from sklearn.neighbors import KNeighborsClassifier
import builtins
import types
from typing import Dict, Any, Optional, Union, List, Set, Hashable, Literal, Tuple

#Check if a function is referencing global variables - bad
#use: @up_no_globals(globals())  #globals is function that returns *current* globals as dict
#DANGER DANGER: this fails on forward refs. Assumes helper functions all defined before main function. If not will get spurious error.
def up_no_globals(gfn:dict):

  def wrap(f):
    new_globals = {'__builtins__': builtins} 
    # removing keys from globals() storing global values in old_globals
    for key, val in gfn.items():
      if  callable(val):
          new_globals[key] = val
    new_f = types.FunctionType(f.__code__, globals=new_globals, argdefs=f.__defaults__)
    new_f.__annotations__ = f.__annotations__ # for some reason annotations aren't copied over
    return new_f

  return wrap

#titanic_variance_based_split = 112  #newer value from chapter 7 but not compatible with notebooks that follow
#customer_variance_based_split = 135
titanic_variance_based_split = 107   #value obtained when first created videos and notebooks
customer_variance_based_split = 113

#This class maps values in a column, numeric or categorical.
from sklearn.base import BaseEstimator, TransformerMixin

class CustomMappingTransformer(BaseEstimator, TransformerMixin):
    """
    A transformer that maps values in a specified column according to a provided dictionary.
    
    This transformer follows the scikit-learn transformer interface and can be used in
    a scikit-learn pipeline. It applies value substitution to a specified column using
    a mapping dictionary, which can be useful for encoding categorical variables or
    transforming numeric values.
    
    Parameters
    ----------
    mapping_column : str or int
        The name (str) or position (int) of the column to which the mapping will be applied.
    mapping_dict : dict
        A dictionary defining the mapping from existing values to new values.
        Keys should be values present in the mapping_column, and values should
        be their desired replacements.
        
    Attributes
    ----------
    mapping_dict : dict
        The dictionary used for mapping values.
    mapping_column : str or int
        The column (by name or position) that will be transformed.
        
    Examples
    --------
    >>> import pandas as pd
    >>> df = pd.DataFrame({'category': ['A', 'B', 'C', 'A']})
    >>> mapper = CustomMappingTransformer('category', {'A': 1, 'B': 2, 'C': 3})
    >>> transformed_df = mapper.fit_transform(df)
    >>> transformed_df
       category
    0        1
    1        2
    2        3
    3        1
    """

    def __init__(self, mapping_column: Hashable, mapping_dict: Dict[Any, Any]) -> None:
        """
        Initialize the CustomMappingTransformer.
        
        Parameters
        ----------
        mapping_column : Hashable
            The name (str) or position (int) of the column to apply the mapping to.
        mapping_dict : Dict[Any, Any]
            A dictionary defining the mapping from existing values to new values.
            
        Raises
        ------
        AssertionError
            If mapping_dict is not a dictionary.
        """
        assert isinstance(mapping_dict, dict), f'{self.__class__.__name__} constructor expected dictionary but got {type(mapping_dict)} instead.'
        self.mapping_dict: Dict[Any, Any] = mapping_dict
        self.mapping_column: Hashable = mapping_column  # Column to focus on

    def fit(self, X: pd.DataFrame, y: Optional[Any] = None) -> 'CustomMappingTransformer':
        """
        Fit method - performs no actual fitting operation.
        
        This method is implemented to adhere to the scikit-learn transformer interface
        but doesn't perform any computation.
        
        Parameters
        ----------
        X : pandas.DataFrame
            The input data to fit.
        y : array-like, default=None
            Ignored. Present for compatibility with scikit-learn interface.
            
        Returns
        -------
        self : CustomMappingTransformer
            Returns self to allow method chaining.
        """
        print(f"\nWarning: {self.__class__.__name__}.fit does nothing.\n")
        return self  #always the return value of fit

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        """
        Apply the mapping to the specified column in the input DataFrame.
        
        Parameters
        ----------
        X : pandas.DataFrame
            The DataFrame containing the column to transform.
            
        Returns
        -------
        pandas.DataFrame
            A copy of the input DataFrame with mapping applied to the specified column.
            
        Raises
        ------
        AssertionError
            If X is not a pandas DataFrame or if mapping_column is not in X.
            
        Notes
        -----
        This method provides warnings if:
        1. Keys in mapping_dict are not found in the column values
        2. Values in the column don't have corresponding keys in mapping_dict
        """
        assert isinstance(X, pd.core.frame.DataFrame), f'{self.__class__.__name__}.transform expected Dataframe but got {type(X)} instead.'
        assert self.mapping_column in X.columns.to_list(), f'{self.__class__.__name__}.transform unknown column "{self.mapping_column}"'  #column legit?
        warnings.filterwarnings('ignore', message='.*downcasting.*')  #squash warning in replace method below

        #now check to see if all keys are contained in column
        column_set: Set[Any] = set(X[self.mapping_column].unique())
        keys_not_found: Set[Any] = set(self.mapping_dict.keys()) - column_set
        if keys_not_found:
            print(f"\nWarning: {self.__class__.__name__}[{self.mapping_column}] does not contain these keys as values {keys_not_found}\n")

        #now check to see if some keys are absent
        keys_absent: Set[Any] = column_set - set(self.mapping_dict.keys())
        if keys_absent:
            print(f"\nWarning: {self.__class__.__name__}[{self.mapping_column}] does not contain keys for these values {keys_absent}\n")

        X_: pd.DataFrame = X.copy()
        X_[self.mapping_column] = X_[self.mapping_column].replace(self.mapping_dict)
        return X_

    def fit_transform(self, X: pd.DataFrame, y: Optional[Any] = None) -> pd.DataFrame:
        """
        Fit to data, then transform it.
        
        Combines fit() and transform() methods for convenience.
        
        Parameters
        ----------
        X : pandas.DataFrame
            The DataFrame containing the column to transform.
        y : array-like, default=None
            Ignored. Present for compatibility with scikit-learn interface.
            
        Returns
        -------
        pandas.DataFrame
            A copy of the input DataFrame with mapping applied to the specified column.
        """
        #self.fit(X,y)  #commented out to avoid warning message in fit
        result: pd.DataFrame = self.transform(X)
        return result

class CustomRenamingTransformer(BaseEstimator, TransformerMixin):
    """
    A transformer that renames one or more columns in a pandas DataFrame.
    
    This transformer follows the scikit-learn transformer interface and can be used in
    a scikit-learn pipeline. It applies column renaming according to the provided
    mapping dictionary.
    
    Parameters
    ----------
    mapping_dict : Dict[Hashable, Hashable]
        A dictionary defining the mapping from existing column names to new column names.
        Keys represent the original column names, and values represent the new column names.
        
    Attributes
    ----------
    mapping_dict : Dict[Hashable, Hashable]
        The dictionary used for column renaming.
        
    Examples
    --------
    >>> import pandas as pd
    >>> df = pd.DataFrame({0: [1, 2, 3], 'old_name2': ['a', 'b', 'c']})
    >>> renamer = CustomRenamingTransformer({0: 'new_name1', 'old_name2': 'new_name2'})
    >>> renamed_df = renamer.fit_transform(df)
    >>> renamed_df.columns.tolist()
    ['new_name1', 'new_name2']
    """

    def __init__(self, mapping_dict: Dict[Hashable, Hashable]) -> None:
        """
        Initialize the CustomRenamingTransformer.
        
        Parameters
        ----------
        mapping_dict : Dict[Hashable, Hashable]
            A dictionary defining the mapping from existing column names to new column names.
            
        Raises
        ------
        AssertionError
            If mapping_dict is not a dictionary.
        """
        assert isinstance(mapping_dict, dict), f'{self.__class__.__name__} constructor expected dictionary but got {type(mapping_dict)} instead.'
        self.mapping_dict: Dict[Hashable, Hashable] = mapping_dict

    def fit(self, X: pd.DataFrame, y: Optional[Any] = None) -> "CustomRenamingTransformer":
        """
        Fit method - performs no actual fitting operation.
        
        This method is implemented to adhere to the scikit-learn transformer interface
        but doesn't perform any computation.
        
        Parameters
        ----------
        X : pandas.DataFrame
            The input data to fit.
        y : array-like, default=None
            Ignored. Present for compatibility with scikit-learn interface.
            
        Returns
        -------
        self : CustomRenamingTransformer
            Returns self to allow method chaining.
        """
        return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        """
        Rename columns in the input DataFrame according to the mapping dictionary.
        
        Parameters
        ----------
        X : pandas.DataFrame
            The DataFrame containing the columns to rename.
            
        Returns
        -------
        pandas.DataFrame
            A copy of the input DataFrame with columns renamed according to mapping_dict.
            
        Raises
        ------
        AssertionError
            If X is not a pandas DataFrame or if any keys in mapping_dict are not 
            found in the DataFrame columns.
            
        Notes
        -----
        This method validates that all columns specified in the mapping dictionary
        exist in the input DataFrame before attempting any renaming.
        """
        assert isinstance(X, pd.DataFrame), f'{self.__class__.__name__}.transform expected a DataFrame but got {type(X)} instead.'
        
        column_set: Set[Hashable] = set(X.columns)
        not_found: Set[Hashable] = set(self.mapping_dict.keys()) - column_set
        assert not not_found, f"Columns {not_found} are not in the data table"

        X_: pd.DataFrame = X.copy()
        return X_.rename(columns=self.mapping_dict)

    def fit_transform(self, X: pd.DataFrame, y: Optional[Any] = None) -> pd.DataFrame:
        """
        Fit to data, then transform it.
        
        Combines fit() and transform() methods for convenience.
        
        Parameters
        ----------
        X : pandas.DataFrame
            The DataFrame containing the columns to rename.
        y : array-like, default=None
            Ignored. Present for compatibility with scikit-learn interface.
            
        Returns
        -------
        pandas.DataFrame
            A copy of the input DataFrame with columns renamed according to mapping_dict.
        """
        return self.transform(X)


class CustomOHETransformer(BaseEstimator, TransformerMixin):
    """
    A transformer that performs one-hot encoding on a specified column.
    
    This transformer follows the scikit-learn transformer interface and can be used in
    a scikit-learn pipeline. It applies pandas' get_dummies functionality to the specified
    target column with customizable options.
    
    Parameters
    ----------
    target_column : str or int
        The name (str) or position (int) of the column to one-hot encode.
    dummy_na : bool, default=False
        Whether to include a column for NaN values in the encoding.
        If True, NaN values will be encoded as a separate category.
    drop_first : bool, default=False
        Whether to drop the first category in the encoding.
        This is useful for avoiding the dummy variable trap.
        
    Attributes
    ----------
    target_column : str or int
        The column that will be one-hot encoded.
    dummy_na : bool
        Whether NaN values are encoded as a separate category.
    drop_first : bool
        Whether the first category is dropped from the encoding.
        
    Examples
    --------
    >>> import pandas as pd
    >>> df = pd.DataFrame({'category': ['A', 'B', 'A', None, 'C']})
    >>> encoder = CustomOHETransformer('category', dummy_na=True)
    >>> encoded_df = encoder.fit_transform(df)
    >>> encoded_df.columns.tolist()
    ['category_A', 'category_B', 'category_C', 'category_nan']
    """

    def __init__(self, target_column: Union[str, int], dummy_na: bool = False, drop_first: bool = False) -> None:
        """
        Initialize the CustomOHETransformer.
        
        Parameters
        ----------
        target_column : str or int
            The name (str) or position (int) of the column to one-hot encode.
        dummy_na : bool, default=False
            Whether to include a column for NaN values in the encoding.
        drop_first : bool, default=False
            Whether to drop the first category in the encoding.
        """
        self.target_column: Union[str, int] = target_column
        self.dummy_na: bool = dummy_na
        self.drop_first: bool = drop_first

    def fit(self, X: pd.DataFrame, y: Optional[Any] = None) -> 'CustomOHETransformer':
        """
        Fit method - performs no actual fitting operation.
        
        This method is implemented to adhere to the scikit-learn transformer interface
        but doesn't perform any computation.
        
        Parameters
        ----------
        X : pandas.DataFrame
            The input data to fit.
        y : array-like, default=None
            Ignored. Present for compatibility with scikit-learn interface.
            
        Returns
        -------
        self : CustomOHETransformer
            Returns self to allow method chaining.
        """
        print(f"Warning: {self.__class__.__name__}.fit does nothing.")
        return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        """
        Apply one-hot encoding to the target column in the input DataFrame.
        
        Parameters
        ----------
        X : pandas.DataFrame
            The DataFrame containing the column to encode.
            
        Returns
        -------
        pandas.DataFrame
            A copy of the input DataFrame with the target column one-hot encoded.
            
        Raises
        ------
        AssertionError
            If X is not a pandas DataFrame or if target_column is not in X.
            
        Notes
        -----
        The resulting DataFrame will have the target column replaced with multiple
        binary columns, one for each unique value in the original column.
        """
        assert isinstance(X, pd.core.frame.DataFrame), f'{self.__class__.__name__}.transform expected Dataframe but got {type(X)} instead.'
        assert self.target_column in X.columns.to_list(), f'{self.__class__.__name__}.transform unknown column {self.target_column}'
        
        X_: pd.DataFrame = X.copy()
        X_ = pd.get_dummies(X_, 
                           columns=[self.target_column],
                           dummy_na=self.dummy_na,
                           drop_first=self.drop_first,
                           dtype=int)
        return X_

    def fit_transform(self, X: pd.DataFrame, y: Optional[Any] = None) -> pd.DataFrame:
        """
        Fit to data, then transform it.
        
        Combines fit() and transform() methods for convenience.
        
        Parameters
        ----------
        X : pandas.DataFrame
            The DataFrame containing the column to encode.
        y : array-like, default=None
            Ignored. Present for compatibility with scikit-learn interface.
            
        Returns
        -------
        pandas.DataFrame
            A copy of the input DataFrame with the target column one-hot encoded.
        """
        # Intentionally not calling self.fit(X,y) to avoid printing the warning message
        result: pd.DataFrame = self.transform(X)
        return result

class CustomDropColumnsTransformer(BaseEstimator, TransformerMixin):
    """
    A transformer that either drops or keeps specified columns in a DataFrame.
    
    This transformer follows the scikit-learn transformer interface and can be used in
    a scikit-learn pipeline. It allows for selectively keeping or dropping columns 
    from a DataFrame based on a provided list.
    
    Parameters
    ----------
    column_list : List[Hashable]
        List of column names to either drop or keep, depending on the action parameter.
    action : str, default='drop'
        The action to perform on the specified columns. Must be one of:
        - 'drop': Remove the specified columns from the DataFrame
        - 'keep': Keep only the specified columns in the DataFrame
        
    Attributes
    ----------
    column_list : List[Hashable]
        The list of column names to operate on.
    action : str
        The action to perform ('drop' or 'keep').
        
    Examples
    --------
    >>> import pandas as pd
    >>> df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6], 'C': [7, 8, 9]})
    >>> 
    >>> # Drop columns example
    >>> dropper = CustomDropColumnsTransformer(column_list=['A', 'B'], action='drop')
    >>> dropped_df = dropper.fit_transform(df)
    >>> dropped_df.columns.tolist()
    ['C']
    >>> 
    >>> # Keep columns example
    >>> keeper = CustomDropColumnsTransformer(column_list=['A', 'C'], action='keep')
    >>> kept_df = keeper.fit_transform(df)
    >>> kept_df.columns.tolist()
    ['A', 'C']
    """

    def __init__(self, column_list: List[Hashable], action: Literal['drop', 'keep'] = 'drop') -> None:
        """
        Initialize the CustomDropColumnsTransformer.
        
        Parameters
        ----------
        column_list : List[Hashable]
            List of column names to either drop or keep.
        action : str, default='drop'
            The action to perform on the specified columns.
            Must be either 'drop' or 'keep'.
            
        Raises
        ------
        AssertionError
            If action is not 'drop' or 'keep', or if column_list is not a list.
        """
        assert action in ['keep', 'drop'], f'DropColumnsTransformer action {action} not in ["keep", "drop"]'
        assert isinstance(column_list, list), f'DropColumnsTransformer expected list but saw {type(column_list)}'
        self.column_list: List[Hashable] = column_list
        self.action: Literal['drop', 'keep'] = action

    def fit(self, X: pd.DataFrame, y: Optional[Any] = None) -> 'CustomDropColumnsTransformer':
        """
        Fit method - performs no actual fitting operation.
        
        This method is implemented to adhere to the scikit-learn transformer interface
        but doesn't perform any computation.
        
        Parameters
        ----------
        X : pandas.DataFrame
            The input data to fit.
        y : array-like, default=None
            Ignored. Present for compatibility with scikit-learn interface.
            
        Returns
        -------
        self : CustomDropColumnsTransformer
            Returns self to allow method chaining.
        """
        print(f"Warning: {self.__class__.__name__}.fit does nothing.")
        return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        """
        Transform the DataFrame by dropping or keeping specified columns.
        
        Parameters
        ----------
        X : pandas.DataFrame
            The DataFrame to transform.
            
        Returns
        -------
        pandas.DataFrame
            A copy of the input DataFrame with columns dropped or kept according to
            the specified action.
            
        Raises
        ------
        AssertionError
            If X is not a pandas DataFrame or, when action='keep', if any columns
            in column_list are not in X.
            
        Notes
        -----
        When action='drop', missing columns are ignored with a warning.
        When action='keep', missing columns raise an AssertionError.
        """
        assert isinstance(X, pd.core.frame.DataFrame), f'{self.__class__.__name__}.transform expected Dataframe but got {type(X)} instead.'
        remaining_set: Set[Hashable] = set(self.column_list) - set(X.columns)

        X_: pd.DataFrame = X.copy()
        if self.action == 'drop':
            if remaining_set:
                print(f"\nWarning: {self.__class__.__name__} does not contain these columns to drop: {remaining_set}.")
            X_ = X_.drop(columns=self.column_list, errors='ignore')
        else:  # action == 'keep'
            assert not remaining_set, f'{self.__class__.__name__}.transform unknown columns to keep: {remaining_set}'
            X_ = X_[self.column_list]
        return X_

    def fit_transform(self, X: pd.DataFrame, y: Optional[Any] = None) -> pd.DataFrame:
        """
        Fit to data, then transform it.
        
        Combines fit() and transform() methods for convenience.
        
        Parameters
        ----------
        X : pandas.DataFrame
            The DataFrame to transform.
        y : array-like, default=None
            Ignored. Present for compatibility with scikit-learn interface.
            
        Returns
        -------
        pandas.DataFrame
            A copy of the input DataFrame with columns dropped or kept.
        """
        # Intentionally not calling self.fit(X,y) to avoid printing the warning message
        result: pd.DataFrame = self.transform(X)
        return result

class CustomPearsonTransformer(BaseEstimator, TransformerMixin):
    """
    A custom scikit-learn transformer that removes highly correlated features 
    based on Pearson correlation.

    Parameters
    ----------
    threshold : float
        The correlation threshold above which features are considered too highly correlated 
        and will be removed.
    
    Attributes
    ----------
    correlated_columns : Optional[List[Hashable]]
        A list of column names (which can be strings, integers, or other hashable types) 
        that are identified as highly correlated and will be removed.
    """

    def __init__(self, threshold: float) -> None:
        """
        Initializes the transformer with the correlation threshold.

        Parameters
        ----------
        threshold : float
            The threshold value above which features are considered highly correlated.
        """
        self.threshold: float = threshold
        self.correlated_columns: Optional[List[Hashable]] = None

    def fit(self, X: pd.DataFrame, y: Optional[pd.Series] = None) -> "CustomPearsonTransformer":
        """
        Identifies highly correlated features based on the Pearson correlation coefficient.

        Parameters
        ----------
        X : pd.DataFrame
            The input dataframe containing features.
        y : Optional[pd.Series], default=None
            The target variable (not used in this transformer).

        Returns
        -------
        self : CustomPearsonTransformer
            The fitted transformer with identified correlated columns stored.
        """
        df_corr: pd.DataFrame = X.corr(method='pearson')  # Pearson correlation matrix
        masked_df: pd.DataFrame = df_corr.abs() > self.threshold  # Boolean mask of high correlations
        upper_mask: np.ndarray = np.triu(masked_df.to_numpy(), k=1)  # Extract upper triangle (excluding diagonal)

        self.correlated_columns: List[Hashable] = [
            c for i, c in enumerate(df_corr.columns) if any(upper_mask[:, i])
        ]
        return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        """
        Removes the highly correlated columns identified during the `fit` step.

        Parameters
        ----------
        X : pd.DataFrame
            The input dataframe to transform.

        Returns
        -------
        X_transformed : pd.DataFrame
            The transformed dataframe with correlated columns removed.

        Raises
        ------
        AssertionError
            If `X` is not a pandas DataFrame or if `transform` is called before `fit`.
        """
        assert isinstance(X, pd.DataFrame), (
            f'{self.__class__.__name__}.transform expected a DataFrame but got {type(X)} instead.'
        )
        assert self.correlated_columns is not None, (
            f'{self.__class__.__name__}.transform called before fit.'
        )

        X_transformed: pd.DataFrame = X.drop(columns=self.correlated_columns, errors='ignore')
        return X_transformed

    def fit_transform(self, X: pd.DataFrame, y: Optional[pd.Series] = None) -> pd.DataFrame:
        """
        Fits the transformer and then applies the transformation to remove correlated columns.

        Parameters
        ----------
        X : pd.DataFrame
            The input dataframe.
        y : Optional[pd.Series], default=None
            The target variable (not used in this transformer).

        Returns
        -------
        X_transformed : pd.DataFrame
            The transformed dataframe with correlated columns removed.
        """
        self.fit(X, y)
        return self.transform(X)

class CustomDythonTransformer(BaseEstimator, TransformerMixin):
  def __init__(self, threshold):
    self.threshold = threshold
    self.drop_columns = None

  #define methods below

  def fit(self, X, y = None):
    assoc_matrix = nominal.associations(X, nominal_columns='auto', compute_only=True)
    corr_matrix = assoc_matrix['corr'].abs().round(2)
    masked_df = corr_matrix > self.threshold
    upper_mask = np.triu(masked_df, k=1)
    self.drop_columns = [c for i,c in enumerate(X.columns) if upper_mask[:,i].any()]
    return self

  def transform(self, X):
    assert isinstance(X, pd.core.frame.DataFrame), f'{self.__class__.__name__}.transform expected Dataframe but got {type(X)} instead.'
    assert isinstance(self.drop_columns, list), f'NotFittedError: This {self.__class__.__name__} instance is not fitted yet. Call "fit" with appropriate arguments before using this estimator.'

    X_ = X.drop(columns=self.drop_columns)
    return X_

  def fit_transform(self, X, y = None):
    self.fit(X, y)
    result = self.transform(X)
    return result

class CustomSigma3Transformer(BaseEstimator, TransformerMixin):
    """
    A transformer that applies 3-sigma clipping to a specified column in a pandas DataFrame.
    
    This transformer follows the scikit-learn transformer interface and can be used in
    a scikit-learn pipeline. It clips values in the target column to be within three standard 
    deviations from the mean.

    Parameters
    ----------
    target_column : Hashable
        The name of the column to apply 3-sigma clipping on.

    Attributes
    ----------
    high_wall : Optional[float]
        The upper bound for clipping, computed as mean + 3 * standard deviation.
    low_wall : Optional[float]
        The lower bound for clipping, computed as mean - 3 * standard deviation.
    """

    def __init__(self, target_column: Hashable) -> None:
        """
        Initializes the transformer with the target column to be clipped.

        Parameters
        ----------
        target_column : Hashable
            The column to apply 3-sigma clipping on.
        """
        self.target_column: Hashable = target_column
        self.high_wall: Optional[float] = None
        self.low_wall: Optional[float] = None

    def fit(self, X: pd.DataFrame, y: Optional[pd.Series] = None) -> "CustomSigma3Transformer":
        """
        Computes the mean and standard deviation of the target column 
        and determines the clipping range as (mean ± 3 * std).

        Parameters
        ----------
        X : pd.DataFrame
            The input DataFrame containing the target column.
        y : Optional[pd.Series], default=None
            Ignored. Present for compatibility with scikit-learn interface.

        Returns
        -------
        self : CustomSigma3Transformer
            The fitted transformer with computed `high_wall` and `low_wall`.
        
        Raises
        ------
        AssertionError
            If `X` is not a DataFrame or if `target_column` is not in `X`.
        """
        assert isinstance(X, pd.DataFrame), f'{self.__class__.__name__}.fit expected a DataFrame but got {type(X)} instead.'
        assert self.target_column in X.columns, f'{self.__class__.__name__}.fit unrecognizable column {self.target_column}.'

        mean: float = X[self.target_column].mean()
        sigma: float = X[self.target_column].std()
        self.high_wall: float = mean + 3.0 * sigma
        self.low_wall: float = mean - 3.0 * sigma
        return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        """
        Clips values in the target column to be within (mean ± 3 * std) computed during `fit`.

        Parameters
        ----------
        X : pd.DataFrame
            The DataFrame to transform.

        Returns
        -------
        X_transformed : pd.DataFrame
            A copy of `X` with the target column clipped within 3 standard deviations.

        Raises
        ------
        AssertionError
            If `X` is not a DataFrame, if `fit` was not called before `transform`, 
            or if `target_column` is missing.
        """
        assert isinstance(X, pd.DataFrame), f'{self.__class__.__name__}.transform expected a DataFrame but got {type(X)} instead.'
        assert isinstance(self.high_wall, float) and isinstance(self.low_wall, float), (
            f'{self.__class__.__name__}.transform appears no fit was called prior.'
        )
        assert self.target_column in X.columns, f'{self.__class__.__name__}.transform unrecognizable column {self.target_column}.'

        X_transformed: pd.DataFrame = X.copy()
        X_transformed[self.target_column]: pd.Series = X_transformed[self.target_column].clip(lower=self.low_wall, upper=self.high_wall)
        return X_transformed

    def fit_transform(self, X: pd.DataFrame, y: Optional[pd.Series] = None) -> pd.DataFrame:
        """
        Fits the transformer and then applies 3-sigma clipping to the target column.

        Parameters
        ----------
        X : pd.DataFrame
            The DataFrame containing the target column.
        y : Optional[pd.Series], default=None
            Ignored. Present for compatibility with scikit-learn interface.

        Returns
        -------
        X_transformed : pd.DataFrame
            A copy of `X` with the target column clipped within 3 standard deviations.
        """
        self.fit(X, y)
        return self.transform(X)


class CustomTukeyTransformer(BaseEstimator, TransformerMixin):
    """
    A transformer that applies Tukey's fences (inner or outer) to a specified column in a pandas DataFrame.

    This transformer follows the scikit-learn transformer interface and can be used in a scikit-learn pipeline. 
    It clips values in the target column based on Tukey's inner or outer fences.

    Parameters
    ----------
    target_column : Hashable
        The name of the column to apply Tukey's fences on.
    fence : Literal['inner', 'outer'], default='outer'
        Determines whether to use the inner fence (1.5 * IQR) or the outer fence (3.0 * IQR).
    
    Attributes
    ----------
    inner_low : Optional[float]
        The lower bound for clipping using the inner fence (Q1 - 1.5 * IQR).
    outer_low : Optional[float]
        The lower bound for clipping using the outer fence (Q1 - 3.0 * IQR).
    inner_high : Optional[float]
        The upper bound for clipping using the inner fence (Q3 + 1.5 * IQR).
    outer_high : Optional[float]
        The upper bound for clipping using the outer fence (Q3 + 3.0 * IQR).

    Examples
    --------
    >>> import pandas as pd
    >>> df = pd.DataFrame({'values': [10, 15, 14, 20, 100, 5, 7]})
    >>> tukey_transformer = CustomTukeyTransformer(target_column='values', fence='inner')
    >>> transformed_df = tukey_transformer.fit_transform(df)
    >>> transformed_df
    """

    def __init__(self, target_column: Hashable, fence: Literal['inner', 'outer'] = 'outer') -> None:
        """
        Initializes the transformer with the target column and Tukey's fence type.

        Parameters
        ----------
        target_column : Hashable
            The column to apply Tukey's fences on.
        fence : Literal['inner', 'outer'], default='outer'
            The type of fence to use for clipping.
        
        Raises
        ------
        AssertionError
            If `fence` is not 'inner' or 'outer'.
        """
        assert fence in ['inner', 'outer'], f"Invalid fence value '{fence}', expected 'inner' or 'outer'."
        self.target_column: Hashable = target_column
        self.fence: Literal['inner', 'outer'] = fence
        self.inner_low: Optional[float] = None
        self.outer_low: Optional[float] = None
        self.inner_high: Optional[float] = None
        self.outer_high: Optional[float] = None

    def fit(self, X: pd.DataFrame, y: Optional[pd.Series] = None) -> "CustomTukeyTransformer":
        """
        Computes Tukey's inner and outer fences for the target column.

        Parameters
        ----------
        X : pd.DataFrame
            The input DataFrame containing the target column.
        y : Optional[pd.Series], default=None
            Ignored. Present for compatibility with scikit-learn interface.

        Returns
        -------
        self : CustomTukeyTransformer
            The fitted transformer with computed clipping bounds.

        Raises
        ------
        AssertionError
            If `X` is not a DataFrame or if `target_column` is not in `X`.
        """
        assert isinstance(X, pd.DataFrame), f'{self.__class__.__name__}.fit expected a DataFrame but got {type(X)} instead.'
        assert self.target_column in X.columns, f'{self.__class__.__name__}.fit unrecognizable column {self.target_column}.'

        q1: float = X[self.target_column].quantile(0.25)
        q3: float = X[self.target_column].quantile(0.75)
        iqr: float = q3 - q1

        self.inner_low: float = q1 - 1.5 * iqr
        self.outer_low: float = q1 - 3.0 * iqr
        self.inner_high: float = q3 + 1.5 * iqr
        self.outer_high: float = q3 + 3.0 * iqr
        return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        """
        Clips values in the target column based on Tukey's fences.

        Parameters
        ----------
        X : pd.DataFrame
            The DataFrame to transform.

        Returns
        -------
        X_transformed : pd.DataFrame
            A copy of `X` with the target column clipped based on the selected fence.

        Raises
        ------
        AssertionError
            If `X` is not a DataFrame, if `fit` was not called before `transform`, 
            or if `target_column` is missing.
        """
        assert isinstance(X, pd.DataFrame), f'{self.__class__.__name__}.transform expected a DataFrame but got {type(X)} instead.'
        assert all(isinstance(v, float) for v in [self.inner_low, self.outer_low, self.inner_high, self.outer_high]), (
            f'{self.__class__.__name__}.transform appears no fit was called prior.'
        )
        assert self.target_column in X.columns, f'{self.__class__.__name__}.transform unrecognizable column {self.target_column}.'

        X_transformed: pd.DataFrame = X.copy()

        if self.fence == 'inner':
            X_transformed[self.target_column]: pd.Series = X_transformed[self.target_column].clip(
                lower=self.inner_low, upper=self.inner_high
            )
        elif self.fence == 'outer':
            X_transformed[self.target_column]: pd.Series = X_transformed[self.target_column].clip(
                lower=self.outer_low, upper=self.outer_high
            )
        else:
            assert False, f"Unexpected fence value '{self.fence}'"

        return X_transformed

    def fit_transform(self, X: pd.DataFrame, y: Optional[pd.Series] = None) -> pd.DataFrame:
        """
        Fits the transformer and then applies Tukey's clipping to the target column.

        Parameters
        ----------
        X : pd.DataFrame
            The DataFrame containing the target column.
        y : Optional[pd.Series], default=None
            Ignored. Present for compatibility with scikit-learn interface.

        Returns
        -------
        X_transformed : pd.DataFrame
            A copy of `X` with the target column clipped based on the selected fence.
        """
        self.fit(X, y)
        return self.transform(X)

#from scratch
class CustomRobustTransformer(BaseEstimator, TransformerMixin):
    """
    A transformer that applies robust scaling using the median and interquartile range (IQR) 
    to a specified column in a pandas DataFrame.

    This transformer follows the scikit-learn transformer interface and can be used in 
    a scikit-learn pipeline. It scales the target column by subtracting the median and 
    dividing by the interquartile range.

    Parameters
    ----------
    target_column : Hashable
        The name of the column to apply robust scaling to.

    Attributes
    ----------
    iqr : Optional[float]
        The interquartile range (IQR), computed as Q3 - Q1.
    med : Optional[float]
        The median of the target column.

    Examples
    --------
    >>> import pandas as pd
    >>> df = pd.DataFrame({'values': [10, 15, 14, 20, 100, 5, 7]})
    >>> robust_transformer = CustomRobustTransformer(target_column='values')
    >>> transformed_df = robust_transformer.fit_transform(df)
    >>> transformed_df
    """

    def __init__(self, target_column: Hashable) -> None:
        """
        Initializes the transformer with the target column to be scaled.

        Parameters
        ----------
        target_column : Hashable
            The column to apply robust scaling to.
        """
        self.target_column: Hashable = target_column
        self.iqr: Optional[float] = None
        self.med: Optional[float] = None

    def fit(self, X: pd.DataFrame, y: Optional[pd.Series] = None) -> "CustomRobustTransformer":
        """
        Computes the median and interquartile range (IQR) for the target column.

        Parameters
        ----------
        X : pd.DataFrame
            The input DataFrame containing the target column.
        y : Optional[pd.Series], default=None
            Ignored. Present for compatibility with scikit-learn interface.

        Returns
        -------
        self : CustomRobustTransformer
            The fitted transformer with computed `iqr` and `med` values.

        Raises
        ------
        AssertionError
            If `X` is not a DataFrame or if `target_column` is not in `X`.
        """
        assert isinstance(X, pd.DataFrame), f'{self.__class__.__name__}.fit expected a DataFrame but got {type(X)} instead.'
        assert self.target_column in X.columns, f'{self.__class__.__name__}.fit unrecognizable column {self.target_column}.'

        q1: float = float(X[self.target_column].quantile(0.25))
        q3: float = float(X[self.target_column].quantile(0.75))
        self.iqr: float = q3 - q1
        self.med: float = float(X[self.target_column].median())

        return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        """
        Scales values in the target column using the median and IQR.

        Parameters
        ----------
        X : pd.DataFrame
            The DataFrame to transform.

        Returns
        -------
        X_transformed : pd.DataFrame
            A copy of `X` with the target column scaled.

        Raises
        ------
        AssertionError
            If `X` is not a DataFrame, if `fit` was not called before `transform`, 
            or if `target_column` is missing.
        """
        assert isinstance(X, pd.DataFrame), f'{self.__class__.__name__}.transform expected a DataFrame but got {type(X)} instead.'
        assert self.iqr is not None and self.med is not None, (
            f'NotFittedError: This {self.__class__.__name__} instance is not fitted yet. '
            'Call "fit" with appropriate arguments before using this estimator.'
        )
        assert self.target_column in X.columns, f'{self.__class__.__name__}.transform unrecognizable column {self.target_column}.'

        X_transformed: pd.DataFrame = X.copy()

        if self.iqr > 0:
            X_transformed[self.target_column]: pd.Series = (X_transformed[self.target_column] - self.med) / self.iqr

        return X_transformed

    def fit_transform(self, X: pd.DataFrame, y: Optional[pd.Series] = None) -> pd.DataFrame:
        """
        Fits the transformer and then applies robust scaling to the target column.

        Parameters
        ----------
        X : pd.DataFrame
            The DataFrame containing the target column.
        y : Optional[pd.Series], default=None
            Ignored. Present for compatibility with scikit-learn interface.

        Returns
        -------
        X_transformed : pd.DataFrame
            A copy of `X` with the target column scaled.
        """
        self.fit(X, y)
        return self.transform(X)


#wrapping RobustScaler (not used)
class __CustomRobustTransformer(BaseEstimator, TransformerMixin):
    def __init__(self, target_column):
        self.target_column = target_column
        self.scaler = RobustScaler()
        
    def fit(self, X, y=None):
        # Input validation
        assert isinstance(X, pd.DataFrame), (
            f'{self.__class__.__name__}.fit expected DataFrame but got {type(X)} instead.'
        )
        assert self.target_column in X.columns, (
            f'{self.__class__.__name__}.fit unrecognizable column {self.target_column}.'
        )
        
        # Fit the scaler on the target column
        self.scaler.fit(X[[self.target_column]])
        return self

    def transform(self, X):
        # Input validation
        assert isinstance(X, pd.DataFrame), (
            f'{self.__class__.__name__}.transform expected DataFrame but got {type(X)} instead.'
        )
        assert self.target_column in X.columns, (
            f'{self.__class__.__name__}.transform unrecognizable column {self.target_column}.'
        )
        # Check if scaler has been fitted
        assert hasattr(self.scaler, 'center_'),f'This {self.__class__.__name__} instance is not fitted yet. Call "fit" before using this estimator.'
      

        # Create a copy to avoid modifying the original
        X_ = X.copy()
        # Transform only the target column
        X_[self.target_column] = self.scaler.transform(X_[[self.target_column]])
        return X_

    def fit_transform(self, X, y=None):
        return self.fit(X).transform(X)

#allows a list of columns
class CustomTargetTransformer_v1(BaseEstimator, TransformerMixin):
    """
    A target encoder that applies smoothing and returns np.nan for unseen categories.

    Parameters:
    -----------
    cols : list or None, default=None
        List of columns to encode. If None, all string/object columns will be encoded.
    smoothing : float, default=10.0
        Smoothing factor. Higher values give more weight to the global mean.
    """

    def __init__(self, cols=None, smoothing=10.0):
        self.cols = cols
        self.smoothing = smoothing

    def fit(self, X, y):
        """
        Fit the target encoder using training data.

        Parameters:
        -----------
        X : array-like of shape (n_samples, n_features)
            Training data features.
        y : array-like of shape (n_samples,)
            Target values.
        """
        assert isinstance(X, pd.core.frame.DataFrame), f'{self.__class__.__name__}.fit expected Dataframe but got {type(X)} instead.'

        #Convert y to Series so can use groupby, etc.
        y_ = pd.Series(y, index=X.index)


        # Determine which columns to encode
        if self.cols is None:
            self.cols_ = X.select_dtypes(include=['object', 'string', 'category']).columns
        else:
            self.cols_ = self.cols

        #Check for bogus columns
        residue = set(self.cols_) - set(X.columns)
        assert not residue, f'{self.__class__.__name__}.fit unknown columns "{residue}"'

        # Debug prints
        #print("\nDEBUG INFO:")
        #print("Cherbourg samples:", sum(X['Joined'] == 'Cherbourg'))
        #print("Cherbourg labels:", y_[X['Joined'] == 'Cherbourg'].tolist())
        
        # Calculate global mean
        self.global_mean_ = y_.mean()

        # Initialize encoding dictionary
        self.encoding_dict_ = {}

        # For each column
        for col in self.cols_:
            # Debug the groupby operation specifically
            #print("\nGroupby before means calculation:")
            #print(y_.groupby(X[col]).groups)
            
            # Get counts and means
            counts = X[col].value_counts().to_dict()    #dictionary of unique values in the column col and their counts
            means = y_.groupby(X[col]).mean().to_dict() #dictionary of unique values in the column col and their means

            #print("\nCounts:", counts)
            #print("Means:", means)

            # Calculate smoothed means
            smoothed_means = {}
            for category in counts.keys():
                n = counts[category]
                category_mean = means[category]
                # Apply smoothing formula: (n * cat_mean + m * global_mean) / (n + m)
                smoothed_mean = (n * category_mean + self.smoothing * self.global_mean_) / (n + self.smoothing)
                smoothed_means[category] = smoothed_mean

            # Store smoothed means for this column
            self.encoding_dict_[col] = smoothed_means

        return self

    def transform(self, X):
        """
        Transform the data using the fitted target encoder.
        Unseen categories will be encoded as np.nan.

        Parameters:
        -----------
        X : array-like of shape (n_samples, n_features)
            Input data to transform.
        """

        assert isinstance(X, pd.core.frame.DataFrame), f'{self.__class__.__name__}.transform expected Dataframe but got {type(X)} instead.'
        try:
          self.encoding_dict_  #if defined then fit was called
        except:
          assert False, f'{self.__class__.__name__}.transform not fitted'

        X_ = X.copy()

        # Apply encoding to each column
        for col in self.cols_:
            # Map values to encodings, naturally producing np.nan for unseen categories, i.e.,
            # when map tries to look up a value in the dictionary and doesn't find the key, it automatically returns np.nan. That is what we want.
            X_[col] = X_[col].map(self.encoding_dict_[col])

        return X_

    def fit_transform(self, X, y):
        """
        Fit the target encoder and transform the input data.

        Parameters:
        -----------
        X : array-like of shape (n_samples, n_features)
            Training data features.
        y : array-like of shape (n_samples,)
            Target values.
        """
        return self.fit(X, y).transform(X)

from typing import Optional, Hashable, Dict, Union
import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin

class CustomTargetTransformer(BaseEstimator, TransformerMixin):
    """
    A target encoder that applies smoothing and returns np.nan for unseen categories.

    This transformer follows the scikit-learn transformer interface and can be used in 
    a scikit-learn pipeline. It encodes categorical variables based on their target mean 
    with a smoothing factor to reduce overfitting.

    Parameters
    ----------
    col : Hashable
        The column name to encode. Can be a string, integer, or any hashable type.
    smoothing : float, default=10.0
        Smoothing factor. Higher values give more weight to the global mean.

    Attributes
    ----------
    global_mean_ : Optional[float]
        The global mean of the target variable.
    encoding_dict_ : Optional[Dict[Hashable, float]]
        A dictionary mapping each unique category to its smoothed mean encoding.

    Examples
    --------
    >>> import pandas as pd
    >>> df = pd.DataFrame({'category': ['A', 'B', 'A', 'C'], 'target': [1, 2, 1, 3]})
    >>> encoder = CustomTargetTransformer(col='category')
    >>> transformed_df = encoder.fit_transform(df, df['target'])
    >>> transformed_df
    """

    def __init__(self, col: Hashable, smoothing: float = 10.0) -> None:
        """
        Initializes the target encoder with the specified column and smoothing factor.

        Parameters
        ----------
        col : Hashable
            The column to encode.
        smoothing : float, default=10.0
            Smoothing factor to control how much weight the global mean has.
        """
        self.col: Hashable = col
        self.smoothing: float = smoothing
        self.global_mean_: Optional[float] = None
        self.encoding_dict_: Optional[Dict[Hashable, float]] = None

    def fit(self, X: pd.DataFrame, y: pd.Series) -> "CustomTargetTransformer":
        """
        Fit the target encoder using training data.

        Parameters
        ----------
        X : pd.DataFrame
            Training data features.
        y : pd.Series
            Target values.

        Returns
        -------
        self : CustomTargetTransformer
            The fitted transformer with computed encodings.

        Raises
        ------
        AssertionError
            If `X` is not a DataFrame, `y` is not a Series, or if `col` is missing in `X`.
        """
        assert isinstance(X, pd.DataFrame), f'{self.__class__.__name__}.fit expected a DataFrame but got {type(X)} instead.'
        assert isinstance(y, pd.Series), f'{self.__class__.__name__}.fit expected a Series but got {type(y)} instead.'
        assert self.col in X.columns, f'{self.__class__.__name__}.fit column not in X: {self.col}. Actual columns: {X.columns}'

        # Create a DataFrame with just the target column and values
        X_ = X[[self.col]].copy()
        target_name: str = f"{self.col}_target_"
        X_[target_name] = y

        # Calculate global mean
        self.global_mean_: float = float(X_[target_name].mean())

        # Get category counts and means
        counts: Dict[Hashable, int] = X_[self.col].value_counts().to_dict()
        means: Dict[Hashable, float] = X_.groupby(self.col)[target_name].mean().to_dict()

        # Compute smoothed means using the smoothing formula
        self.encoding_dict_: Dict[Hashable, float] = {
            category: (counts[category] * means[category] + self.smoothing * self.global_mean_) / (counts[category] + self.smoothing)
            for category in counts.keys()
        }

        return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        """
        Transform the data using the fitted target encoder.
        Unseen categories will be encoded as np.nan.

        Parameters
        ----------
        X : pd.DataFrame
            Input data to transform.

        Returns
        -------
        X_transformed : pd.DataFrame
            A copy of `X` with the target column encoded.

        Raises
        ------
        AssertionError
            If `X` is not a DataFrame or if `fit` was not called before `transform`.
        """
        assert isinstance(X, pd.DataFrame), f'{self.__class__.__name__}.transform expected a DataFrame but got {type(X)} instead.'
        assert self.encoding_dict_ is not None, f'{self.__class__.__name__}.transform was called before fit.'

        X_transformed: pd.DataFrame = X.copy()

        # Map categories to smoothed means, leaving unseen categories as np.nan
        X_transformed[self.col]: pd.Series = X_transformed[self.col].map(self.encoding_dict_)

        return X_transformed

    def fit_transform(self, X: pd.DataFrame, y: pd.Series) -> pd.DataFrame:
        """
        Fit the target encoder and transform the input data.

        Parameters
        ----------
        X : pd.DataFrame
            Training data features.
        y : pd.Series
            Target values.

        Returns
        -------
        X_transformed : pd.DataFrame
            A copy of `X` with the target column encoded.
        """
        return self.fit(X, y).transform(X)


from sklearn.impute import KNNImputer

class CustomKNNTransformer(BaseEstimator, TransformerMixin):
    """
    A custom transformer that applies K-Nearest Neighbors (KNN) imputation to a pandas DataFrame.

    This transformer follows the scikit-learn transformer interface and can be used in a 
    scikit-learn pipeline. It imputes missing values using the mean of the nearest neighbors.

    Parameters
    ----------
    n_neighbors : int, default=5
        Number of neighboring samples to use for imputation.
    weights : Literal['uniform', 'distance', None], default='uniform'
        Weight function used in prediction:
        - 'uniform': All neighbors are equally weighted.
        - 'distance': Closer neighbors have greater influence.
        - None: Equivalent to 'uniform'.

    Attributes
    ----------
    imputer : KNNImputer
        The scikit-learn KNNImputer instance used for imputation.

    Examples
    --------
    >>> import pandas as pd
    >>> import numpy as np
    >>> df = pd.DataFrame({'A': [1, np.nan, 3], 'B': [4, 5, np.nan]})
    >>> knn_transformer = CustomKNNTransformer(n_neighbors=2)
    >>> transformed_df = knn_transformer.fit_transform(df)
    """

    def __init__(self, n_neighbors: int = 5, weights: Optional[Literal["uniform", "distance", None]] = "uniform") -> None:
        """
        Initializes the KNN imputer with the specified number of neighbors and weighting method.

        Parameters
        ----------
        n_neighbors : int, default=5
            Number of neighboring samples to use for imputation.
        weights : Literal['uniform', 'distance', None], default='uniform'
            Weight function used in prediction.
        """
        self.n_neighbors: int = n_neighbors
        self.weights: Optional[Literal["uniform", "distance", None]] = weights
        self.imputer: KNNImputer = KNNImputer(n_neighbors=self.n_neighbors, weights=self.weights, add_indicator=False)

    def fit(self, X: pd.DataFrame, y: Optional[pd.Series] = None) -> "CustomKNNTransformer":
        """
        Fits the KNN imputer on the input data.

        Parameters
        ----------
        X : pd.DataFrame
            The input DataFrame with missing values.
        y : Optional[pd.Series], default=None
            Ignored. Present for compatibility with scikit-learn interface.

        Returns
        -------
        self : CustomKNNTransformer
            The fitted transformer.
        """
        assert isinstance(X, pd.DataFrame), f'{self.__class__.__name__}.fit expected a DataFrame but got {type(X)} instead.'
        self.imputer.fit(X)
        return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        """
        Transforms the input DataFrame by imputing missing values using the fitted KNN model.

        Parameters
        ----------
        X : pd.DataFrame
            The input DataFrame to transform.

        Returns
        -------
        result_df : pd.DataFrame
            The transformed DataFrame with missing values imputed.

        Raises
        ------
        AssertionError
            If `X` is not a DataFrame or if `fit` was not called before `transform`.
        """
        assert isinstance(X, pd.DataFrame), f'{self.__class__.__name__}.transform expected a DataFrame but got {type(X)} instead.'
        assert hasattr(self.imputer, 'n_features_in_'), (
            f'NotFittedError: This {self.__class__.__name__} instance is not fitted yet. '
            'Call "fit" with appropriate arguments before using this estimator.'
        )

        X_transformed: pd.DataFrame = X.copy()
        columns: pd.Index = X_transformed.columns

        # Check for column name mismatches
        expected_columns: pd.Index = pd.Index(self.imputer.feature_names_in_)
        if not columns.equals(expected_columns):
            print(
                f'Column names mismatch warning: This {self.__class__.__name__} was fitted with {expected_columns} '
                f'but transformed with {columns}'
            )

        # Perform KNN imputation
        matrix = self.imputer.transform(X_transformed)
        result_df: pd.DataFrame = pd.DataFrame(matrix, columns=columns)

        return result_df

    def fit_transform(self, X: pd.DataFrame, y: Optional[pd.Series] = None) -> pd.DataFrame:
        """
        Fits the KNN imputer and then transforms the data.

        Parameters
        ----------
        X : pd.DataFrame
            The input DataFrame with missing values.
        y : Optional[pd.Series], default=None
            Ignored. Present for compatibility with scikit-learn interface.

        Returns
        -------
        result_df : pd.DataFrame
            The transformed DataFrame with missing values imputed.
        """
        return self.fit(X).transform(X)

##BELOW ORIGINAL 423 library
#drop by removing or keeping
class DropColumnsTransformer(BaseEstimator, TransformerMixin):
  def __init__(self, column_list, action='drop'):
    assert action in ['keep', 'drop'], f'DropColumnsTransformer action {action} not in ["keep", "drop"]'
    assert isinstance(column_list, list), f'DropColumnsTransformer expected list but saw {type(column_list)}'
    self.column_list = column_list
    self.action = action

  #fill in rest below
  def fit(self, X, y = None):
    print(f"Warning: {self.__class__.__name__}.fit does nothing.")
    return X

  def transform(self, X):
    assert isinstance(X, pd.core.frame.DataFrame), f'{self.__class__.__name__}.transform expected Dataframe but got {type(X)} instead.'
    remaining_set = set(self.column_list) - set(X.columns)

    X_ = X.copy()
    if self.action=='drop':
      if remaining_set:
        print(f"\nWarning: {self.__class__.__name__} does not contain these columns to drop: {remaining_set}.")
      X_ = X_.drop(columns=self.column_list, errors='ignore')
    else:
      assert not remaining_set, f'{self.__class__.__name__}.transform unknown columns to keep: {remaining_set}'
      X_ = X_[self.column_list]
    return X_

  def fit_transform(self, X, y = None):
    result = self.transform(X)
    return result
  
#This class maps values in a column, numeric or categorical.
#Importantly, it does not change NaNs, leaving that for the imputer step.
#This class maps values in a column, numeric or categorical.
class MappingTransformer(BaseEstimator, TransformerMixin):

  def __init__(self, mapping_column, mapping_dict:dict):
    assert isinstance(mapping_dict, dict), f'{self.__class__.__name__} constructor expected dictionary but got {type(mapping_dict)} instead.'
    self.mapping_dict = mapping_dict
    self.mapping_column = mapping_column  #column to focus on

  def fit(self, X, y = None):
    print(f"\nWarning: {self.__class__.__name__}.fit does nothing.\n")
    return X

  def transform(self, X):
    assert isinstance(X, pd.core.frame.DataFrame), f'{self.__class__.__name__}.transform expected Dataframe but got {type(X)} instead.'
    assert self.mapping_column in X.columns.to_list(), f'{self.__class__.__name__}.transform unknown column "{self.mapping_column}"'  #column legit?

    #now check to see if all keys are contained in column
    column_set = set(X[self.mapping_column].unique())
    keys_not_found = set(self.mapping_dict.keys()) - column_set
    if keys_not_found:
      print(f"\nWarning: {self.__class__.__name__}[{self.mapping_column}] does not contain these keys as values {keys_not_found}\n")

    #now check to see if some keys are absent
    keys_absent = column_set -  set(self.mapping_dict.keys())
    if keys_absent:
      print(f"\nWarning: {self.__class__.__name__}[{self.mapping_column}] does not contain keys for these values {keys_absent}\n")

    X_ = X.copy()
    X_[self.mapping_column] = X_[self.mapping_column].replace(self.mapping_dict)
    return X_

  def fit_transform(self, X, y = None):
    result = self.transform(X)
    return result
    

class OHETransformer(BaseEstimator, TransformerMixin):
  def __init__(self, target_column, dummy_na=False, drop_first=False):  #False because worried about mismatched columns after splitting. Easier to add missing column.
    self.target_column = target_column
    self.dummy_na = dummy_na
    self.drop_first = drop_first
 
  def fit(self, X, y = None):
    print(f"Warning: {self.__class__.__name__}.fit does nothing.")
    return X

  def transform(self, X):
    assert isinstance(X, pd.core.frame.DataFrame), f'{self.__class__.__name__}.transform expected Dataframe but got {type(X)} instead.'
    assert self.target_column in X.columns.to_list(), f'{self.__class__.__name__}.transform unknown column {self.target_column}'
    X_ = X.copy()
    X_ = pd.get_dummies(X_, columns=[self.target_column],
                        dummy_na=self.dummy_na,
                        drop_first = self.drop_first)
    return X_

  def fit_transform(self, X, y = None):
    result = self.transform(X)
    return result
  
#This class will rename one or more columns.
class RenamingTransformer(BaseEstimator, TransformerMixin):
  #your __init__ method below

  def __init__(self, mapping_dict:dict):
    assert isinstance(mapping_dict, dict), f'{self.__class__.__name__} constructor expected dictionary but got {type(mapping_dict)} instead.' 
    self.mapping_dict = mapping_dict

  #write the transform method without asserts. Again, maybe copy and paste from MappingTransformer and fix up.   
  def transform(self, X):
    assert isinstance(X, pd.core.frame.DataFrame), f'RenamingTransformer.transform expected Dataframe but got {type(X)} instead.'
    #your assert code below

    column_set = set(X.columns)
    not_found = set(self.mapping_dict.keys()) - column_set
    assert not not_found, f"Columns {not_found}, are not in the data table"

    X_ = X.copy()
    return X_.rename(columns=self.mapping_dict)
  
#chapter 4 asks for 2 new transformers

class Sigma3Transformer(BaseEstimator, TransformerMixin):
  def __init__(self, target_column):  
    self.target_column = target_column
    
  def fit(self, X, y = None):
    print(f"Warning: {self.__class__.__name__}.fit does nothing.")
    return self

  def transform(self, X):
    assert isinstance(X, pd.core.frame.DataFrame), f'{self.__class__.__name__}.transform expected Dataframe but got {type(X)} instead.'
    X_ = X.copy()
    mean = X_[self.target_column].mean()
    sigma = X_[self.target_column].std()
    high_wall = mean + 3*sigma
    low_wall = mean - 3*sigma
    #print(f'{self.__class__.__name__} mean, sigma, low_wall, high_wall: {round(mean, 2)}, {round(sigma, 2)}, {round(low_wall, 2)}, {round(high_wall, 2)}')
    X_[self.target_column] = X_[self.target_column].clip(lower=low_wall, upper=high_wall)
    return X_

  def fit_transform(self, X, y = None):
    result = self.transform(X)
    return result

class TukeyTransformer(BaseEstimator, TransformerMixin):
  def __init__(self, target_column, fence='outer'):
    assert fence in ['inner', 'outer']
    self.target_column = target_column
    self.fence = fence
    
  def fit(self, X, y = None):
    print(f"Warning: {self.__class__.__name__}.fit does nothing.")
    return self

  def transform(self, X):
    assert isinstance(X, pd.core.frame.DataFrame), f'{self.__class__.__name__}.transform expected Dataframe but got {type(X)} instead.'
    if len(set(X[self.target_column]))<20:
      print(f'{self.__class__.__name__} warning: {self.target_column} has less than 20 unique values. Consider it as categorical?')
      
    X_ = X.copy()
    q1 = X_[self.target_column].quantile(0.25)
    q3 = X_[self.target_column].quantile(0.75)
    iqr = q3-q1
    inner_low = q1-1.5*iqr
    outer_low = q1-3*iqr
    inner_high = q3+1.5*iqr
    outer_high = q3+3*iqr
    #print(f'{self.__class__.__name__} inner_low, inner_high, outer_low, outer_high: {round(inner_low, 2)}, {round(outer_low, 2)}, {round(inner_high, 2)}, {round(outer_high, 2)}')
    if self.fence=='inner':
      X_[self.target_column] = X_[self.target_column].clip(lower=inner_low, upper=inner_high)
    elif self.fence=='outer':
      X_[self.target_column] = X_[self.target_column].clip(lower=outer_low, upper=outer_high)
    else:
      assert False, f"fence has unrecognized value {self.fence}"
      
    if len(set(X_[self.target_column]))<5:
      print(f'{self.__class__.__name__} warning: {self.target_column} has less than 5 unique values after clipping.')
      
    return X_

  def fit_transform(self, X, y = None):
    result = self.transform(X)
    return result

#chapter 5 asks for 1 new transformer

class MinMaxTransformer(BaseEstimator, TransformerMixin):
  def __init__(self):
    pass
    
  #fill in rest below
  def fit(self, X, y = None):
    print(f'Warning: {self.__class__.__name__}.fit does nothing.')
    return X

  def transform(self, X):
    assert isinstance(X, pd.core.frame.DataFrame), f'{self.__class__.__name__}.transform expected Dataframe but got {type(X)} instead.'
    X_ = X.copy()
    from sklearn.preprocessing import MinMaxScaler
    scaler = MinMaxScaler()
    new_df = pd.DataFrame(scaler.fit_transform(X_), columns=X_.columns)
    return new_df

  def fit_transform(self, X, y = None):
    result = self.transform(X)
    return result
  
MinMaxTransformerWrapped = MinMaxTransformer  #for fall 22 bug

class MinMaxTransformerScratch(BaseEstimator, TransformerMixin):
  def __init__(self):
    self.column_stats = dict()

  #fill in rest below
  def fit(self, X, y = None):
    assert isinstance(X, pd.core.frame.DataFrame), f'MinMaxTransformer.fit expected Dataframe but got {type(X)} instead.'
    if y: print(f'Warning: {self.__class__.__name__}.fit did not expect a value for y but got {type(y)} instead.')
    self.column_stats = {c:(X[c].min(),X[c].max()) for c in X.columns.to_list()}
    return X

  def transform(self, X):
    assert isinstance(X, pd.core.frame.DataFrame), f'{self.__class__.__name__}.transform expected Dataframe but got {type(X)} instead.'
    assert self.column_stats, f'{self.__class__.__name__}.transform expected fit method to be called prior.'
    X_ = X.copy()
    fit_columns = set(self.column_stats.keys())
    transform_columns = set(X_.columns.to_list())
    not_fit = transform_columns - fit_columns
    not_transformed = fit_columns - transform_columns
    if not_fit: print(f'Warning: {self.__class__.__name__}.transform has more columns than fit: {not_fit}.')
    if not_transformed: print(f'Warning: {self.__class__.__name__}.transform has fewer columns than fit: {not_transformed}.')

    for c in fit_columns:
      if c not in transform_columns: continue
      cmin,cmax = self.column_stats[c]
      denom = cmax-cmin
      if not denom:
        print(f'Warning: column {c} has same min and max. No change made.')
      else:
        new_col = [(v-cmin)/denom for v in X_[c].to_list()]  #note NaNs remain NaNs - nice
        X_[c] = new_col
    
    return X_

  def fit_transform(self, X, y = None):
    self.fit(X,y)
    result = self.transform(X)
    return result

##added in chapter 6

class KNNTransformer(BaseEstimator, TransformerMixin):
  def __init__(self,n_neighbors=5, weights="uniform"):
    #your code
    self.n_neighbors = n_neighbors
    self.weights=weights 

  def fit(self, X, y = None):
    print(f'Warning: KNNTransformer.fit does nothing.')
    return X

  def transform(self, X):
    assert isinstance(X, pd.core.frame.DataFrame), f'KNNTransformer.transform expected Dataframe but got {type(X)} instead.'
    X_ = X.copy()
    from sklearn.impute import KNNImputer
    imputer = KNNImputer(n_neighbors=self.n_neighbors, weights=self.weights, add_indicator=False)  #if True will screw up column match
    columns = X_.columns
    matrix = imputer.fit_transform(X_)
    result_df = pd.DataFrame(matrix,columns=columns)
    return result_df

  def fit_transform(self, X, y = None):
    result = self.transform(X)
    return result

class IterativeTransformer(BaseEstimator, TransformerMixin):
  def __init__(self, estimator, max_iter=10, random_state=1234):
    self.estimator = estimator
    self.max_iter=max_iter 
    self.random_state=random_state

  #your code
  def fit(self, X, y = None):
    print(f'Warning: {self.__class__.__name__}.fit does nothing.')
    return X

  def transform(self, X):
    assert isinstance(X, pd.core.frame.DataFrame), f'{self.__class__.__name__}.transform expected Dataframe but got {type(X)} instead.'
    X_ = X.copy()
    imputer = IterativeImputer(estimator=self.estimator, max_iter=self.max_iter, random_state=self.random_state)
    columns = X_.columns
    matrix = imputer.fit_transform(X_)
    result_df = pd.DataFrame(matrix,columns=columns)
    return result_df

  def fit_transform(self, X, y = None):
    result = self.transform(X)
    return result

#chapter 7 add

from sklearn.metrics import f1_score  #, balanced_accuracy_score, precision_score, recall_score
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegressionCV
from sklearn.neighbors import KNeighborsClassifier

from typing import Tuple, List, Union
import numpy as np
import pandas as pd
from sklearn.base import TransformerMixin
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import f1_score

def find_random_state(
    features_df: pd.DataFrame, 
    labels: Union[pd.Series, List], 
    transformer: TransformerMixin, 
    n: int = 200
) -> Tuple[int, List[float]]:
    """
    Finds an optimal random state for train-test splitting based on F1-score stability.

    This function iterates through `n` different random states when splitting the data,
    applies a transformation pipeline, and trains a K-Nearest Neighbors classifier.
    It calculates the ratio of test F1-score to train F1-score and selects the random 
    state where this ratio is closest to the mean.

    Parameters
    ----------
    features_df : pd.DataFrame
        The feature dataset.
    labels : Union[pd.Series, List]
        The corresponding labels for classification (can be a pandas Series or a Python list).
    transformer : TransformerMixin
        A scikit-learn compatible transformer for preprocessing.
    n : int, default=200
        The number of random states to evaluate.

    Returns
    -------
    rs_value : int
        The optimal random state where the F1-score ratio is closest to the mean.
    Var : List[float]
        A list containing the F1-score ratios for each evaluated random state.

    Notes
    -----
    - If the train F1-score is below 0.1, that iteration is skipped.
    - A higher F1-score ratio (closer to 1) indicates better train-test consistency.
    """

    model = KNeighborsClassifier(n_neighbors=5)
    Var: List[float] = []  # Collect test_f1/train_f1 ratios

    for i in range(n):
        train_X, test_X, train_y, test_y = train_test_split(
            features_df, labels, test_size=0.2, shuffle=True,
            random_state=i, stratify=labels  # Works with both lists and pd.Series
        )

        # Apply transformation pipeline
        transform_train_X = transformer.fit_transform(train_X, train_y)
        transform_test_X = transformer.transform(test_X)

        # Train model and make predictions
        model.fit(transform_train_X, train_y)
        train_pred = model.predict(transform_train_X)
        test_pred = model.predict(transform_test_X)

        train_f1 = f1_score(train_y, train_pred)

        if train_f1 < 0.1:
            continue  # Skip if train_f1 is too low

        test_f1 = f1_score(test_y, test_pred)
        f1_ratio = test_f1 / train_f1  # Ratio of test to train F1-score

        Var.append(f1_ratio)

    mean_f1_ratio: float = np.mean(Var)
    rs_value: int = np.abs(np.array(Var) - mean_f1_ratio).argmin()  # Index of value closest to mean

    return rs_value, Var



import matplotlib.pyplot as plt

def heat_map(zipped, label_list=(0,1)):
  zlist = list(zipped)
  case_list = []
  for i in range(len(label_list)):
    inner_list = []
    for j in range(len(label_list)):
      inner_list.append(zlist.count((label_list[i], label_list[j])))
    case_list.append(inner_list)


  fig, ax = plt.subplots(figsize=(5, 5))
  ax.imshow(case_list)
  ax.grid(False)
  title = ''
  for i,c in enumerate(label_list):
    title += f'{i}={c} '
  ax.set_title(title)
  ax.set_xlabel('Predicted outputs', fontsize=16, color='black')
  ax.set_ylabel('Actual outputs', fontsize=16, color='black')
  ax.xaxis.set(ticks=range(len(label_list)))
  ax.yaxis.set(ticks=range(len(label_list)))
  
  for i in range(len(label_list)):
      for j in range(len(label_list)):
          ax.text(j, i, case_list[i][j], ha='center', va='center', color='white', fontsize=32)
  plt.show()
  return None

#ch9

titanic_transformer = Pipeline(steps=[
    ('map_gender', CustomMappingTransformer('Gender', {'Male': 0, 'Female': 1})),
    ('map_class', CustomMappingTransformer('Class', {'Crew': 0, 'C3': 1, 'C2': 2, 'C1': 3})),
    ('target_joined', CustomTargetTransformer(col='Joined', smoothing=10)),
    ('tukey_age', CustomTukeyTransformer(target_column='Age', fence='outer')),
    ('tukey_fare', CustomTukeyTransformer(target_column='Fare', fence='outer')),
    ('scale_age', CustomRobustTransformer(target_column='Age')),
    ('scale_fare', CustomRobustTransformer(target_column='Fare')),
    ('impute', CustomKNNTransformer(n_neighbors=5)),
    ], verbose=True)


customer_transformer = Pipeline(steps=[
    ('map_os', CustomMappingTransformer('OS', {'Android': 0, 'iOS': 1})),
    ('target_isp', CustomTargetTransformer(col='ISP')),
    ('map_level', CustomMappingTransformer('Experience Level', {'low': 0, 'medium': 1, 'high':2})),
    ('map_gender', CustomMappingTransformer('Gender', {'Male': 0, 'Female': 1})),
    ('tukey_age', CustomTukeyTransformer('Age', 'inner')),  #from chapter 4
    ('tukey_time spent', CustomTukeyTransformer('Time Spent', 'inner')),  #from chapter 4
    ('scale_age', CustomRobustTransformer(target_column='Age')), #from 5
    ('scale_time spent', CustomRobustTransformer(target_column='Time Spent')), #from 5
    ('impute', CustomKNNTransformer(n_neighbors=5)),
    ], verbose=True)

def dataset_setup(original_table, label_column_name:str, the_transformer, rs, ts=.2):
  #your code below
  feature_table = original_table.drop(columns=label_column_name)
  labels = original_table[label_column_name].to_list()
  X_train, X_test, y_train, y_test  = train_test_split(feature_table, labels, test_size=ts, shuffle=True,
                                                    random_state=rs, stratify=labels)
  X_train_transformed = the_transformer.fit_transform(X_train, y_train)
  X_test_transformed = the_transformer.transform(X_test)
  x_train_numpy = X_train_transformed.to_numpy()
  x_test_numpy = X_test_transformed.to_numpy()
  y_train_numpy = np.array(y_train)
  y_test_numpy = np.array(y_test)
  return x_train_numpy, x_test_numpy, y_train_numpy,  y_test_numpy

def titanic_setup(titanic_table, transformer=titanic_transformer, rs=titanic_variance_based_split, ts=.2):
  return dataset_setup(titanic_table, 'Survived', transformer, rs=rs, ts=ts)

def customer_setup(customer_table, transformer=customer_transformer, rs=76, ts=.2):
  return dataset_setup(customer_table, 'Rating', transformer, rs=rs, ts=ts)

def threshold_results(thresh_list, actuals, predicted):
  result_df = pd.DataFrame(columns=['threshold', 'precision', 'recall', 'f1', 'auc', 'accuracy'])
  for t in thresh_list:
    yhat = [1 if v >=t else 0 for v in predicted]
    #note: where TP=0, the Precision and Recall both become 0. And I am saying return 0 in that case.
    precision = precision_score(actuals, yhat, zero_division=0)
    recall = recall_score(actuals, yhat, zero_division=0)
    f1 = f1_score(actuals, yhat)
    accuracy = accuracy_score(actuals, yhat)
    auc = roc_auc_score(actuals, yhat)
    result_df.loc[len(result_df)] = {'threshold':t, 'precision':precision, 'recall':recall, 'f1':f1, 'auc': auc, 'accuracy':accuracy}

  result_df = result_df.round(2)

  #Next bit fancies up table for printing. See https://betterdatascience.com/style-pandas-dataframes/
  #Note that fancy_df is not really a dataframe. More like a printable object.
  headers = {
    "selector": "th:not(.index_name)",
    "props": "background-color: #800000; color: white; text-align: center"
  }
  properties = {"border": "1px solid black", "width": "65px", "text-align": "center"}

  fancy_df = result_df.style.highlight_max(color = 'pink', axis = 0).format(precision=2).set_properties(**properties).set_table_styles([headers])
  return (result_df, fancy_df)

def sort_grid(grid):
  sorted_grid = grid.copy()

  #sort values - note that this will expand range for you
  for k,v in sorted_grid.items():
    sorted_grid[k] = sorted(sorted_grid[k], key=lambda x: (x is None, x))

  #sort keys
  sorted_grid = dict(sorted(sorted_grid.items()))

  return sorted_grid
  
def halving_search(model, grid, x_train, y_train, factor=3, scoring='roc_auc'):
  #your code below
  halving_cv = HalvingGridSearchCV(
    model, grid,  #our model and the parameter combos we want to try
    scoring=scoring,  #could alternatively choose f1, accuracy or others
    n_jobs=-1,
    min_resources="exhaust",
    factor=factor,  #a typical place to start so triple samples and take top 3rd of combos on each iteration
    cv=5, random_state=1234,
    refit=True  #remembers the best combo and gives us back that model already trained and ready for testing
)

  grid_result = halving_cv.fit(x_train, y_train)
  return grid_result
