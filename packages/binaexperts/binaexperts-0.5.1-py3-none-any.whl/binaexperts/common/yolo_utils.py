import os
import sys
import importlib
import torch
import cv2
import numpy as np
from binaexperts.common.logger import get_logger

# Initialize the logger using the current module name.
logger = get_logger(__name__)

# Define absolute paths for the YOLO model assets (YOLOv5 and YOLOv7).
YOLO_MODELS = {
    "yolov5": os.path.abspath(os.path.join(os.path.dirname(__file__), "../SDKs/YOLO/yolov5")),
    "yolov7": os.path.abspath(os.path.join(os.path.dirname(__file__), "../SDKs/YOLO/yolov7")),
}


def set_yolo_path(model_type):
    """
    Dynamically adjust the system path to include only the directory of the specified YOLO model.

    This avoids conflicts between different YOLO versions by removing paths of other models
    and inserting the path for the chosen model at the beginning of sys.path.

    Parameters:
        model_type (str): The YOLO model type to use ('yolov5' or 'yolov7').
    """
    # Remove the paths of models that are not the selected one.
    for yolo_type, path in YOLO_MODELS.items():
        if yolo_type != model_type and path in sys.path:
            sys.path.remove(path)
    # Add the selected model's path to the system path if not already present.
    if YOLO_MODELS[model_type] not in sys.path:
        sys.path.insert(0, YOLO_MODELS[model_type])


def dynamic_import(module_path, class_name):
    """
    Dynamically import a module and retrieve a specific class or function from it.

    This allows for flexible imports where the module path or function may change.

    Parameters:
        module_path (str): The dot-separated path of the module.
        class_name (str): The name of the class or function to import.

    Returns:
        The imported class or function.
    """
    module = importlib.import_module(module_path)
    return getattr(module, class_name)


def fallback_letterbox(im, new_shape=(640, 640), stride=32, color=(114, 114, 114),
                       auto=True, scaleFill=False, scaleup=True):
    """
    Resize and pad an image using a letterbox technique to maintain aspect ratio.

    The function resizes the image to a new shape while preserving its aspect ratio,
    adding padding to reach the target dimensions. It returns the processed image,
    the scaling ratio, and the padding values.

    Parameters:
        im (np.array): The input image.
        new_shape (tuple or int): The desired output dimensions. If an integer is given,
                                  the image will be resized to (new_shape, new_shape).
        stride (int): The stride used during resizing (typically related to the model).
        color (tuple): The color for padding (in BGR format).
        auto (bool): Whether to automatically adjust padding.
        scaleFill (bool): Whether to scale the image to exactly fill the new shape.
        scaleup (bool): Whether to allow the image to be scaled up.

    Returns:
        tuple: (resized and padded image, scaling ratio, (dw, dh) padding values)
    """
    # Get current image height and width.
    shape = im.shape[:2]
    if isinstance(new_shape, int):
        new_shape = (new_shape, new_shape)
    # Determine the scaling ratio for resizing.
    r = min(new_shape[0] / shape[0], new_shape[1] / shape[1])
    if not scaleup:
        r = min(r, 1.0)
    # Compute the new dimensions after scaling.
    new_unpad = (int(round(shape[1] * r)), int(round(shape[0] * r)))
    # Calculate the padding needed to reach the desired shape.
    dw, dh = new_shape[1] - new_unpad[0], new_shape[0] - new_unpad[1]
    dw, dh = dw / 2, dh / 2

    # Resize the image if the new size is different.
    if shape[::-1] != new_unpad:
        im = cv2.resize(im, new_unpad, interpolation=cv2.INTER_LINEAR)

    # Determine padding values (top, bottom, left, right).
    top, bottom = int(round(dh - 0.1)), int(round(dh + 0.1))
    left, right = int(round(dw - 0.1)), int(round(dw + 0.1))
    # Apply border to the image with the specified padding and color.
    im = cv2.copyMakeBorder(im, top, bottom, left, right, cv2.BORDER_CONSTANT, value=color)

    return im, r, (dw, dh)


