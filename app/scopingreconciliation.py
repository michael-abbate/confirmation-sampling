import pandas as pd
import os

def scopingRec(scope_file1, scope_file2):
    cols_to_join = ['Profit Center 0PROFIT_CTR','Company Code 0COMP_CODE','Functional Area 0FUNC_AREA']
    df1 = pd.read_csv(scope_file1)
    df1 = df1.astype(str)
    print(df1.dtypes)
    df2 = pd.read_csv(scope_file2)
    df2 = df2.astype(str)
    print()
    print(df2.dtypes)
                     
    df2 = df2.loc[(df2[cols_to_join[0]].isin(df1[cols_to_join[0]].unique()))
                &   (df2[cols_to_join[1]].isin(df1[cols_to_join[1]].unique()))  
                &   (df2[cols_to_join[2]].isin(df1[cols_to_join[2]].unique())) 
    ,:]

    return df2