import pandas as pd
import os

def scopingRec(scope_file1, scope_file2):
    cols_to_join = ['Profit Center 0PROFIT_CTR','Company Code 0COMP_CODE','Functional Area 0FUNC_AREA']
    df1 = pd.read_csv(scope_file1)
    df2 = pd.read_csv(scope_file2)
    new_df = pd.merge(df1, df2,  how='inner', on=cols_to_join)
    return new_df