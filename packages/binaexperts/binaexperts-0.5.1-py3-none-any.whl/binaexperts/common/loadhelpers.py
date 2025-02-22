import zipfile
import io
import yaml
import os
import base64

from binaexperts.convertors.const import *

def loadhelper_coco_data(
        coco_data,
        dataset,
        subdir,
        source_zip=None
):

    # Load categories if not already present
    if not dataset[CATEGORIES_KEY]:
        for cat in coco_data.get(CATEGORIES_KEY, []):
            category = {
                ID_KEY: cat[ID_KEY],
                NAME_KEY: cat[NAME_KEY],
                SUPERCATEGORY_KEY: cat.get(SUPERCATEGORY_KEY, DEFAULT_SUPERCATEGORY)
            }
            dataset[CATEGORIES_KEY].append(category)

    # Load images
    for img in coco_data.get(IMAGES_KEY, []):
        unique_image_id = f"{subdir}_{img[ID_KEY]}"  # Prefix with split
        image_file_name = img[FILE_NAME_KEY]
        image_path = f"{subdir}/{image_file_name}"

        image_content = None
        if source_zip and image_path in source_zip.namelist():
            with source_zip.open(image_path) as img_file:
                image_content = img_file.read()
        elif source_zip:
            continue

        image = {
            ID_KEY: unique_image_id,
            FILE_NAME_KEY: image_file_name,
            WIDTH_KEY: img.get(WIDTH_KEY, 0),
            HEIGHT_KEY: img.get(HEIGHT_KEY, 0),
            SPLIT_KEY: subdir,
            SOURCE_ZIP_KEY: source_zip,
            IMAGE_CONTENT_KEY: image_content
        }
        dataset[IMAGES_KEY].append(image)

    # Load annotations
    for ann in coco_data.get(ANNOTATIONS_KEY, []):
        unique_image_id = f"{subdir}_{ann[IMAGE_ID_KEY]}"
        annotation = {
            ID_KEY: ann[ID_KEY],
            IMAGE_ID_KEY: unique_image_id,
            CATEGORY_ID_KEY: ann[CATEGORY_ID_KEY],
            BBOX_KEY: ann[BBOX_KEY],
            SEGMENTATION_KEY: ann.get(SEGMENTATION_KEY, []),
            AREA_KEY: ann.get(AREA_KEY, 0.0),
            ISCROWD_KEY: ann.get(ISCROWD_KEY, 0)
        }
        if not isinstance(annotation[SEGMENTATION_KEY], list):
            continue
        dataset[ANNOTATIONS_KEY].append(annotation)

def loadhelper_yolo_from_zip(
            zip_file: zipfile.ZipFile,
            dataset: dict,
            subdirs: list
    ):

    if YOLO_YAML_FILENAME in zip_file.namelist():
        with zip_file.open(YOLO_YAML_FILENAME) as file:
            data_yaml = yaml.safe_load(file)
            dataset[DATASET_CLASS_NAMES_KEY] = data_yaml.get('names', [])
            dataset[LICENSES_KEY] = [{ID_KEY: 1, NAME_KEY: data_yaml.get('license', 'Unknown License'),
                                      "url": data_yaml.get('license_url', '')}]

    for subdir in subdirs:
        image_dir = YOLO_IMAGE_DIR_PATH_TEMPLATE.format(subdir)
        label_dir = YOLO_LABEL_DIR_PATH_TEMPLATE.format(subdir)

        if not any(path.startswith(image_dir) for path in zip_file.namelist()):
            continue

        for img_path in zip_file.namelist():
            if img_path.startswith(image_dir) and (img_path.endswith('.jpg') or img_path.endswith('.png')):
                image_file_name = os.path.basename(img_path)
                image_path = f"{subdir}/{YOLO_IMAGES_SUBDIR}/{image_file_name}"
                label_file_name = image_file_name.replace('.jpg', TXT_EXT).replace('.png', TXT_EXT)
                label_path = f"{subdir}/{YOLO_LABELS_SUBDIR}/{label_file_name}"

                if image_path in zip_file.namelist():
                    with zip_file.open(image_path) as img_file:
                        image_content = img_file.read()

                    yolo_image = {
                        FILE_NAME_KEY: image_file_name,
                        ANNOTATIONS_KEY: [],
                        SPLIT_KEY: subdir,
                        SOURCE_ZIP_KEY: zip_file,
                        IMAGE_CONTENT_KEY: image_content
                    }

                    if label_path in zip_file.namelist():
                        with zip_file.open(label_path) as label_file:
                            for line in io.TextIOWrapper(label_file, encoding='utf-8'):
                                values = list(map(float, line.strip().split()))
                                if len(values) == 5:
                                    class_id, cx, cy, w, h = values
                                    yolo_annotation = {
                                        CLASS_ID_KEY: int(class_id),
                                        "cx": cx,
                                        "cy": cy,
                                        "width": w,
                                        "height": h
                                    }
                                    yolo_image[ANNOTATIONS_KEY].append(yolo_annotation)
                                elif len(values) > 5:
                                    class_id = int(values[0])
                                    segmentation = values[1:]
                                    yolo_annotation = {
                                        CLASS_ID_KEY: class_id,
                                        SEGMENTATION_KEY: segmentation
                                    }
                                    yolo_image[ANNOTATIONS_KEY].append(yolo_annotation)

                    dataset[IMAGES_KEY].append(yolo_image)

