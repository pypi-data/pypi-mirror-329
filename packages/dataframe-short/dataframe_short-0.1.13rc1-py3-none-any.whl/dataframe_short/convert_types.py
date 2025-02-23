from dataframe_short.utils_ds import *
from typing import List, Dict, Literal, Union, Any
# ########################################## imported from work Mar 17, 2024 #######################################################################

def convert_to_numpy_type(df:pd.DataFrame):
    """
    there's an issue of converting pyarrow type to normal type so I need to create this function 
    """
    # medium tested
    from tqdm import tqdm
    for col in tqdm(df.columns):
        curr_dtype = df[col].dtype
        try:
            if curr_dtype in ["string"]:
                df[col] = df[col].values.astype(str)
            elif curr_dtype in ["int64[pyarrow]","Int64","int32[pyarrow]","int16[pyarrow]","int8[pyarrow]","Int32","Int16","Int8"]:
                df[col] = df[col].values.astype(int)
            elif curr_dtype in ["double[pyarrow]","Float64"]:
                df[col] = df[col].values.astype(float)
        except:
            print(f"There's error at column: '{col}'")


def to_list(df_sr_list:Union[pd.DataFrame,pd.Series,List[Any]]):
    import pandas as pd
    # can only be used in this code bc it select 1st column(not all column)
    # convert pd.Dataframe, series, list, or 1string to list
    out_list = []
    # select only 1st column
    if isinstance(df_sr_list, list):
        out_list = df_sr_list
        
    elif isinstance(df_sr_list, pd.DataFrame):
        out_list = df_sr_list.iloc[:, 0].values.tolist()
        
    elif isinstance(df_sr_list, pd.Series):
        out_list = df_sr_list.tolist()
        
    elif isinstance(df_sr_list, (int,float,complex,str)):
        out_list = [df_sr_list]
    
    else:
        print("This datatype is not suppored by this function")
        return False
    
    return out_list


# ########################################## imported from work Mar 17, 2024 #######################################################################

def to_category(data):
    object_cols = data.select_dtypes(include=['object']).columns
    data[object_cols] = data[object_cols].astype('category')
    return data

def to_str_decimal(df,cols,decimal_place = 1, inplace = True, except_level = []):
    # based on pd = 2.1.0
    # Next: add except_level
    from pandas.api.types import is_numeric_dtype

    if isinstance(cols,list):
        except_level_in = list(cols)
    else:
        except_level_in = [except_level]

    if isinstance(cols,list):
        cols_in = list(cols)
    else:
        cols_in = [cols]
    
    for col in cols_in:
        if is_numeric_dtype(df[col]):
            df[col] = df[col].apply(lambda row: f"{row:.{decimal_place}f}")
        # df[col] = df[col].apply(lambda row: f"{row:.{decimal_place}f}" if row not in except_level, axis = 1)

def to_datetime(df,cols = None,inplace=True, print_col = True):
    # little tested
    # required: pd_get_col
    """
    Convert columns of a DataFrame to datetime dtype.

    This function uses the pd.to_datetime() function to convert the columns
    of a DataFrame that contain date-like values to datetime dtype. It can
    either modify the original DataFrame or return a new one.

    Parameters
    ----------
    df : pandas.DataFrame
        The DataFrame to convert.
    cols : list-like, optional
        The list of column names or positions to convert. If None, the function
        will use the pd_get_col() function to find the columns that contain
        'date' in their names. Default None.
    inplace : bool, optional
        Whether to modify the original DataFrame or return a new one. If True,
        the original DataFrame will be modified and nothing will be returned.
        If False, a new DataFrame will be returned and the original one will
        be unchanged. Default True.

    Returns
    -------
    pandas.DataFrame or None
        A new DataFrame with the converted columns, or None if inplace is True.

    Examples
    --------
    >>> df = pd.DataFrame({'date': ['2020-01-01', '2020-01-02'],
                           'value': [1, 2]})
    >>> df
            date  value
    0 2020-01-01      1
    1 2020-01-02      2
    >>> pd_to_datetime(df)
    >>> df
          date  value
    0 2020-01-01      1
    1 2020-01-02      2
    >>> df.dtypes
    date     datetime64[ns]
    value             int64
    dtype: object
    >>> pd_to_datetime(df, cols=['value'], inplace=False)
          date      value
    0 2020-01-01 1970-01-01
    1 2020-01-02 1970-01-02
    """

    import pandas as pd

    if cols is None:
        cols = get_col(df,contain='date',print_col=print_col)

    
    out_df = pd.DataFrame()
    
    if not inplace:
        out_df = df.copy()
    
    for col in cols:
        if inplace:
            df[col] = pd.to_datetime(df[col]) 
        else:
            out_df[col] = pd.to_datetime(out_df[col]) 
    
    if not inplace:
        return out_df

def to_num(df,cols,num_type = "int64",inplace = True,fill_na = 0):
    # still doesn't work

    # fill_na has to be 0 for it to work properly ----> need more investigation
    
    # it seems to work even when it's already number
    # must import
    from pandas.api.types import is_object_dtype
    if isinstance(cols, str):
        # convert to list
        cols_in = [cols]
    else:
        cols_in = [x for x in cols]
        
    if isinstance(cols_in, list):
        for col in cols_in:
            if inplace:
                if is_object_dtype(df[col]):
                    try:
                        df[col] = df[col].str.replace("," ,  "")
                        if fill_na is not False: 
                            df[col] = df[col].fillna(fill_na)
                        # df[col] = df[col].astype(num_type)
                        df[col] = pd.to_numeric(df[col],errors='coerce')
                    except Exception as e:
                        e_str = str(e)
                        print(e_str)
                        print(f"'{col}' has an error")

            else:
                df_copy = df.copy()
                if is_object_dtype(df_copy[col]):
                    try:
                        df_copy[col] = df_copy[col].str.replace("," ,  "")
                        if fill_na is not False: 
                            df_copy[col] = df_copy[col].fillna(fill_na)
                        # df_copy[col] = df_copy[col].astype(num_type)
                        df_copy[col] = pd.to_numeric(df_copy[col],errors='coerce')
                    except Exception as e:
                        e_str = str(e)
                        print(e_str)
                        print(f"'{col}' has an error")
                return df_copy

    else:
        pass

def to_str(df:Union[pd.DataFrame],cols = None,inplace = True,fill_na = False) -> Union[None,pd.DataFrame]:
    # medium tested inplace seems to work now
    # if cols is None convert all columns to string
    if cols is None:
        cols_in = list(df.columns)
    elif isinstance(cols, str):
        # convert to list
        cols_in = [cols]
    else:
        cols_in = [x for x in cols]
        
    if isinstance(cols_in, list):
        if inplace:
            for col in cols_in:
                df[col] = df[col].astype(str)
        else:
            df_copy = df.copy()
            for col in cols_in:
                df_copy[col] = df_copy[col].astype(str)
            return df_copy

