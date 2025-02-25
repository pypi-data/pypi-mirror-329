# binaexperts/app/inference/inference.py (updated)
import cv2
import torch
import numpy as np
import time
from .base import BaseInference
from binaexperts.common.yolo_utils import save_annotated_image  # Import the new utility

class Inference:
    """
    A unified class for performing both local (static image) and live (video) YOLO model inference.
    """

    def __init__(self, model_type='yolov5', device='cpu', model_path=None, iou=0.5, confidence_thres=0.5):
        """
        Initialize the Inference class.

        Parameters:
            model_type (str): The type of YOLO model (e.g., 'yolov5').
            device (str): The computation device ('cpu' or 'cuda').
            model_path (str): The file path to the YOLO model weights.
            iou (float): The Intersection over Union (IoU) threshold for non-max suppression.
            confidence_thres (float): The confidence threshold for filtering detections.
        """
        self.model_type = model_type
        self.device = device
        self.iou = iou
        self.confidence_thres = confidence_thres
        self.model_path = model_path

        # Initialize base inference for shared functionality
        self.base = BaseInference(model_type=model_type, device=device)

        if model_path:
            self.base.load_model(model_path)

    def local_inference(self, image_path, destination=None, output_format="jpg"):
        """
        Run inference on a static image and optionally save the annotated image with a specified format.

        Parameters:
            image_path (str): The file path to the image on which inference should be performed.
            destination (str, optional): The file path to save the annotated image (without extension). If None, only return results.
            output_format (str, optional): The format for the saved image (e.g., 'jpg', 'jpeg', 'png'). Default is 'jpg'.

        Returns:
            List of detection results.
        """
        print(f"Output format in Inference.local_inference: {output_format}")  # Debug print
        print(f"Full call args: image_path={image_path}, destination={destination}, output_format={output_format}")
        # Create an instance of local_inference
        local_infer = local_inference(model_type=self.model_type, device=self.device)
        if self.model_path:
            local_infer.load_model(self.model_path)
        return local_infer.predict(image_path, iou_thres=self.iou, confidence_thres=self.confidence_thres,
                                   destination=destination, output_format=output_format)

    def live_inference(self, source=0):
        """
        Perform real-time inference on a video source (webcam or video file).

        Parameters:
            source (int or str): The video source (0 for webcam or a file path for a video file).
        """
        # Create an instance of LiveInference
        live_infer = LiveInference(model_type=self.model_type, device=self.device, source=source)
        if self.model_path:
            live_infer.load_model(self.model_path)
        live_infer.run(iou_thres=self.iou, confidence_thres=self.confidence_thres)