def loadhelper_yolo_from_directory(
            source: str,
            dataset: dict,
            subdirs: list
    ):

    for subdir in subdirs:
        image_dir = os.path.join(source, subdir, YOLO_IMAGES_SUBDIR)
        label_dir = os.path.join(source, subdir, YOLO_LABELS_SUBDIR)

        if not os.path.isdir(image_dir) or not os.path.isdir(label_dir):
            continue

        for image_file_name in os.listdir(image_dir):
            if image_file_name.endswith('.jpg') or image_file_name.endswith('.png'):
                image_path = os.path.join(image_dir, image_file_name)
                label_file_name = image_file_name.replace('.jpg', TXT_EXT).replace('.png', TXT_EXT)
                label_path = os.path.join(label_dir, label_file_name)

                with open(image_path, 'rb') as img_file:
                    image_content = img_file.read()

                yolo_image = {
                    FILE_NAME_KEY: image_file_name,
                    ANNOTATIONS_KEY: [],
                    SPLIT_KEY: subdir,
                    IMAGE_CONTENT_KEY: image_content
                }

                if os.path.isfile(label_path):
                    with open(label_path, 'r') as label_file:
                        for line in label_file:
                            values = list(map(float, line.strip().split()))
                            if len(values) == 5:
                                class_id, cx, cy, w, h = values
                                yolo_annotation = {
                                    CLASS_ID_KEY: int(class_id),
                                    "cx": cx,
                                    "cy": cy,
                                    "width": w,
                                    "height": h
                                }
                                yolo_image[ANNOTATIONS_KEY].append(yolo_annotation)
                            elif len(values) > 5:
                                class_id = int(values[0])
                                segmentation = values[1:]
                                yolo_annotation = {
                                    CLASS_ID_KEY: class_id,
                                    SEGMENTATION_KEY: segmentation
                                }
                                yolo_image[ANNOTATIONS_KEY].append(yolo_annotation)

                dataset[IMAGES_KEY].append(yolo_image)


def loadhelper_binaexperts_data(
            bina_data,
            dataset,
            image_folder,
            source_zip=None
    ):

    if not dataset[CATEGORIES_KEY]:
        for cat in bina_data.get(CATEGORIES_KEY, []):
            category = {
                ID_KEY: cat[ID_KEY],
                NAME_KEY: cat[NAME_KEY],
                SUPERCATEGORY_KEY: cat.get(SUPERCATEGORY_KEY, DEFAULT_SUPERCATEGORY)
            }
            dataset[CATEGORIES_KEY].append(category)

    for img in bina_data.get(IMAGES_KEY, []):
        image_id = img[ID_KEY]
        image_file_name = img[FILE_NAME_KEY]
        image_path = f"{image_folder}/{image_file_name}"

        image_content = None
        if source_zip and image_path in source_zip.namelist():
            with source_zip.open(image_path) as img_file:
                image_content = img_file.read()

        image = {
            ID_KEY: image_id,
            FILE_NAME_KEY: image_file_name,
            WIDTH_KEY: img.get(WIDTH_KEY, 0),
            HEIGHT_KEY: img.get(HEIGHT_KEY, 0),
            SPLIT_KEY: image_folder.replace('_images', ''),
            SOURCE_ZIP_KEY: source_zip,
            IMAGE_CONTENT_KEY: image_content
        }
        dataset[IMAGES_KEY].append(image)

    image_ids = set(img[ID_KEY] for img in dataset[IMAGES_KEY])
    for ann in bina_data.get(ANNOTATIONS_KEY, []):
        image_id = ann[IMAGE_ID_KEY]
        if image_id not in image_ids:
            continue
        annotation = {
            ID_KEY: ann[ID_KEY],
            IMAGE_ID_KEY: image_id,
            CATEGORY_ID_KEY: ann[CATEGORY_ID_KEY],
            BBOX_KEY: ann[BBOX_KEY],
            SEGMENTATION_KEY: ann.get(SEGMENTATION_KEY, []),
            AREA_KEY: ann.get(AREA_KEY, 0.0),
            ISCROWD_KEY: ann.get(ISCROWD_KEY, 0),
            BBOX_FORMAT_KEY: COCO_BBOX_FORMAT
        }
        dataset[ANNOTATIONS_KEY].append(annotation)

    dataset[LABELS_KEY] = bina_data.get(LABELS_KEY, [])
    dataset[CLASSIFICATIONS_KEY] = bina_data.get(CLASSIFICATIONS_KEY, [])
    dataset[AUGMENTATION_SETTINGS_KEY] = bina_data.get(AUGMENTATION_SETTINGS_KEY, {})
    dataset[TILE_SETTINGS_KEY] = bina_data.get(TILE_SETTINGS_KEY, DEFAULT_TILE_SETTINGS)
    dataset[FALSE_POSITIVE_KEY] = bina_data.get(FALSE_POSITIVE_KEY, DEFAULT_FALSE_POSITIVE)

    if ERRORS_KEY not in dataset:
        dataset[ERRORS_KEY] = []
    dataset[ERRORS_KEY].extend(bina_data.get(ERRORS_KEY, []))


def encode_file_to_base64(file_path):
    """Encode a file to Base64 format."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    with open(file_path, "rb") as file:
        return "data:@file/zip;base64," + base64.b64encode(file.read()).decode("utf-8")