def preprocess_image(image_path, letterbox_func, device, infer_dims=(576, 576)):
    """
    Preprocess an image for inference.

    This function loads an image from the provided path, applies a letterbox resizing
    to maintain aspect ratio, converts the image from BGR to RGB format, rearranges the
    dimensions, normalizes pixel values, and converts it into a PyTorch tensor.

    Parameters:
        image_path (str): The file path of the image.
        letterbox_func (function): The letterbox function used for resizing and padding.
        device (torch.device): The device to which the tensor is moved (CPU or GPU).
        infer_dims (tuple): Target dimensions for the model inference.

    Returns:
        torch.Tensor: The preprocessed image tensor.

    Raises:
        FileNotFoundError: If the image file does not exist.
        ValueError: If the letterbox function is not provided.
    """
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"❌ Image file not found: {image_path}")
    if letterbox_func is None:
        raise ValueError("❌ Letterbox function is None. Model might not have been properly loaded.")

    # Read the image from disk.
    image = cv2.imread(image_path)
    # Apply letterbox resizing to the image.
    image_resized = letterbox_func(image, infer_dims, stride=32, auto=False)[0]
    # Convert from BGR to RGB and rearrange dimensions to (channels, height, width).
    image_resized = image_resized[:, :, ::-1].transpose(2, 0, 1)
    image_resized = np.ascontiguousarray(image_resized)
    # Convert the image to a PyTorch tensor and normalize pixel values.
    image_tensor = torch.from_numpy(image_resized).float() / 255.0
    image_tensor = image_tensor.unsqueeze(0).to(device)
    return image_tensor


def fallback_letterbox_yolov5(image, new_shape=(640, 640), stride=32, color=(114, 114, 114),
                              auto=True, scaleFill=False, scaleup=True):
    """
    A wrapper for the fallback_letterbox function specifically for YOLOv5.

    Parameters are identical to fallback_letterbox.

    Returns:
        tuple: The processed image, scaling ratio, and padding values.
    """
    return fallback_letterbox(image, new_shape, stride, color, auto, scaleFill, scaleup)


def fallback_letterbox_yolov7(image, new_shape=(640, 640), stride=32, color=(114, 114, 114),
                              auto=True, scaleFill=False, scaleup=True):
    """
    A wrapper for the fallback_letterbox function specifically for YOLOv7.

    Parameters are identical to fallback_letterbox.

    Returns:
        tuple: The processed image, scaling ratio, and padding values.
    """
    return fallback_letterbox(image, new_shape, stride, color, auto, scaleFill, scaleup)


