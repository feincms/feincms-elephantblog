import warnings

warnings.warn('Please use elephantblog.views.legacy.urls instead of elephantblog.urls',
    DeprecationWarning)

from elephantblog.views.legacy.urls import *
