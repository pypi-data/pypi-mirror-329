# binaexperts/app/inference/base.py
from binaexperts.app.services.inference_service import InferenceService
import cv2
import torch
import numpy as np

class BaseInference:
    """
    A base class for inference-related functionality using YOLO models.
    """

    def __init__(self, model_type='yolov5', device='cpu'):
        """
        Initialize the base inference class with a model type and device.

        Parameters:
            model_type (str): The type of YOLO model (e.g., 'yolov5').
            device (str): The computation device ('cpu' or 'cuda').
        """
        self.service = InferenceService(model_type=model_type, device=device)

    def load_model(self, model_path):
        """
        Load the YOLO model from the specified path.

        Parameters:
            model_path (str): The file path to the YOLO model weights.
        """
        self.service.load_model(model_path)

    def _preprocess_image(self, image):
        """
        Preprocess an image or frame for inference.

        Parameters:
            image: Input image (numpy array for OpenCV or torch tensor).

        Returns:
            torch.Tensor: Preprocessed image tensor ready for inference.
        """
        if isinstance(image, np.ndarray):  # Assuming OpenCV format (BGR)
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            image_tensor = torch.from_numpy(image_rgb).float() / 255.0
            image_tensor = image_tensor.permute(2, 0, 1).unsqueeze(0).to(self.service.device)
        return image_tensor

    def _postprocess_detections(self, outputs, original_shape, iou_thres=0.5, confidence_thres=0.5):
        """
        Postprocess detection outputs, applying NMS and scaling boxes.

        Parameters:
            outputs: Model detection outputs.
            original_shape: Shape of the original image or frame (height, width).
            iou_thres (float): IoU threshold for non-max suppression.
            confidence_thres (float): Confidence threshold for filtering detections.

        Returns:
            List of detections with scaled coordinates.
        """
        if outputs is None or len(outputs) == 0:
            return []

        detections = self.service.non_max_suppression(outputs, conf_thres=confidence_thres, iou_thres=iou_thres)
        if detections is None or len(detections) == 0:
            return []

        h, w = original_shape[:2]
        scaled_detections = []
        for det in detections:
            if det is not None and len(det):
                det[:, :4] = self.service.scale_coords((h, w), det[:, :4], (h, w)).round()
                scaled_detections.extend(det.tolist())
        return scaled_detections