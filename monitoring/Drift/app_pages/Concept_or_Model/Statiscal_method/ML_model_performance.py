# import necessary libriary
import numpy as np
import pandas as pd
from sklearn.metrics import f1_score


class ConceptDriftDetector_with_PredictedProbability:
    def __init__(self, drift_threshold, reference_data_frame, new_data_frame):
        self.drift_threshold = drift_threshold
        self.reference_data_frame = reference_data_frame
        self.new_data_frame = new_data_frame

    def get_data_from_db(self):
        # Initialize reference and new data
        reference_data_frame = pd.DataFrame()
        new_data_frame = pd.DataFrame()

        # # from data base
        # # pipe_drd = pipelines.download_reference_data_pipe
        # # reference_data_frame = pipe_drd.fit_transform(reference_data_frame)
        # pipe_dnd = pipelines.download_new_data_pipe
        # new_data_frame = pipe_dnd.fit_transform(new_data_frame)
        # reference_data_frame = new_data_frame.copy().iloc[2:6]

        # # # from csv file
        # # reference_data_frame = pd.read_csv('./building_monitoring_app/reference_data.csv')
        # # new_data_frame = pd.read_csv('./building_monitoring_app/new_data.csv')

        reference_data_frame = self.reference_data_frame.copy()
        new_data_frame = self.new_data_frame.copy()

        # predicted probability for new and reference data
        ref_prob_list = np.random.randint(
            low=55, high=100, size=(reference_data_frame.shape[0], 1)
        )
        new_prob_list = np.random.randint(
            low=40, high=90, size=(new_data_frame.shape[0], 1)
        )

        # create new dataframe with list
        ref_prob_frame = pd.DataFrame(ref_prob_list, columns=["probability"])
        new_prob_frame = pd.DataFrame(new_prob_list, columns=["probability"])

        # concatenate new dataframe horizontaly
        reference_data_frame = pd.concat([reference_data_frame, ref_prob_frame], axis=1)
        new_data_frame = pd.concat([new_data_frame, new_prob_frame], axis=1)

        return reference_data_frame, new_data_frame

    def monitor_concept_drift(self):
        # get new data from data base
        new_data_frame = self.get_data_from_db()[1]

        # get new predict probability from data
        new_predicted_probabilities_list = []
        new_predicted_probabilities_list = new_data_frame["probability"].values.tolist()

        # Use the predicted probabilities or decisions to monitor for concept drift
        new_concept_drift_statut_list = []
        for pred_prob in range(len(new_predicted_probabilities_list)):
            if new_predicted_probabilities_list[pred_prob] >= self.drift_threshold:
                new_concept_drift_statut_list.append("Not Detected")
            else:
                new_concept_drift_statut_list.append("Detected")

        # create new dataframe with list
        new_concept_drift_statut_frame = pd.DataFrame(
            new_concept_drift_statut_list, columns=["concept_drift_statut"]
        )

        # concatenate new dataframe horizontaly
        new_data_with_concept_drift_statut_frame = pd.concat(
            [new_data_frame, new_concept_drift_statut_frame], axis=1
        )

        return new_data_with_concept_drift_statut_frame, new_concept_drift_statut_list

    def save_data_into_new_db(self, concept_drift_statut_list):
        # Your prediction logic here using the pre-trained model
        return

    def plot_performance(self):
        # plot predict probability of new data prediction and the drift threshold defined
        reference_data_frame, new_data_frame = self.get_data_from_db()

        # create dataframe to plot with list
        drift_threshold_list = [
            self.drift_threshold for _ in range(new_data_frame.shape[0])
        ]
        drift_threshold_frame = pd.DataFrame(
            drift_threshold_list, columns=["drift_threshold"]
        )

        # create dataframe to plot
        plot_reference_data_frame = pd.DataFrame(
            reference_data_frame["probability"].values.tolist(), columns=["probability"]
        )

        plot_new_data_frame = pd.DataFrame(
            new_data_frame["probability"].values.tolist(), columns=["probability"]
        )

        plot_drift_threshold_frame = pd.DataFrame(
            drift_threshold_frame["drift_threshold"].values.tolist(),
            columns=["drift_threshold"],
        )

        # add "index" column to dataframe
        plot_reference_data_frame["index"] = plot_reference_data_frame.index
        plot_new_data_frame["index"] = plot_new_data_frame.index
        plot_drift_threshold_frame["index"] = plot_drift_threshold_frame.index

        return (
            plot_reference_data_frame,
            plot_new_data_frame,
            plot_drift_threshold_frame,
        )


