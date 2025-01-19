import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score 
from sklearn.metrics import precision_score


class Predictor:
    def __init__(self, data):
        self.matches = pd.read_csv(data, index_col=0)
        self.rf = RandomForestClassifier(n_estimators=100, min_samples_split=10, random_state=1)




    def preprocess_data(self):
        #convert all the data we will use into numeric representations(preprossessing)
        self.matches['Venue_code'] = self.matches['Venue'].astype('category').cat.codes
        self.matches['Date'] = pd.to_datetime(self.matches['Date'])
        self.matches['Opp_code'] = self.matches['Opponent'].astype('category').cat.codes
        self.matches['Hour'] = self.matches['Time'].str.replace(':.+','',regex=True).astype('int')
        self.matches['Day_code'] = self.matches['Date'].dt.dayofweek

        choices = [2,1,0]

        conditions = [
            self.matches['Result'] == 'W',  
            self.matches['Result'] == 'D',  
            self.matches['Result'] == 'L'   
        ]

        self.matches['Target'] = np.select(conditions,choices, default=-1)

        #creating the model
        


        #create first set of predictions (going to be a bad prediction percentage)
        train = self.matches[self.matches['Date'] < '2023-08-01']
        test = self.matches[self.matches['Date'] > '2023-08-01']

        predictors = ['Venue_code','Opp_code','Hour','Day_code']

        self.rf.fit(train[predictors],train['Target'])



        preds = self.rf.predict(test[predictors])
        acc = accuracy_score(test['Target'], preds)
        print(acc)
        print(precision_score(test['Target'],preds, average=None))


        #use rolling averages in order to get better predictions 
        def rolling_averages(group,cols,new_cols):
            group = group.sort_values('Date')
            rolling_stats = group[cols].rolling(4,closed='left').mean()
            group[new_cols] = rolling_stats
            group = group.dropna(subset=new_cols)
            return group


        #testing out with liverpool 
        grouped_matches = self.matches.groupby('Team')
        group = grouped_matches.get_group('Liverpool')
        cols = ['GF', 'GA','Sh', 'SoT','Dist', 'FK', 'PK', 'PKatt']
        new_cols = [f"{c}_rolling" for c in cols]

        rolling_averages(group,cols,new_cols)

        #applying to all teams
        matches_rolling = self.matches.groupby('Team').apply(lambda x: rolling_averages(x, cols, new_cols))

        matches_rolling = matches_rolling.droplevel('Team')


        return matches_rolling, predictors, new_cols


    def make_predictions(self,data,predictors): 
        train = data[data['Date'] < '2023-08-01']
        test = data[data['Date'] > '2023-08-01']

        self.rf.fit(train[predictors],train['Target'])



        preds = self.rf.predict(test[predictors])
        combined = pd.DataFrame(dict(actual=test['Target'], prediction=preds))
        precision = precision_score(test['Target'],preds, average=None)

        return  combined, precision
    

    def create_final_df(self,combined,matches_rolling):
        combined = combined.merge(matches_rolling[['Date','Team','Opponent','Result']], left_index=True, right_index=True)
        #combined = combined.sort_values('Date')


'''
Prem_predictor = Predictor('backend/PremierLeague.csv')

matches_rolling, predictors, new_cols = Prem_predictor.preprocess_data()


combined, precision = Prem_predictor.make_predictions(matches_rolling, predictors + new_cols)
#print(combined)
#print(precision)
'''



