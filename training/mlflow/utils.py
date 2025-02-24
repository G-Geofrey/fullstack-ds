import mlflow

def set_mlflow_tracking_uri(tracking_uri):
    if mlflow.is_tracking_uri_set():
        current_uri = mlflow.get_tracking_uri()
        if current_uri == tracking_uri:
            print(f"Tracking URI is already set to: {tracking_uri}")
        else:
            print("Overwritting existing tracking uri {current_uri}...")
    else:
        mlflow.set_tracking_uri(tracking_uri)
        print(f"Tracking URI set to: {tracking_uri}")
        
