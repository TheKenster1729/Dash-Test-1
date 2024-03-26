import pandas as pd
import numpy as np
import plotly.graph_objects as go
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sql_utils import SQLConnection, DataRetrieval
from styling import Readability, Options
from tslearn.clustering import TimeSeriesKMeans

class InputOutputMapping:
    def __init__(self, output, region, scenario, year, df, threshold = 70, gt = True, num_to_plot = 5):
        self.output = output
        self.df = df
        self.scenario = scenario
        self.year = year
        self.y_continuous = self.df["Value"]
        self.threshold = threshold
        self.gt = gt
        self.inputs = pd.read_csv(r"Cleaned Data/InputsMaster.csv")
        self.num_to_plot = num_to_plot

        # need to remove input pop/gdp not relevant to this region
        self.region = region
        columns_to_remove = []
        for column in self.inputs.columns:
            signifiers = [" GDP", "Non-{} GDP".format(self.region), " Pop", "Non-{} Pop".format(self.region)]
            if any(signifier in column for signifier in signifiers) and self.region not in column:
                columns_to_remove.append(column)
        self.inputs = self.inputs.drop(columns = columns_to_remove)

        # some scenarios have runs that didn't solve in all cases, so remove those as well
        runs_to_drop_dict = {"percapita_consumption_loss_percent":
                             {"About15C_pes": [82, 98, 283, 305, 338, 373],
                             "15C_med": [184, 221, 314, 374, 383]}
                             }
        drop_runs = runs_to_drop_dict.get(self.output)
        if drop_runs:
            runs_to_drop_for_scenario = drop_runs.get(self.scenario)
            if runs_to_drop_for_scenario:
                self.inputs = self.inputs.drop(self.inputs[self.inputs["Run #"].isin(runs_to_drop_for_scenario)].index)

    def preprocess_for_classification(self):

        try:
            assert len(self.inputs) == len(self.y_continuous)
        except AssertionError:
            # will happen when runs have been removed, e.g. because of creating a custom variable
            # that produced a division by 0 error
            # infer missing run numbers and remove them
            existing_output_run_numbers_set = set(self.df["Run #"].values)
            existing_input_run_numbers_set = set(self.inputs["Run #"].values)
            inputs_to_keep = existing_input_run_numbers_set.intersection(existing_output_run_numbers_set)
            self.y_continuous = self.df[self.df["Run #"].isin(inputs_to_keep)]["Value"]
            self.inputs = self.inputs[self.inputs["Run #"].isin(inputs_to_keep)]

        X = self.inputs[self.inputs.columns[1:]]

        percentile = np.percentile(self.y_continuous, self.threshold)
        if self.gt:
            y_discrete = np.where(self.y_continuous.to_numpy() > percentile, 1, 0)
        else:
            y_discrete = np.where(self.y_continuous.to_numpy() < percentile, 1, 0)


        return X, y_discrete

    def CART(self):
        X, y = self.preprocess_for_classification()
        fit_model = DecisionTreeClassifier().fit(X, y)

        return fit_model

    def random_forest(self):
        X, y = self.preprocess_for_classification()
        fit_model = RandomForestClassifier(n_estimators = 100).fit(X, y)

        # get the average feature importances
        feature_importances = pd.DataFrame([estimator.feature_importances_ for estimator in fit_model.estimators_], columns = X.columns)
        sorted_labeled_importances = feature_importances.mean().sort_values(ascending = False)
        top_n = sorted_labeled_importances.index[:self.num_to_plot].to_list()

        return feature_importances, sorted_labeled_importances, top_n

