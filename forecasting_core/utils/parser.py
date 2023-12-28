from box import Box


def read_yaml_files(list_yml_files) -> Box:
    """Read config yml files and outputs a config Box object"""
    config = Box()
    for yml_file in list_yml_files:
        config.update(Box.from_yaml(filename=yml_file))
    return config
