# functions Monthly. Input - xlsx file. Output - html results. Excepctions if not in the correct format.

import pandas as pd
import matplotlib.pyplot as plt
import warnings
import seaborn as sns
from operator import attrgetter
import matplotlib.colors as mcolors
import numpy as np
import seaborn as sns
import plotly.express as px
import os

#### FT AUXILIARES

def get_month(x):
    return df.datetime(x.year, x.month, 1) #year, month, incremints of day

def get_week(x):
    return df.datetime(x.month, x.week, 1) # month, week, incremints of day

def get_date(df, column):
    year = df[column].dt.year
    month = df[column].dt.month
    day = df[column].dt.day
    return year, month, day

#### FUNCT PRINCIPAL MONTHLY

def monthly(xlsxfile="test", save=True): # if not xlsxfile passed, test xlsx. save plots = True or false. 
    
    if xlsxfile=="test":
        
        url = "https://github.com/i-rb/datadreamer/blob/master/data/input_trial.xlsx?raw=true"
        df = pd.read_excel(url,sheet_name=0)
        
    elif xlsxfile!="test":
        
        df = pd.read_excel(xlsxfile,
                dtype={'User ID': str,
                          'EventID': str},
                parse_dates=['Date'], 
                infer_datetime_format=True)
    try:
        cpath=os.getcwd()
        cnew=cpath+"/Output_Cohorts"
        if save==True:
            if not os.path.exists(cnew):
                os.mkdir(cnew)
        df.dropna(subset=['User ID'], inplace=True)
        df['order_month'] = df['Date'].dt.to_period('M')
        df['Cohort_Month'] = df.groupby('User ID')['order_month'].transform('min')
        order_year, order_month, _ = get_date(df, 'order_month')
        cohort_year, cohort_month, _ = get_date(df, 'Cohort_Month')
        year_diff = order_year - cohort_year
        month_diff = order_month - cohort_month
        df['CohortIndex'] = year_diff * 12 + month_diff + 1
        cohort_data = df.groupby(['Cohort_Month', 'CohortIndex'])['User ID'].apply(pd.Series.nunique).reset_index()
        cohort_count = cohort_data.pivot_table(index = 'Cohort_Month', columns = 'CohortIndex',values = 'User ID')
        cohort_size = cohort_count.iloc[:,0] #select all the rows : select the first column
        
        
        retention = cohort_count.divide(cohort_size, axis=0) #Divide the cohort by the first column
        retention = retention.round(3)
        i=0
        while i<len(retention):
            j=0
            while i<(len(retention.columns)-j):
                try:
                    int(retention.iloc[i,j])
                except:
                    retention.iloc[i,j]=0
                j=j+1
            i=i+1
        fig = plt.figure(figsize=(12,12))
        r = sns.heatmap(retention, cmap='RdYlGn', annot=True, fmt='.0%')
        r.set_xlabel("Cohort Index")
        r.set_ylabel("Cohort Month")
        r.set_title("Retention Matrix");
        
        f11=fig
        
        if save==True:
            fig.savefig('Output_Cohorts/retention.png', format='png', dpi=1200)
        ret_new=pd.DataFrame()
        for i in retention.columns:
            for j in retention.index:
                ret_new=ret_new.append([[i,j,float(retention[i][j])]])
                
        data=ret_new.dropna()
        data.columns=["Cohort Index","Cohort Month", "Retention %"]
        fig2 = plt.figure(figsize=(12,8))
        r = sns.lineplot(data=data, x="Cohort Index", y="Retention %");
        r.set(xticks=data.groupby("Cohort Index").count().index);
        r.set_title("Mean of the Retention");
        
        f22=fig2
        
        
        if save==True:
            fig2.savefig('Output_Cohorts/retention_median.png', format='png', dpi=1200)
        
        
        cohort_data_eng = df.groupby(['Cohort_Month', 'CohortIndex'])['EventID'].apply(pd.Series.nunique).reset_index()
        cohort_eng = cohort_data_eng.pivot_table(index = 'Cohort_Month', columns = 'CohortIndex', values = 'EventID')
        engagement = cohort_eng.divide(cohort_count, axis=0)
        engagement=round(engagement,3)
        i=0
        while i<len(engagement):
            j=0
            while i<(len(engagement.columns)-j):
                try:
                    int(engagement.iloc[i,j])
                except:
                    engagement.iloc[i,j]=0
                j=j+1
            i=i+1
        fig3 = plt.figure(figsize=(12,12))
        r3 = sns.heatmap(engagement, cmap='RdYlGn', annot=True, fmt='g')
        r3.set_xlabel("Cohort Index")
        r3.set_ylabel("Cohort Month")
        r3.set_title("Engagement Matrix");
        
        f33=fig3
        
        if save==True:
            fig3.savefig('Output_Cohorts/engagement.png', format='png', dpi=1200)
            
        
        ret_new2=pd.DataFrame()
        for i in engagement.columns:
            for j in engagement.index:
                ret_new2=ret_new2.append([[i,j,float(engagement[i][j])]])
        data2=ret_new2.dropna()
        data2.columns=["Cohort Index","Cohort Month", "Engagement"]
        fig3 = plt.figure(figsize=(12,8))
        r3 = sns.lineplot(data=data2, x="Cohort Index", y="Engagement");
        r3.set(xticks=data.groupby("Cohort Index").count().index);
        r3.set_title("Mean of the Engagement");
        
        f44=fig3
            
        if save==True:
            fig3.savefig('Output_Cohorts/engagement_median.png', format='png', dpi=1200)
        
        
        nueva_metrica = engagement.values*retention.values
        df_nueva_metrica = pd.DataFrame(nueva_metrica)
        fig4 = plt.figure(figsize=(12,12))
        r4 = sns.heatmap(df_nueva_metrica, cmap='RdYlGn', annot=True, fmt='g')
        r4.set_xlabel("Cohort Index")
        r4.set_ylabel("Cohort Month")
        r4.set_title("RxE Matrix");
        
        f55=fig4
        
        if save==True:
            fig4.savefig('Output_Cohorts/rxe.png', format='png', dpi=1200)
        
        ret_new3=pd.DataFrame()
        for i in df_nueva_metrica.columns:
            for j in df_nueva_metrica.index:
                ret_new3=ret_new3.append([[i,j,float(df_nueva_metrica[i][j])]])
        data3=ret_new3.dropna()
        data3.columns=["Cohort Index","Cohort Month", "RxE"]
        fig4 = plt.figure(figsize=(12,8))
        r4 = sns.lineplot(data=data3, x="Cohort Index", y="RxE");
        r4.set(xticks=data.groupby("Cohort Index").count().index);
        r4.set_title("Mean of RxE");
        
        f66=fig4
        
        
        if save==True:
            fig4.savefig('Output_Cohorts/rxe_median.png', format='png', dpi=1200)
            
        if save!=True:
            print("The End (not saving)")
            return f11, f22, f33, f44, f55, f66
            
        
        print("The End")
            

    except:
        print("Se ha producido un error. / An error has occurred.")
        
        
        
