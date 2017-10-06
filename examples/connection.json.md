## Input Config JSON

```json
{
  "services": {
    "HDFS": {
      "config": {
        "dfs_data_transfer_protection": "privacy",
        "dfs_datanode_read_shortcircuit": "true",
        "hadoop_security_authentication": "true",
        "hdfs_hadoop_ssl_enabled": "false",
        "ssl_client_truststore_location": "/etc/cdep-ssl-conf/CA_STANDARDS/truststore.jks"
      },
      "roleConfigGroups": {
        "BALANCER": {
          "balancer_java_heapsize": "597688320"
        },
        "DATANODE": {
          "datanode_java_heapsize": "961544192",
          "dfs_data_dir_list": "/dfs/dx",
          "dfs_datanode_max_locked_memory": "14040439"
        },
        "FAILOVERCONTROLLER" : {
          "heap_dump_directory_free_space_percentage_thresholds": "{\"critical\":\"10.0\",\"warning\":\"20.0\"}"
        },
        "SECONDARYNAMENODE" : {
          "dfs_secondary_http_port": "20201"
        }
      }
    },
    "ZOOKEEPER": {
      "config": {
        "enableSecurity": "true"
      },
      "roleConfigGroups": {
        "SERVER" : {
          "maxSessionTimeout": "60000"
        }
      }
    }
  }
}

```
##### The input JSON is essentially a stripped down version of a cluster config with only the necessary information

> **NOTE:** The services and the roleConfigs must be listed by Type NOT Name

