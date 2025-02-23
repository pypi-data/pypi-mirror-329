from typing import Union, List, Literal
import pandas as pd
# from dataframe_short.utils_ds import value_counts,dtypes, count_null

def display_head(
        df:pd.DataFrame
        ,n:int = 15
        ,display_height=300
        ):
    from IPython.display import display, HTML
    html = return_display_html(df.head(n),display_height)
    display(HTML(html))

def display_tail(
        df:pd.DataFrame
        ,n:int = 15
        ,display_height=300
        ):
    from IPython.display import display, HTML
    html = return_display_html(df.tail(n),display_height)
    display(HTML(html))

def display_unique_score(
        df:pd.DataFrame
        ,dropna:bool = False
        ,display_height=300
        ,sort_by_index:Literal["auto",True,False] = "auto"
        ) -> None:
    
    
    from dataframe_short.utils_ds import unique_score
    unique_score_df = unique_score(df,dropna, return_type=pd.DataFrame)

    # display_nice_df(count_of_values,display_height)

    from IPython.display import display, HTML
    html = return_display_html(unique_score_df,display_height)
    display(HTML(html))

def return_display_html(df:Union[pd.DataFrame], display_height=300):
    """
    this is needed as simply use display_nice_df does not work in jupyter notebook
    display_nice_df(value_counts) doesn't seem to work
    """

    from IPython.display import display, HTML
    if isinstance(df, pd.Series):
        df_in = df.to_frame()
        html = f"""
        <div style="max-height: {display_height}px; overflow-y: scroll;">
            {df_in.to_html()}
        </div>
        """
        # display(HTML(html))
    else:
        html = f"""
        <div style="max-height: {display_height}px; overflow-y: scroll;">
            {df.to_html()}
        </div>
        """
        # display(HTML(html))
    return html

def display_nice_df(df:Union[pd.DataFrame], display_height=300):

    """
    main reason I create this is to display the row with the scrolling
    display_height: is the height of diplayed cells
    """
    from IPython.display import display, HTML
    if isinstance(df, pd.Series):
        df_in = df.to_frame()
        html = f"""
        <div style="max-height: {display_height}px; overflow-y: scroll;">
            {df_in.to_html()}
        </div>
        """
        display(HTML(html))
    else:
        html = f"""
        <div style="max-height: {display_height}px; overflow-y: scroll;">
            {df.to_html()}
        </div>
        """
        display(HTML(html))

def display_value_counts(
        df:pd.DataFrame
        ,dropna:bool = False
        ,display_height=300
        ,sort_by_index:Literal["auto",True,False] = "auto"
        ):
    
    
    from dataframe_short.utils_ds import value_counts
    count_of_values = value_counts(df,dropna, sort_by_index=sort_by_index)

    # display_nice_df(count_of_values,display_height)

    from IPython.display import display, HTML
    html = return_display_html(count_of_values,display_height)
    display(HTML(html))

def display_dtype(df:pd.DataFrame, display_height=300):
    from dataframe_short.utils_ds import dtypes
    dtype_df = dtypes(df,return_type=pd.DataFrame)

    # display_nice_df(count_of_values,display_height)

    from IPython.display import display, HTML
    html = return_display_html(dtype_df,display_height)
    display(HTML(html))

def display_null(df:pd.DataFrame, display_height=300):
    from dataframe_short.utils_ds import count_null
    null_df = count_null(df,return_type=pd.DataFrame)

    # display_nice_df(count_of_values,display_height)

    from IPython.display import display, HTML
    html = return_display_html(null_df,display_height)
    display(HTML(html))

# not allow package's user to have access to these
del Union
del List
del Literal

# del value_counts
# del dtypes
# del count_null

