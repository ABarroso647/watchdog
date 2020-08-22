#from google.cloud import storage
from flask import Flask, jsonify
from flask import request
'''
    def download_blob(bucket_name, source_blob_name, destination_file_name):
    """Downloads a blob from the bucket."""
    # bucket_name = "your-bucket-name"
    # source_blob_name = "storage-object-name"
    # destination_file_name = "local/path/to/file"
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(source_blob_name)
    blob.download_to_filename(destination_file_name)

    print(
        "Blob {} downloaded to {}.".format(
            source_blob_name, destination_file_name
        )
    )
'''
app = Flask(__name__)
@app.route('/', methods=['POST'])
def hello_world():
    data = request.data
    return data
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')