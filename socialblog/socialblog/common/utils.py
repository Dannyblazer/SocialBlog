
def upload_location(self, filename):
    """Generator function for image upload path"""
    return 'profile_images/' + str(self.pk) + '/profile_image.png'

# Return a default image path incase no image was uploaded
def default_image():
    return 'account/nnajidanny004@gmail.com/20221119_205632.jpg'

