import io
import yaml
import json
import os
import zipfile
import cv2
import numpy as np
import datetime

from jsonschema import validate, ValidationError
from abc import ABC, abstractmethod
from typing import Union, IO, Any, Dict

from binaexperts.convertors import const
from binaexperts.common.loadhelpers import *
from binaexperts.common.utils import *
from binaexperts.convertors.const import *


class BaseConvertor(ABC):
    """
    Base class for data format converters. This class provides a framework
    for converting datasets between different formats, such as COCO, YOLO,
    and others, using a normalized intermediate format.
    """

    def __init__(self):
        """
        Initialize the base converter class. This base class is intended to be
        inherited by specific format converters (e.g., COCO, YOLO).
        """
        pass

    @abstractmethod
    def load(
            self,
            source: Union[str, IO[bytes]]
    ) -> Any:
        """
        Load the data from the source format.

        :param source: File-like object or path representing the source dataset.
        :return: Loaded data in the source format.
        """
        raise NotImplementedError("The 'load' method must be overridden by subclasses.")

    @abstractmethod
    def normalize(
            self,
            data: Any
    ) -> Dict:
        """
        Convert the source format data to the normalized format.

        :param data: Loaded data in the source format.
        :return: Data converted to the normalized format as a dictionary.
        """
        raise NotImplementedError("The 'normalize' method must be overridden by subclasses.")

    @abstractmethod
    def convert(
            self,
            normalized_data: Dict,
            destination: Union[str, IO[bytes]]
    ) -> Any:
        """
        Convert the normalized format data to the target format.

        :param normalized_data: Data in the normalized format as a dictionary.
        :param destination: File-like object or path representing the target dataset.
        :return: Converted data in the target format.
        """
        raise NotImplementedError("The 'convert' method must be overridden by subclasses.")

    @abstractmethod
    def save(
            self,
            data: Any,
            destination: Union[str, IO[bytes]]
    ) -> None:
        """
        Save the data in the target format.

        :param data: Data in the target format.
        :param destination: File-like object to save the target dataset.
        """
        raise NotImplementedError("The 'save' method must be overridden by subclasses.")


