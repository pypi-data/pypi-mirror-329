from binaexperts.bina.services.inference_service import InferenceService


class local_inference:
    """
    A high-level wrapper that delegates inference tasks to the InferenceService.

    This class provides a simplified interface for loading a YOLO model and running
    inference on images. It abstracts the underlying complexity by delegating these tasks
    to an instance of InferenceService.
    """

    def __init__(self, model_type='yolov5', device='cpu'):
        """
        Initialize the image_inference instance.

        Parameters:
            model_type (str): Specifies the type of YOLO model to use, for example, 'yolov5' or 'yolov7'.
            device (str): The computation device on which the model should run (e.g., 'cpu' or 'cuda').

        During initialization, an InferenceService is instantiated with the provided model type and device.
        """
        self.service = InferenceService(model_type=model_type, device=device)

    def load_model(self, model_path):
        """
        Load the YOLO model from the specified file path.

        Parameters:
            model_path (str): The file path to the YOLO model.

        This method delegates the model loading task to the underlying InferenceService.
        If the model file is not found, the service's error handling (likely FileNotFoundError) will be triggered.
        """
        self.service.load_model(model_path)

    def predict(self, image_path, iou_thres=0.5, confidence_thres=0.5):
        """
        Run inference on the specified image using the loaded YOLO model.

        Parameters:
            image_path (str): The file path to the image on which inference should be performed.
            iou_thres (float): The Intersection over Union (IoU) threshold for non-max suppression.
                               Default value is 0.5.
            confidence_thres (float): The confidence threshold for filtering detections. Default is 0.5.
                                    (Note: Although provided as a parameter, the current implementation only
                                    passes the IoU threshold to the service.)

        Returns:
            The detection results produced by the InferenceService.

        This method delegates the prediction task to the underlying InferenceService,
        which handles image processing, model inference, and postprocessing.
        """
        return self.service.predict(image_path, iou_thres=iou_thres)
