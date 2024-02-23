config_file = "config.cnf"

def get_all():
    config_dict = {}

    with open(config_file, 'r') as file:
        for line in file:
            line = line.strip()
            if not line or line.startswith('#'):
                continue

            name, value = line.split(':', 1)
            name = name.strip()
            value = value.strip()
            config_dict[name] = value
        file.close()

    return config_dict

def get(name):
    data = get_all()

    try:
        return data[name]
    except:
        from . import default_prefs

        set(name, default_prefs.get(name))

def write_config_file(config_data):
    with open(config_file, 'w') as file:
        for key, value in config_data.items():
            file.write(f"{key}: {value}\n")
        file.close()

def set(name, value):
    config_data = get_all()
    config_data[name] = value
    write_config_file(config_data)
    return get(name)
