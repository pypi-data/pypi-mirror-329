from PIL import Image
import os


class ImageConverter:
    """A class to handle image conversion to WebP format"""

    def __init__(self, quality=80):
        """
        Initialize the converter

        Args:
            quality (int): Default quality for WebP conversion (0-100)
        """
        self.quality = quality
        self.supported_formats = ('.png', '.jpg', '.jpeg', '.tiff', '.bmp')

    def convert_to_webp(self, source_path, output_path=None, quality=None):
        """
        Convert a single image to WebP format

        Args:
            source_path (str): Path to source image
            output_path (str, optional): Path to save the WebP image. If None,
                                       replaces original extension with .webp
            quality (int, optional): Quality of WebP image (0-100).
                                   If None, uses default quality

        Returns:
            str: Path to the converted image
        """
        if quality is None:
            quality = self.quality

        if output_path is None:
            output_path = os.path.splitext(source_path)[0] + '.webp'

        try:
            img = Image.open(source_path)

            if img.mode in ('RGBA', 'LA'):
                background = Image.new('RGB', img.size, (255, 255, 255))
                background.paste(img, mask=img.split()[-1])
                img = background

            img.save(output_path, 'WEBP', quality=quality)
            return output_path

        except Exception as e:
            raise ConversionError(f"Error converting {source_path}: {str(e)}")

    def batch_convert(self, input_folder, output_folder=None, quality=None):
        """
        Convert all supported images in a folder to WebP format

        Args:
            input_folder (str): Folder containing source images
            output_folder (str, optional): Folder to save WebP images.
                                         If None, creates 'webp' subfolder
            quality (int, optional): Quality of WebP images (0-100)

        Returns:
            list: Paths to all converted images
        """
        if output_folder is None:
            output_folder = os.path.join(input_folder, 'webp')

        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        converted_files = []

        for filename in os.listdir(input_folder):
            if filename.lower().endswith(self.supported_formats):
                source_path = os.path.join(input_folder, filename)
                output_path = os.path.join(output_folder,
                                           os.path.splitext(filename)[0] + '.webp')
                converted_files.append(
                    self.convert_to_webp(source_path, output_path, quality)
                )

        return converted_files


class ConversionError(Exception):
    """Custom exception for conversion errors"""
    pass