class COCOConvertor(BaseConvertor):
    """
    A convertor class for handling datasets in COCO format.

    This class extends the `BaseConvertor` and provides methods for loading, normalizing,
    and converting datasets specifically to and from the COCO format. It supports
    operations such as reading COCO-formatted data, transforming it to a normalized
    internal structure, and writing it back into the COCO format.

    COCO (Common Objects in Context) is a popular dataset format for object detection,
    segmentation, and image captioning tasks.

    Inherits from:
        BaseConvertor: A base class for dataset convertors that provides
        common methods for dataset operations.

    Usage:
        The `COCOConvertor` can be used to load a COCO dataset, normalize it for
        intermediate processing, and convert it back into COCO format or another supported format.

    Attributes:
        coco_schema (dict): A dictionary representing the COCO JSON schema, used
        for validation of COCO datasets during load and save operations.
    """

    def __init__(self):
        """
        Initializes the converter class by loading the required JSON schemas for COCO and normalizer formats.

        This constructor performs the following steps:
        1. Calls the superclass constructor to ensure proper initialization.
        2. Loads the COCO dataset schema from a JSON file located in the schema directory.
        3. Loads the normalizer dataset schema from a JSON file located in the schema directory.

        Raises:
            FileNotFoundError: If the schema files are not found at the specified paths.
            JSONDecodeError: If the schema files contain invalid JSON.
        """

        super().__init__()

        schema_path = os.path.join(os.path.dirname(__file__), '..', const.SCHEMA_DIR, const.COCO_SCHEMA_FILE)
        with open(schema_path, 'r') as schema_file:
            self.coco_schema = json.load(schema_file)

        normalizer_schema_path = os.path.join(os.path.dirname(__file__), '..', const.SCHEMA_DIR,
                                              const.NORMALIZER_SCHEMA_FILE)
        with open(normalizer_schema_path, 'r') as schema_file:
            self.normalizer_schema = json.load(schema_file)

    def load(
            self,
            source: Union[str, IO[bytes]]
    ) -> Dict:
        """
        Load a COCO dataset from various sources, including a zip file, directory, or an in-memory object.

        This method loads a COCO dataset, validates it against the COCO schema, and returns it as a dictionary.
        It supports loading data from:
        - A zip file containing COCO-formatted annotations and images.
        - A directory containing COCO-formatted annotation files.
        - An in-memory file-like object (e.g., BytesIO).

        The dataset is divided into 'train', 'test', and 'valid' splits, and the method searches for
        `_annotations.coco.json` files within each split directory. The data is validated against the
        COCO schema before being loaded into a unified dataset dictionary.

        :param source: A string representing a file path to a zip archive or directory, or a file-like
                       object (such as a BytesIO or an opened ZipFile) containing the COCO dataset.

        :return: A dictionary representing the COCO dataset, containing the following keys:
                 - 'info': General information about the dataset.
                 - 'images': A list of image metadata, including image IDs, file names, dimensions, and more.
                 - 'annotations': A list of annotations, including bounding boxes, segmentation, and other relevant details.
                 - 'categories': A list of categories (object classes) defined in the dataset.
                 - 'licenses': License information related to the dataset.

        :raises ValueError: If the source is not a valid directory path, file-like object, or an opened zip file.
        :raises ValidationError: If the COCO dataset does not conform to the expected schema.


        :note:
            - This method is flexible enough to handle both file paths (directories and zip files) and in-memory
              file-like objects.
            - The helper method `_loadhelper_coco_data` is used to manage the loading and processing of the
              COCO-formatted data.
        """

        subdirs = [const.TRAIN_DIR, const.TEST_DIR, const.VALID_DIR]
        dataset = {key: [] for key in const.DATASET_KEYS}
        dataset[const.INFO_KEY] = []

        if isinstance(source, str):
            if zipfile.is_zipfile(source):
                with zipfile.ZipFile(source, 'r') as zip_file:
                    for subdir in subdirs:
                        annotation_path = f"{subdir}/{const.COCO_ANNOTATION_FILE}"
                        if annotation_path not in zip_file.namelist():
                            continue

                        coco_data = load_json_from_source(zip_file, annotation_path)
                        if not validate_data(coco_data, self.coco_schema, context=subdir):
                            continue
                        loadhelper_coco_data(coco_data, dataset, subdir, source_zip=zip_file)

            else:
                for subdir in subdirs:
                    annotation_file = os.path.join(source, subdir, const.COCO_ANNOTATION_FILE)
                    if not os.path.isfile(annotation_file):
                        continue

                    coco_data = load_json_from_source(source, annotation_file)
                    if not validate_data(coco_data, self.coco_schema, context=subdir):
                        continue
                    loadhelper_coco_data(coco_data, dataset, subdir)

        elif isinstance(source, zipfile.ZipFile):
            for subdir in subdirs:
                annotation_path = f"{subdir}/{const.COCO_ANNOTATION_FILE}"
                if annotation_path not in source.namelist():
                    continue

                coco_data = load_json_from_source(source, annotation_path)
                if not validate_data(coco_data, self.coco_schema, context=subdir):
                    continue
                loadhelper_coco_data(coco_data, dataset, subdir, source_zip=source)

        elif hasattr(source, 'read'):
            with zipfile.ZipFile(source, 'r') as zip_file:
                for subdir in subdirs:
                    annotation_path = f"{subdir}/{const.COCO_ANNOTATION_FILE}"
                    if annotation_path not in zip_file.namelist():
                        continue

                    coco_data = load_json_from_source(zip_file, annotation_path)
                    if not validate_data(coco_data, self.coco_schema, context=subdir):
                        continue
                    loadhelper_coco_data(coco_data, dataset, subdir, source_zip=zip_file)

        else:
            raise

        return dataset

    def normalize(
            self,
            data: dict
    ) -> dict:
        """
        Convert a COCO-formatted dataset dictionary into a normalized dataset dictionary.

        This method processes the input COCO dataset, which may contain both object detection
        and segmentation data, and converts it into a normalized format that is simpler and
        more consistent for downstream use. It maps COCO's categories, images, and annotations
        into a format that supports object detection and segmentation.

        :param data: A dictionary representing the COCO dataset. It must contain the following keys:
                     - `images`: A list of dictionaries with image metadata (file names, dimensions, etc.).
                     - `annotations`: A list of dictionaries with annotation metadata (bounding boxes, categories, etc.).
                     - `categories`: A list of dictionaries representing object classes.
                     - Optionally, `licenses`: A list of dictionaries with licensing information.

        :return: A dictionary representing the normalized dataset with keys:
                 - `info`: Information about the dataset.
                 - `images`: A list of image metadata dictionaries.
                 - `annotations`: A list of annotation metadata dictionaries.
                 - `categories`: A list of category dictionaries.
                 - `licenses`: A list of license dictionaries (if provided).
                 - `nc`: Number of categories.
                 - `names`: A list of category names.

        :raises KeyError: If a required field (such as 'images', 'annotations', or 'categories') is missing from `data`.
        :raises ValueError: If an image or annotation does not meet the required format.

        :notes:
            - The bounding boxes (bbox) are expected to be in COCO's xywh format (x, y, width, height).
            - Segmentation data is included in the normalized annotations if present.
            - Categories are mapped from the COCO format to a normalized format, and an internal ID mapping is created for consistency.

        """

        normalized_dataset = {
            const.INFO_KEY: {
                const.DESCRIPTION_KEY: const.NORMALIZED_DATASET_DESCRIPTION,
                const.DATASET_NAME_KEY: const.NORMALIZED_DATASET_NAME,
                const.DATASET_TYPE_KEY: const.NORMALIZED_DATASET_TYPE,
                const.SPLITS_KEY: {}
            },
            const.IMAGES_KEY: [],
            const.ANNOTATIONS_KEY: [],
            const.CATEGORIES_KEY: [],
            const.LICENSES_KEY: data.get(const.LICENSES_KEY, []),
            const.NC_KEY: len(data[const.CATEGORIES_KEY]),
            const.NAMES_KEY: [cat[const.NAME_KEY] for cat in data[const.CATEGORIES_KEY]]
        }

        category_id_map = {cat[const.ID_KEY]: idx for idx, cat in enumerate(data[const.CATEGORIES_KEY])}
        image_id_map = {image[const.ID_KEY]: idx for idx, image in enumerate(data[const.IMAGES_KEY])}
        annotation_id = 1

        for image in data[const.IMAGES_KEY]:
            if const.WIDTH_KEY not in image or const.HEIGHT_KEY not in image:
                continue

            normalized_image = {
                const.ID_KEY: image_id_map[image[const.ID_KEY]],
                const.FILE_NAME_KEY: image[const.FILE_NAME_KEY],
                const.WIDTH_KEY: image[const.WIDTH_KEY],
                const.HEIGHT_KEY: image[const.HEIGHT_KEY],
                const.SPLIT_KEY: image.get(const.SPLIT_KEY, const.DEFAULT_TRAIN_SPLIT),
                const.SOURCE_ZIP_KEY: image.get(const.SOURCE_ZIP_KEY),
                const.IMAGE_CONTENT_KEY: image.get(const.IMAGE_CONTENT_KEY)
            }
            normalized_dataset[const.IMAGES_KEY].append(normalized_image)

        for ann in data[const.ANNOTATIONS_KEY]:
            if ann[const.CATEGORY_ID_KEY] not in category_id_map or const.IMAGE_ID_KEY not in ann or ann[
                const.IMAGE_ID_KEY] not in image_id_map:
                continue

            normalized_annotation = {
                const.ID_KEY: annotation_id,
                const.IMAGE_ID_KEY: image_id_map[ann[const.IMAGE_ID_KEY]],
                const.CATEGORY_ID_KEY: category_id_map[ann[const.CATEGORY_ID_KEY]],
                const.BBOX_KEY: ann.get(const.BBOX_KEY, []),
                const.SEGMENTATION_KEY: ann.get(const.SEGMENTATION_KEY, []),
                const.AREA_KEY: ann.get(const.AREA_KEY, 0.0),
                const.ISCROWD_KEY: ann.get(const.ISCROWD_KEY, 0),
                const.BBOX_FORMAT_KEY: const.COCO_BBOX_FORMAT
            }
            normalized_dataset[const.ANNOTATIONS_KEY].append(normalized_annotation)
            annotation_id += 1

        for cat in data[const.CATEGORIES_KEY]:
            normalized_category = {
                const.ID_KEY: category_id_map[cat[const.ID_KEY]],
                const.NAME_KEY: cat[const.NAME_KEY],
                const.SUPERCATEGORY_KEY: cat.get(const.SUPERCATEGORY_KEY, const.DEFAULT_SUPERCATEGORY)
            }
            normalized_dataset[const.CATEGORIES_KEY].append(normalized_category)

        return normalized_dataset

    def convert(
            self,
            normalized_data: dict,
            destination: Union[str, IO[bytes]]
    ) -> dict:
        """
        Convert the normalized dataset format back to the COCO format and save it.

        This method converts a normalized dataset (which might be in formats such as YOLO or custom formats)
        back into the COCO dataset format. The function constructs the COCO-compliant dataset by adding
        required metadata, images, annotations, categories, and licenses. It also validates the dataset
        against the COCO schema to ensure the correct structure before saving.

        :param normalized_data: A dictionary representing the normalized data. It should contain:
                                - `info`: General information about the dataset (e.g., description, dataset name, type, etc.).
                                - `images`: A list of dictionaries representing image metadata (file names, dimensions, etc.).
                                - `annotations`: A list of dictionaries representing annotations (bounding boxes, segmentation, etc.).
                                - `categories`: A list of dictionaries representing object categories (names, supercategories, etc.).
                                - `licenses`: (Optional) A list of dictionaries representing licensing information.

        :param destination: The path or in-memory object (e.g., a BytesIO object) to save the COCO dataset.

        :return: A dictionary representing the COCO dataset, following the COCO format.

        :raises ValidationError: If the resulting COCO dataset doesn't conform to the COCO schema.
        """

        # Create a COCO dataset object with the required metadata
        coco_dataset = {
            const.INFO_KEY: {
                const.DESCRIPTION_KEY: normalized_data.get(const.DESCRIPTION_KEY, const.DEFAULT_DESCRIPTION),
                const.DATASET_NAME_KEY: normalized_data.get(const.DATASET_NAME_KEY, const.DEFAULT_DATASET_NAME),
                const.DATASET_TYPE_KEY: normalized_data.get(const.DATASET_TYPE_KEY, const.DEFAULT_DATASET_TYPE),
                const.DATE_CREATED_KEY: normalized_data.get(const.DATE_CREATED_KEY,
                                                            datetime.datetime.now().strftime(const.DEFAULT_DATE_FORMAT))
            },
            const.IMAGES_KEY: [],
            const.ANNOTATIONS_KEY: [],
            const.CATEGORIES_KEY: [],
            const.LICENSES_KEY: normalized_data.get(const.LICENSES_KEY, [const.DEFAULT_LICENSE])
        }

        for normalized_image in normalized_data.get(const.IMAGES_KEY, []):
            coco_image = {
                const.ID_KEY: normalized_image.get(const.ID_KEY),
                const.FILE_NAME_KEY: normalized_image.get(const.FILE_NAME_KEY),
                const.WIDTH_KEY: normalized_image.get(const.WIDTH_KEY, 0),
                const.HEIGHT_KEY: normalized_image.get(const.HEIGHT_KEY, 0),
                const.SPLIT_KEY: normalized_image.get(const.SPLIT_KEY, ""),
                const.SOURCE_ZIP_KEY: normalized_image.get(const.SOURCE_ZIP_KEY, None),
                const.IMAGE_CONTENT_KEY: normalized_image.get(const.IMAGE_CONTENT_KEY, None)
            }
            coco_dataset[const.IMAGES_KEY].append(coco_image)

        annotation_id = 1
        for normalized_annotation in normalized_data.get(const.ANNOTATIONS_KEY, []):
            segmentation = normalized_annotation.get(const.SEGMENTATION_KEY, [])
            if segmentation and (
                    not isinstance(segmentation, list) or not all(
                isinstance(seg, list) for seg in segmentation)): continue

            coco_annotation = {
                const.ID_KEY: annotation_id,
                const.IMAGE_ID_KEY: normalized_annotation.get(const.IMAGE_ID_KEY),
                const.CATEGORY_ID_KEY: normalized_annotation.get(const.CATEGORY_ID_KEY),
                const.BBOX_KEY: normalized_annotation.get(const.BBOX_KEY, []),
                const.SEGMENTATION_KEY: segmentation,
                const.AREA_KEY: normalized_annotation.get(const.AREA_KEY, 0.0),
                const.ISCROWD_KEY: normalized_annotation.get(const.ISCROWD_KEY, 0)
            }
            coco_dataset[const.ANNOTATIONS_KEY].append(coco_annotation)
            annotation_id += 1

        for normalized_category in normalized_data.get(const.CATEGORIES_KEY, []):
            coco_category = {
                const.ID_KEY: normalized_category.get(const.ID_KEY),
                const.NAME_KEY: normalized_category.get(const.NAME_KEY),
                const.SUPERCATEGORY_KEY: normalized_category.get(const.SUPERCATEGORY_KEY, const.DEFAULT_SUPERCATEGORY)
            }
            coco_dataset[const.CATEGORIES_KEY].append(coco_category)

        try:
            validate_data(coco_dataset, self.coco_schema, context=const.COCO_DATASET_CONTEXT)

        except ValidationError as e:
            raise

        self.save(coco_dataset, destination)
        return coco_dataset

    def save(
            self,
            data: dict,
            destination: Union[str, IO[bytes], None] = None
    ):
        """
        Save the COCO dataset to a zip file or an in-memory buffer.

        This method validates the COCO dataset and saves it to the specified destination. The dataset is organized
        into 'train', 'valid', and 'test' splits, and each split's images and annotations are stored separately in
        the zip file or in-memory buffer.

        :param data: A dictionary representing the COCO dataset. It must include keys such as 'info', 'images',
                     'annotations', and 'categories'.
        :param destination: Path, file-like object (e.g., BytesIO), or None where the zip archive will be written.
                            If None, an in-memory buffer (BytesIO) is used.

        :raises ValidationError: If the COCO dataset does not conform to the COCO schema.

        Notes:
        - The method handles multiple formats ('valid', 'val', 'validation') for the 'valid' split from YOLO and BinaExperts.
        - The saved zip file contains image and annotation files for 'train', 'valid', and 'test' splits.
        """

        # Handle the case when destination is None by using BytesIO
        if destination is None:
            destination = io.BytesIO()

        try:
            validate_data(data, self.coco_schema, context=const.COCO_DATASET_CONTEXT)
        except ValidationError as e:
            raise

        with create_zip_writer(destination) as zip_file:
            for split in [const.TRAIN_SPLIT, const.VALID_SPLIT, const.TEST_SPLIT]:
                # Filter images based on split type
                split_images = [
                    img for img in data.get(const.IMAGES_KEY, [])
                    if (img.get(const.SPLIT_KEY,
                                "").lower() in const.VALID_SPLIT_ALIASES if split == const.VALID_SPLIT else img.get(
                        const.SPLIT_KEY, "").lower() == split)
                ]

                split_annotations = [
                    ann for ann in data.get(const.ANNOTATIONS_KEY, [])
                    if ann.get(const.IMAGE_ID_KEY) in {img.get(const.ID_KEY) for img in split_images}
                ]

                if not split_images:
                    continue

                # Create a COCO format dictionary for the split
                split_coco = create_coco_dict(data, split_images, split_annotations, split)

                # Save annotations JSON for the split
                json_filename = const.ANNOTATION_JSON_PATH_TEMPLATE.format(split)
                zip_file.writestr(json_filename, json.dumps(split_coco, indent=4))

                # Save each image to its respective split directory
                for image in split_images:
                    image_path = os.path.join(split, image.get(const.FILE_NAME_KEY))
                    save_image_to_zip(image, image_path, zip_file)

        if isinstance(destination, io.BytesIO):
            destination.seek(0)
            return destination


