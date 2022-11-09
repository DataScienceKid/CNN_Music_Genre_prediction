from apache_beam.options.pipeline_options import PipelineOptions

class CNNOptions(PipelineOptions):
    @classmethod
    def _add_argparse_args(cls, parser):
        parser.add_argument("--bucket_name", required=True, type=str, help="bucket_name", dest="bucket_name")