class ConceptDriftDetector_with_Accuracy:
    def __init__(
        self, drift_threshold, reference_data_frame, new_data_frame, target_true
    ):
        self.drift_threshold = drift_threshold
        self.reference_data_frame = reference_data_frame
        self.new_data_frame = new_data_frame
        self.target_true = target_true

    def get_data_from_db(self):
        # Initialize reference and new data
        reference_data_frame = pd.DataFrame()
        new_data_frame = pd.DataFrame()

        # # from data base
        # pipe_drd = pipelines.download_reference_data_pipe
        # pipe_dnd = pipelines.download_new_data_pipe
        # reference_data_frame = pipe_drd.fit_transform(reference_data_frame)
        # new_data_frame = pipe_dnd.fit_transform(new_data_frame)

        # # # from csv file
        # # reference_data_frame = pd.read_csv('./reference_data.csv')
        # # new_data_frame = pd.read_csv('./new_data.csv')

        reference_data_frame = self.reference_data_frame
        new_data_frame = self.new_data_frame

        return reference_data_frame, new_data_frame

    def monitor_concept_drift(self):
        # get new data from data base
        new_data_frame = self.get_data_from_db()[1]

        # get new predict probability from data
        new_predicted_accuracy = f1_score(
            y_true=self.target_true,
            y_pred=new_data_frame["survived"].values.tolist(),
            average="micro",
        )

        # Use the predicted probabilities or decisions to monitor for concept drift
        new_concept_drift_statut_list = []
        for pred_accur in range(len(new_data_frame["survived"].values.tolist())):
            if new_predicted_accuracy >= self.drift_threshold:
                new_concept_drift_statut_list.append("Not Detected")
            else:
                new_concept_drift_statut_list.append("Detected")

        # drift statut dictionary
        new_concept_drift_statut_dict = {
            "drift_threshold": [self.drift_threshold],
            "new_pred_accuracy": [new_predicted_accuracy],
            "drift_statut": [new_concept_drift_statut_list[0]],
        }

        # create new dataframe from dictionary
        new_concept_drift_statut_frame_to_plot = pd.DataFrame.from_dict(
            new_concept_drift_statut_dict
        )

        # create new dataframe with list
        new_concept_drift_statut_frame = pd.DataFrame(
            new_concept_drift_statut_list,
            columns=["concept_drift_statut_with_accuracy"],
        )

        # concatenate new dataframe horizontaly
        new_data_with_concept_drift_statut_frame = pd.concat(
            [new_data_frame, new_concept_drift_statut_frame], axis=1
        )

        return (
            new_data_with_concept_drift_statut_frame,
            new_concept_drift_statut_list,
            new_concept_drift_statut_frame_to_plot,
        )

    def save_data_into_new_db(self, concept_drift_statut_list):
        # Your prediction logic here using the pre-trained model
        return

    def plot_performance(self):
        # plot predict probability of new data prediction and the drift threshold defined
        reference_data_frame, new_data_frame = self.get_data_from_db()

        # create new dataframe of true target from list
        plot_target_true_frame = pd.DataFrame(self.target_true, columns=["target_true"])

        # create target predicted frame
        plot_target_predict_frame = pd.DataFrame(
            new_data_frame["survived"].values.tolist(), columns=["target_predicted"]
        )

        # create index frame
        plot_target_true_frame["index"] = plot_target_true_frame.index
        plot_target_predict_frame["index"] = plot_target_predict_frame.index

        return plot_target_predict_frame, plot_target_true_frame
