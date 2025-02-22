from __future__ import annotations

import sys
import typing
import pathlib
import datetime
import functools
import numpy as np
import pandas as pd

# add this files directory to path
_path_to_this_file = pathlib.Path(__file__).parent.resolve()
sys.path.append(str(_path_to_this_file))

# project specific imports
global _config
global _util_funcs
import _config
import _util_funcs

def sort_portfolios(dfin: pd.DataFrame,
                    sorting_funcs: dict[str, typing.Callable],
                    char_bkpts: dict[str, list[float]] = None,
                    identifier: str = 'permno',
                    date_col: str = 'date',
                    rebalance_freq: str = 'A',
                    return_col: str = 'adjret',
                    weight_col: str = 'me',
                    sort_month: int = 7,
                    drop_na: bool = False,
                    breakpoint_exchanges: list[int] = [1],
                    suppress: bool = False
                ) -> pd.DataFrame:
    """
    Sorts stocks into portfolios based on multiple characteristics and 
        calculates portfolio returns.

    Args:
        - dfin (pd.DataFrame): Input DataFrame containing stock data.
        - sorting_funcs (dict[str, Callable]): Dictionary of sorting functions,
                                                keyed by characteristic names.
        - char_bkpts (dict[str, list[float]], optional): Breakpoints for 
                                                            characteristics, used 
                                                            for ranking. Defaults 
                                                            to None.
        - identifier (str, optional): Name of the stock identifier column. 
                                        Defaults to 'permno'.
        - date_col (str, optional): Name of the date column. Defaults to 'date'.
        - rebalance_freq (str, optional): Rebalancing frequency ('A' for annual, 'M' for monthly). 
                                            Defaults to 'A'.
        - return_col (str, optional): Name of the return column. 
                                        Defaults to 'adjret'.
        - weight_col (str, optional): Name of the weight column. Defaults to 'me'.
        - sort_month (int, optional): Month for annual sorting. Defaults to 7.
        - drop_na (bool, optional): If True, drops rows with missing values. 
                                        Defaults to False.
        - breakpoint_exchanges (list[int], optional): Exchange codes to use for 
                                                        breakpoint calculation. 
                                                        Defaults to [1].
        - suppress (bool, optional): If True, suppresses warning that some stocks 
                                        couldnt be sorted. Defaults to False.

    Returns:
        - pd.DataFrame: DataFrame with portfolio returns and number of firms in each portfolio.

    Raises:
        - TypeError: If date_col cannot be cast to datetime64[ns].

    Key Steps:
        1. Preprocesses the input DataFrame.
        2. Calculates breakpoints for characteristics if provided.
        3. Ranks stocks based on sorting functions.
        4. Removes unsortable stocks.
        5. Assigns stocks to portfolios.
        6. Calculates portfolio returns and number of firms.
        7. Merges returns and firm counts into a final DataFrame.

    Example:
    ```python
    import pandas as pd

    # Sample DataFrame
    dfin = pd.DataFrame({'permno': [1, 1, 2, 2], 
                         'date': pd.to_datetime(['2023-01-01', '2023-02-01', '2023-01-01', '2023-02-01']),
                         'adjret': [0.05, 0.03, 0.02, 0.01], 
                         'me': [100, 120, 80, 90], 
                         'size': ['small', 'small', 'large', 'large']
                         }
                        )

    # Sorting functions
    sorting_funcs = {'size': lambda x: 'S' if x == 'small' else 'L'}

    # Sort portfolios and calculate returns
    portfolio_returns = sort_portfolios(dfin, sorting_funcs)
    print(portfolio_returns)
    """
    
    # only keep necessary columns
    needed_cols = [identifier, date_col, return_col, weight_col, 'exchcd']
    needed_cols += list(sorting_funcs.keys())
    needed_cols = list(set(needed_cols))
    dfin = dfin[needed_cols]
    dfin = dfin.sort_values(by = [date_col, identifier])
    dfin = dfin.dropna()
        
    # cast date column to datetime64[ns]
    if(not isinstance(dfin[date_col], datetime.datetime)):
        try: 
            dfin[date_col] = pd.to_datetime(dfin[date_col], format = 'ISO8601')
        except:
            raise TypeError(_config.Messages.NOT_CONVERTABLE_DATETIME.format(color = _config.bcolors.FAIL,
                                                                             obj = 'date_col'))
        
    # when to sort
    dfin['sort_month'] = dfin[date_col].dt.month    
    if(rebalance_freq == 'A'):
        rebalance_df = dfin[dfin.sort_month == sort_month]
    else:
        rebalance_df = dfin
    
    # calculate breakpoints
    breakpoint_stocks_df = rebalance_df[rebalance_df.exchcd.isin(breakpoint_exchanges)]
    breakpoints_df = breakpoint_ts(breakpoint_stocks_df, vars = char_bkpts)

    # merge breakpoints to the rebalance df
    rebalance_df = breakpoints_df.merge(rebalance_df, how = 'inner', on = [date_col])

    # apply ranking to stocks
    rank_cols = []
    for char, func in sorting_funcs.items():
        rank_cols.append(f'{char}_rank')
        rebalance_df[f'{char}_rank'] = rebalance_df.apply(func, args = (char, ), axis = 1)

    # remove stocks that could not be sorted
    for rank_col in rank_cols:
        if('--fail' in rebalance_df[rank_col].unique()):
            if(not suppress):
                print(_config.Messages.STOCKS_NOT_SORTABLE.format(color = _config.bcolors.WARNING,
                                                                  rank_col = rank_col))
            rebalance_df = rebalance_df[rebalance_df[rank_col] != '--fail']

    # create portfolio name
    rebalance_df['port_name'] = rebalance_df[rank_cols].agg('_'.join, axis = 1)

    # merge portfolio name back to input data
    fin = None
    if(rebalance_freq == 'A'):
        fin = dfin.merge(rebalance_df[[identifier, date_col, 'port_name']], 
                         how = 'left', 
                         on = [identifier, date_col]
                        )
    else:
        fin = rebalance_df
        
    fin = fin.sort_values(by = [identifier, 'date'])
            
    # front fill portfolio name
    fin.port_name = fin.groupby(by = [identifier])[['port_name']].ffill()
        
    # create portfolio returns    
    fin = fin.dropna(subset = ['port_name'])
    rets = _util_funcs.gorup_avg(df = fin, 
                                 gr = [date_col, 'port_name'], 
                                 vr = return_col, 
                                 wt = weight_col
                                )   
    
    # count number of firms in each portfolio 
    firm = _util_funcs.groupby_nunique(fin, 
                                       gr = [date_col, 'port_name'], 
                                       var = identifier, 
                                       name = 'num_firms', 
                                       no_merge = True
                                    )
    
    rets = rets.pivot(index = date_col, columns = 'port_name', values = return_col)
    firm = firm.pivot(index = date_col, columns = 'port_name', values = 'num_firms')
    firm = firm.add_suffix('_num_firms')
    res = rets.merge(firm, how = 'inner', on = [date_col])
    if(drop_na): 
        res = res.dropna()
    res = res.reset_index()
    return(res)