class OutputOutputMapping:
    def __init__(self, output, region, scenario, year, df, db, threshold = 70, gt = True, num_to_plot = 5, other_outputs = []):
        self.output = output
        self.region = region
        self.scenario = scenario
        self.year = year
        self.df = df
        self.db_obj = db
        self.y_continuous = self.df["Value"]
        self.threshold = threshold
        self.gt = gt
        self.num_to_plot = num_to_plot
        self.other_outputs = other_outputs

    def preprocess_for_classification(self):
        # not all runs have solved in all regions and all scenarios
        # we need criteria that outputs must meet in order to be considered by the model
        # we also need to make sure run numbers are consistent

        # ensure the selected output is >350 data points
        # and that the majority of these are not 0
        if not len(self.df) > 350 :
            return "insufficient length (< 350)"
        
        if not len(self.df.query("Value==0")) < 175:
            return "too many (> half) zero values"
        
        # get the initial set of run numbers to use as a first filter for subsequent outputs
        target_output_run_numbers = self.df["Run #"]

        # create the X data frame for CART for this input/region/scenario/year combination
        main_df = pd.DataFrame(data = {"Run #": target_output_run_numbers})
        list_to_use = list(Options().outputs) + self.other_outputs
        list_to_use.remove(self.output)
        for output in list_to_use:
            df = DataRetrieval(self.db_obj, output, self.region, self.scenario, 2050).mapping_df()[["Run #", "Value"]]

            # only proceed if this new output includes at least all the solved runs of the target output
            target_runs_set = set(target_output_run_numbers.values)
            new_df_runs_set = set(df["Run #"].values)
            if target_runs_set.issubset(new_df_runs_set):
                # no need to verify length, we know it is at least 350 if target runs are a subset of new runs
                filtered_df = df[df["Run #"].isin(target_output_run_numbers)]["Value"].rename(output)
                main_df = pd.concat([main_df, filtered_df], axis = 1)
        
        percentile = np.percentile(self.y_continuous, self.threshold)
        if self.gt:
            y_discrete = np.where(self.y_continuous.to_numpy() > percentile, 1, 0)
        else:
            y_discrete = np.where(self.y_continuous.to_numpy() < percentile, 1, 0)
        
        self.main_df = main_df.drop(columns = "Run #")

        return y_discrete

    def random_forest(self):
        y = self.preprocess_for_classification()
        if type(y) is str:
            return y
        
        fit_model = RandomForestClassifier(n_estimators = 100).fit(self.main_df, y)

        # get the average feature importances
        feature_importances = pd.DataFrame([estimator.feature_importances_ for estimator in fit_model.estimators_], columns = self.main_df.columns)
        sorted_labeled_importances = feature_importances.mean().sort_values(ascending = False)
        top_n = sorted_labeled_importances.index[:self.num_to_plot].to_list()

        return feature_importances, sorted_labeled_importances, top_n
    
class TimeSeriesClustering:
    def __init__(self, df, output, region, scenario, n_clusters = 3, metric = "euclidean"):
        self.df = df
        self.output = output
        self.region = region
        self.scenario = scenario
        self.n_clusters = n_clusters
        self.df_for_clustering = self.df.pivot(columns = "Year", index = "Run #")
        self.metric = metric

    def generate_clusters(self):
        clusters = TimeSeriesKMeans(n_clusters = self.n_clusters, metric = self.metric).fit(self.df_for_clustering)

        return clusters
            

if __name__ == "__main__":
    db = SQLConnection("all_data_jan_2024")
    custom_output_example = "elec_prod_renewables_twh_pol-division-elec_prod_total_twh_pol-Renewable Share"
    
    # input-output-mapping
    # df = DataRetrieval(db, "emissions_CO2eq_total_million_ton_CO2eq", "GLB", "Ref", 2050).input_output_mapping_df()
    # io = InputOutputMapping("emissions_CO2eq_total_million_ton_CO2eq", "GLB", "Ref", 2050, df).random_forest()
    # print(io[-1])

    # time series clustering
    # time_series = TimeSeriesClustering(db, "emissions_CO2eq_total_million_ton_CO2eq", "GLB", "Ref")
    # clusters = time_series.plot_clusters()

    # output/output mapping
    df = DataRetrieval(db, "primary_energy_use_Biofuel_FirstGen_EJ", "GLB", "2C_med", 2050).mapping_df()
    res = OutputOutputMapping("primary_energy_use_Biofuel_FirstGen_EJ", "GLB", "2C_med", 2050, df, other_outputs = [custom_output_example]).random_forest()
    print(res[1])