#### FUNCT PRINCIPAL WEEKLY

        

def weekly(xlsxfile="test", save=True): # if not xlsxfile passed, test xlsx. save plots = True or false. 
    
    if xlsxfile=="test":
        
        url = "https://github.com/i-rb/datadreamer/blob/master/data/input_trial.xlsx?raw=true"
        df = pd.read_excel(url, sheet_name=0)
        
    elif xlsxfile!="test":
        
        df = pd.read_excel(xlsxfile,
                dtype={'User ID': str,
                          'EventID': str},
                parse_dates=['Date'], 
                infer_datetime_format=True)
    try:
        cpath=os.getcwd()
        cnew=cpath+"/Output_Cohorts_W"
        if save:
            if not os.path.exists(cnew):
                os.mkdir(cnew)
        df.dropna(subset=['User ID'], inplace=True)
        df['order_Week'] = df['Date'].dt.to_period('W')
        df['Cohort_Week'] = df.groupby('User ID')['order_Week'].transform('min')
        df["o_w"] = df.rank(0,"dense")["order_Week"]
        df["c_w"] = df.rank(0,"dense")["Cohort_Week"]
        week_diff2 = df.o_w - df.c_w
        df['CohortIndex'] = week_diff2
        cohort_data = df.groupby(['Cohort_Week', 'CohortIndex'])['User ID'].apply(pd.Series.nunique).reset_index()
        cohort_count = cohort_data.pivot_table(index = 'Cohort_Week', columns = 'CohortIndex', values = 'User ID')
        cohort_size = cohort_count.iloc[:,0] 
        
        retention = cohort_count.divide(cohort_size, axis=0) #Divide the cohort by the first column
        retention = retention.round(3)
        i=0
        while i<len(retention):
            j=0
            while i<(len(retention.columns)-j):
                try:
                    int(retention.iloc[i,j])
                except:
                    retention.iloc[i,j]=0
                j=j+1
            i=i+1
        fig = plt.figure(figsize=(12,12))
        r = sns.heatmap(retention, cmap='RdYlGn', annot=True, fmt='.0%')
        r.set_xlabel("Cohort Index")
        r.set_ylabel("Cohort Month")
        r.set_title("Retention Matrix");
        
        f11=fig
        
        if save==True:
            fig.savefig('Output_Cohorts_W/retention.png', format='png', dpi=1200)
        ret_new=pd.DataFrame()
        for i in retention.columns:
            for j in retention.index:
                ret_new=ret_new.append([[i,j,float(retention[i][j])]])
                
        data=ret_new.dropna()
        data.columns=["Cohort Index","Cohort Week", "Retention %"]
        fig2 = plt.figure(figsize=(12,8))
        r = sns.lineplot(data=data, x="Cohort Index", y="Retention %");
        r.set(xticks=data.groupby("Cohort Index").count().index);
        r.set_title("Mean of the Retention");
        
        f22=fig2
        
        if save==True:
            fig2.savefig('Output_Cohorts_W/retention_median.png', format='png', dpi=1200)
        
        
        cohort_data_eng = df.groupby(['Cohort_Week', 'CohortIndex'])['EventID'].apply(pd.Series.nunique).reset_index()
        cohort_eng = cohort_data_eng.pivot_table(index = 'Cohort_Week', columns = 'CohortIndex', values = 'EventID')
        engagement = cohort_eng.divide(cohort_count, axis=0)
        engagement=round(engagement,3)
        i=0
        while i<len(engagement):
            j=0
            while i<(len(engagement.columns)-j):
                try:
                    int(engagement.iloc[i,j])
                except:
                    engagement.iloc[i,j]=0
                j=j+1
            i=i+1
        fig3 = plt.figure(figsize=(12,12))
        r3 = sns.heatmap(engagement, cmap='RdYlGn', annot=True, fmt='g')
        r3.set_xlabel("Cohort Index")
        r3.set_ylabel("Cohort Week")
        r3.set_title("Engagement Matrix");
        
        f33=fig3
        
        if save==True:
            fig3.savefig('Output_Cohorts_W/engagement.png', format='png', dpi=1200)
        
        ret_new2=pd.DataFrame()
        for i in engagement.columns:
            for j in engagement.index:
                ret_new2=ret_new2.append([[i,j,float(engagement[i][j])]])
        data2=ret_new2.dropna()
        data2.columns=["Cohort Index","Cohort Week", "Engagement"]
        fig3 = plt.figure(figsize=(12,8))
        r3 = sns.lineplot(data=data2, x="Cohort Index", y="Engagement");
        r3.set(xticks=data.groupby("Cohort Index").count().index);
        r3.set_title("Mean of the Engagement");
        
        f44=fig3
            
        if save==True:
            fig3.savefig('Output_Cohorts_W/engagement_median.png', format='png', dpi=1200)
        
        
        nueva_metrica = engagement.values*retention.values
        df_nueva_metrica = pd.DataFrame(nueva_metrica)
        fig4 = plt.figure(figsize=(12,12))
        r4 = sns.heatmap(df_nueva_metrica, cmap='RdYlGn', annot=True, fmt='g')
        r4.set_xlabel("Cohort Index")
        r4.set_ylabel("Cohort Week")
        r4.set_title("RxE Matrix");
        
        f55=fig4
        
        if save==True:
            fig4.savefig('Output_Cohorts_W/rxe.png', format='png', dpi=1200)
        
        ret_new3=pd.DataFrame()
        for i in df_nueva_metrica.columns:
            for j in df_nueva_metrica.index:
                ret_new3=ret_new3.append([[i,j,float(df_nueva_metrica[i][j])]])
        data3=ret_new3.dropna()
        data3.columns=["Cohort Index","Cohort Week", "RxE"]
        fig4 = plt.figure(figsize=(12,8))
        r4 = sns.lineplot(data=data3, x="Cohort Index", y="RxE");
        r4.set(xticks=data.groupby("Cohort Index").count().index);
        r4.set_title("Mean of RxE");
        
        f66=fig4
        
        
        if save==True:
            fig4.savefig('Output_Cohorts_W/rxe_median.png', format='png', dpi=1200)
            
                    
        if save!=True:
            print("The End (not saving)")
            return f11, f22, f33, f44, f55, f66
        
        print("The End")
            

    except:
        print("Se ha producido un error. / An error has occurred.")
