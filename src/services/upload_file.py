import cloudinary
import cloudinary.uploader


class UploadFileService:
    def __init__(self, cloud_name, api_key, api_secret):
        """
        Initializes the service for uploading files to Cloudinary.

        Arguments:
            cloud_name: Cloud name in Cloudinary.
            api_key: API key for accessing Cloudinary.
            api_secret: API secret for accessing Cloudinary.
        """
        self.cloud_name = cloud_name
        self.api_key = api_key
        self.api_secret = api_secret
        # Cloudinary configuration for uploading files
        cloudinary.config(
            cloud_name=self.cloud_name,
            api_key=self.api_key,
            api_secret=self.api_secret,
            secure=True,
        )

    @staticmethod
    def upload_file(file, username) -> str:
        """
        Uploads a file to Cloudinary and generates a URL to access the image.

        Creates a unique identifier for the user and uploads the file to the server.
        After successful upload, returns the image URL with specific parameters (size, crop).

        Arguments:
            file: The file to be uploaded.
            username: The username for generating a unique public_id.

        Returns:
            str: The URL of the image available on Cloudinary.
        """
        # Creating a unique public_id for the user
        public_id = f"RestApp/{username}"
        # Uploading the file to the Cloudinary server
        r = cloudinary.uploader.upload(file.file, public_id=public_id, overwrite=True)
        # Generating the URL to access the image with specified dimensions
        src_url = cloudinary.CloudinaryImage(public_id).build_url(
            width=250, height=250, crop="fill", version=r.get("version")
        )
        return src_url
