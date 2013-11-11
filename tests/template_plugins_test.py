import dexy.load_plugins
from dexy.filter import Filter
from dexy.plugin import TemplatePlugin

def by_default_dexy_runs_all_template_plugins__test():
        f = Filter.create_instance('template')
        n_plugins = len(list(f.template_plugins()))
        expected_plugins = len(list(instance for instance in TemplatePlugin))
        assert n_plugins == expected_plugins

def use_plugins_attribute_to_specify_whitelist__test():
        f = Filter.create_instance('template')
        f.update_settings({'plugins' : ['dexyversion']})
        n_plugins = len(list(f.template_plugins()))
        assert n_plugins == 1

def use_skip_plugins_attribute_to_specify_blacklist__test():
        f = Filter.create_instance('template')
        f.update_settings({'plugins' : ['dexyversion']})
        n_plugins = len(list(f.template_plugins()))
        assert n_plugins == 1
