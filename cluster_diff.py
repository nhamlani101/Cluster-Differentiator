import provisionator.config as config
import config_parser
import report
import argparse
import urllib2
import json
from datetime import datetime

from flask import Flask, render_template

app = Flask(__name__)

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

@app.route('/')
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
    check_parsed = config_parser.parse_cluster(check_json)
    print check_name + " has been parsed"
    print "Parsing reference cluster: " + ref_name
    ref_parsed = config_parser.parse_cluster(ref_json)
    print ref_name + " has been parsed"

    print "\n"
    output_file_name = ""
    if args.output is not None:
        output_file_name = args.output
    else:
        output_file_name =  check_name + "-" + datetime.now().strftime("%Y%m%d-%H%M")
    file = open("output/" + output_file_name + ".txt", 'w')

    out_list = report.generate_report_file(check_parsed, ref_parsed, file, check_name, ref_name)
    file.write("Report completed!")
    print "Report created! Look for output in /output/" + output_file_name


    for i in out_list:
        print i.type
        print i.service
    #return Response(report.generate_report_html(check_parsed, ref_parsed, file, check_name, ref_name))

    return render_template('index.html', output_list=out_list, check_host=check_name, ref_host=ref_name)

if __name__ == '__main__':
    app.run(host='localhost')
    cluster_diff()

