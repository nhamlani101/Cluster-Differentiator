import provisionator.config as config
import parser
import report
import argparse
from datetime import datetime

import urllib2
import json

def get_page_response(config):

    check_cluster_name = str(config['clusters']['name']).replace(" ", "%20")

    check_url = "http://" + config['cm']['host'] + ":" + str(
        config['cm']['server_port']) + "/api/v12/clusters/" + check_cluster_name + "/export"

    username = config['cm']['user']
    password = config['cm']['password']
    p = urllib2.HTTPPasswordMgrWithDefaultRealm()
    p.add_password(None, check_url, username, password)
    handler = urllib2.HTTPBasicAuthHandler(p)
    opener = urllib2.build_opener(handler)
    urllib2.install_opener(opener)
    page = urllib2.urlopen(check_url).read()
    return json.loads(page)

def cluster_diff():
    args_parser = argparse.ArgumentParser(
        description="Checks for differences between an input file and currently running Cloudera cluster")
    args_parser.add_argument("--check", help="JSON file representing connection information for the cluster you need to check", required=True)
    args_parser.add_argument("--reference", help="JSON file representing connection information for your reference cluster", required=True)
    args_parser.add_argument("--output",
                             help="Name of report output file, will be stored in /output, default is timestamp")

    args = args_parser.parse_args()

    print "Reading through connecting configs"
    check_config = config.read_config("configs/connect_config_check.json")
    ref_config = config.read_config("configs/connect_config_reference.json")

    check_name = check_config['cm']['host']
    ref_name = ref_config['cm']['host']

    print "Getting page responses from cluster exports..."
    check_json = get_page_response(check_config)
    ref_json = get_page_response(ref_config)

    print "Parsing check cluster: " + check_name
    check_parsed = parser.parse_cluster(check_json)
    print "Parsing reference cluster: " + ref_name
    ref_parsed = parser.parse_cluster(ref_json)

    print "\n"
    output_file_name = ""
    if args.output is not None:
        output_file_name = args.output
    else:
        output_file_name =  check_name + "-" + datetime.now().strftime("%Y%m%d-%H%M")
    file = open("output/" + output_file_name + ".txt", 'w')

    report.generate_report(check_parsed, ref_parsed, file, check_name, ref_name)

    file.write("Report completed!")

    print "Report created! Look for output in /output" + output_file_name

if __name__ == '__main__':
    cluster_diff()

