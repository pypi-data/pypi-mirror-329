from datetime import datetime


from mlgame.utils.azure import upload_data_to_azure_blob, upload_data_to_azure_blob_by_container


def test_upload_to_azure_blob():
    az_container_url = "https://paialocal.blob.core.windows.net/upload?sv=2023-11-03&st=2024-12-20T02%3A07%3A09Z&se=2024-12-21T02%3A07%3A09Z&sr=c&sp=racwl&sig=%2FEZeF8xflktrzykm9YZsEkhGH4xG1pih7b0wNxTrQQ4%3D"
    current_time = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    blob_name = f"upload/blob_{current_time}.json"
    data = {"key": "value"}
    upload_data_to_azure_blob_by_container(az_container_url, blob_name, [data])

def test_create_new_file_in_azure_blob():
    file_name = "03.json"
    az_blob_url = "https://paialocal.blob.core.windows.net/upload/test?sp=racw&st=2024-12-20T08:37:07Z&se=2024-12-20T16:37:07Z&spr=https&sv=2022-11-02&sr=d&sig=Gz2GL2uQEjdcFeQNpbN6VnRWvDY5Dp0Xv0srqy%2Fqb3Q%3D&sdd=1"

    data = {"key": "value"}
    
    upload_data_to_azure_blob(az_blob_url, file_name, [data])