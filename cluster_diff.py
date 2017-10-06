import provisionator.config as config
import provisionator.util as util
import parser
import report
import argparse
from datetime import datetime


def connect_to_cluster(conf_file):
    api = util.get_api_handle(conf_file)
    cm = api.get_cluster(conf_file["clusters"]["name"])
    print "Cluster has connected to: " + conf_file["cm"]["host"]
    return cm


if __name__ == '__main__':
    args_parser = argparse.ArgumentParser(
        description="Checks for differences between an input file and currently running Cloudera cluster")
    args_parser.add_argument("--input", help="JSON file representing ideal cluster configuarations", required=True)
    args_parser.add_argument("--connect", help="JSON file with cluster connection attributes", required=True)
    args_parser.add_argument("--output",
                             help="Name of report output file, will be stored in /output, default is timestamp")

    args = args_parser.parse_args()

    cm_connection = config.read_config(args.connect)
    gold = config.read_config(args.input)

    try:
        cluster_to_check = connect_to_cluster(cm_connection)
    except:
        print "ERROR: Could not connect to cluster"
        exit(1)

    store = parser.get_store(cluster_to_check, gold)

    host_name = cm_connection["cm"]["host"]

    output_file_name = ""
    if args.output is not None:
        output_file_name = args.output
    else:
        output_file_name = host_name + "-" + datetime.now().strftime("%Y%m%d-%H%M")
    file = open("output/" + output_file_name + ".txt", 'w')

    report.create_report(store, host_name, file)

    print "Report has been completed"
    print "Find report in output/" + output_file_name
