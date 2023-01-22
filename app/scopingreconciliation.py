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
    # new_df = pd.merge(df1, df2,  how='inner', on=cols_to_join)
    # new_df = pd.merge(df2,df1, on = cols_to_join) 
    # print("Step 0:", df2.shape)
    # df2 = df2.loc[(df2[cols_to_join[0]].isin(df1[cols_to_join[0]].unique())),:]
    # print("Step 1:", df2.shape)
    # df2 = df2.loc[(df2[cols_to_join[1]].isin(df1[cols_to_join[1]].unique())),:]
    # print("Step 2:", df2.shape)
    # df2 = df2.loc[(df2[cols_to_join[2]].isin(df1[cols_to_join[2]].unique())),:]
    # print("Step 3:", df2.shape)
                     
    df2 = df2.loc[(df2[cols_to_join[0]].isin(df1[cols_to_join[0]].unique()))
                &   (df2[cols_to_join[1]].isin(df1[cols_to_join[1]].unique()))  
                &   (df2[cols_to_join[2]].isin(df1[cols_to_join[2]].unique())) 
    ,:]

    # new_df = df2.merge(df1, how = 'inner', on=cols_to_join, suffixes=('', '_remove'))
    
    # new_df.drop([i for i in new_df.columns if '_remove' in i],
    #            axis=1, inplace=True)

    # new_df = df2.join(df1, on = cols_to_join)
    # print(new_df.to_string())
    # return new_df
    return df2