## Built in Sorting Functions -------------------------------------------------

def sort_50(row: pd.Series, var: str) -> str:
    """
    Sorts a row of data into one of two groups based on whether a specified 
        variable's value is below or above its 50th percentile breakpoint.

    Args:
        - row (pd.Series): A row of data from a DataFrame.
        - var (str): The name of the variable to use for sorting.

    Returns:
        - str: A string indicating the group the row belongs to, formatted as 
                '{var}1' or '{var}2'. Returns '--fail' if sorting fails.

    Key Steps:
        1. Compares the value of `var` in the row to the 50th percentile 
            breakpoint for that variable.
        2. Assigns the row to group 1 ('{var}1') if the value is below the 
            breakpoint, and group 2 ('{var}2') if it's above or equal.
        3. Returns '--fail' if the comparison fails.
    """
    if(row[var] < row[f'{var}_50%']):
        res = f'{var}1'
    elif(row[var] >= row[f'{var}_50%']):
        res = f'{var}2'
    else:
        res = '--fail'
    return(res)

def sort_050(row: pd.Series, var: str) -> str:
    """
    Sorts a row of data into one of three groups based on the value of a 
        specified variable relative to 0 and its 50th percentile breakpoint.

    Args:
        - row (pd.Series): A row of data from a DataFrame.
        - var (str): The name of the variable to use for sorting.

    Returns:
        - str: A string indicating the group the row belongs to, formatted as 
            '{var}1', '{var}2', or '{var}3'. Returns '--fail' if sorting fails.

    Key Steps:
        1. Assigns the row to group 1 ('{var}1') if the value of `var` is less 
            than 0.
        2. Assigns the row to group 2 ('{var}2') if the value of `var` is 
            greater than or equal to 0 but less than its 50th percentile breakpoint.
        3. Assigns the row to group 3 ('{var}3') if the value of `var` is greater 
            than or equal to its 50th percentile breakpoint.
        4. Returns '--fail' if the comparisons fail.
    """
    if(row[var] < 0):
        res = f'{var}1'
    if(row[var] >= 0 and row[var] < row[f'{var}_50%']):
        res = f'{var}2'
    elif(row[var] >= row[f'{var}_50%']):
        res = f'{var}3'
    else:
        res = '--fail'
    return(res)

