import io
import os
import zipfile
import json
import yaml
import datetime
from struct import unpack
from typing import Tuple, Union, IO
from jsonschema import validate, ValidationError
from binaexperts.convertors import const

def detect_format(source: Union[str, IO[bytes]]) -> str:
    """
    Detect the format of the dataset based on specific files or directories within the source.

    :param source: The source dataset, either as a file path or an in-memory object (BytesIO).
    :return: Detected format type (e.g., 'yolo', 'coco', 'binaexperts').
    :raises ValueError: If the format cannot be determined.
    """
    if isinstance(source, str) and zipfile.is_zipfile(source):
        with zipfile.ZipFile(source, 'r') as zip_ref:
            file_list = zip_ref.namelist()
    elif isinstance(source, IO):
        # For in-memory bytes, we need to work with zip content directly
        source.seek(0)
        with zipfile.ZipFile(source, 'r') as zip_ref:
            file_list = zip_ref.namelist()
    else:
        raise

    # Detect format by checking for unique identifiers in the file list
    if any("cocos/" in filename for filename in file_list):
        return const.CONVERTOR_FORMAT_BINAEXPERTS
    elif any("data.yaml" == os.path.basename(filename) for filename in file_list):
        return const.CONVERTOR_FORMAT_YOLO
    elif any("_annotations.coco.json" in filename for filename in file_list):
        return const.CONVERTOR_FORMAT_COCO
    else:
        raise


def extract_zip(zip_path: str, extract_to: str) -> None:
    """
    Extracts all files from a zip archive to the specified directory.

    :param zip_path: Path to the zip archive file.
    :param extract_to: Directory where the files should be extracted.
    """
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)


def get_image_dimensions(image_bytes: bytes) -> Tuple[int, int]:
    """
    Get dimensions (width, height) of an image from its byte content.

    :param image_bytes: Byte content of the image.
    :return: A tuple containing the width and height of the image.
    """
    if len(image_bytes) < 10:
        return const.DEFAULT_WIDTH, const.DEFAULT_HEIGHT

    with io.BytesIO(image_bytes) as img_file:
        img_file.seek(0)
        img_file.read(2)
        b = img_file.read(1)
        try:
            max_iterations, iteration_count = 100, 0
            while b and b != b'\xDA':
                iteration_count += 1
                if iteration_count > max_iterations:
                    return const.DEFAULT_WIDTH, const.DEFAULT_HEIGHT

                while b != b'\xFF':
                    b = img_file.read(1)
                while b == b'\xFF':
                    b = img_file.read(1)
                if b >= b'\xC0' and b <= b'\xC3':
                    img_file.read(3)
                    h, w = unpack('>HH', img_file.read(4))
                    return w, h
                else:
                    segment_length = unpack('>H', img_file.read(2))[0]
                    if segment_length <= 2:
                        return const.DEFAULT_WIDTH, const.DEFAULT_HEIGHT
                    img_file.read(segment_length - 2)
                b = img_file.read(1)
        except Exception:
            return const.DEFAULT_WIDTH, const.DEFAULT_HEIGHT


def validate_data(instance: dict, schema: dict, context: str = "") -> bool:
    """
    Validates JSON data against a schema.

    :param instance: JSON data instance to validate.
    :param schema: JSON schema to validate against.
    :param context: Context or label for the data, such as a split name.
    :return: True if valid, False otherwise.
    """
    try:
        validate(instance=instance, schema=schema)
        return True
    except ValidationError:
        return False


def load_json_from_source(source: Union[str, zipfile.ZipFile], path: str) -> dict:
    """
    Load JSON data from a file or a zip source.

    :param source: File path or open ZipFile object.
    :param path: Path within the source to the JSON file.
    :return: Loaded JSON data as a dictionary.
    """
    if isinstance(source, zipfile.ZipFile):
        with source.open(path) as file:
            return json.load(file)
    else:
        with open(path, 'r') as file:
            return json.load(file)


def create_zip_writer(destination: Union[str, IO[bytes]]) -> zipfile.ZipFile:
    """
    Creates and returns a ZipFile object for the specified destination.

    :param destination: File path or in-memory buffer where the zip will be written.
    :return: A zipfile.ZipFile object opened for writing.
    """
    if isinstance(destination, str) and not destination.lower().endswith('.zip'):
        destination += '.zip'
    return zipfile.ZipFile(destination, 'w')