class local_inference(BaseInference):
    """
    A high-level wrapper that delegates inference tasks to the InferenceService.

    This class provides a simplified interface for loading a YOLO model and running
    inference on images.
    """

    def predict(self, image_path, iou_thres=0.5, confidence_thres=0.5, destination=None, output_format="jpg"):
        """
        Run inference on the specified image using the loaded YOLO model and optionally save the annotated image with a specified format.

        Parameters:
            image_path (str): The file path to the image on which inference should be performed.
            iou_thres (float): The Intersection over Union (IoU) threshold for non-max suppression.
                               Default value is 0.5.
            confidence_thres (float): The confidence threshold for filtering detections. Default is 0.5.
            destination (str, optional): The file path to save the annotated image (without extension). If None, only return results.
            output_format (str, optional): The format for the saved image (e.g., 'jpg', 'jpeg', 'png'). Default is 'jpg'.

        Returns:
            The detection results produced by the InferenceService.
        """
        print(f"Output format parameter: {output_format}")  # Debug print
        print(f"Full predict args: image_path={image_path}, iou_thres={iou_thres}, confidence_thres={confidence_thres}, destination={destination}, output_format={output_format}")

        # Get post-NMS results from InferenceService (already processed with NMS)
        results = self.service.predict(image_path, iou_thres=iou_thres)

        # Load the original image to annotate
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError(f"Could not load image at {image_path}")

        # Get the letterbox dimensions used during preprocessing (default from YOLOv5)
        infer_dims = (576, 576)  # Default inference dimensions from yolo_utils.preprocess_image

        # Annotate the image with detections (using the post-NMS results)
        annotated = False
        if results and len(results) > 0 and results[0] is not None:
            det_tensor = results[0]  # Access the first tensor in the list (post-NMS results)
            if len(det_tensor.shape) == 2 and det_tensor.shape[1] == 6:  # Ensure shape is [num_detections, 6]
                for det in det_tensor:  # Iterate over each detection row
                    x1, y1, x2, y2, conf, cls = det.tolist()  # Convert tensor row to list for unpacking
                    # Create a 2D tensor for coordinates with shape [1, 4], using the service's device
                    coords = torch.tensor([[x1, y1, x2, y2]], device=self.service.device)
                    # Scale coordinates back to original image dimensions using scale_coords
                    scaled_coords = self.service.scale_coords(infer_dims, coords, image.shape[:2])
                    x1, y1, x2, y2 = map(int, scaled_coords[0].tolist())  # Extract first (and only) row
                    x1, y1 = max(0, x1), max(0, y1)
                    h, w = image.shape[:2]
                    x2, y2 = min(w - 1, x2), min(h - 1, y2)
                    print(
                        f"✅ Detected Object: x1={x1}, y1={y1}, x2={x2}, y2={y2}, conf={conf:.2f}, class={cls}")
                    cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    label = f"Class {int(cls)}: {conf:.2f}"
                    cv2.putText(image, label, (x1, max(10, y1 - 10)), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                                (0, 255, 0), 2)
                annotated = True
            else:
                logger.warning("⚠ Unexpected detection tensor shape or format, skipping annotation.")
        else:
            logger.warning("⚠ No detections found or results are invalid, skipping annotation.")

        # Save the annotated image if destination is provided, using the utility function
        if destination:
            try:
                save_annotated_image(image, destination, output_format)
            except Exception as e:
                logger.error(f"❌ Error saving annotated image: {str(e)}")
                raise

        return results if results is not None and len(results) > 0 and results[0] is not None else None


class LiveInference(BaseInference):
    """
    Perform live YOLO model inference on a video source (webcam or video file).
    """

    def __init__(self, model_type='yolov5', device='cuda', source=0):
        """
        Initialize the LiveInference class.

        Parameters:
            model_type (str): The type of YOLO model (e.g., 'yolov5').
            device (str): The computation device ('cpu' or 'cuda').
            source (int or str): The video source (0 for webcam or a file path for a video file).
        """
        super().__init__(model_type=model_type, device=device)
        self.source = source
        self.cap = cv2.VideoCapture(self.source, cv2.CAP_V4L2)
        if not self.cap.isOpened():
            print(f"❌ Error: Unable to open video source {self.source}.")
            exit()

    def run(self, iou_thres=0.5, confidence_thres=0.5):
        """
        Perform real-time inference on a video stream.
        """
        prev_frame_time = 0

        while True:
            ret, frame = self.cap.read()
            if not ret:
                print("❌ Error: Failed to retrieve frame, ending video stream.")
                break

            new_frame_time = time.time()
            if prev_frame_time != 0:
                fps = 1 / (new_frame_time - prev_frame_time)
            else:
                fps = 0
            prev_frame_time = new_frame_time

            cv2.putText(frame, f"FPS: {int(fps)}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

            image_tensor = self._preprocess_image(frame)
            with torch.no_grad():
                results = self.service.model(image_tensor)[0]

            detections = self._postprocess_detections(results, frame.shape, iou_thres, confidence_thres)

            if not detections:
                print("⚠️ Warning: No objects detected.")
            else:
                for det in detections:
                    x1, y1, x2, y2, conf, cls = map(float, det)
                    x1, y1, x2, y2 = map(int, [x1, y1, x2, y2])
                    x1, y1 = max(0, x1), max(0, y1)
                    h, w = frame.shape[:2]
                    x2, y2 = min(w - 1, x2), min(h - 1, y2)
                    print(
                        f"✅ Detected Object: x1={x1}, y1={y1}, x2={x2}, y2={y2}, conf={conf:.2f}, class={cls}")
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    label = f"Class {int(cls)}: {conf:.2f}"
                    cv2.putText(frame, label, (x1, max(10, y1 - 10)), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                                (0, 255, 0), 2)

            cv2.imshow("Live Inference", frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        self.cap.release()
        cv2.destroyAllWindows()