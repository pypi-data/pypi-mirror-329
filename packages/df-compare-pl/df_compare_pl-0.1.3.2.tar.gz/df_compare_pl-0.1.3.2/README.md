# df compare pl

compares two polars dataframes for equality  
`equality` in this case means that:

- both dfs must have the same columns: column names, dtypes, number of cols
- both dfs must have the same rows
- if the dfs have different columns they will not be checked for a difference in rows
- row and column order do not matter for row and column comparisons

  args:  
   `a`: a pl.Dataframe  
   `b`: a pl.Dataframe  
   `col_only`: a boolean indicating whether only the columns should be checked  
   `write_csv`: a boolean indicating whether or not to write csvs with the row differences, this is helpful when there are many row differences and the normal prints won't contain everything; defaults to `False`

  returns:  
   `True` if the dataframes are equal, `False` if not  
   prints the difference if `False`
