from taggit.managers import TaggableManager

def register(cls, admin_cls, *args):   
    cls.add_to_class('tags', TaggableManager())
