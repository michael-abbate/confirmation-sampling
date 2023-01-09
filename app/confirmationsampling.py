'''
confirmation sampling process
'''
# random sampling by company code 
# cutoff = mean(balance)+3std by company code
# total_pop = sum(balance)
# main params are the comapny code & business area

import pandas as pd
import numpy as np

# df = pd.read_csv('OTC Asset Dummy.csv')
# 1465399
# df = df[['Company Code 0COMP_CODE','Functional Area 0FUNC_AREA','Business Group','Group ID TB035','USD Equivalent (at EOD) LIQ_PO990']]
# print("TOTAL SUM:", df['USD Equivalent (at EOD) LIQ_PO990'].sum())
# print("TOTAL DASH:", df[df['Group ID TB035']==' -'].count())

def determineCutoffThreshold(df):
    rows=[]
    # main_col='Company Code 0COMP_CODE'
    main_col_list = ['Company Code 0COMP_CODE', 'Business Group', 'Business Unit']
    for main_col in main_col_list:
        print(main_col)
        if main_col in df.columns:
            print("retrieving", main_col, df[main_col].unique())

            for criteria in df[main_col].unique():
                print(f"{main_col}: {criteria}")
                # STEP 1: Filter the table by the respective company code or business area (depends on main_col)
                filtered_df = df[df[main_col] == criteria]                
                # print(filtered_df.head())
                # print("Total Original Rows:",filtered_df.shape[0])
                # print("Total Original Balance:",filtered_df['USD Equivalent (at EOD) LIQ_PO990'].sum())

                # STEP 2: Aggregate by the trade balance ID, sum the balance, convert sums to absolute value            
                filtered_agg_by_trade_df = filtered_df.groupby([main_col,'Group ID TB035'])['USD Equivalent (at EOD) LIQ_PO990'].sum().reset_index().rename(columns={0:'USD Equivalent (at EOD) LIQ_PO990'})
                filtered_agg_by_trade_df['USD Equivalent (at EOD) LIQ_PO990'] = abs(filtered_agg_by_trade_df['USD Equivalent (at EOD) LIQ_PO990'])
                # print(filtered_agg_by_trade_df.head())
                # print(len(filtered_agg_by_trade_df['Group ID TB035']))
                # print(len(filtered_agg_by_trade_df['Group ID TB035'].unique()))
                # Below confirms it is the dash that has 2 rows
                # print(filtered_agg_by_trade_df['Group ID TB035'].value_counts())
                # vc = filtered_agg_by_trade_df['Group ID TB035'].value_counts().reset_index()
                # print("Dashes:",filtered_agg_by_trade_df[filtered_agg_by_trade_df['Group ID TB035']==' -'])
                # print("Total Balance After Agg:",filtered_agg_by_trade_df['USD Equivalent (at EOD) LIQ_PO990'].sum())

                # STEP 3: Find total population, mean and standard deviation to calculate cutoff
                total_pop_bc = filtered_agg_by_trade_df['USD Equivalent (at EOD) LIQ_PO990'].sum()
                mean_bc = filtered_agg_by_trade_df['USD Equivalent (at EOD) LIQ_PO990'].mean()
                # std_bc = filtered_agg_by_trade_df['USD Equivalent (at EOD) LIQ_PO990'].std()
                std_bc = np.std(filtered_agg_by_trade_df['USD Equivalent (at EOD) LIQ_PO990'], ddof=0)
                # std2 = np.std(filtered_agg_by_trade_df['USD Equivalent (at EOD) LIQ_PO990'], ddof=1)
                cutoff = mean_bc + 3*std_bc
                # print("Standard Deviation:", std_bc)
                # print("Cutoff:", cutoff)
                # STEP 4: Apply the cutoff filter to the table that was aggregated by trade balance ID
                cutoff_applied_to_filtered_agg_df = filtered_agg_by_trade_df[filtered_agg_by_trade_df['USD Equivalent (at EOD) LIQ_PO990']>=cutoff]
                key_item_total = cutoff_applied_to_filtered_agg_df['USD Equivalent (at EOD) LIQ_PO990'].sum()
                # STEP 5: Get unique trade balance IDs after filtering by cutoff
                valid_trade_balance_ids = cutoff_applied_to_filtered_agg_df['Group ID TB035'].unique()
                key_item_count = len(valid_trade_balance_ids)
                # print("Unique Trade IDs that made cutoff:", len(valid_trade_balance_ids))

                # STEP 6: Return all rows from the company code or business area table 
                final_df = filtered_df[filtered_df['Group ID TB035'].isin(valid_trade_balance_ids)]
                # total_bal_greater_than_cutoff = final_df['USD Equivalent (at EOD) LIQ_PO990'].sum()

                # print("Total Balance of Items Greater than Cutoff:", total_bal_greater_than_cutoff)
                # print("Total Rows to pass to EY Bot:", final_df.shape[0])
                
                #TODO: need to add output file for EY bot
                row = {
                    "data_type":main_col,
                    "results":{
                        "Criteria": [criteria],
                        "Mean":[mean_bc], 
                        "Standard Deviation": [std_bc],
                        "3 Standard Deviations Plus the Mean": [cutoff],
                        "Population Value": [total_pop_bc]
                        ,
                        "Graph":"scatterplot of USD Values order desc",
                        "Key Item Count": [key_item_count],
                        "Key Item Total": [key_item_total]
                    }
                    }
                rows.append(row)
        else:
            print("Error in reading column:", main_col)
    print(rows)
    return rows

#Rules
# Trade A in functional areas 1 and 2.
# Functional area 1 = balance 3
# Functional area 2 = balance -3
# NET = 0 which wont make cutoff


#TODO: Table for each type on a different tab
#TODO: level4description/main_col/allfiles
#TODO: SAMPLING
## Pull in all trade balance IDs and the sum of USD equiv