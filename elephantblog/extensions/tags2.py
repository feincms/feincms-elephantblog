from taggit.managers import TaggableManager

def register(cls, admin_cls):
    cls.add_to_class('tags', TaggableManager())
