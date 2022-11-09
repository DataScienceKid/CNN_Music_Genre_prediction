from google.cloud import storage
import google.auth
import apache_beam as beam
import librosa
import numpy as np
import logging
from apache_beam.runners.runner import PipelineState


def download_data_from_gcs(args):
    pass


def convert_single_file_to_audio_timeseries(track_file_name):
    data, sr = librosa.load(f"downloaded_tracks/{track_file_name}")
    yield data, sr


def feature_engineering(audio_timeseries_with_sr):
    audio_timeseries, sr = audio_timeseries_with_sr

    features_numpy_array = np.array([
        sr,
        np.mean(librosa.feature.chroma_stft(y=audio_timeseries)),
        np.var(librosa.feature.chroma_stft(y=audio_timeseries)),
        np.mean(librosa.feature.rms(y=audio_timeseries)),
        np.var(librosa.feature.rms(y=audio_timeseries)),
        np.mean(librosa.feature.rms(y=audio_timeseries)),
        np.var(librosa.feature.rms(y=audio_timeseries))
    ], dtype=float)

    yield features_numpy_array


def data_preparation():
    pass


def model_training():
    pass


def list_blobs(bucket_name, project):
    """Lists all the blobs in the bucket."""
    # GCP Credentials
    credentials, project = google.auth.default(
        scopes=['https://www.googleapis.com/auth/cloud-platform'])

    storage_client = storage.Client(credentials=credentials, project=project)
    blobs = storage_client.list_blobs(bucket_name)
    json_paths = []
    for blob in blobs:
        # json_paths.append(f"gs://{bucket_name}/{blob.name}")
        json_paths.append(f"{blob.name}")
    return json_paths


class ReadFileContent(beam.DoFn):

    def setup(self):
        # Called whenever the DoFn instance is deserialized on the worker.
        # This means it can be called more than once per worker because multiple instances of a given DoFn subclass may be created (e.g., due to parallelization, or due to garbage collection after a period of disuse).
        # This is a good place to connect to database instances, open network connections or other resources.
        self.storage_client = storage.Client()

    def process(self, *args, **kwargs):
        bucket_name = args[0]
        file_name = args[1]
        destination_file_name = f"downloaded_tracks/{file_name}"

        bucket = self.storage_client.get_bucket(bucket_name)
        blob = bucket.get_blob(file_name)
        yield blob.download_to_filename(destination_file_name)

class GoogleCloudFunctions:

    @staticmethod
    def data_flow_job_status(state):
        try:
            if state == PipelineState.DONE:
                return 0
            else:
                return -1
        except Exception as e:
            logging.error("Error in dataflowJobStatus method", exc_info=True)