import cv2
import torch
import time
from binaexperts.bina.services.inference_service import InferenceService


class LiveInference:
    """
    Perform live YOLO model inference on a video source (either a webcam or a video file).

    This class initializes video capture from a specified source, loads a YOLO model via the
    InferenceService, and processes each video frame in real time. Detected objects are highlighted
    with bounding boxes and labeled with their class and confidence score.
    """

    def __init__(self, model_type='yolov5', device='cuda', source=0):
        """
        Initialize the LiveInference class.

        Parameters:
            model_type (str): The type of YOLO model (e.g., 'yolov5'). Determines which model and assets are used.
            device (str): The computation device on which to run the model ('cpu' or 'cuda').
            source (int or str): The video source. Use 0 (or another integer) for a webcam or a file path for a video file.

        This method instantiates the InferenceService and initializes the video capture.
        """
        self.service = InferenceService(model_type=model_type, device=device)
        self.source = source
        self.cap = cv2.VideoCapture(self.source, cv2.CAP_V4L2)
        if not self.cap.isOpened():
            print(f"❌ Error: Unable to open video source {self.source}.")
            exit()

    def load_model(self, model_path):
        """
        Load the YOLO model.

        Parameters:
            model_path (str): The file path to the YOLO model weights.

        This method delegates the model loading to the underlying InferenceService.
        """
        self.service.load_model(model_path)

    def run(self, iou_thres=0.5, confidence_thres=0.5):
        """
        Perform real-time inference on a video stream.

        Parameters:
            iou_thres (float): The Intersection over Union (IoU) threshold used during non-maximum suppression.
            confidence_thres (float): The confidence threshold used to filter out weak detections.

        This method reads frames from the video capture, preprocesses each frame, performs inference using
        the YOLO model, applies non-maximum suppression (NMS) to filter overlapping detections, scales the
        bounding boxes back to the original frame dimensions, and displays the annotated frame.
        The loop exits if the video ends or if the user presses the 'q' key.
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

            h, w, _ = frame.shape

            image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image_tensor = torch.from_numpy(image_rgb).float() / 255.0
            image_tensor = image_tensor.permute(2, 0, 1).unsqueeze(0).to(self.service.device)

            with torch.no_grad():
                results = self.service.model(image_tensor)[0]

            outputs = self.service.non_max_suppression(results, conf_thres=confidence_thres, iou_thres=iou_thres)

            if outputs is None or len(outputs) == 0:
                print("⚠️ Warning: No objects detected.")
            else:
                for det in outputs:
                    if det is not None and len(det):
                        det[:, :4] = self.service.scale_coords(image_tensor.shape[2:], det[:, :4], frame.shape).round()

                        for *xyxy, conf, cls in det:
                            x1, y1, x2, y2 = map(int, xyxy)
                            x1, y1 = max(0, x1), max(0, y1)
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
