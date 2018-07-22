import pandas as pd
#from CanFrame import CanFrame

class DfProcess:
    def __init__(self, df=pd.DataFrame()):
        self._df = df
        #self.f = open('temp.txt', 'r', encoding='utf-8')

    def test(self):
        #self._df = CanFrame().get_dataframe_original(self.f.readlines())
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

