import pandas as pd
import os

def checkForBlank(col_data):
    if "" in col_data:
        return "YES"
    else:
        return "NO"

def scopingRec(scope_file1, scope_file2):
    cols_to_join = ['Profit Center 0PROFIT_CTR','Company Code 0COMP_CODE','Functional Area 0FUNC_AREA']
    
    df1 = pd.read_csv(scope_file1)
    print("File 1 Row Count:", df1.shape[0])
    df1_usd = df1["USD Equivalent (at EOD) LIQ_PO990"].sum()
    print("File 1 USD Sum:", df1_usd)
    df1 = df1.astype(str)
    df1_profit_centers = df1['Profit Center 0PROFIT_CTR'].unique()
    print("Are there blank profit centers in file 1:", checkForBlank(df1_profit_centers))
    # print(df1.dtypes)
    print()

    df2 = pd.read_csv(scope_file2)
    print("File 2 Row Count:", df2.shape[0])
    df2_usd = df2["USD Equivalent (at EOD) LIQ_PO990"].sum()
    print("File 2 USD Sum:", df2_usd)
    df2 = df2.astype(str)
    df2_profit_centers = df2['Profit Center 0PROFIT_CTR'].unique()
    print("Are there blank profit centers in file 2:", checkForBlank(df2_profit_centers))
    # print()
    # print(df2.dtypes)
    print()
                     
    df2 = df2.loc[(df2[cols_to_join[0]].isin(df1[cols_to_join[0]].unique()))
                &   (df2[cols_to_join[1]].isin(df1[cols_to_join[1]].unique()))  
                &   (df2[cols_to_join[2]].isin(df1[cols_to_join[2]].unique())) 
    ,:]
    print("Output File Row Count:", df2.shape[0])

    return df2