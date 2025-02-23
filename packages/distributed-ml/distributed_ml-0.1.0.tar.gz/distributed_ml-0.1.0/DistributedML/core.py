import requests
import time

API_URL = "http://localhost:5001/execute_task"
STATUS_URL = "https://your-api.com/status"

# payload = {
#     "algorithm": "RandomForest",
#     "dataset_id": "dataset1",
#     "hyperparameters": {"n_estimators": "100", "max_depth": "5"}
# }


def DisGridSearch(data):
    """
    Sends data to a backend API and polls for real-time status updates.

    Args:
        data (dict): The data to send for training.

    Returns:
        dict: The final response from the backend.
    """
    response = requests.post(API_URL, json=data)
    if response.status_code != 200:
        raise Exception(f"Failed to start training: {response.text}")

    print(response)

    # while True:
    #     # status_response = requests.get(f"{STATUS_URL}/{job_id}")
    #     if status_response.status_code != 200:
    #         raise Exception("Failed to fetch status.")
    #
    #     status = status_response.json()
    #     print(f"Training Status: {status['status']}")
    #
    #     if status["status"] in ["COMPLETED", "FAILED"]:
    #         return status
    #
    #     time.sleep(5)  # Poll every 5 seconds