def sort_3070(row: pd.Series, var: str) -> str:
    """
    Sorts a given row based on the values of the specified variable and its 
        associated 30% and 70% thresholds.

    Args:
        - row (dict): A dictionary representing a data row.
        - var (str): The variable to be used for sorting.

    Returns:
        - str: A string indicating the sorting result:
            - '{var}1' if row[var] is less than row[f'{var}_30%'].
            - '{var}2' if row[var] is between row[f'{var}_30%'] (inclusive) and 
                row[f'{var}_70%'] (exclusive).
            - '{var}3' if row[var] is greater than or equal to row[f'{var}_70%'].
            - '--fail' if none of the above conditions are met.
    """
    if(row[var] < row[f'{var}_30%']):
        res = f'{var}1'
    elif(row[var] >= row[f'{var}_30%'] and row[var] < row[f'{var}_70%']):
        res = f'{var}2'
    elif(row[var] >= row[f'{var}_70%']):
        res = f'{var}3'
    else:
        res = '--fail'
    return(res)

def sort_03070(row: pd.Series, var: str) -> str:
    """
    Sorts a given Pandas Series row based on the values of the specified 
        variable and its associated 30% and 70% thresholds.

    Args:
        - row (pd.Series): A Pandas Series representing a data row.
        - var (str): The variable to be used for sorting.

    Returns:
        - str: A string indicating the sorting result:
            - '{var}1' if row[var] is less than or equal to 0.
            - '{var}2' if row[var] is between 0 (exclusive) and 
                row[f'{var}_30%'] (inclusive).
            - '{var}3' if row[var] is between row[f'{var}_30%'] (exclusive) 
                and row[f'{var}_70%'] (inclusive).
            - '{var}4' if row[var] is greater than or equal to row[f'{var}_70%'].
            - '--fail' if none of the above conditions are met.
    """
    if(row[var] <= 0):
        res = f'{var}1'
    elif(row[var] >= 0 and row[var] < row[f'{var}_30%']):
        res = f'{var}2'
    elif(row[var] >= row[f'{var}_30%'] and row[var] < row[f'{var}_70%']):
        res = f'{var}3'
    elif(row[var] >= row[f'{var}_70%']):
        res = f'{var}4'
    else:
        res = '--fail'
    return(res)

def sort_tercile(row: pd.Series, var: str) -> str:
    """
    Sorts a given Pandas Series row into terciles based on the values of the 
        specified variable and its associated 33% and 66% thresholds.

    Args:
        - row (pd.Series): A Pandas Series representing a data row.
        - var (str): The variable to be used for sorting.

    Returns:
        - str: A string indicating the tercile classification:
            - '{var}1' if row[var] is less than or equal to row[f'{var}_33%'].
            - '{var}2' if row[var] is between row[f'{var}_33%'] (exclusive) and 
                row[f'{var}_66%'] (inclusive).
            - '{var}3' if row[var] is greater than row[f'{var}_66%'].
            - '--fail' if none of the above conditions are met.
    """
    if(row[var] <= row[f'{var}_33%']):
        res = f'{var}1'
    elif(row[var] > row[f'{var}_33%'] and row[var] <= row[f'{var}_66%']):
        res = f'{var}2'
    elif(row[var] > row[f'{var}_66%']):
        res = f'{var}3'
    else:
        res = '--fail'
    return(res)

def sort_quartile(row: pd.Series, var: str) -> str:
    """
    Sorts a given Pandas Series row into quartiles based on the values of 
        the specified variable and its associated 25%, 50%, and 75% thresholds.

    Args:
        - row (pd.Series): A Pandas Series representing a data row.
        - var (str): The variable to be used for sorting.

    Returns:
        - str: A string indicating the quartile classification:
            - '{var}1' if row[var] is less than or equal to row[f'{var}_25%'].
            - '{var}2' if row[var] is between row[f'{var}_25%'] (exclusive) and 
                row[f'{var}_50%'] (inclusive).
            - '{var}3' if row[var] is between row[f'{var}_50%'] (exclusive) and 
                row[f'{var}_75%'] (inclusive).
            - '{var}4' if row[var] is greater than row[f'{var}_75%'].
            - '--fail' if none of the above conditions are met.
    """
    if(row[var] <= row[f'{var}_25%']):
        res = f'{var}1'
    elif(row[var] > row[f'{var}_25%'] and row[var] <= row[f'{var}_50%']):
        res = f'{var}2'
    elif(row[var] > row[f'{var}_50%'] and row[var] <= row[f'{var}_75%']):
        res = f'{var}3'
    elif(row[var] > row[f'{var}_75%']):
        res = f'{var}4'
    else:
        res = '--fail'
    return(res)

