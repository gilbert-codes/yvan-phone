# ============= CLOUDINARY CONFIGURATION =============
import cloudinary
import cloudinary.uploader
import cloudinary.api

# Configure Cloudinary with lowercase keys
cloudinary.config(
    cloud_name="di5r5oiju",
    api_key="347921383578929",
    api_secret="IEm7tgeNxPZig0XD_rxrszfFW7M",
    secure=True
)

DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'