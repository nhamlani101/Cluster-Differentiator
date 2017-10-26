## Cluster-Differentiator

Cluster configuration comparator to determine differences between your cluster and ideal configurations

### Usage

```
python cluster_diff.py --check <cluster_to_check json> 
                       --reference <reference_cluster json> 
                       --output <filename> 
```

### Examples

Examples JSON connection files can be found in the examples directory

### General Procedure 
1. Grabs the export file from CM hosts
2. Parses the JSON file into Python Objects
3. Compares the two clusters per config (service and role layer)
4. Exports changes into report file
5. Starts localhost:5000 to run web interface showing differences


### Pre-reqs
1. Python 2.7
2. Flask


> **NOTE:** This project is a work in progress
