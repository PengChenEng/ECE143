import pandas as pd
import numpy as np

# data loader
def data_loader(path):
    '''
    Return a dataframe from the read csv file.
    
    Parameters:
    path: file name, type:str
    
    Returns:
    dataframe
    '''
    assert isinstance(path, str)    
    return pd.read_csv(path)

# Data Preprocessing
def data_processing(df):
    '''
    Returns Processed dataframe
    '''
    # Drop few columns
    df = df.drop(['Address', 'Method','Postcode','Propertycount'], axis=1)
    
    # clean data without valid price value
    df = df[np.isfinite(df['Price'])]
    
    # Extract and add month and year columns from the Date Column
    df['year'] = df.Date.apply(lambda x: int(x.split('/')[2]))
    df['month'] = df.Date.apply(lambda x: int(x.split('/')[1]))
    
    # Add Month(String) column
    month_list= ['January', 'Feburary', 'March', 'April', 'May', 'June', 'July', 
              'August', 'September', 'October', 'November', 'December']
    df['Month']=df.month.apply(lambda x: month_list[x-1])
    
    # Add season columns
    season_list = ['Winter', 'Spring','Summer','Autumn']    
    df['Season'] = df.month.apply(lambda x: season_list[(((x-1)//3)%4)])
    
    #Remove Jan 2016 data
    df = df[~((df.year==2016) & (df.month==1))]
    df['Price_M'] = df.Price/1000000
    
    return df

# Merge Two dataframes

def merger(df1,df2):
    '''
    Returns a merged and preprocessed dataframe from two input dataframes
    '''
    
    df = pd.concat([df1, df2], axis=0, join_axes=[df2.columns if len(df2.columns)<=len(df1.columns) else df1.columns]) 
    df = data_processing(df)
    # Dropping any NaN rows:
    df = df.dropna()
    
    return df

