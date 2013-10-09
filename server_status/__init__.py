

def autodiscover():
    import copy
    from django.utils.importlib import import_module
    from django.utils.module_loading import module_has_submodule

    from .conf import settings
    from .registry import plugins

    """
    Auto-discover INSTALLED_APPS plugin modules and fail silently when
    not present. This forces an import on them to register the plugin.
    """
    for app in settings.INSTALLED_APPS:
        mod = import_module(app)
        # Attempt to import the app's plugin module.
        try:
            before_import_registry = copy.copy(plugins._registry)
            name = '{}.{}'.format(app, settings.SERVER_STATUS_PLUGIN_MODULE_NAME)
            import_module(name)
        except Exception as error:
            # Reset the model registry to the state before the last import as
            # this import will have to reoccur on the next request and this
            # could raise NotRegistered and AlreadyRegistered exceptions
            # (see #8245).
            plugins._registry = before_import_registry

            # Decide whether to bubble up this error. If the app just
            # doesn't have a plugin module, we can ignore the error
            # attempting to import it, otherwise we want it to bubble up.
            if module_has_submodule(mod, settings.SERVER_STATUS_PLUGIN_MODULE_NAME):
                raise