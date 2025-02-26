import polars as pl

def df_compare(a:pl.DataFrame, b:pl.DataFrame, col_only:bool=False, write_csv:bool=False) -> bool:
    """
    compares two polars dataframes for equality
    `equality` in this case means that:
    - both dfs must have the same columns: column names, dtypes, number of cols
    - both dfs must have the same rows
    - if the dfs have different columns they will not be checked for a difference
    in rows
    - row and column order do not matter for row and column comparisons

    args:
        `a`: a pl.Dataframe
        `b`: a pl.Dataframe
        `col_only`: a boolean indicating whether only the columns should be checked
        `write_csv`: a boolean indicating whether or not to write csvs with the 
        row differences, this is helpful when there are many row differences
        and the normal prints won't contain everything, defaults to `False`

    returns:
        `True` if the dataframes are equal, `False` if not        
        prints the difference if `False`
    """
    a_cols = set(a.schema.items())
    b_cols = set(b.schema.items())
    dif_ab = a_cols.difference(b_cols)
    dif_ba = b_cols.difference(a_cols)
    if dif_ab or dif_ba:
        print('columns are different:')
        if dif_ab:
            print(f'col(s) in a but not b: {dif_ab}')
        if dif_ba:
            print(f'col(s) in b but not a: {dif_ba}')
        return False
    if not col_only:
        anti_ab = (
            a.join(b, how='anti', on=a.columns, coalesce=True)
        )
        anti_ba = (
            b.join(a, how='anti', on=b.columns, coalesce=True)
        )
        if not (anti_ab.is_empty() and anti_ba.is_empty()):
            print('rows are different:')
            if not anti_ab.is_empty():
                print('row(s) in a but not b:')
                print(anti_ab)
                if write_csv:
                    fn1 = 'a_not_b.csv'
                    anti_ab.write_csv(fn1)
                    print(f'{fn1} written')
            if not anti_ba.is_empty():
                print('row(s) in b but not a:')
                print(anti_ba)
                if write_csv:
                    fn2 = 'b_not_a.csv'
                    anti_ba.write_csv(fn2)
                    print(f'{fn2} written')
            return False
    return True


