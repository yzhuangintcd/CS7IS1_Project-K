import pandas as pd 


if __name__ == '__main__':
    
    df_one = pd.read_csv('Museums__Collections___Archives_2015.csv')
    df_two = pd.read_csv('NMSMonumentsToVisit.csv')
    df_three = pd.read_csv('UNESCO_Sites_in_Ireland.csv')
        
    print("hello")