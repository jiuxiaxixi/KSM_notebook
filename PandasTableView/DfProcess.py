import pandas as pd
from CanFrame import CanFrame


class DfProcess:
    def __init__(self, df=pd.DataFrame()):
        self._df = df
        self.f = open('temp.txt', 'r', encoding='utf-8')

        #self.test()

    def test(self):
        self._df = CanFrame().get_dataframe_original(self.f.readlines())
        return self._df

    def filter1_df(self, column, value, df_filter=pd.DataFrame()):
        if column in df_filter.columns:
            return df_filter[df_filter[column] == value]
        else:
            print(column+" not find !!")
            return pd.DataFrame()

    def filter2_df(self, column1, value1, column2, value2, df_filter=pd.DataFrame()):
        if value1 != '' and value2 == '':
            return self.filter1_df(column1, value1, df_filter)

        if value1 == '' and value2 != '':
            return self.filter1_df(column2, value2, df_filter)

        temp_df = self.filter1_df(column1, value1, df_filter)
        return self.filter1_df(column2, value2, temp_df)

    def save_to_text(self, filename, df=pd.DataFrame()):
        df.to_csv(filename, header=False, index=False, sep=' ', mode='a')

    def dataframe_to_numpy(self,df=pd.DataFrame(),colunm=''):
        if colunm in df.columns:
            return df[colunm].apply(self.hex_to_dec).values

    def hex_to_dec(self, x):
        return int(x, 16)

    def numpy_merge(self, df=pd.DataFrame(), high_column='', low_column=''):

        if high_column in df.columns and low_column in df.columns:
            merge_value = df[high_column]+ df[low_column]
            return merge_value.apply(self.hex_to_dec).values
        else:
            print("column not found :"+ high_column+ " "+ low_column)



#df = DfProcess().test()
#data = DfProcess().numpy_merge(df,'d2','d3')
