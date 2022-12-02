# MEDIA
# media/path
def directory_path(instance, filename):
    return "products/product_{0}/{1}".format(instance, filename)


# generate sizes like ((10, 10,),) tuple
def get_sizes():
    size = [
        ('S', 'S'),
        ('M', 'M'),
        ('L', 'L'),
        ('XL', 'XL'),
    ]
    for i in range(20, 60, 2):
        size.append((str(i), (str(i))))
    size = tuple(size)
    return size
