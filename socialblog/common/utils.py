
def upload_location(self):
    """Generator function for image upload path"""
    return f"profile_images/{self.pk}"

# Return a default image path incase no image was uploaded
def default_image():
    return "default image path"
