import pandas as pd
from sklearn import preprocessing
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import confusion_matrix
import pylogit as pl
from collections import OrderedDict
import numpy as np


class WorksetController:
    def __init__(self, view, logger):
        self.main_view = view
        self.logger = logger
        self.path = None
        self.df_view = None
        self.attr_view = None
        self.results_view = None
        self.training_attr_view = None
        self.df = None
        self.df_view_method = 'Head'
        self.df_view_no_of_rows = 5

    def set_file_path(self, path):
        self.path = path

    def get_file_path(self):
        return self.path

    def set_df_view(self, df_view):
        self.df_view = df_view

    def set_attr_view(self, attr_view):
        self.attr_view = attr_view

    def set_training_attr_view(self, view):
        self.training_attr_view = view

    def set_df_view_method(self, method):
        self.df_view_method = method

    def set_df_view_no_of_rows(self, rows_no):
        self.df_view_no_of_rows = rows_no

    def set_results_view(self, view):
        self.results_view = view

    def load_csv(self, path):
        try:
            self.set_file_path(path)
            self.df = pd.read_csv(path, low_memory=False)
            self.main_view.enable()
            self.refresh_views()
        except Exception as e:
            self.logger.write("The following exception occurred: %s" % e)
        else:
            self.logger.write('You opened the following file: %s' % path)

    def to_csv(self, path):
        try:
            self.df.to_csv(path, index=False)
        except Exception as e:
            self.logger.write("The following exception occurred %s" % e)
        else:
            self.logger.write('You saved the dataframe as: %s' % path)

    def refresh_views(self, attr_view_col="All"):
        self.refresh_df_view()
        self.refresh_attr_view(attr_view_col)
        self.refresh_training_attr_view()

    def refresh_training_attr_view(self):
        self.training_attr_view.DeleteAllItems()
        self.training_attr_view.populate()

    def refresh_df_view(self):
        self.df_view.clear()
        if self.df_view_method == 'Head':
            self.df_view.populate(self.df.head(self.df_view_no_of_rows))
        elif self.df_view_method == 'Tail':
            self.df_view.populate(self.df.tail(self.df_view_no_of_rows))

    def refresh_attr_view(self, column):
        self.attr_view.clear()
        if column == 'All':
            self.attr_view.populate_df(self.df.describe())
        else:
            attr_series = self.df[column].value_counts(dropna=False)
            self.attr_view.populate_series(attr_series)

    def replace(self, new_val, old_val, col):
        try:
            if new_val.isdigit():
                new_val = int(new_val)
            elif self.is_val_float(new_val):
                new_val = float(new_val)

            self.df[col] = self.df[col].replace(old_val, new_val)

            if old_val.isdigit():
                old_val = int(old_val)
            elif self.is_val_float(old_val):
                old_val = float(old_val)

            self.df[col] = self.df[col].replace(old_val, new_val)

            self.refresh_views(col)
        except Exception as e:
            self.logger.write("The following exception occurred: %s" % e)
        else:
            self.logger.write("%s was replaced with %s." % (old_val, new_val))

    def replace_all_others(self, new_val, old_vals, col, kept_val):
        try:
            if new_val.isdigit():
                new_val = int(new_val)
            elif self.is_val_float(new_val):
                new_val = float(new_val)
            for old_val in old_vals:
                self.df[col] = self.df[col].replace(old_val, new_val)
                if old_val.isdigit():
                    old_val = int(old_val)
                elif self.is_val_float(old_val):
                    old_val = float(old_val)
                self.df[col] = self.df[col].replace(old_val, new_val)
            self.refresh_views(col)
        except Exception as e:
            self.logger.write("The following exception occurred: %s" % e)
        else:
            self.logger.write("Replaced all values (except %s) with %s" % (kept_val, new_val))

    def get_df(self):
        return self.df

    def set_df(self, df):
        self.df = df

    def get_columns_list(self):
        ans = self.df.columns
        return list(ans)

    def update_df(self, name, op, val):
        try:
            if val.isdigit():
                val = int(val)
            if op == '=':
                self.df = self.df[(self.df[name] == val)]
            elif op == '<':
                self.df = self.df[(self.df[name] < val)]
            elif op == '<=':
                self.df = self.df[(self.df[name] <= val)]
            elif op == '>=':
                self.df = self.df[(self.df[name] >= val)]
            elif op == '>':
                self.df = self.df[(self.df[name] > val)]
            elif op == '!=':
                self.df = self.df[(self.df[name] != val)]
            self.refresh_df_view()
            self.refresh_attr_view(name)
        except Exception as e:
            self.logger.write("The following exception occurred: %s" % e)
        else:
            self.logger.write("New dataframe created where %s %s %s." % (name, op, val))

    def remove_nans(self, subset):
        try:
            old_df = self.get_df()
            new_df = old_df.dropna(subset=[subset])
            self.set_df(new_df)
            self.refresh_views(subset)
        except Exception as e:
            self.logger.write("The following exception occurred: %s" % e)
        else:
            self.logger.write("Removed records with missing values in %s" % subset)

    def add_feature(self, instructions):
        try:
            for line in instructions.splitlines():
                df = self.get_df()
                exec(line)
                self.set_df(df)
            self.refresh_views()
        except Exception as e:
            self.logger.write("The following exception occurred: %s" % e)
        else:
            self.logger.write("Successfully added feature")

    def create_dummies(self, column):
        try:
            df = self.get_df()
            dummies = pd.get_dummies(df[column])
            self.set_df(pd.concat([df, dummies], axis=1))
            self.refresh_views(column)
        except Exception as e:
            self.logger.write("The following exception occurred: %s" % e)
        else:
            self.logger.write("Successfully created dummies from %s" % column)

    def encode_labels(self, column):
        try:
            df = self.get_df()
            le = preprocessing.LabelEncoder()
            df[column] = le.fit_transform(list(df[column].array))
            self.set_df(df)
            self.refresh_views(column)
        except Exception as e:
            self.logger.write("The following exception occurred: %s" % e)
        else:
            self.logger.write("Successfully encoded labels for %s" % column)

    def random_forest(self, features_list, target, split):
        pd.set_option('mode.chained_assignment', None)

        df = self.get_df()
        race_id = 'race_id' if "race_id" in df.columns else "race.id" if "race.id" in df.columns else "racenum"
        training_treshold = float(split) * df[race_id].max()

        if target in features_list:
            features_list.remove(target)

        finish_time = "finish_time"

        train_data = df.loc[df[race_id] <= training_treshold]
        test_data = df.loc[df[race_id] > training_treshold]

        x_train = train_data[features_list]
        y_train = train_data[finish_time]

        x_test = test_data[features_list]
        y_test = test_data[finish_time]

        forest = RandomForestRegressor(n_estimators=100)
        output = forest.fit(x_train, y_train)

        test_data['pred_finish_time'] = forest.predict(x_test)
        if len(test_data[target].unique()) == 2:
            test_data['pred_result'] = test_data.groupby(race_id)['pred_finish_time'].transform(max) == test_data['pred_finish_time']
        else:
            test_data['pred_result'] = test_data.groupby(race_id)['pred_finish_time'].rank(ascending=True)

        test_data['pred_result'] = test_data['pred_result'].astype(int)

        self.draw_confusion_matrix(test_data[target],
                                   test_data['pred_result'])

        return output

    def mlogit(self, features_list, target, split):
        pd.set_option('mode.chained_assignment', None)

        df = self.get_df()

        race_id = 'race_id' if "race_id" in df.columns else "race.id" if "race.id" in df.columns else "racenum"
        training_treshold = float(split) * df[race_id].max()

        if target in features_list:
            features_list.remove(target)

        train_data = df.loc[df[race_id] <= training_treshold]
        test_data = df.loc[df[race_id] > training_treshold]

        spec = OrderedDict()
        for feature in features_list:
            spec[feature] = "all_same"

        obs_id_col = race_id
        alt_id_col = "draw" if "draw" in df.columns else "horse.ref" if "horse.ref" in df.columns else \
            "horse_ref" if "horse_ref" in df.columns else "postpos"
        choice_col = target

        if alt_id_col in spec.keys():
            spec.pop(alt_id_col)
        if obs_id_col in spec.keys():
            spec.pop(obs_id_col)
        if choice_col in spec.keys():
            spec.pop(choice_col)

        model = pl.create_choice_model(dlabata=train_data,
                                       alt_id_col=alt_id_col,
                                       obs_id_col=obs_id_col,
                                       choice_col=choice_col,
                                       specification=spec,
                                       model_type="MNL")
        output = model.fit_mle(np.zeros(len(spec.keys())), just_point=True)

        model_params = output['x']
        param_list = [model_params, None, None, None]
        predictions = model.predict(test_data, param_list=param_list)

        test_data['predictions'] = predictions
        test_data['pred_result'] = test_data.groupby(obs_id_col)['predictions'].transform(max) == test_data['predictions']

        test_data['pred_result'] = test_data['pred_result'].astype(int)

        self.draw_confusion_matrix(test_data[target],
                                   test_data['pred_result'])

        return output

    def draw_confusion_matrix(self, y_true, y_pred):
        conf_mat = confusion_matrix(y_true, y_pred)
        conf_mat_normalized = conf_mat.astype('float') / conf_mat.sum(axis=1)[:, np.newaxis]
        self.results_view.draw_confusion_mat(conf_mat_normalized)

    @staticmethod
    def is_val_float(element):
        try:
            float(element)
            return True
        except ValueError:
            return False
