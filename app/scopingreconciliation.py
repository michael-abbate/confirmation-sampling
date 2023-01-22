import pandas as pd
import os

def scopingRec(scope_file1, scope_file2):
    cols_to_join = ['Profit Center 0PROFIT_CTR','Company Code 0COMP_CODE','Functional Area 0FUNC_AREA']
    df1 = pd.read_csv(scope_file1)
    df2 = pd.read_csv(scope_file2)
    # new_df = pd.merge(df1, df2,  how='inner', on=cols_to_join)
    # new_df = pd.merge(df2,df1, on = cols_to_join) 
    
    # new_df = df2.loc[(df2[cols_to_join[0]].isin(df1[cols_to_join[0]]))
    #                 &   (df2[cols_to_join[1]].isin(df1[cols_to_join[1]]))  
    #                 &   (df2[cols_to_join[2]].isin(df1[cols_to_join[2]]))  
    # ,:]
    new_df = df2.merge(df1, how = 'inner', on=cols_to_join, suffixes=('', '_remove'))
    
    new_df.drop([i for i in new_df.columns if '_remove' in i],
               axis=1, inplace=True)

    # new_df = df2.join(df1, on = cols_to_join)
    print(new_df.to_string())
    return new_df