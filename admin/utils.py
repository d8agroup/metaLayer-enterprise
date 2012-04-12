import os
import re
from enterprise.utils import my_import
from django.conf import settings

def get_all_available_data_points():
    import enterprise.metalayercore.datapoints.lib as datapoints_lib
    path = os.path.dirname(datapoints_lib.__file__)
    data_point_directories = [d for d in os.listdir(path) if not re.search(r'\.', d)]
    data_points = [_dynamically_load_type('enterprise.metalayercore.datapoints.lib.%s.datapoint' % d, 'DataPoint') for d in data_point_directories]
    return data_points

def get_all_available_actions():
    import enterprise.metalayercore.actions.lib as actions_lib
    path = os.path.dirname(actions_lib.__file__)
    modules = [d for d in os.listdir(path) if not re.search(r'\.', d)]
    objects = [_dynamically_load_type('enterprise.metalayercore.actions.lib.%s.action' % d, 'Action') for d in modules]
    return objects

def get_all_available_outputs():
    import enterprise.metalayercore.outputs.lib as outputs_lib
    path = os.path.dirname(outputs_lib.__file__)
    modules = [d for d in os.listdir(path) if not re.search(r'\.', d)]
    objects = [_dynamically_load_type('enterprise.metalayercore.outputs.lib.%s.output' % d, 'Output') for d in modules]
    return objects

def get_all_available_visualizations():
    import enterprise.metalayercore.visualizations.lib as visualizations_lib
    path = os.path.dirname(visualizations_lib.__file__)
    modules = [d for d in os.listdir(path) if not re.search(r'\.', d)]
    objects = [_dynamically_load_type('enterprise.metalayercore.visualizations.lib.%s.visualization' % d, 'Visualization') for d in modules]
    return objects

def get_all_available_company_themes():
    themes_root = settings.THEMES_ROOT
    company_themes_root = os.path.join(themes_root, 'companies')
    themes = os.listdir(company_themes_root)
    return themes

def _dynamically_load_type(module_name, type):
    data_point = my_import(module_name)
    data_point = getattr(data_point, type)()
    return data_point