def convert_bbox_yolo_to_coco(annotation: dict, img_width: int, img_height: int) -> list:
    """
    Convert YOLO bbox (cx, cy, w, h) to COCO bbox (x, y, w, h).

    :param annotation: Dictionary with YOLO bbox data.
    :param img_width: Image width in pixels.
    :param img_height: Image height in pixels.
    :return: COCO-formatted bbox as [x, y, width, height].
    """
    cx, cy, w, h = annotation[const.CX_KEY], annotation[const.CY_KEY], annotation[const.WIDTH_BOX_KEY], annotation[const.HEIGHT_BOX_KEY]
    x = (cx - w / 2) * img_width
    y = (cy - h / 2) * img_height
    return [x, y, w * img_width, h * img_height]


def convert_bbox_to_yolo_format(bbox: list, img_width: int, img_height: int) -> list:
    """
    Convert COCO bbox (x, y, w, h) to YOLO bbox (cx, cy, w, h) format.

    :param bbox: COCO bbox as [x, y, width, height].
    :param img_width: Image width in pixels.
    :param img_height: Image height in pixels.
    :return: YOLO-formatted bbox as [cx, cy, width, height].
    """
    x, y, w, h = bbox
    cx = (x + w / 2) / img_width
    cy = (y + h / 2) / img_height
    width = w / img_width
    height = h / img_height
    return [round(val, 6) for val in (cx, cy, width, height)]


def process_segmentation_data(segmentation: list, img_width: int, img_height: int) -> list:
    """
    Normalize segmentation data points to YOLO format.

    :param segmentation: List of segmentation points.
    :param img_width: Image width in pixels.
    :param img_height: Image height in pixels.
    :return: Normalized segmentation data.
    """
    yolo_segmentation = []
    if isinstance(segmentation, list):
        for seg in segmentation:
            if isinstance(seg, list):
                normalized_seg = [
                    coord / img_width if i % 2 == 0 else coord / img_height
                    for i, coord in enumerate(seg)
                ]
                yolo_segmentation.append(normalized_seg)
    return yolo_segmentation


def generate_yaml_content(class_names: list) -> str:
    """
    Generate precise content for a YOLO dataset YAML configuration file.

    :param class_names: List of class names.
    :return: Formatted YAML content as a string.
    """
    # Manually construct YAML lines to avoid extra entries
    dataset_yaml = [
        "train: '../train/images'",
        "val: '../valid/images'",
        "test: '../test/images'",
        f"nc: {len(class_names)}",
        "names: [" + ", ".join([f"'{name}'" for name in class_names]) + "]"
    ]

    # Join lines to create the final YAML content string
    yaml_content = "\n".join(dataset_yaml)
    return yaml_content


def create_label_content(annotations: list, img_width: int, img_height: int) -> str:
    """
    Create YOLO label content for annotations.

    :param annotations: List of annotations with bbox and segmentation data.
    :param img_width: Image width in pixels.
    :param img_height: Image height in pixels.
    :return: Label content as a formatted string.
    """
    label_content = ""
    for annotation in annotations:
        if const.SEGMENTATION_KEY in annotation and annotation[const.SEGMENTATION_KEY]:
            for seg in annotation[const.SEGMENTATION_KEY]:
                if isinstance(seg, list):
                    normalized_seg = [
                        coord / img_width if i % 2 == 0 else coord / img_height
                        for i, coord in enumerate(seg)
                    ]
                    seg_str = " ".join(f"{coord:.6f}" for coord in normalized_seg)
                    line = f"{annotation[const.CLASS_ID_KEY]} {seg_str}"
                    label_content += line + "\n"
        elif const.BBOX_KEY in annotation and annotation[const.BBOX_KEY]:
            cx, cy, width, height = annotation[const.BBOX_KEY]
            line = f"{annotation[const.CLASS_ID_KEY]} {cx:.6f} {cy:.6f} {width:.6f} {height:.6f}"
            label_content += line + "\n"
    return label_content


