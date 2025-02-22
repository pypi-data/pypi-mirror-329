import io
import logging
import os
import zipfile
from io import BytesIO
from typing import Any, Union, IO
from binaexperts.convertors import const
from binaexperts.convertors.base import YOLOConvertor, COCOConvertor, BinaExpertsConvertor
from binaexperts.common.utils import detect_format

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Convertor:
    """
    A class responsible for converting datasets between different formats (YOLO, COCO, BinaExperts).

    This class facilitates the conversion of datasets by using the appropriate convertor based on the detected
    format of the dataset. It supports loading data from different sources (file paths, in-memory objects),
    normalizing it, and converting it to the target format.
    """

    def __init__(self):
        pass

    @staticmethod
    def get_convertor(format_type: str):
        """
        Get the appropriate convertor class based on the detected format type.

        :param format_type: The type of dataset format (e.g., 'yolo', 'coco', 'binaexperts').
        :return: An instance of the corresponding convertor class.
        :raises ValueError: If the provided format type is not supported.
        """
        if format_type == const.CONVERTOR_FORMAT_YOLO:
            return YOLOConvertor()
        elif format_type == const.CONVERTOR_FORMAT_COCO:
            return COCOConvertor()
        elif format_type == const.CONVERTOR_FORMAT_BINAEXPERTS:
            return BinaExpertsConvertor()
        else:
            raise ValueError(f"Unsupported format type: {format_type}")

    def convert(
            self,
            target_format: str,
            source: Union[str, IO[bytes]],
            destination: Union[str, IO[bytes]] = None
    ) -> Union[None, IO[bytes]]:
        """
        Convert a dataset to the target format and save the output.

        This method detects the format of the source dataset, then converts it to the specified target format.
        The converted dataset can either be saved to a file (specified in `destination`) or returned as an
        in-memory object if no destination is provided.

        :param target_format: The format of the target dataset (e.g., 'yolo', 'coco', 'binaexperts').
        :param source: The source dataset, either as a file path or an in-memory object (BytesIO).
        :param destination: (Optional) The destination to save the converted dataset. Can be a directory path,
                            file path, or an in-memory object (BytesIO).
        :return: None if saved to disk, or an in-memory IO object containing the converted dataset.
        :raises ValueError: If the target format is unsupported or the format detection fails.
        """
        # Start the conversion process
        try:
            # Detect source format based on the contents of the zip or IO file
            source_format = detect_format(source)
            logger.info("Converting...")
            # Get the correct convertors based on the detected source and target formats
            source_convertor = self.get_convertor(source_format)
            target_convertor = self.get_convertor(target_format)

            # Handle source as either a path or file-like object
            if isinstance(source, str):
                if zipfile.is_zipfile(source):  # Handle zip file case
                    with zipfile.ZipFile(source, 'r') as zip_ref:
                        source_data = source_convertor.load(zip_ref)
                else:
                    with open(source, 'rb') as source_file:
                        source_data = source_convertor.load(source_file)
            else:
                source_data = source_convertor.load(source)

            # Convert to the normalized format
            normalized_data = source_convertor.normalize(source_data)

            # If destination is specified, save the output to it
            if destination:
                if isinstance(destination, str) and os.path.isdir(destination):
                    destination_file_path = os.path.join(destination, 'converted_dataset.zip')
                    with open(destination_file_path, 'wb') as destination_file:
                        target_data = target_convertor.convert(normalized_data, destination_file)
                else:
                    target_data = target_convertor.convert(normalized_data, destination)

                # Save the target format dataset
                target_convertor.save(target_data, destination)
                logger.info(f"Conversion completed!")
                return None  # No need to return anything when saved to disk

            else:
                # No destination provided, output the result as an in-memory IO object
                in_memory_output = BytesIO()
                target_data = target_convertor.convert(normalized_data, in_memory_output)
                in_memory_output.seek(0)  # Reset pointer to the beginning of the BytesIO object
                return in_memory_output

        except Exception as e:
            logger.error(f"Conversion failed: {str(e)}")
            raise
