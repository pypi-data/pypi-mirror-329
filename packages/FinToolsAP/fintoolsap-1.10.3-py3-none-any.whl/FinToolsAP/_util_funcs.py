from __future__ import annotations

# standard imports
import os
import numpy
import pandas
import typing
import pathlib
import datetime
import dateutil

# custom imports
import _config

def _rhasattr(obj, attr):
    """
    Recursively checks if an object has an attribute, 
    even if the attribute is nested.

    Parameters:
    obj : object
        The object to check for the attribute.
    attr : str
        The attribute to check, which may be a nested 
        attribute (e.g., 'a.b.c').

    Returns:
    bool
        True if the object has the attribute, False otherwise.
    """
    try:
        # Attempt to split the attribute on the first 
        # dot ('.') to handle nested attributes
        left, right = attr.split('.', 1)
    except:
        # If there is no dot, check if the object has the 
        # simple attribute
        return hasattr(obj, attr)
    # Recursively check the next level of the attribute
    return _rhasattr(getattr(obj, left), right)

def _rgetattr(obj, attr, default = None):
    """
    Recursively retrieves the value of an attribute, even 
    if the attribute is nested.
    Returns a default value if the attribute does not exist.

    Parameters:
    obj : object
        The object to retrieve the attribute from.
    attr : str
        The attribute to retrieve, which may be a nested 
        attribute (e.g., 'a.b.c').
    default : any, optional
        The value to return if the attribute does not exist 
        (default is None).

    Returns:
    any
        The value of the attribute, or the default value if
        the attribute does not exist.
    """
    try:
        # Attempt to split the attribute on the first dot ('.') 
        # to handle nested attributes
        left, right = attr.split('.', 1)
    except:
        # If there is no dot, retrieve the simple attribute or 
        # return the default value
        return getattr(obj, attr, default)
    # Recursively retrieve the next level of the attribute
    return _rgetattr(getattr(obj, left), right, default)

def _rsetattr(obj, attr, val):
    """
    Recursively sets the value of an attribute, even if the
    attribute is nested.

    Parameters:
    obj : object
        The object on which to set the attribute.
    attr : str
        The attribute to set, which may be a nested attribute 
        (e.g., 'a.b.c').
    val : any
        The value to set the attribute to.

    Returns:
    None
    """
    try:
        # Attempt to split the attribute on the first dot ('.')
        # to handle nested attributes
        left, right = attr.split('.', 1)
    except:
        # If there is no dot, set the simple attribute to the 
        # given value
        return setattr(obj, attr, val)
    # Recursively set the next level of the attribute
    return _rsetattr(getattr(obj, left), right, val)


def _check_file_path_type(path, path_arg: str) -> pathlib.Path:
    try:
        path = pathlib.Path(path)
        return(path)
    except:
        raise TypeError(_config.Messages.PATH_FORMAT.format(color = _config.bcolors.FAIL,
                                                            obj = path_arg))

def percentile_rank(df: pandas.DataFrame, var: str) -> pandas.DataFrame:
    ptiles = list(df[var].quantile(q = list(numpy.arange(start = 0, step = 0.01, stop = 1))))
    df[f'{var}_pr'] = 100
    for i in range(99, 0, -1):
        mask = df[var] < ptiles[i]
        df.loc[mask, f'{var}_pr'] = i
    return(df)

def prior_returns(df: pandas.DataFrame, 
                  id_type: str, 
                  return_types: list[str], 
                  return_intervals: list[tuple[int, int]]
                  ) -> pandas.DataFrame:
    """ Calculates the cummulative return between two backward looking time
    intervals
    """
    for ret_typ in return_types:
        for typ in return_intervals:
            name = f'pr{typ[0]}_{typ[1]}' if(ret_typ == 'adjret') else f'prx{typ[0]}_{typ[1]}'
            df[name] = 1
            dic = {}
            for i in range(typ[0], typ[1] + 1):
                dic[f'{ret_typ}_L{i}'] = 1 + df.groupby(by = [id_type])[ret_typ].shift(i)
                df[name] *= dic[f'{ret_typ}_L{i}']
            df = df.drop(df.filter(regex = '_L').columns, axis = 1)
            df[name] -= 1
    return(df)

