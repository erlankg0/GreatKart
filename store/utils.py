# MEDIA
# media/path
def directory_path(instance, filename):
    return "products/product_{0}/{1}".format(instance.name.lower(), filename)


# generate sizes like ((10, 10,),) tuple
def get_sizes():
    size = []
    for i in range(38, 60, 2):
        size.append((str(i), (str(i))))
    size = tuple(size)
    return size
