import os.path


# MEDIA
# media/path
def directory_image_path(instance, filename):
    """
    Менеджер файлов
    instance -> Это класс
    filename имя файла
    """
    # логика изменения имя файла
    filename, ext = os.path.splitext(filename)
    filename = instance.name.lower() + ext
    return "products/{0}".format(filename)


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