def create_error_entry(annotation: dict, images: list) -> dict:
    """
    Create an error entry for annotations with incorrect attributes.

    :param annotation: Annotation data as a dictionary.
    :param images: List of images in the dataset.
    :return: Error entry dictionary.
    """
    image = next((img for img in images if img[const.ID_KEY] == annotation[const.IMAGE_ID_KEY]), None)
    return {
        "annotation_type": "box",
        "annotation": {
            "x": annotation[const.BBOX_KEY][0],
            "y": annotation[const.BBOX_KEY][1],
            "width": annotation[const.BBOX_KEY][2],
            "height": annotation[const.BBOX_KEY][3]
        },
        const.IMAGE_ID_KEY: annotation[const.IMAGE_ID_KEY],
        const.FILE_NAME_KEY: image[const.FILE_NAME_KEY] if image else "",
        "error_message": f"Expected bbox height to be <= 1.0, got {annotation[const.BBOX_KEY][3]}"
    }


def save_images_to_zip(images: list, zip_file: zipfile.ZipFile) -> None:
    """
    Save images to a zip file, organized by data split.

    :param images: List of images to save.
    :param zip_file: Zip file object to write to.
    """
    for image in images:
        split_dir = const.VALIDATION_IMAGES_DIR if image[const.SPLIT_KEY] in const.VALID_SPLIT_ALIASES else f"{image[const.SPLIT_KEY]}_images"
        image_path = os.path.join(split_dir, image[const.FILE_NAME_KEY])
        if image.get(const.IMAGE_CONTENT_KEY):
            zip_file.writestr(image_path, image.get(const.IMAGE_CONTENT_KEY))


def create_coco_dict(data: dict, split_images: list, split_annotations: list, split: str) -> dict:
    """
    Generate a COCO-format dictionary for a specific data split.

    :param data: Source data dictionary.
    :param split_images: List of images in the current split.
    :param split_annotations: List of annotations in the current split.
    :param split: The current data split.
    :return: Dictionary in COCO format.
    """
    return {
        const.INFO_KEY: {
            const.DESCRIPTION_KEY: data.get(const.INFO_KEY, {}).get(const.DESCRIPTION_KEY, const.DEFAULT_DESCRIPTION),
            const.DATASET_NAME_KEY: data.get(const.INFO_KEY, {}).get(const.DATASET_NAME_KEY, const.DEFAULT_DATASET_NAME),
            const.DATASET_TYPE_KEY: data.get(const.INFO_KEY, {}).get(const.DATASET_TYPE_KEY, const.DEFAULT_DATASET_TYPE),
            const.DATE_CREATED_KEY: data.get(const.INFO_KEY, {}).get(
                const.DATE_CREATED_KEY, datetime.datetime.now().strftime(const.DEFAULT_DATE_FORMAT)
            ),
        },
        const.LICENSES_KEY: data.get(const.LICENSES_KEY, []),
        const.IMAGES_KEY: [
            {
                const.ID_KEY: img.get(const.ID_KEY),
                const.FILE_NAME_KEY: img.get(const.FILE_NAME_KEY),
                const.WIDTH_KEY: img.get(const.WIDTH_KEY, 0),
                const.HEIGHT_KEY: img.get(const.HEIGHT_KEY, 0),
                const.SPLIT_KEY: split
            }
            for img in split_images
        ],
        const.ANNOTATIONS_KEY: [
            {
                const.ID_KEY: ann.get(const.ID_KEY),
                const.IMAGE_ID_KEY: ann.get(const.IMAGE_ID_KEY),
                const.CATEGORY_ID_KEY: ann.get(const.CATEGORY_ID_KEY),
                const.BBOX_KEY: ann.get(const.BBOX_KEY, []),
                const.SEGMENTATION_KEY: ann.get(const.SEGMENTATION_KEY, []),
                const.AREA_KEY: ann.get(const.AREA_KEY, 0.0),
                const.ISCROWD_KEY: ann.get(const.ISCROWD_KEY, 0)
            }
            for ann in split_annotations
        ],
        const.CATEGORIES_KEY: data.get(const.CATEGORIES_KEY, [])
    }


def save_image_to_zip(image: dict, image_path: str, zip_file: zipfile.ZipFile) -> None:
    """
    Save an individual image to a zip file.

    :param image: Image dictionary containing file and content information.
    :param image_path: Path within the zip file where the image will be saved.
    :param zip_file: Zip file object to write to.
    """
    if image.get(const.IMAGE_CONTENT_KEY):
        zip_file.writestr(image_path, image.get(const.IMAGE_CONTENT_KEY))
