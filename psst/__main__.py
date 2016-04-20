import argparse
import json
import math
import psst
import string
import sys


CONFIG = {'choices': string.ascii_letters + string.digits + '!@',
          'length': 20
          }


def read_config(config, json_data_file, unsafe):
    """ Read the config for bob

    Args:
        config -- the configuration object whith the default values
        json_data_file -- the json file which holds the configuration inforation
    Returns:
        the updated configuration
    """
    with json_data_file:
        loaded_conf = json.load(json_data_file)
        config.update(loaded_conf["psst"])
        length = config['length']
        if not (isinstance(length, int) and length > 0):
            raise ValueError('length needs to be a positive integer')
        choices = config['choices']
        if not (isinstance(choices, str) and len(choices) > 1):
            raise ValueError('choices should be a string of atleast 32 characters')
        
        entropy = math.log2(len(choices)) * length
        if not unsafe and entropy < 64:
            raise ValueError('Current password entropy is {} bits. \nThe entropy of your passwords should be above 64 bits for your own sake.\n If the low entropy is desired add "--unsafe"'.format(entropy))

        return config


def parse_args():
    """ Prarse the arguments """
    parser = argparse.ArgumentParser(description='Bob the certificate builder.')
    parser.add_argument('config',
                        type=argparse.FileType('r'),
                        help='configuration file for the creation of passwords')
    parser.add_argument('--unsafe', action='store_true',
                        help='allow passwords with an entropy lesser than 64 bits')
    return parser.parse_args()


def main():
    """ Main function """
    args = parse_args()
    try:
        config = read_config(CONFIG, args.config, args.unsafe)
    except ValueError as e:
        print(str(e), file=sys.stderr)
        sys.exit(1)

    pws = psst.create_pws(config["services"], config["length"], config["choices"])

    print(json.dumps(pws))


main()
