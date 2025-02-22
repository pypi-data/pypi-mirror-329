import os
import torch
from binaexperts.common.logger import get_logger
from binaexperts.common.yolo_utils import (
    preprocess_image, postprocess, fallback_letterbox_yolov5, fallback_letterbox_yolov7,
    load_model_yolov5, load_model_yolov7
)

logger = get_logger(__name__)

class InferenceService:
    def __init__(self, model_type="yolov5", device=None):
        """
        Initialize the inference service.

        :param model_type: Type of YOLO model ('yolov5' or 'yolov7').
        :param device: Device to run inference ('cuda' or 'cpu').
        """
        self.model_type = model_type.lower()
        self.device = torch.device("cuda" if torch.cuda.is_available() and device != "cpu" else "cpu")
        self.model = None
        self.non_max_suppression = None
        self.scale_coords = None
        self.letterbox = None
        logger.info(f"🟢 Using device: {self.device}")

    def load_model(self, model_path: str):
        """
        Load the YOLO model along with associated functions.

        :param model_path: Path to the YOLO model weights.
        """
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"❌ Model file not found: {model_path}")

        if self.model_type == "yolov5":
            self.model, self.non_max_suppression, self.scale_coords, self.letterbox = load_model_yolov5(model_path, self.device)
        elif self.model_type == "yolov7":
            self.model, self.non_max_suppression, self.scale_coords, self.letterbox = load_model_yolov7(model_path, self.device)
        else:
            raise ValueError(f"❌ Unsupported model type: {self.model_type}")

        logger.info(f"✅ {self.model_type.upper()} Model loaded successfully.")

        # Check and set the default letterbox function if None
        if self.letterbox is None:
            logger.warning(f"⚠ Letterbox function is None for {self.model_type}. Using fallback.")
            self.letterbox = fallback_letterbox_yolov5 if self.model_type == "yolov5" else fallback_letterbox_yolov7

        logger.info(f"🟢 Letterbox function set successfully: {self.letterbox}")

    def predict(self, image_path, iou_thres=0.5, confidence_thres=0.5):
        """
        Runs inference on a given image.

        :param image_path: Path to the image file.
        :param iou_thres: IoU threshold for non-max suppression.
        :param confidence_thres: Confidence threshold for object detection.
        :return: Processed results.
        """
        if self.model is None:
            raise RuntimeError("❌ Model is not loaded. Call load_model() first.")

        if not os.path.exists(image_path):
            raise FileNotFoundError(f"❌ Image file not found: {image_path}")

        logger.info(f"🟢 Running inference on {image_path}")

        if self.letterbox is None:
            raise RuntimeError("❌ Letterbox function is None. Ensure the model is correctly initialized.")

        # Process the image
        image_tensor = preprocess_image(image_path, self.letterbox, self.device)

        with torch.no_grad():
            outputs = self.model(image_tensor)[0]

        logger.info(f"🟢 Raw model output shape: {outputs.shape}")

        # Validate outputs before further processing
        if outputs is None or len(outputs) == 0:
            logger.warning("⚠ Model did not return any outputs. Skipping postprocessing.")
            return None

        # Adjust output shape for NMS compatibility
        if len(outputs.shape) == 2:
            outputs = outputs.unsqueeze(0)

        logger.info(f"🟢 Adjusted model output shape: {outputs.shape}")

        # Apply Non-Max Suppression
        outputs = self.non_max_suppression(outputs, conf_thres=confidence_thres, iou_thres=iou_thres)

        logger.info(f"🟢 Model output after NMS: {outputs}")

        # Process and return the final results
        return postprocess(outputs, image_path, self.scale_coords)