def winsorize(col: pandas.Series, pct_lower: float = None, pct_upper: float = None) -> pandas.Series:
    if(pct_lower is None and pct_upper is None):
        raise ValueError('pct_lower and pct_upper can not bth be None.')
    val_lower, val_upper = -numpy.inf, numpy.inf
    if(pct_lower is not None):
        val_lower = numpy.percentile(col, pct_lower)
    if(pct_upper is not None):
        val_upper = numpy.percentile(col, pct_upper)
    col = numpy.where(col < val_lower, val_lower, col)
    col = numpy.where(col > val_upper, val_upper, col)
    return(col)

def date_intervals(min_date: datetime.datetime, 
                   max_date: datetime.datetime, 
                   overlap: bool = False, 
                   **kwargs
                   ) -> list[tuple[datetime.datetime, datetime.datetime]]:    
    blocks = []
    start_date = min_date
    while(True):
        end_date = start_date + dateutil.relativedelta.relativedelta(**kwargs)
        if(end_date >= max_date):
            end_date = max_date
            blocks.append((start_date, end_date))
            break 
        
        end_date_adj = end_date
        if(not overlap):
            end_date_adj -= dateutil.relativedelta.relativedelta(days = 1)
        blocks.append((start_date, end_date_adj))
        start_date = end_date
    return(blocks)

def convert_to_list(val: list|str|float|int):
    if(isinstance(val, list)):
        return(val)
    else:
        return([val])

def list_diff(list1: list, list2: list) -> list:
    res = [e for e in list1 if e not in list2]
    return(res)

def list_inter(list1: list, list2: list) -> list:
    res = [e for e in list1 if e in list2]
    return(res)

def msci_quality(Z: float) -> float:
    if(Z >= 0):
        return(1 + Z)
    else:
        return(1 / (1 - Z))
        
# Weighted average
# can be used with groupby:  df.groupby('col1').apply(wavg, 'avg_name', 'weight_name')
# ML: corrected by ML to allow for missing values
def wavg(group, avg_name, weight_name=None):
    if weight_name==None:
        return group[avg_name].mean()
    else:
        x = group[[avg_name,weight_name]].dropna()
        try:
            return (x[avg_name] * x[weight_name]).sum() / x[weight_name].sum()
        except ZeroDivisionError:
            return group[avg_name].mean()
        
def list_dir(path: typing.Union[str, pathlib.Path],
             only_dir: bool = False,
             extension: str = None,
             only_files: bool = True,
             keep_hidden: bool = False,
             absolute_paths: bool = False
            ) -> list[typing.Union[str, pathlib.Path]]:
    """
    List directories and/or files in a given path with optional filtering.

    Parameters:
    - path (Union[str, pathlib.Path]): The path to list contents from.
    - only_dir (bool, optional): Whether to list only directories. Default is False.
    - extension (str, optional): Filter files by extension. Default is None.
    - only_files (bool, optional): Whether to list only files. Default is True.
    - keep_hidden (bool, optional): Whether to include hidden files. Default is False.
    - absolute_paths (bool, optional): Whether to return absolute paths. Default is False.

    Returns:
    list[str]: A list of directory and/or file names.

    Notes:
    - If only_dir is True, only directories will be included.
    - If only_files is True, only files will be included.
    - If keep_hidden is True, hidden files will be included.
    - If extension is provided, only files with that extension will be included.
    - If absolute_paths is True, the full paths of directories and/or files will be returned.
    """
    
    path = pathlib.Path(path)
    path = path.resolve()
    _tmp = os.listdir(path)

    res = []
    for _obj in _tmp:
        _obj_path = path / _obj
        if(_obj_path.is_dir() and only_dir):
            res.append(_obj)
        elif(_obj_path.is_file() and only_files):
            if(keep_hidden or not _obj_path.stem.startswith('.')):
                if(extension is None or _obj_path.suffix == extension):
                    res.append(_obj)
    if(absolute_paths):
        res = [path / f for f in res]

    return(res)
        