def sort_quintile(row: pd.Series, var: str) -> str:
    """
    Sorts a given Pandas Series row into quintiles based on the values of the 
        specified variable and its associated 20%, 40%, 60%, and 80% thresholds.

    Args:
        - row (pd.Series): A Pandas Series representing a data row.
        - var (str): The variable to be used for sorting.

    Returns:
        - str: A string indicating the quintile classification:
            - '{var}1' if row[var] is less than or equal to row[f'{var}_20%'].
            - '{var}2' if row[var] is between row[f'{var}_20%'] (exclusive) and 
                row[f'{var}_40%'] (inclusive).
            - '{var}3' if row[var] is between row[f'{var}_40%'] (exclusive) and 
                row[f'{var}_60%'] (inclusive).
            - '{var}4' if row[var] is between row[f'{var}_60%'] (exclusive) and 
                row[f'{var}_80%'] (inclusive).
            - '{var}5' if row[var] is greater than row[f'{var}_80%'].
            - '--fail' if none of the above conditions are met.
    """
    if(row[var] <= row[f'{var}_20%']):
        res = f'{var}1'
    elif(row[var] > row[f'{var}_20%'] and row[var] <= row[f'{var}_40%']):
        res = f'{var}2'
    elif(row[var] > row[f'{var}_40%'] and row[var] <= row[f'{var}_60%']):
        res = f'{var}3'
    elif(row[var] > row[f'{var}_60%'] and row[var] <= row[f'{var}_80%']):
        res = f'{var}4'
    elif(row[var] > row[f'{var}_80%']):
        res = f'{var}5'
    else:
        res = '--fail'
    return(res)

def sort_decile(row: pd.Series, var: str) -> str:
    """
    Sorts a given Pandas Series row into deciles based on the values of the 
        specified variable and its associated 10%, 20%, ..., 90% thresholds.

    Args:
        - row (pd.Series): A Pandas Series representing a data row.
        - var (str): The variable to be used for sorting.

    Returns:
        - str: A string indicating the decile classification:
            - '{var}1' if row[var] is less than row[f'{var}_10%'].
            - '{var}2' if row[var] is between row[f'{var}_10%'] (inclusive) and 
                row[f'{var}_20%'] (exclusive).
            - '{var}3' if row[var] is between row[f'{var}_20%'] (inclusive) and 
                row[f'{var}_30%'] (exclusive).
            - '{var}4' if row[var] is between row[f'{var}_30%'] (inclusive) and 
                row[f'{var}_40%'] (exclusive).
            - '{var}5' if row[var] is between row[f'{var}_40%'] (inclusive) and 
                row[f'{var}_50%'] (exclusive).
            - '{var}6' if row[var] is between row[f'{var}_50%'] (inclusive) and 
                row[f'{var}_60%'] (exclusive).
            - '{var}7' if row[var] is between row[f'{var}_60%'] (inclusive) and 
                row[f'{var}_70%'] (exclusive).
            - '{var}8' if row[var] is between row[f'{var}_70%'] (inclusive) and 
                row[f'{var}_80%'] (exclusive).
            - '{var}9' if row[var] is between row[f'{var}_80%'] (inclusive) and 
                row[f'{var}_90%'] (exclusive).
            - '{var}10' if row[var] is greater than or equal to row[f'{var}_90%'].
            - '--fail' if none of the above conditions are met.
    """
    if(row[var] < row[f'{var}_10%']):
        res = f'{var}1'
    elif(row[var] >= row[f'{var}_10%'] and row[var] < row[f'{var}_20%']):
        res = f'{var}2'
    elif(row[var] >= row[f'{var}_20%'] and row[var] < row[f'{var}_30%']):
        res = f'{var}3'
    elif(row[var] >= row[f'{var}_30%'] and row[var] < row[f'{var}_40%']):
        res = f'{var}4'
    elif(row[var] >= row[f'{var}_40%'] and row[var] < row[f'{var}_50%']):
        res = f'{var}5'
    elif(row[var] >= row[f'{var}_50%'] and row[var] < row[f'{var}_60%']):
        res = f'{var}6'
    elif(row[var] >= row[f'{var}_60%'] and row[var] < row[f'{var}_70%']):
        res = f'{var}7'
    elif(row[var] >= row[f'{var}_70%'] and row[var] < row[f'{var}_80%']):
        res = f'{var}8'
    elif(row[var] >= row[f'{var}_80%'] and row[var] < row[f'{var}_90%']):
        res = f'{var}9'
    elif(row[var] >= row[f'{var}_90%']):
        res = f'{var}10'
    else:
        res = '--fail'
    return(res)