class YOLOConvertor(BaseConvertor):
    """
        A convertor class for handling datasets in YOLO format.

        This class extends the `BaseConvertor` and provides methods for loading, normalizing,
        and converting datasets specifically to and from the YOLO format. YOLO (You Only Look Once)
        is a widely used format for object detection tasks, where annotations are typically represented
        as bounding boxes normalized to the image size.

        The `YOLOConvertor` supports reading YOLO-formatted data (usually stored in `.txt` files),
        converting it into a normalized structure, and writing it back into the YOLO format or other
        supported formats.

        Inherits from:
            BaseConvertor: A base class for dataset convertors that provides
            common methods for dataset operations.

        Usage:
            The `YOLOConvertor` can be used to load a YOLO dataset, normalize it for
            intermediate processing, and convert it back into YOLO format or another supported format.

        Attributes:
            yolo_schema (dict): A dictionary representing the YOLO JSON schema, used
            for validation of YOLO datasets during load and save operations.
        """

    def __init__(self):

        """
        Initialize the converter class and load the YOLO and Normalizer JSON schemas.

        This constructor method loads the JSON schema files for both YOLO and Normalizer formats, which are required
        to validate datasets during conversion processes. The schema files are loaded from predefined paths relative
        to the current file's directory.

        :raises FileNotFoundError: If the schema files cannot be found at the specified paths.
        :raises json.JSONDecodeError: If the schema files cannot be decoded as valid JSON.

        Notes:
        - The paths for the schemas are assumed to be relative to the current file. Ensure that the file structure
          follows the expected organization.
        """

        super().__init__()

        import os

        current_dir = os.path.dirname(__file__)  # مسیر فایل جاری (احتمالاً convertor.py)

        # مسیرهای صحیح برای YOLO و Normalizer در convertors/schema/
        yolo_schema_path = os.path.join(current_dir, '..', 'convertors', 'schema', YOLO_SCHEMA_FILE)
        normalizer_schema_path = os.path.join(current_dir, '..', 'convertors', 'schema', NORMALIZER_SCHEMA_FILE)

        # استانداردسازی مسیرها
        yolo_schema_path = os.path.abspath(yolo_schema_path)
        normalizer_schema_path = os.path.abspath(normalizer_schema_path)

        # Load YOLO schema
        with open(yolo_schema_path, 'r') as schema_file:
            self.yolo_schema = json.load(schema_file)

        # Load Normalizer schema
        with open(normalizer_schema_path, 'r') as schema_file:
            self.normalizer_schema = json.load(schema_file)

    def load(
            self,
            source: Union[str, IO[bytes]]
    ) -> dict:

        """
        Load a YOLO dataset from various sources, including a zip file, directory, or in-memory object.

        This method supports loading YOLO datasets from different sources, such as:
        - A zip file containing YOLO-formatted data.
        - A directory path containing the necessary files for YOLO.
        - An in-memory file-like object (e.g., BytesIO) that contains the YOLO dataset.

        The method processes the dataset and populates it into a dictionary with images, class names, and licenses.
        The dataset is validated against the YOLO schema to ensure correct formatting.

        :param source:
            A string representing either a path to a zip file or directory, or a file-like object (e.g., BytesIO)
            containing the YOLO data.

        :return:
            A dictionary representing the YOLO dataset. The dictionary contains:
            - `images`: A list of dictionaries representing image metadata.
            - `class_names`: A list of class names in the dataset.
            - `licenses`: License information for the dataset, if available.

        :raises ValueError:
            If the provided source is neither a valid directory path, a file-like object, nor an opened zip file.

        :raises ValidationError:
            If the YOLO dataset does not conform to the expected schema (as defined in `yolo.json`).

        Processing Steps:
        1. If the source is a zip file, open it and load class names from `data.yaml` if available.
        2. If the source is a directory, load the necessary YOLO files from the directory structure.
        3. Validate the dataset against the YOLO schema.
        4. Return the loaded dataset.

        Notes:
        - The method supports three types of input sources: a zip file path, a directory path, and an in-memory file-like object.
        - A helper method (`_loadhelper_yolo_from_zip` or `_loadhelper_yolo_from_directory`) is used to handle different source types.
        """

        subdirs = [TRAIN_DIR, VALID_DIR, TEST_DIR]
        dataset = {
            DATASET_IMAGES_KEY: [],
            DATASET_CLASS_NAMES_KEY: [],
            DATASET_LICENSES_KEY: []
        }

        if isinstance(source, str):
            if zipfile.is_zipfile(source):
                with zipfile.ZipFile(source, 'r') as zip_file:
                    loadhelper_yolo_from_zip(zip_file, dataset, subdirs)
            else:
                loadhelper_yolo_from_directory(source, dataset, subdirs)
        elif isinstance(source, zipfile.ZipFile):
            loadhelper_yolo_from_zip(source, dataset, subdirs)
        elif hasattr(source, 'read'):
            with zipfile.ZipFile(source) as zip_file:
                loadhelper_yolo_from_zip(zip_file, dataset, subdirs)
        else:
            raise

        try:
            validate(instance=dataset, schema=self.yolo_schema)
        except ValidationError as e:
            raise

        return dataset

    def normalize(
            self,
            data: dict
    ) -> dict:

        """
        Normalize the YOLO dataset into a standardized format, supporting both object detection and segmentation datasets.

        This method processes the input YOLO dataset and converts it into a normalized format that is compatible
        with downstream applications, such as COCO-like object detection or segmentation tasks.

        :param data:
            A dictionary representing the YOLO dataset. The YOLO dataset should include:
            - `images`: A list of dictionaries, each containing image metadata (file names, content, etc.) and
              annotations (bounding boxes or segmentation data).
            - `class_names`: A list of class names used in the dataset.
            - Optionally, `licenses`: A list of license dictionaries associated with the dataset.

        :return:
            A dictionary representing the normalized dataset. The normalized dataset includes:
            - `info`: General metadata about the dataset (e.g., description, dataset name, type, creation date).
            - `images`: A list of image dictionaries with normalized metadata (file names, dimensions, split, etc.).
            - `annotations`: A list of annotation dictionaries for each image, including bounding boxes or segmentation data.
            - `categories`: A list of object categories from the dataset.
            - `licenses`: A list of licenses from the dataset (if provided).
            - `nc`: The number of categories in the dataset.
            - `names`: A list of category names.

        Raises:
            ValidationError: If the normalized dataset does not conform to the Normalizer schema.

        Notes:
            - The method automatically detects whether the dataset includes object detection or segmentation data by
              inspecting annotations. It sets the `dataset_type` field to "Object Detection" or "Segmentation" accordingly.
            - Bounding boxes (in YOLO format) are converted to COCO's "xywh" format (x, y, width, height), and segmentation
              data is transformed into a compatible format if present.
            - For segmentation data, the method calculates the bounding box and area from the segmentation points using
              OpenCV functions.
            - If an image's dimensions (width, height) are missing or invalid, the image and its annotations are skipped.


        Processing Steps:
            1. The method first checks if any segmentation data is present in the annotations. If found, the dataset type is set to "Segmentation".
            2. Each image in the dataset is processed: its metadata is extracted, and dimensions are calculated from the content if provided.
            3. Annotations are converted from YOLO's format to a normalized format. Bounding boxes are translated from YOLO's center format (cx, cy, width, height) to COCO's "xywh" format. Segmentation data is processed if present.
            4. Categories are added to the dataset, and a mapping between class IDs and category names is created.
            5. The resulting dataset is validated against the Normalizer schema to ensure its correctness.

        """

        # Determine the dataset type (Object Detection or Segmentation)
        dataset_type = OBJECT_DETECTION_TYPE
        for image in data.get(DATASET_IMAGES_KEY, []):
            for ann in image.get(ANNOTATIONS_KEY, []):
                if SEGMENTATION_KEY in ann and ann[SEGMENTATION_KEY]:
                    dataset_type = SEGMENTATION_TYPE
                    break

        normalized_dataset = {
            INFO_KEY: {
                DESCRIPTION_KEY: f"{CONVERTED_FROM_YOLO} ({dataset_type})",
                DATASET_NAME_KEY: YOLO_DATASET_NAME,
                DATASET_TYPE_KEY: dataset_type,
                DATE_CREATED_KEY: datetime.datetime.now().strftime(DATE_FORMAT_YOLO),
                SPLITS_KEY: {}
            },
            DATASET_IMAGES_KEY: [],
            ANNOTATIONS_KEY: [],
            CATEGORIES_KEY: [],
            DATASET_LICENSES_KEY: data.get(DATASET_LICENSES_KEY, []),
            NC_KEY: len(data.get(DATASET_CLASS_NAMES_KEY, [])),
            NAMES_KEY: data.get(DATASET_CLASS_NAMES_KEY, [])
        }

        image_id_map = {}
        annotation_id = 1

        for idx, yolo_image in enumerate(data.get(DATASET_IMAGES_KEY, [])):
            image_content = yolo_image.get(IMAGE_CONTENT_KEY)
            file_name = yolo_image[FILE_NAME_KEY]
            split = yolo_image[SPLIT_KEY]

            if image_content:
                width, height = get_image_dimensions(image_content)

            if width == 0 or height == 0:
                continue

            normalized_image = {
                ID_KEY: idx,
                FILE_NAME_KEY: file_name,
                WIDTH_KEY: width,
                HEIGHT_KEY: height,
                SPLIT_KEY: split,
                SOURCE_ZIP_KEY: yolo_image.get(SOURCE_ZIP_KEY),
                IMAGE_CONTENT_KEY: image_content
            }
            image_id_map[file_name] = idx
            normalized_dataset[DATASET_IMAGES_KEY].append(normalized_image)

        for yolo_image in data.get(DATASET_IMAGES_KEY, []):
            image_id = image_id_map.get(yolo_image[FILE_NAME_KEY])
            if image_id is None:
                continue

            width = normalized_dataset[DATASET_IMAGES_KEY][image_id][WIDTH_KEY]
            height = normalized_dataset[DATASET_IMAGES_KEY][image_id][HEIGHT_KEY]

            for ann in yolo_image.get(ANNOTATIONS_KEY, []):
                area = 0  # Default area is 0 if no segmentation data is provided
                segmentation = []  # Default segmentation is an empty list

                if SEGMENTATION_KEY in ann and ann[SEGMENTATION_KEY]:
                    segmentation = [
                        [coord * width if i % 2 == 0 else coord * height for i, coord in
                         enumerate(ann[SEGMENTATION_KEY])]
                    ]
                    area = cv2.contourArea(np.array(segmentation).reshape(-1, 2).astype(np.float32))
                    bbox = cv2.boundingRect(np.array(segmentation).reshape(-1, 2).astype(np.float32))
                    x, y, w, h = bbox
                else:
                    bbox = convert_bbox_yolo_to_coco(ann, width, height)

                normalized_annotation = {
                    ID_KEY: annotation_id,
                    IMAGE_ID_KEY: image_id,
                    CATEGORY_ID_KEY: ann[CLASS_ID_KEY],
                    BBOX_KEY: bbox,
                    SEGMENTATION_KEY: segmentation,  # Segmentation now always has a value
                    AREA_KEY: area,
                    ISCROWD_KEY: 0,
                    BBOX_FORMAT_KEY: BBOX_FORMAT_VALUE
                }
                normalized_dataset[ANNOTATIONS_KEY].append(normalized_annotation)
                annotation_id += 1

        for idx, class_name in enumerate(data.get(DATASET_CLASS_NAMES_KEY, [])):
            normalized_category = {
                ID_KEY: idx,
                NAME_KEY: class_name,
                SUPERCATEGORY_KEY: SUPERCATEGORY_DEFAULT
            }
            normalized_dataset[CATEGORIES_KEY].append(normalized_category)

        if not validate_data(normalized_dataset, self.normalizer_schema, context=NORMALIZED_DATASET_CONTEXT):
            raise

        return normalized_dataset

    def convert(
            self,
            normalized_data: dict,
            destination: Union[str, IO[bytes]]
    ) -> dict:

        """
        Convert a normalized dataset to YOLO format and save it to a specified destination.

        This method takes a normalized dataset, which may include bounding box or segmentation data, and converts
        it into the YOLO format. The function processes images and their corresponding annotations, ensuring that
        bounding boxes and segmentation data are formatted correctly for YOLO. It then saves the YOLO dataset to
        the provided destination, either as a file or in-memory object.

        :param normalized_data:
            A dictionary representing the normalized dataset. The expected keys are:
            - `images`: A list of dictionaries with image metadata (file names, dimensions, content, etc.).
            - `annotations`: A list of dictionaries with annotation data (bounding boxes or segmentation).
            - `names`: A list of category names for the dataset (object classes).

        :param destination:
            A path (string) or a file-like object (such as BytesIO) where the YOLO dataset will be saved. The
            function writes the dataset to a zip file in YOLO format.

        :return:
            A dictionary representing the YOLO dataset. This includes:
            - `images`: A list of images with annotations formatted in YOLO-style.
            - `class_names`: A list of object categories from the dataset.

        Raises:
            ValueError: If the `destination` is not a valid path or file-like object.
            KeyError: If required fields (such as 'images' or 'annotations') are missing in the normalized dataset.

        Notes:
            - Bounding boxes are converted from COCO format (x, y, width, height) to YOLO format (cx, cy, width, height).
            - Segmentation data is normalized by scaling polygon coordinates relative to the image dimensions.
            - Each annotation is processed to ensure that values are normalized between 0 and 1 (as required by YOLO format).
            - The method checks for both bounding box and segmentation data in the annotations. If neither is found,
              the annotation is skipped with a warning.
            - Width and height values are required for all images; images without these values will be skipped.

        Processing Steps:
            1. For each image in the dataset, retrieve its annotations and process bounding boxes or segmentation data.
            2. Convert bounding boxes from COCO's "xywh" format to YOLO's "cxcywh" format (center x, center y, width, height).
            3. Ensure all bounding box values are normalized (between 0 and 1) and round to six decimal places.
            4. If segmentation data is present, normalize the coordinates and format them for YOLO.
            5. Group the annotations by image and save the resulting YOLO dataset to the provided destination.

        Warnings:
            - If an image has missing or invalid dimensions (width, height), it will be skipped.
            - If an annotation lacks both bounding box and segmentation data, it will be skipped with a warning.
            - Segmentation data is expected to be in the form of a list of polygons (list of lists). If it's not in the correct format,
              the segmentation will be skipped with a warning.
        """

        # Initialize a list to store YOLO-format images
        yolo_images = []
        image_to_annotations = {ann[IMAGE_ID_KEY]: [] for ann in normalized_data.get(ANNOTATIONS_KEY, [])}

        for annotation in normalized_data.get(ANNOTATIONS_KEY, []):
            image_to_annotations[annotation[IMAGE_ID_KEY]].append(annotation)

        for normalized_image in normalized_data.get(DATASET_IMAGES_KEY, []):
            annotations = image_to_annotations.get(normalized_image[ID_KEY], [])
            yolo_annotations = []

            for normalized_annotation in annotations:
                img_width, img_height = normalized_image[WIDTH_KEY], normalized_image[HEIGHT_KEY]
                has_bbox = BBOX_KEY in normalized_annotation and normalized_annotation[BBOX_KEY]
                has_segmentation = SEGMENTATION_KEY in normalized_annotation and normalized_annotation[SEGMENTATION_KEY]

                if has_bbox:
                    bbox = normalized_annotation[BBOX_KEY]
                    if normalized_annotation.get(BBOX_FORMAT_KEY) == BBOX_FORMAT_VALUE:
                        yolo_bbox = convert_bbox_to_yolo_format(bbox, img_width, img_height)
                        yolo_annotation = {
                            CLASS_ID_KEY: normalized_annotation[CATEGORY_ID_KEY],
                            BBOX_KEY: yolo_bbox,
                            SEGMENTATION_KEY: normalized_annotation.get(SEGMENTATION_KEY, [])
                        }
                        yolo_annotations.append(yolo_annotation)

                if has_segmentation:
                    segmentation_result = process_segmentation_data(
                        normalized_annotation[SEGMENTATION_KEY], img_width, img_height
                    )
                    if segmentation_result:
                        yolo_annotations.append({
                            CLASS_ID_KEY: normalized_annotation[CATEGORY_ID_KEY],
                            SEGMENTATION_KEY: segmentation_result,
                            BBOX_KEY: []
                        })

            yolo_image = {
                FILE_NAME_KEY: normalized_image[FILE_NAME_KEY],
                ANNOTATIONS_KEY: yolo_annotations,
                SPLIT_KEY: normalized_image[SPLIT_KEY],
                SOURCE_ZIP_KEY: normalized_image.get(SOURCE_ZIP_KEY),
                IMAGE_CONTENT_KEY: normalized_image.get(IMAGE_CONTENT_KEY),
                WIDTH_KEY: normalized_image[WIDTH_KEY],
                HEIGHT_KEY: normalized_image[HEIGHT_KEY]
            }
            yolo_images.append(yolo_image)

        yolo_dataset = {
            DATASET_IMAGES_KEY: yolo_images,
            DATASET_CLASS_NAMES_KEY: normalized_data.get(NAMES_KEY, [])
        }
        self.save(yolo_dataset, destination)

        return yolo_dataset

    def save(
            self,
            data: dict,
            destination: Union[str, io.BytesIO, None] = None
    ):

        """
        Save the YOLO dataset to a zip file or an in-memory buffer.

        This method validates the YOLO dataset against the YOLO schema, then writes the dataset to the specified
        destination in YOLO format, including images, annotations, and the `data.yaml` configuration file.

        :param data:
            A dictionary representing the YOLO dataset. The dictionary should have the following structure:
            - `images`: A list of dictionaries with image metadata, including:
                - `file_name`: The name of the image file.
                - `annotations`: A list of annotations for the image, which can include:
                    - `class_id`: The category ID for the object in the image.
                    - `bbox`: The bounding box for the object (in YOLO format).
                    - `segmentation`: The segmentation points (if applicable).
                - `split`: The data split to which the image belongs (e.g., 'train', 'valid', or 'test').
                - `image_content`: The raw binary content of the image file.
            - `class_names`: A list of object class names.

        :param destination:
            The path or BytesIO object where the YOLO dataset will be saved. If `None`, the dataset is written to
            an in-memory BytesIO zip file and returned.

        :return:
            If `destination` is a BytesIO object or `None`, the method returns the in-memory BytesIO object containing
            the zip file. Otherwise, it returns `None`.

        Raises:
            ValidationError: If the YOLO dataset does not conform to the expected schema.

        Notes:
            - This method generates the YOLO `data.yaml` configuration file, which includes paths to the images, the number
              of classes (`nc`), and the class names (`names`).
            - Each image is saved into its corresponding split folder (`train`, `valid`, or `test`), and the annotations are
              saved as text files in the respective `labels` folder.
            - Bounding boxes are expected to be in YOLO format (cx, cy, width, height), where all values are normalized between 0 and 1.
            - Segmentation data, if available, is saved in the label files following the class ID and bounding box data.

        Processing Steps:
            1. Validate the YOLO dataset against the provided YOLO schema.
            2. Write the `data.yaml` file with the dataset's structure and class names.
            3. Save each image and its corresponding label (if available) into their respective split directories (`train`, `valid`, `test`).
            4. Ensure segmentation and bounding box data are correctly formatted and saved in the label files.
            5. Return the in-memory zip file if no destination is provided.
        """

        if not validate_data(data, self.yolo_schema, context=YOLO_DATASET_CONTEXT):
            raise ValidationError(YOLO_DATASET_VALIDATION_FAILED)

        # Use BytesIO if no destination is provided
        if destination is None:
            destination = io.BytesIO()

        with zipfile.ZipFile(destination, 'w') as zip_file:
            # Use the manually constructed YAML content
            yaml_content = generate_yaml_content(data[DATASET_CLASS_NAMES_KEY])
            zip_file.writestr(DATA_YAML_FILE, yaml_content)

            # Save images and labels
            for image in data[DATASET_IMAGES_KEY]:
                # Set correct split directory
                split_dir = f"{VALID_DIR if image[SPLIT_KEY] == VALIDATION_SPLIT else image[SPLIT_KEY]}/images"
                labels_dir = f"{VALID_DIR if image[SPLIT_KEY] == VALIDATION_SPLIT else image[SPLIT_KEY]}/labels"

                # Save image content
                if image.get(IMAGE_CONTENT_KEY):
                    zip_file.writestr(os.path.join(split_dir, image[FILE_NAME_KEY]), image[IMAGE_CONTENT_KEY])

                # Save label file
                label_file_name = os.path.splitext(image[FILE_NAME_KEY])[0] + TXT_EXT
                label_zip_path = os.path.join(labels_dir, label_file_name)
                width, height = image.get(WIDTH_KEY), image.get(HEIGHT_KEY)

                # Create label content if width and height are valid
                if width and height:
                    label_content = create_label_content(image[ANNOTATIONS_KEY], width, height)
                    if label_content.strip():
                        zip_file.writestr(label_zip_path, label_content)

        # Return the in-memory zip file if destination was None
        if isinstance(destination, io.BytesIO):
            destination.seek(0)
            return destination


