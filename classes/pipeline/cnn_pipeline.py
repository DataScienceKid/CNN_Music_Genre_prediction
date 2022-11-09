import os
import numpy as np
import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions
from classes.options.cnn_options import CNNOptions
from classes.functions.functions import list_blobs, ReadFileContent, convert_single_file_to_audio_timeseries, \
    feature_engineering, GoogleCloudFunctions
import subprocess


class CNNPipeline:
    result = -1
    pipeline = None

    def create_pipeline(self, args):
        options = PipelineOptions(args)
        self.CNNOptions = options.view_as(CNNOptions)
        self.pipeline = beam.Pipeline(options=self.CNNOptions)

    def execute(self):
        # Options
        # bucket_name = CNNOptions.bucket_name
        bucket_name = "audio_tracks_w207_final_project_test"

        # Get a list of the tracks that are in the
        list_files = list_blobs(bucket_name)

        # Download the tracks from GCS Bucket into the local
        # Then convert mp3 audio files into audio time series numpy arrays
        # audio_time_series output is a list of tuples (time series - numpy array, scanning rate)
        audio_time_series = self.pipeline | "Download audio tracks from " >> ReadFileContent() | \
        "Transform audio files to audio time series (librosa-load)" >> \
        beam.FlatMap(convert_single_file_to_audio_timeseries)

        print(subprocess.check_output(['find', '.', '-name', '*.mp3']).decode("utf-8"))

        print(audio_time_series[0])

        unstiched_features = audio_time_series | "Extract features from audio time series" >> beam.FlatMap(feature_engineering)

        pipeline_result = self.pipeline.run()

        state = pipeline_result.wait_until_finish()

        np.array(unstiched_features).tofile("dataframe.csv", sep=",")

        os.system(f"gsutil -m cp dataframe.csv gs://{bucket_name}")

        self.result = GoogleCloudFunctions.data_flow_job_status(state)

        return self.result



