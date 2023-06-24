import napalm
from jinja2 import Environment, FileSystemLoader
import yaml
import re
import logging
import sys
import os
import json
import argparse


def setup_custom_logger(file):
    '''
    Creates a Log File and returns Logger object

    Parameters:
        - file: fullname for the logging file (must include extension if needed)

    Returns:
        - logger: Logger object
    '''

    logformat = "[%(asctime)s - %(lineno)s - %(funcName)s() - %(levelname)s ] %(message)s"
    formatter = logging.Formatter(fmt=logformat, datefmt='%Y-%m-%d %H:%M:%S')
    handler = logging.FileHandler(file, mode='w')
    handler.setFormatter(formatter)
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)

    return logger


def logger(fn):
    '''
    Decorator function to be used for logging

    Parameters:
        - fn: decorated function

    Returns:
        - inner: decorated function return's
    '''

    logger = setup_custom_logger(file="logging.log")

    def inner(*args, **kwargs):
        to_execute = fn(*args, **kwargs)
        logger.debug(f'*** {fn.__name__} executed - {args}')
        return to_execute

    return inner


@logger
def get_config_data(file, logger):
    '''
    Loads data from YAML into Python dictionary

    Parameters:
        - file: fullname for the input file

    Returns:
        - data: Python dictionary with all data from YAML file
    '''
    logger.debug(f'get_config_data() executed for {file}')

    data = yaml.load(open(file), Loader=yaml.FullLoader)
    logger.debug(f'get_config_data() {data}')

    return data


@logger
def get_target_config(vendor, target, feature, logger, folder="templates"):
    '''
    Gets configuration for a certain device within a dictionary

    Parameters:
        - vendor: vendor device
        - target: looked up device
        - feature: used to distriminate between interfaces and routing/bgp configuration
        - logger: used for logging

    Returns:
        - result: rendered template according to input parameters
    '''
    config_data = get_config_data('input.yml', logger)
    logger.debug('get_target_config() executed from input.yml')
    logger.debug(f'get_target_config() extract \n {config_data}')
    # Selects target from config_data
    config_data = {target: config_data.get(target)}
    logger.debug(f'get_target_config() filtered \n {config_data}')
    # This line uses the current directory and loads the jinja2 template
    env = Environment(loader=FileSystemLoader('.'), trim_blocks=True, lstrip_blocks=True)
    template = env.get_template(f'{folder}/{vendor}_{feature}.j2')
    logger.debug(f'get_target_config() selected template {vendor}_{feature}.j2')
    # Return the template with data
    result = template.render(config_data=config_data)
    logger.debug(f'get_target_config() result is \n {result}')

    return result


@logger
def config_interfaces(device, logger):
    '''
    Configures IP / Mask / Admin Status for input device using NAPALM

    Parameters:
        - device: target device
        - logger: used for logging

    Returns:
        - result: none explicit
    '''

    logger.debug(f'config_interfaces() connecting to {device.hostname}...')
    device.open()
    logger.debug(f'config_interfaces() getting device facts for {device.hostname}')
    device_facts = device.get_facts()
    device.load_merge_candidate(filename=None, config=get_target_config(device_facts["vendor"],
                                                                        target=device.hostname,
                                                                        feature="interfaces",
                                                                        logger=logger))
    logger.debug(f'config_interfaces() config_diff is \n {device.compare_config()}...')
    device.commit_config()
    logger.debug(f'config_interfaces() executed on {device.hostname}')
    device.close()
    logger.debug(f'config_interfaces() connection to {device.hostname} closed')


@logger
def check_layer2(device, logger):
    '''
    Checks IP connectivity for input device using NAPALM.
    IP data for remote peer is gathered by using LLDP information (NAPALM CLI) on device.

    Parameters:
        - device: target device
        - logger: used for logging

    Returns:
        - result: True, once all device checks are successful. DANGER: infinite loop might arise.
    '''

    # RexEx expression is used to gather IP add from 'show lldp nei {interface} detail'
    # import re
    logger.debug(f'check_layer2() connecting to {device.hostname}')
    device.open()
    # F841 local variable 'device_facts' is assigned to but never used
    # device_facts = device.get_facts()
    config_data = get_config_data('input.yml', logger)

    # This selects target from config_data
    config_data = {device.hostname: config_data.get(device.hostname)}
    target_list = []

    # Get target IP's
    for iface, iface_data in config_data.get(device.hostname).get("interfaces").items():
        cmd_list = [f'show lldp nei {iface} detail']
        send_command = device.cli(cmd_list)
        stdout = send_command.get(cmd_list[0])
        pattern = re.compile(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})')
        matched = pattern.search(stdout)
        if matched:
            target_list.append(matched[0])
        # Run target IP's
        ping_command = {}
        for target in target_list:
            while ping_command.get("success") is None:
                ping_command = device.ping(target)
            logger.debug(f'check_layer2() PING to {target} from {device.hostname} is OK')
        logger.info(f'check_layer2() PING checks on {device.hostname} are ALL OK')
        device.close()
        logger.debug(f'check_layer2() finished on {device.hostname}')

        return True


