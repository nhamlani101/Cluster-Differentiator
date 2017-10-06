#!usr/bin/env python

import logging

import provisionator.config as config
import provisionator.util as util
from extras import utils

LOG = logging.getLogger(__name__)

items_to_look_for = ["threshold", "size", "port", "memory", "location", "security"
                     "dir", "list", "enable"]

class Type(object):
    JSON = 0
    BOOL = 1
    INT = 2
    DIRECTORY = 3
    UNKNOWN = 4


def connect_to_cluster(conf_file):
    api = util.get_api_handle(conf_file)
    cm = api.get_cluster(conf_file["clusters"]["name"])
    print "Successfully connected to the cluster"
    return cm

def get_name_type_dict(cm_cluster):
    all_services_names = cm_cluster.get_all_services()

    name_type_dict = {}
    for i in all_services_names:
        name_arr = str(i).split(" ")
        name_type_dict[i.type] = name_arr[1]

    return name_type_dict

def role_groups_compare_clusters(cm_cluster, standard, name_to_type):
    print "Started role group comparisons\n"

    #Loop through the ideal file
    for service_name in standard["services"]:
       print "Looping through the standard file"
       if service_name in name_to_type:
           print "Service: " + service_name
           #print cm_cluster.get_service(name_to_type[service_name]).get_config()
           role_group_list = cm_cluster.get_service(name_to_type[service_name]).get_all_role_config_groups()
           #print role_group_list
           for i in role_group_list:
                if i.roleType in standard["services"][service_name]["roleConfigGroups"]:
                    #print i.get_config("full")
                    print "Current role config: " + i.roleType
                    compare_inner_role_groups(standard, service_name, i.roleType, i.get_config())
                    print "\n"

def compare_inner_role_groups(standard, service_name, role_type, cm_role_config):
    file_roles_in_groups = standard["services"][service_name]["roleConfigGroups"][role_type]
    for index in file_roles_in_groups:
        if index in cm_role_config:
            print "Value in question: " + index
            print "THE FILE HAS : " + file_roles_in_groups[index]
            #print classify_output_type(file_roles_in_groups[index])
            print "THE CLUSTER HAS : " + cm_role_config[index]
            #print classify_output_type(cm_role_config[index])

def config_compare_clusters(cm_cluster, standard, name_to_type):
    print "Started service config comparisons\n"

    for service_name in standard["services"]:
        print "Service: " + service_name
        if service_name in name_to_type:
            service_config = cm_cluster.get_service(name_to_type[service_name]).get_config("summary")
            print service_config[0]
            for config_item in service_config[0]: #For some reason get_config gives back an array of the config
                standard_config = standard["services"][service_name]["config"]
                if config_item in standard_config:
                    #TODO: Maybe have some more defensvie programming, maybe check the number in the standard
                    #TODO: and if it doesnt match, do a .contains() because of spelling error in the standard file
                    print "Got a match: " + config_item
                    print "THE FILE HAS: " + standard_config[config_item]
                    print classify_output_type(standard_config[config_item])
                    print "THE CLUSTER HAS: " + service_config[0][config_item]
                    print classify_output_type(service_config[0][config_item])
        print "\n"

def classify_output_type(output):
    if utils.is_int(output):
        return Type.INT
    elif utils.is_bool(output):
        return Type.BOOL
    elif utils.is_directory(output):
        return Type.DIRECTORY
    elif utils.is_json(output):
        return Type.JSON
    else:
        return Type.UNKNOWN


if __name__ == '__main__':

    #start_time = time.time()

    #Open files to parseable format
    cm_connection = config.read_config("configs/connect_config.json")
    gold = config.read_config("configs/test_json_template_input.json")

    #Connect to cluster
    cluster_to_check = connect_to_cluster(cm_connection)

    #Create name to type dictionary once from cluster
    name_type_dict = get_name_type_dict(cluster_to_check)

    #Compare clusters by role-config-groups
    #role_groups_compare_clusters(cluster_to_check, gold, name_type_dict)

    #Compare clusters by config
    config_compare_clusters(cluster_to_check, gold, name_type_dict)

    #print("--- %s seconds ---" % (time.time() - start_time))