class BinaExpertsConvertor(BaseConvertor):
    """
        BinaExpertsConvertor is responsible for converting datasets to and from the BinaExperts format.

        This class inherits from `BaseConvertor` and provides methods to handle conversions between
        normalized datasets and the BinaExperts-specific dataset format. The format includes metadata,
        image data, annotations, and specific settings required by the BinaExperts platform.

        Attributes:
            binaexperts_schema (dict):
                The JSON schema for validating BinaExperts dataset formats.
            normalizer_schema (dict):
                The JSON schema for validating normalized datasets before conversion.

        Methods:
            convert(normalized_data: dict, destination: Union[str, IO[bytes]]) -> dict:
                Converts a normalized dataset into the BinaExperts format and saves it to the specified destination.

            normalize(data: dict) -> dict:
                Converts a BinaExperts dataset into a normalized format.

            save(data: dict, destination: Union[str, IO[bytes]] = None):
                Saves the BinaExperts dataset to a zip file or an in-memory buffer.


        Notes:
            - The BinaExperts format includes additional fields like `labels`, `errors`, `tile_settings`, and
              `augmentation_settings`, which are not part of standard formats like COCO or YOLO.
            - This converter ensures that these additional fields are handled appropriately during conversion.
        """

    def __init__(self):
        """
            Initialize the BinaExpertsConvertor class.

            This constructor loads the JSON schemas for BinaExperts and Normalizer formats, which are used
            for validating datasets during the conversion process. The schemas are stored in JSON files
            and loaded when the class is instantiated.

            The BinaExperts schema defines the structure for datasets in the BinaExperts format, and the
            Normalizer schema provides the structure for normalized datasets that will be converted into
            or from the BinaExperts format.

            The schemas are loaded from the following paths:
            - `binaexperts.json`: Defines the structure of BinaExperts datasets.
            - `normalizer.json`: Defines the structure of the normalized dataset format.

            Attributes:
                binaexperts_schema (dict):
                    A dictionary representing the BinaExperts dataset schema, loaded from `binaexperts.json`.
                normalizer_schema (dict):
                    A dictionary representing the normalized dataset schema, loaded from `normalizer.json`.

            """

        super().__init__()

        import os

        current_dir = os.path.dirname(__file__)  # مسیر دایرکتوری جاری (convertor.py)

        # مسیر صحیح برای فایل‌های schema داخل convertors/schema/
        binaexperts_schema_path = os.path.join(current_dir, '..', 'convertors', 'schema', BINAEXPERTS_SCHEMA_FILE)
        normalizer_schema_path = os.path.join(current_dir, '..', 'convertors', 'schema', NORMALIZER_SCHEMA_FILE)

        # استانداردسازی مسیر برای اطمینان از سازگاری با تمام سیستم‌ها
        binaexperts_schema_path = os.path.abspath(binaexperts_schema_path)
        normalizer_schema_path = os.path.abspath(normalizer_schema_path)

        with open(binaexperts_schema_path, 'r') as schema_file:
            self.binaexperts_schema = json.load(schema_file)

        with open(normalizer_schema_path, 'r') as schema_file:
            self.normalizer_schema = json.load(schema_file)

    def load(
            self,
            source: Union[str, IO[bytes]]
    ) -> Dict:

        """
            Load BinaExperts dataset from a zip file, directory, or an in-memory object.

            This method loads a BinaExperts dataset, validates it against the BinaExperts schema, and returns it as a dictionary.
            It supports loading data from:
            - A zip file containing BinaExperts-formatted annotations and images
            - A directory containing BinaExperts-formatted annotation files
            - An in-memory file-like object (e.g., BytesIO)

            The dataset is divided into 'train', 'test', and 'valid' splits, and the method searches for the corresponding
            annotation files within each split directory. The data is validated against the BinaExperts schema before being
            loaded into a unified dataset dictionary.

            :param source:
                A Path, a file-like object (such as a BytesIO), or an opened ZipFile containing the BinaExperts data.

            :return:
                A dictionary representing the BinaExperts dataset, containing the following keys:
                - 'info': General information about the dataset.
                - 'images': A list of image metadata, including image IDs, file names, dimensions, and more.
                - 'annotations': A list of annotations, including bounding boxes, segmentation, and other relevant details.
                - 'categories': A list of categories (object classes) defined in the dataset.
                - 'licenses': License information related to the dataset.

            :raises ValueError:
                If the source is not a valid directory path, file-like object, or an opened zip file.

            :raises ValidationError:
                If the dataset in a split does not conform to the BinaExperts schema.

            Notes:
                - This method is flexible enough to handle both file paths (directories and zip files) and in-memory file-like objects.
                - The helper method `_loadhelper_binaexperts_data` is used to manage the loading and processing of BinaExperts-formatted data.
            """

        subdir_mapping = {
            TRAIN_SPLIT: TRAIN_IMAGES_DIR,
            TEST_SPLIT: TEST_IMAGES_DIR,
            VALID_SPLIT: VALIDATION_IMAGES_DIR
        }
        annotation_files = {
            TRAIN_SPLIT: TRAIN_COCO_FILE,
            TEST_SPLIT: TEST_COCO_FILE,
            VALID_SPLIT: VALID_COCO_FILE
        }

        dataset = {
            INFO_KEY: {},
            IMAGES_KEY: [],
            ANNOTATIONS_KEY: [],
            CATEGORIES_KEY: [],
            LICENSES_KEY: []
        }

        if isinstance(source, str):
            if zipfile.is_zipfile(source):
                with zipfile.ZipFile(source, 'r') as zip_file:
                    for split, subdir in subdir_mapping.items():
                        annotation_path = f"{COCOS_DIR}/{annotation_files[split]}"
                        if annotation_path not in zip_file.namelist():
                            continue
                        with zip_file.open(annotation_path) as file:
                            coco_data = json.load(file)
                            if not validate_data(coco_data, self.binaexperts_schema, context=subdir):
                                continue
                        loadhelper_binaexperts_data(coco_data, dataset, subdir, source_zip=zip_file)
            else:
                for split, subdir in subdir_mapping.items():
                    annotation_file = os.path.join(source, COCOS_DIR, annotation_files[split])
                    if not os.path.isfile(annotation_file):
                        continue
                    with open(annotation_file, 'r') as file:
                        coco_data = json.load(file)
                        if not validate_data(coco_data, self.binaexperts_schema, context=subdir):
                            continue
                    loadhelper_binaexperts_data(coco_data, dataset, subdir)

        elif isinstance(source, zipfile.ZipFile):
            for split, subdir in subdir_mapping.items():
                annotation_path = f"{COCOS_DIR}/{annotation_files[split]}"
                if annotation_path not in source.namelist():
                    continue
                with source.open(annotation_path) as file:
                    coco_data = json.load(file)
                    if not validate_data(coco_data, self.binaexperts_schema, context=subdir):
                        continue
                loadhelper_binaexperts_data(coco_data, dataset, subdir, source_zip=source)
        elif hasattr(source, 'read'):
            with zipfile.ZipFile(source, 'r') as zip_file:
                for split, subdir in subdir_mapping.items():
                    annotation_path = f"{COCOS_DIR}/{annotation_files[split]}"
                    if annotation_path not in zip_file.namelist():
                        continue
                    with zip_file.open(annotation_path) as file:
                        coco_data = json.load(file)
                        if not validate_data(coco_data, self.binaexperts_schema, context=subdir):
                            continue
                    loadhelper_binaexperts_data(coco_data, dataset, subdir, source_zip=zip_file)
        else:
            raise

        return dataset

    def normalize(
            self,
            data: dict
    ) -> dict:

        """
            Convert BinaExperts dataset dictionary to a normalized dataset dictionary.

            This method converts a BinaExperts dataset into a normalized format that simplifies downstream processing
            and ensures consistency across different datasets. It preserves key information from the BinaExperts format
            (such as images, annotations, categories, and additional metadata) and maps it into a format that is more
            widely usable for machine learning tasks, including object detection and segmentation.

            :param data:
                A dictionary representing the BinaExperts dataset, which should include the following keys:
                - `info`: Metadata about the dataset (e.g., dataset name, type, etc.).
                - `images`: A list of dictionaries representing images and their metadata.
                - `annotations`: A list of dictionaries representing annotations for the images (e.g., bounding boxes, segmentation).
                - `categories`: A list of dictionaries representing object categories.
                - `licenses`: (Optional) A list of dictionaries representing license information.
                - `errors`: (Optional) A list of dictionaries representing errors.
                - `labels`, `classifications`, `augmentation_settings`, `tile_settings`, and `false_positive`: (Optional) Additional fields.

            :return:
                A dictionary representing the normalized dataset with the following keys:
                - `info`: General information about the dataset.
                - `images`: A list of normalized image metadata.
                - `annotations`: A list of normalized annotations (with bbox and segmentation data).
                - `categories`: A list of normalized categories.
                - `licenses`: License information if provided.
                - Additional fields: `errors`, `labels`, `classifications`, `augmentation_settings`, `tile_settings`, `false_positive`.
                - `nc`: Number of categories.
                - `names`: List of category names.

            :raises KeyError:
                If required fields (like 'images', 'annotations', or 'categories') are missing from `data`.

            Warnings:
                - If an image is missing 'width' or 'height', it will be skipped.
                - If an annotation is missing 'category_id' or 'image_id', it will be skipped.

            Notes:
                - Bounding boxes (bbox) are expected to be in the xywh format (x, y, width, height).
                - Segmentation data, if present, is carried over in the annotations.
                - The method creates unique mappings for category and image IDs to ensure consistency.
            """

        normalized_dataset = {
            INFO_KEY: {
                DESCRIPTION_KEY: CONVERTED_FROM_BINAEXPERTS,
                DATASET_NAME_KEY: data[INFO_KEY].get(DATASET_KEY, BINAEXPERTS_DATASET_NAME),
                DATASET_TYPE_KEY: data[INFO_KEY].get(DATASET_TYPE_KEY, DEFAULT_DATASET_TYPE),
                SPLITS_KEY: {}
            },
            IMAGES_KEY: [],
            ANNOTATIONS_KEY: [],
            CATEGORIES_KEY: [],
            LICENSES_KEY: data.get(LICENSES_KEY, []),
            NC_KEY: len(data[CATEGORIES_KEY]),
            NAMES_KEY: [cat[NAME_KEY] for cat in data[CATEGORIES_KEY]],
            ERRORS_KEY: data.get(ERRORS_KEY, []),
            LABELS_KEY: data.get(LABELS_KEY, []),
            CLASSIFICATIONS_KEY: data.get(CLASSIFICATIONS_KEY, []),
            AUGMENTATION_SETTINGS_KEY: data.get(AUGMENTATION_SETTINGS_KEY, {}),
            TILE_SETTINGS_KEY: data.get(TILE_SETTINGS_KEY, DEFAULT_TILE_SETTINGS),
            FALSE_POSITIVE_KEY: data.get(FALSE_POSITIVE_KEY, DEFAULT_FALSE_POSITIVE)
        }

        category_id_map = {cat[ID_KEY]: idx for idx, cat in enumerate(data[CATEGORIES_KEY])}
        image_id_map = {image[ID_KEY]: idx for idx, image in enumerate(data[IMAGES_KEY])}
        annotation_id = 1

        for image in data[IMAGES_KEY]:
            if WIDTH_KEY not in image or HEIGHT_KEY not in image:
                continue

            normalized_image = {
                ID_KEY: image_id_map[image[ID_KEY]],
                FILE_NAME_KEY: image[FILE_NAME_KEY],
                WIDTH_KEY: image[WIDTH_KEY],
                HEIGHT_KEY: image[HEIGHT_KEY],
                SPLIT_KEY: image.get(SPLIT_KEY, TRAIN_SPLIT),
                SOURCE_ZIP_KEY: image.get(SOURCE_ZIP_KEY),
                IMAGE_CONTENT_KEY: image.get(IMAGE_CONTENT_KEY)
            }
            normalized_dataset[IMAGES_KEY].append(normalized_image)

        for ann in data[ANNOTATIONS_KEY]:
            if ann[CATEGORY_ID_KEY] not in category_id_map or IMAGE_ID_KEY not in ann or ann[
                IMAGE_ID_KEY] not in image_id_map:
                continue

            normalized_annotation = {
                ID_KEY: annotation_id,
                IMAGE_ID_KEY: image_id_map[ann[IMAGE_ID_KEY]],
                CATEGORY_ID_KEY: category_id_map[ann[CATEGORY_ID_KEY]],
                BBOX_KEY: ann.get(BBOX_KEY, []),
                SEGMENTATION_KEY: ann.get(SEGMENTATION_KEY, []),
                AREA_KEY: ann.get(AREA_KEY, 0.0),
                ISCROWD_KEY: ann.get(ISCROWD_KEY, 0),
                BBOX_FORMAT_KEY: BBOX_FORMAT_VALUE
            }
            normalized_dataset[ANNOTATIONS_KEY].append(normalized_annotation)
            annotation_id += 1

        for cat in data[CATEGORIES_KEY]:
            normalized_category = {
                ID_KEY: category_id_map[cat[ID_KEY]],
                NAME_KEY: cat[NAME_KEY],
                SUPERCATEGORY_KEY: cat.get(SUPERCATEGORY_KEY, SUPERCATEGORY_DEFAULT)
            }
            normalized_dataset[CATEGORIES_KEY].append(normalized_category)

        return normalized_dataset

    def convert(
            self,
            normalized_data: dict,
            destination: Union[str, IO[bytes]]
    ) -> dict:

        """
            Convert the normalized dataset format back to BinaExperts format and write it to the destination.

            This method takes a normalized dataset and converts it into the BinaExperts format, populating
            metadata, images, annotations, and additional fields like errors, labels, classifications, and tile settings.
            The converted dataset is then written to the specified destination, either as a zip file or a file-like object.

            :param normalized_data:
                A dictionary representing the normalized dataset. It should contain:
                - `description`: A string describing the dataset.
                - `organization`: A string representing the dataset's organization.
                - `dataset_name`: The name of the dataset.
                - `dataset_type`: The type of the dataset (e.g., Object Detection).
                - `date_created`: The creation date of the dataset.
                - `licenses`: A list of licenses related to the dataset.
                - `images`: A list of image metadata (image file names, dimensions, etc.).
                - `annotations`: A list of annotations, including bounding boxes and other metadata.
                - `categories`: A list of object categories (e.g., names of object classes).
                - `errors`, `labels`, `classifications`, `augmentation_settings`, `tile_settings`, `False_positive`: (Optional) Additional fields.

            :param destination:
                A file-like object (e.g., zip file, directory path) where the BinaExperts dataset will be written.

            :return:
                A dictionary representing the BinaExperts dataset, including:
                - `info`: General metadata about the dataset.
                - `images`: A list of images with file names and dimensions.
                - `annotations`: A list of annotations with bounding boxes and segmentation.
                - `categories`: Object category information.
                - `licenses`: License information.
                - `errors`, `labels`, `classifications`, `augmentation_settings`, `tile_settings`, `False_positive`: Additional fields.

            Notes:
                - The method ensures that fields like `augmentation_settings`, `labels`, `classifications`, and `tile_settings`
                  are always present in the output dataset, even if they are not provided in the normalized dataset.
                - Bounding boxes are expected to be in the xywh format (x, y, width, height).
                  errors for anomalies.
        """

        # Create a BinaExperts dataset object with required metadata
        binaexperts_dataset = {
            INFO_KEY: {
                DESCRIPTION_KEY: normalized_data.get(DESCRIPTION_KEY, ""),
                ORGANIZATION_KEY: normalized_data.get(ORGANIZATION_KEY, ""),
                DATASET_KEY: normalized_data.get(DATASET_NAME_KEY, ""),
                DATASET_TYPE_KEY: normalized_data.get(DATASET_TYPE_KEY, ""),
                DATE_CREATED_KEY: normalized_data.get(DATE_CREATED_KEY, datetime.datetime.now().strftime(DATE_FORMAT))
            },
            LICENSES_KEY: normalized_data.get(LICENSES_KEY, []),
            IMAGES_KEY: normalized_data.get(IMAGES_KEY, []),
            ANNOTATIONS_KEY: normalized_data.get(ANNOTATIONS_KEY, []),
            CATEGORIES_KEY: normalized_data.get(CATEGORIES_KEY, []),
            ERRORS_KEY: [],
            LABELS_KEY: normalized_data.get(LABELS_KEY, []),
            CLASSIFICATIONS_KEY: normalized_data.get(CLASSIFICATIONS_KEY, []),
            AUGMENTATION_SETTINGS_KEY: normalized_data.get(AUGMENTATION_SETTINGS_KEY, {}),
            TILE_SETTINGS_KEY: normalized_data.get(TILE_SETTINGS_KEY, DEFAULT_TILE_SETTINGS),
            FALSE_POSITIVE_KEY: normalized_data.get(FALSE_POSITIVE_KEY, DEFAULT_FALSE_POSITIVE)
        }

        for annotation in normalized_data.get(ANNOTATIONS_KEY, []):
            if annotation[BBOX_KEY][3] > 1.0:
                error = create_error_entry(annotation, normalized_data[IMAGES_KEY])
                binaexperts_dataset[ERRORS_KEY].append(error)

        self.save(binaexperts_dataset, destination)

        return binaexperts_dataset

    def save(
            self,
            data: dict,
            destination: Union[str, IO[bytes]] = None
    ):

        """
            Save the BinaExperts dataset into a zip file with the appropriate folder structure.

            This method saves a BinaExperts dataset into a zip archive. It includes the dataset's images, annotations,
            and additional fields specific to the BinaExperts format (such as errors, labels, classifications, augmentation settings,
            and tile settings). The resulting archive contains images split into folders based on their dataset split (e.g.,
            'train_images', 'validation_images') and COCO-formatted JSON files for annotations.

            :param data:
                A dictionary representing the BinaExperts dataset. It should include:
                - `info`: General information about the dataset.
                - `images`: A list of dictionaries representing image metadata (file names, dimensions, etc.).
                - `annotations`: A list of dictionaries representing annotations (bounding boxes, segmentation, etc.).
                - `categories`: A list of dictionaries representing object categories.
                - `errors`, `labels`, `classifications`, `augmentation_settings`, `tile_settings`: (Optional) Additional fields.

            :param destination:
                A path or a file-like object (e.g., a BytesIO object) where the zip archive will be written.
                If no destination is provided, an in-memory BytesIO object is used.

            :return:
                If a file-like object (e.g., BytesIO) was provided as the destination, the method returns the BytesIO object
                containing the zip archive.

            Notes:
                - The method ensures that fields like `errors`, `labels`, `classifications`, `augmentation_settings`,
                  and `tile_settings` are always present in the output dataset, even if they are not provided in the
                  input dataset.
                - The method handles the conversion of the `tile_settings` field, correcting the field names from
                  the internal format (`tile_type`) to the BinaExperts format (`type`).
        """

        if destination is None:
            destination = io.BytesIO()

        with zipfile.ZipFile(destination, 'w') as zip_file:
            save_images_to_zip(data[IMAGES_KEY], zip_file)

            for split in [TRAIN_SPLIT, TEST_SPLIT, VALID_SPLIT]:
                # Collect images and annotations for the current split
                split_images = [
                    img for img in data[IMAGES_KEY]
                    if img.get(const.SPLIT_KEY, '') == split
                ]
                split_annotations = [
                    ann for ann in data[ANNOTATIONS_KEY]
                    if ann.get(const.IMAGE_ID_KEY) in {img.get(const.ID_KEY) for img in split_images}
                ]

                # Skip split if no images or annotations exist
                if not split_images or not split_annotations:
                    continue

                # Create the COCO dictionary for the current split
                coco_dict = create_coco_dict(data, split_images, split_annotations, split)

                # Write the COCO JSON file to the zip
                coco_file_name = f"{COCOS_DIR}/{VALIDATION_PREFIX if split == VALID_SPLIT else split}_coco.json"
                zip_file.writestr(coco_file_name, json.dumps(coco_dict, indent=4))

        if isinstance(destination, io.BytesIO):
            destination.seek(0)
            return destination