def postprocess(outputs, image_path, scale_coords, display_size=(800, 600)):
    """
    Postprocess the model outputs to draw detection results on the image.

    This function loads the original image, scales the detection coordinates back to the
    original image size, draws bounding boxes and labels for each detected object, saves the
    annotated image, and then displays it.

    Parameters:
        outputs (list): The list of detections from the model.
        image_path (str): Path to the original image.
        scale_coords (function): Function to rescale coordinates from inference dimensions to original dimensions.
        display_size (tuple): The size for displaying the annotated image.

    Returns:
        str or None: The file path of the saved annotated image or None if no detections were made.

    Raises:
        FileNotFoundError: If the image file does not exist.
        RuntimeError: If the image cannot be loaded.
    """
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"❌ Image file not found: {image_path}")

    image = cv2.imread(image_path)
    if image is None:
        raise RuntimeError(f"❌ Failed to load image at: {image_path}")

    # Check if any detections are present.
    if outputs[0] is None or not len(outputs[0]):
        logger.info("⚠ No objects detected, skipping postprocessing.")
        return None

    # Process each detection.
    for det in outputs[0]:
        if det is None or det.shape[0] < 6:
            continue
        # Ensure detection is in the correct shape.
        if len(det.shape) == 1:
            det = det.unsqueeze(0)

        # Rescale bounding box coordinates to the original image dimensions.
        det[:, :4] = scale_coords((576, 576), det[:, :4], image.shape).round()

        # Draw bounding boxes and labels for each detection.
        for *xyxy, conf, cls in reversed(det):
            label = f"{int(cls)} {conf:.2f}"
            cv2.rectangle(image, (int(xyxy[0]), int(xyxy[1])),
                          (int(xyxy[2]), int(xyxy[3])), (0, 255, 0), 2)
            cv2.putText(image, label, (int(xyxy[0]), int(xyxy[1]) - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Save the resulting image with detections drawn.
    result_path = image_path.replace(".jpg", "_result.jpg")
    cv2.imwrite(result_path, image)

    # Resize the image for display and show it.
    image_resized = cv2.resize(image, display_size, interpolation=cv2.INTER_AREA)
    cv2.imshow("Detection Results", image_resized)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return result_path


def load_model_yolov5(model_path, device):
    """
    Dynamically load the YOLOv5 model and its utility functions.

    This function sets the appropriate system path for YOLOv5, imports the model loading
    function, loads the model from the provided path, moves it to the specified device, and
    sets it to evaluation mode. It also dynamically imports the non-max suppression and
    coordinate scaling utilities.

    Parameters:
        model_path (str): The file path to the YOLOv5 model.
        device (torch.device): The device to load the model onto.

    Returns:
        tuple: (model, non_max_suppression function, scale_coords function, fallback letterbox function for YOLOv5)

    Raises:
        FileNotFoundError: If the model file does not exist.
        ImportError: If the required utility functions cannot be imported.
    """
    set_yolo_path("yolov5")

    # Import the YOLOv5 model loading function from the experimental module.
    from binaexperts.SDKs.YOLO.yolov5.models.experimental import attempt_load as attempt_load_v5

    if not os.path.exists(model_path):
        raise FileNotFoundError(f"❌ Model file not found: {model_path}")

    logger.info(f"🟢 Loading YOLOv5 model from {model_path}")

    # Load the model (YOLOv5 does not require map_location for loading).
    model = attempt_load_v5(model_path)
    model.to(device)
    model.eval()

    # Dynamically import the non-max suppression and coordinate scaling functions.
    try:
        non_max_suppression = dynamic_import("binaexperts.SDKs.YOLO.yolov5.utils.general", "non_max_suppression")
        scale_coords = dynamic_import("binaexperts.SDKs.YOLO.yolov5.utils.general", "scale_coords")
    except ImportError as e:
        logger.error(f"❌ Error importing YOLOv5 utilities: {str(e)}")
        raise

    return model, non_max_suppression, scale_coords, fallback_letterbox_yolov5


def load_model_yolov7(model_path, device):
    """
    Dynamically load the YOLOv7 model and its utility functions.

    This function sets the appropriate system path for YOLOv7, imports the model loading
    function, loads the model from the provided path, moves it to the specified device, and
    sets it to evaluation mode. It also dynamically imports the non-max suppression and
    coordinate scaling utilities.

    Parameters:
        model_path (str): The file path to the YOLOv7 model.
        device (torch.device): The device to load the model onto.

    Returns:
        tuple: (model, non_max_suppression function, scale_coords function, fallback letterbox function for YOLOv7)

    Raises:
        FileNotFoundError: If the model file does not exist.
        ImportError: If the required utility functions cannot be imported.
    """
    set_yolo_path("yolov7")

    # Import the YOLOv7 model loading function from the experimental module.
    from binaexperts.SDKs.YOLO.yolov7.models.experimental import attempt_load as attempt_load_v7

    if not os.path.exists(model_path):
        raise FileNotFoundError(f"❌ Model file not found: {model_path}")

    logger.info(f"🟢 Loading YOLOv7 model from {model_path}")

    # Load the model using map_location to ensure proper device allocation.
    model = attempt_load_v7(model_path, map_location=device)
    model.to(device)
    model.eval()

    # Dynamically import the non-max suppression and coordinate scaling functions.
    try:
        non_max_suppression = dynamic_import("binaexperts.SDKs.YOLO.yolov7.utils.general", "non_max_suppression")
        scale_coords = dynamic_import("binaexperts.SDKs.YOLO.yolov7.utils.general", "scale_coords")
    except ImportError as e:
        logger.error(f"❌ Error importing YOLOv7 utilities: {str(e)}")
        raise

    return model, non_max_suppression, scale_coords, fallback_letterbox_yolov7
