import sys 
import warnings
import mlflow
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt
from PIL import Image
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score, confusion_matrix
from xgboost import XGBClassifier 
from mlflow.models import infer_signature
from hyperopt import STATUS_OK, hp, fmin, tpe, Trials

warnings.filterwarnings("ignore")


module_path = Path.home() /"Desktop/fullstack_ds"
sys.path.insert(1, module_path.as_posix())
from ds_utils  import ProjectDefinition
from utils import set_mlflow_tracking_uri

# Loading data
def load_data():
    data = load_breast_cancer()
    X = pd.DataFrame(data.data, columns=data.feature_names)
    y = data.target
    return train_test_split(X, y, test_size=0.25, random_state=42)

# Hyperopt tunning objective function
def objective(params):
    with mlflow.start_run(nested=True):
        params["max_depth"] = int(params["max_depth"])
        params["n_estimators"] = int(params["n_estimators"])
        
        clf = XGBClassifier(eval_metric="logloss", random_state=801, verbose=0, use_label_encoder=False, **params)
        clf.fit(X_train, y_train)   

        y_pred = clf.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)

        mlflow.log_params(params)
        mlflow.log_metric("accuracy", accuracy)
        mlflow.xgboost.log_model(clf, artifact_path="model", signature=signature)

        return {"loss": -accuracy, "status": STATUS_OK}

if __name__ == "__main__":
    # project definition
    project = "mlflow-basics"
    version = "0.0.1"
    description = "Mlflow basic logging"
    pdef = ProjectDefinition(project, version)

    space = {
        "n_estimators": hp.quniform("n_estimators", 50, 300, 10),
        "max_depth": hp.quniform("max_depth", 3, 15, 1),
        "learning_rate": hp.uniform("learning_rate", 0.01, 0.3),
        "subsample": hp.uniform("subsample", 0.5, 1.0),
        "colsample_bytree": hp.uniform("colsample_bytree", 0.5, 1.0),
    }

    X_train,  X_test, y_train, y_test = load_data()
    X_test.to_csv("test.csv", index=False)

    signature = infer_signature(X_test, y_test)

    # set up mlflow
    tracking_uri = "http://127.0.0.1:5000"
    set_mlflow_tracking_uri(tracking_uri)
    experiment = mlflow.set_experiment(pdef.experiment_name)


    with mlflow.start_run(run_name=pdef.get_run_name('Basic-Logging')):

        best_params = fmin(fn=objective, space=space, algo=tpe.suggest, max_evals=24, trials=Trials())

        # ensure integer values for n_estimators and max_depth
        best_params["n_estimators"] = int(best_params["n_estimators"])
        best_params["max_depth"] = int(best_params["max_depth"])

        # fit model
        model = XGBClassifier(eval_metric="logloss", random_state=42, verbose=0, use_label_encoder=False, **best_params)
        model.fit(X_train, y_train)

        # predictions 
        y_pred = model.predict(X_test)

        # metrices
        accuracy = accuracy_score(y_test, y_pred)
        f1_score = f1_score(y_test, y_pred)
        conf_matrix = confusion_matrix(y_test, y_pred)

        # logging
        ## log text
        mlflow.log_text("Mlflow logging overview: A Hypertopt tuning use case", "description.txt")

        ## log param 
        mlflow.log_param("learning_rate-key_pair", best_params["learning_rate"])

        ## log multiple parameters
        mlflow.log_params(best_params)

        ## log dictionary
        mlflow.log_dict(pdef.project_definition, "project_definition.json")

        ## log data
        data = mlflow.data.from_pandas(X_test)
        mlflow.log_input(data, context="testing")

        ## log figure 
        fig, ax = plt.subplots()
        ax.scatter(X_test["mean radius"], X_test["mean area"])
        plt.savefig("radius_vs_area.png")
        mlflow.log_figure(fig, "matplot_fig.png")

        ## log picture
        image = Image.open("radius_vs_area.png")
        mlflow.log_image(image, "figure.png")

        # log file
        file_path = "./test.csv"
        mlflow.log_artifact(file_path, "y_test.csv")

        # log all files in folder
        folder_path = "."
        mlflow.log_artifacts(folder_path)

        ## log model
        mlflow.xgboost.log_model(model, artifact_path="model", signature=signature)
