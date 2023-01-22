import pandas as pd
import os

def scopingRec(scope_file1, scope_file2):
    cols_to_join = ['Profit Center 0PROFIT_CTR','Company Code 0COMP_CODE','Functional Area 0FUNC_AREA']
    df1 = pd.read_csv(scope_file1)
    df2 = pd.read_csv(scope_file2)
    new_df = pd.merge(df1, df2,  how='inner', on=cols_to_join)
    level4_description = new_df['Level 4 -Description'].unique()[0]
    return new_df,level4_description