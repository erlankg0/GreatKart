# MEDIA
# media/path
def directory_path(instance, filename):
    return "categories/category_{0}/{1}".format(instance.name.lower(), filename)