@logger
def config_bgp(device, logger):
    '''
    Configures BGP for input device using NAPALM

    Parameters:
        - device: target device
        - logger: used for logging

    Returns:
        - result: none explicit
    '''

    logger.debug(f'config_bgp() connecting to {device.hostname}...')
    device.open()
    logger.debug(f'config_bgp() getting device facts for {device.hostname}')
    device_facts = device.get_facts()
    device.load_merge_candidate(filename=None,
                                config=get_target_config(device_facts["vendor"],
                                                         target=device.hostname,
                                                         feature="bgp",
                                                         logger=logger))
    device.commit_config()
    logger.debug(f'config_bgp() executed on {device.hostname}')
    device.close()
    logger.debug(f'config_bgp() connection to {device.hostname} closed')


@logger
def check_bgp(device, logger):
    '''
    Checks BGP adjacency against SoT (input_file) for input device using NAPALM.

    Parameters:
        - device: target device
        - logger: used for logging

    Returns:
        - result: True or False according to comparison
    '''
    logger.debug(f'check_bgp() connecting to {device.hostname}...')
    device.open()
    logger.debug(f'check_bgp() getting device facts for {device.hostname}')
    # F841 local variable 'device_facts' is assigned to but never used
    # # device_facts = device.get_facts()
    # NAPALM getter for BGP
    bgp_neighbours = device.get_bgp_neighbors()
    logger.debug(f'check_bgp() JSON from {device.hostname} \n {json.dumps(bgp_neighbours, indent=4)}')
    config_data = get_config_data('input.yml', logger)
    # This selects target from config_data
    config_data = {device.hostname: config_data.get(device.hostname)}

    device.close()
    logger.debug(f'check_bgp() connection to {device.hostname} closed')

    result_list = []
    # BGP data from configuration
    for configured_bgp in config_data.get(device.hostname).get("bgp").get("neighbors"):
        # BGP data from NAPALM
        for existing_bgp in bgp_neighbours.get("global").get("peers"):
            if existing_bgp == configured_bgp.get("ipaddr"):
                for neighbour in bgp_neighbours:
                    result = bgp_neighbours.get("global").get("peers").get(str(existing_bgp)).get("is_up")
                    result_list.append(result)

    if len(result_list) == len(config_data.get(device.hostname).get("bgp").get("neighbors")):
        if len(result_list) == result_list.count(True):
            logger.debug(f'check_bgp() executed on {device.hostname}')
            logger.info(f'check_bgp() BGP peer validation for {device.hostname} is OK')
            return True
        else:
            logger.debug(f'check_bgp() executed on {device.hostname}')
            logger.info(f'check_bgp() BGP peer validation for {device.hostname} is OK')
            return False


def main(arg_vars):

    # Arguments evaluation
    if arg_vars.get("input") is not None:
        input_file = arg_vars.get("input")

    # Logging
    logger = setup_custom_logger(file="logging.log")

    # Get Devices. Input method should be improved to YAML/JSON file
    print('*** Exercice 1 started. Logging to logging.log')
    driver_ios = napalm.get_network_driver("ios")
    device_list = [["172.17.0.2", "ios", "router"],
                   ["172.17.0.3", "ios", "router"],
                   ["172.17.0.4", "ios", "router"]]

    target_devices = []
    for device in device_list:
        if device[1] == "ios":
            target_devices.append(driver_ios(hostname=device[0], username="vrnetlab", password="VR-netlab9"))

    # Configure interfaces on devices
    print('*** Configuring interfaces')
    for device in target_devices:
        config_interfaces(device, logger)

    # Check IP connectivity
    phase1_val_list = []
    for device in target_devices:
        phase1_val_list.append(check_layer2(device, logger))

    # If IP connectivity is OK, configure BGP
    if len(phase1_val_list) == len(device_list):
        print('*** Overall IP connectivity result is [True]')
        print('*** Configuring EBGP')
        for device in target_devices:
            config_bgp(device, logger)

        # Check BGP
        print('*** Logging detailed BGP Adjacencies from NAPALM getters')
        phase3_val_list = []
        for device in target_devices:
            phase3_val_list.append(check_bgp(device, logger))

        # Exit
        print(f'*** DONE. Peering RESULT is {phase3_val_list}')
    else:
        # Exit
        print('*** Overall IP connectivity result is [False], Exiting')


if __name__ == '__main__':

    # Argument parser
    parser = argparse.ArgumentParser(description='Exercise 1')
    parser.add_argument('--input', '-i', default="input.yml", action='store', help='define input file')

    # Intialize parser
    args = parser.parse_args()
    # Convert the Namespace to Dict
    arg_vars = vars(args)

    # Run main with args and exit
    sys.exit(main(arg_vars))
