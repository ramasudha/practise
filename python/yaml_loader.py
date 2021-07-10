#!/usr/bin/python3

import yaml

with open(r'test.yaml') as file:
    # The FullLoader parameter handles the conversion from YAML
    # scalar values to Python the dictionary format
    config = yaml.load(file) #, Loader=yaml.FullLoader)

    print(config)

    print(config.get("name"))
    print(config.get("email")['recepients'])

    print(config.get("smtp"))
    print(config.get("tasks")[0]["files"])





# if __name__ == '__main__':