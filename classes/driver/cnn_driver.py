from classes.pipeline.cnn_pipeline import CNNPipeline
from classes.constants import constants

class CNNDriver:
    def processor(self, argv):
        execution_mode = argv[1]
        print("execution_mode == execution_mode")
        
        if execution_mode == constants.cnn_model_processor:
            pipeline = CNNPipeline()
            pipeline.create_pipeline(argv[2:])
            result = pipeline.execute()
        else:
            print(f"execution mode not matching constants.{constants.cnn_model_processor}")
            return -1