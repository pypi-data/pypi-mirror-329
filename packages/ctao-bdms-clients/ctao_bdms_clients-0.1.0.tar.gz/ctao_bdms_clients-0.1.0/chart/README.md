# bdms

![Version: 0.1.0](https://img.shields.io/badge/Version-0.1.0-informational?style=flat-square) ![Type: application](https://img.shields.io/badge/Type-application-informational?style=flat-square) ![AppVersion: 0.1.0](https://img.shields.io/badge/AppVersion-0.1.0-informational?style=flat-square)

A Helm chart for the bdms project

## Maintainers

| Name | Email | Url |
| ---- | ------ | --- |
| The BDMS Authors |  |  |

## Requirements

| Repository | Name | Version |
|------------|------|---------|
| oci://harbor.cta-observatory.org/dpps | cert-generator-grid | v0.2.2 |
| oci://harbor.cta-observatory.org/dpps | fts | v0.1.0 |
| oci://harbor.cta-observatory.org/dpps | rucio-daemons | 35.0.0 |
| oci://harbor.cta-observatory.org/dpps | rucio-server | 35.0.0 |
| oci://registry-1.docker.io/bitnamicharts | postgresql | 15.5.10 |

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| auth.authRucioHost | string | `"rucio-server.local"` | The hostname of the Rucio authentication server. It is used by clients and services to authenticate with Rucio |
| auth.certificate.existingSecret.cert | string | `"tls.crt"` | The key inside the kubernetes secret that stores the TLS certificate |
| auth.certificate.existingSecret.enabled | bool | `true` | Use an existing kubernetes (K8s) secret for certificates instead of creating new ones |
| auth.certificate.existingSecret.key | string | `"tls.key"` | The key inside the kubernetes secret that stores the private key |
| auth.certificate.existingSecret.secretName | string | `"rucio-server.local"` | The name of the kubernetes secret containing the TLS certificate and key |
| auth.certificate.letsencrypt.email | string | `""` | Email address for Let's encrypt registration and renewal reminders |
| auth.certificate.letsencrypt.enabled | bool | `false` | Enables SSL/TLS certificate provisioning using Let's encrypt |
| bootstrap.image.repository | string | `"harbor.cta-observatory.org/dpps/bdms-rucio-server"` | The container image for bootstrapping Rucio (initialization, configuration) with the CTAO Rucio policy package installed |
| bootstrap.image.tag | string | `"35.4.1-v0.1.0"` | The specific image tag to use for the bootstrap container |
| cert-generator-grid.enabled | bool | `true` |  |
| cert-generator-grid.generatePreHooks | bool | `true` |  |
| configure_test_setup | bool | `true` | This will configure the rucio server with the storages |
| database | object | `{"default":"postgresql://rucio:XcL0xT9FgFgJEc4i3OcQf2DMVKpjIWDGezqcIPmXlM@bdms-postgresql:5432/rucio"}` | Databases Credentials used by Rucio to access the database. If postgresql subchart is deployed, these credentials should match those in postgresql.global.postgresql.auth. If postgresql subchart is not deployed, an external database must be provided |
| database.default | string | `"postgresql://rucio:XcL0xT9FgFgJEc4i3OcQf2DMVKpjIWDGezqcIPmXlM@bdms-postgresql:5432/rucio"` | The Rucio database connection URI |
| dev.client_image_tag | string | `nil` |  |
| dev.mount_repo | bool | `true` |  |
| dev.run_tests | bool | `true` |  |
| dev.sleep | bool | `false` | sleep after test to allow interactive development |
| fts.enabled | bool | `true` | Specifies the configuration for FTS test step (FTS server, FTS database, and ActiveMQ broker containers). Enables or disables the deployment of a FTS instance for testing. This is set to 'False' if an external FTS is used |
| fts.ftsdb_password | string | `"SDP2RQkbJE2f+ohUb2nUu6Ae10BpQH0VD70CsIQcDtM"` | Defines the password for the FTS database user |
| fts.ftsdb_root_password | string | `"iB7dMiIybdoaozWZMkvRo0eg9HbQzG9+5up50zUDjE4"` | Defines the root password for the FTS database |
| fts.image.pullPolicy | string | `"Always"` |  |
| fts.image.repository | string | `"harbor.cta-observatory.org/proxy_cache/rucio/fts"` | The container image repository for the FTS deployment |
| fts.image.tag | string | `"35.4.1"` | Defines the specific version of the FTS image to use |
| fts.messaging.broker | string | `"localhost:61613"` |  |
| fts.messaging.password | string | `"topsecret"` |  |
| fts.messaging.use_broker_credentials | string | `"true"` |  |
| fts.messaging.username | string | `"fts"` |  |
| postgresql.enabled | bool | `true` | Configuration of built-in postgresql database. If 'enabled: true', a postgresql instance will be deployed, otherwise, an external database must be provided in database.default value |
| postgresql.global.postgresql.auth.database | string | `"rucio"` | The name of the database to be created and used by Rucio |
| postgresql.global.postgresql.auth.password | string | `"XcL0xT9FgFgJEc4i3OcQf2DMVKpjIWDGezqcIPmXlM"` | The password for the database user |
| postgresql.global.postgresql.auth.username | string | `"rucio"` | The database username for authentication |
| prepuller_enabled | bool | `true` | Starts containers with the same image as the one used in the deployment before all volumes are available. Saves time in the first deployment |
| rethinkdb.enabled | bool | `false` |  |
| rethinkdb.storageClassName | string | `nil` |  |
| rethinkdb.storageSize | string | `"1Gi"` |  |
| rucio-daemons.config.database.default | string | `"postgresql://rucio:XcL0xT9FgFgJEc4i3OcQf2DMVKpjIWDGezqcIPmXlM@bdms-postgresql:5432/rucio"` | Specifies the connection URI for the Rucio database, these settings will be written to 'rucio.cfg' |
| rucio-daemons.config.messaging-fts3.brokers | string | `"fts-activemq"` | Specifies the message broker used for FTS messaging |
| rucio-daemons.config.messaging-fts3.destination | string | `"/topic/transfer.fts_monitoring_complete"` | Specifies the message broker queue path where FTS sends transfer status updates. This is the place where Rucio listens for completed transfer notifications |
| rucio-daemons.config.messaging-fts3.nonssl_port | int | `61613` | Specifies the non-SSL port |
| rucio-daemons.config.messaging-fts3.password | string | `"topsecret"` | Specifies the authentication credential (password) for connecting to the message broker |
| rucio-daemons.config.messaging-fts3.port | int | `61613` | Defines the port used for the broker |
| rucio-daemons.config.messaging-fts3.use_ssl | bool | `false` | Determines whether to use SSL for message broker connections. If true, valid certificates are required for securing the connection |
| rucio-daemons.config.messaging-fts3.username | string | `"fts"` | Specifies the authentication credential (username) for connecting to the message broker |
| rucio-daemons.config.policy.permission | string | `"ctao"` | Defines the policy permission model for Rucio for determining how authorization and access controls are applied, its value should be taken from the installed Rucio policy package |
| rucio-daemons.conveyorFinisher.activities | string | `"'User Subscriptions'"` | Specifies which Rucio activities to be handled. Some of the activities for data movements are 'User Subscriptions' and 'Production Transfers' |
| rucio-daemons.conveyorFinisher.resources.limits.cpu | string | `"3000m"` |  |
| rucio-daemons.conveyorFinisher.resources.limits.memory | string | `"4Gi"` |  |
| rucio-daemons.conveyorFinisher.resources.requests.cpu | string | `"700m"` |  |
| rucio-daemons.conveyorFinisher.resources.requests.memory | string | `"200Mi"` |  |
| rucio-daemons.conveyorFinisher.sleepTime | int | `5` | Defines how often (in seconds) the daemon processes finished transfers |
| rucio-daemons.conveyorFinisherCount | int | `1` | Marks completed transfers and updates metadata |
| rucio-daemons.conveyorPoller.activities | string | `"'User Subscriptions'"` | Specifies which Rucio activities to be handled. Some of the activities for data movements are 'User Subscriptions' and 'Production Transfers' |
| rucio-daemons.conveyorPoller.olderThan | int | `600` | Filters transfers that are older than the specified time (in seconds) before polling |
| rucio-daemons.conveyorPoller.resources.limits.cpu | string | `"3000m"` |  |
| rucio-daemons.conveyorPoller.resources.limits.memory | string | `"4Gi"` |  |
| rucio-daemons.conveyorPoller.resources.requests.cpu | string | `"700m"` |  |
| rucio-daemons.conveyorPoller.resources.requests.memory | string | `"200Mi"` |  |
| rucio-daemons.conveyorPoller.sleepTime | int | `60` | Defines how often (in seconds) the daemon polls for transfer status updates |
| rucio-daemons.conveyorPollerCount | int | `1` | Polls FTS to check the status of ongoing transfers |
| rucio-daemons.conveyorReceiverCount | int | `1` | Listens to messages from ActiveMQ, which FTS uses to publish transfer status updates. This ensures Rucio is notified of completed or failed transfers in real time |
| rucio-daemons.conveyorTransferSubmitter.activities | string | `"'User Subscriptions'"` | Specifies which Rucio activities to be handled. Some of the activities for data movements are 'User Subscriptions' and 'Production Transfers' |
| rucio-daemons.conveyorTransferSubmitter.archiveTimeout | string | `""` | Sets the timeout if required for archiving completed transfers |
| rucio-daemons.conveyorTransferSubmitter.resources.limits.cpu | string | `"3000m"` |  |
| rucio-daemons.conveyorTransferSubmitter.resources.limits.memory | string | `"4Gi"` |  |
| rucio-daemons.conveyorTransferSubmitter.resources.requests.cpu | string | `"700m"` |  |
| rucio-daemons.conveyorTransferSubmitter.resources.requests.memory | string | `"200Mi"` |  |
| rucio-daemons.conveyorTransferSubmitter.sleepTime | int | `5` | Defines the interval (in seconds) the daemon waits before checking for new transfers |
| rucio-daemons.conveyorTransferSubmitterCount | int | `1` | Number of container instances to deploy for each Rucio daemon, this daemon submits new transfer requests to the FTS |
| rucio-daemons.image.pullPolicy | string | `"Always"` | It defines when kubernetes should pull the container image, the options available are: Always, IfNotPresent, and Never |
| rucio-daemons.image.repository | string | `"harbor.cta-observatory.org/dpps/bdms-rucio-daemons"` | Specifies the container image repository for Rucio daemons |
| rucio-daemons.image.tag | string | `"35.4.1-v0.1.0"` | Specific image tag to use for deployment |
| rucio-daemons.judgeEvaluatorCount | int | `1` | Evaluates Rucio replication rules and triggers transfers |
| rucio-daemons.useDeprecatedImplicitSecrets | bool | `true` | Enables the use of deprecated implicit secrets for authentication |
| rucio-server.authRucioHost | string | `"rucio-server.local"` | The hostname of the Rucio authentication server. |
| rucio-server.config.database.default | string | `"postgresql://rucio:XcL0xT9FgFgJEc4i3OcQf2DMVKpjIWDGezqcIPmXlM@bdms-postgresql:5432/rucio"` | The database connection URI for Rucio |
| rucio-server.config.persistence.accessMode | string | `"ReadWriteOnce"` | Defines how storage can be accessed, the options available are: ReadWriteOnce, ReadOnlyMany, ReadWriteMany |
| rucio-server.config.persistence.enabled | bool | `true` | Enables persistent storage for Rucio server, setting it to false means using temporary storage ('ephemeral' in the context of kubernetes) that gets wiped out and lost when the container is stopped or restarted |
| rucio-server.config.persistence.size | string | `"1Gi"` | Defines the size of persistent volume claim (PVC) or the amount of the storage capacity provisioned to the Rucio server |
| rucio-server.config.persistence.storageClass | string | `""` | Specifies the kubernetes storage class for persistent volume, default storage class is used when its value is left empty |
| rucio-server.ftsRenewal.enabled | bool | `false` | Enables automatic renewal of FTS credentials using X.509 certificates and proxy |
| rucio-server.httpd_config.encoded_slashes | string | `"True"` | Allows for custom LFNs with slashes in request URLs so that Rucio server (Apache) can decode and handle such requests properly |
| rucio-server.httpd_config.grid_site_enabled | string | `"True"` | Enables Rucio server to support and interact with grid middleware (storages) for X509 authentication with proxies |
| rucio-server.image.pullPolicy | string | `"Always"` | It defines when kubernetes should pull the container image, the options available are: Always, IfNotPresent, and Never |
| rucio-server.image.repository | string | `"harbor.cta-observatory.org/dpps/bdms-rucio-server"` | The container image repository for Rucio server with the CTAO Rucio policy package installed |
| rucio-server.image.tag | string | `"35.4.1-v0.1.0"` | The specific image tag to deploy |
| rucio-server.ingress.enabled | bool | `true` | Enables an ingress resource (controller) for exposing the Rucio server externally to allow clients connect to the Rucio server. It needs one of the ingress controllers (NGINX, Traefik) to be installed |
| rucio-server.ingress.hosts | list | `["rucio-server-manual-tc.local"]` | Defines the hostname to be used to access the Rucio server. It should match DNS configuration and TLS certificates |
| rucio-server.replicaCount | int | `1` | Number of replicas of the Rucio server to deploy. We can increase it to meet higher availability goals |
| rucio-server.service.name | string | `"https"` | The name of the service port |
| rucio-server.service.port | int | `443` | The port exposed by the kubernetes service, making the Rucio server accessible within the cluster |
| rucio-server.service.protocol | string | `"TCP"` | The network protocol used for HTTPS based communication |
| rucio-server.service.targetPort | int | `443` | The port inside the Rucio server container that listens for incoming traffic |
| rucio-server.service.type | string | `"ClusterIP"` | Specifies the kubernetes service type for making the Rucio server accessible within or outside the kubernetes cluster, available options include clusterIP (internal access only, default), NodePort (exposes the service on port across all cluster nodes), and LoadBalancer (Uses an external load balancer) |
| rucio-server.useSSL | bool | `true` | Enables the Rucio server to use SSL/TLS for secure communication, requiring valid certificates to be configured |
| rucio.password | string | `"secret"` |  |
| rucio.username | string | `"dpps"` | Specifies the username for Rucio operations as part of Rucio configuration |
| rucio.version | string | `"35.4.1"` | The version of Rucio being deployed |
| rucio_db.connection | string | `"postgresql://rucio:XcL0xT9FgFgJEc4i3OcQf2DMVKpjIWDGezqcIPmXlM@bdms-postgresql:5432/rucio"` | The database connection URI for Rucio. It is of the format: `postgresql://<user>:<password>@<host>:<port>/<database>`, this field in use only if 'existingSecret.enabled' is set to 'false', otherwise ignored |
| rucio_db.deploy | bool | `true` | If true, deploys a postgresql instance for the Rucio database, otherwise use an external database |
| rucio_db.existingSecret.enabled | bool | `false` | If true, the database connection URI is obtained from a kubernetes secret in |
| rucio_db.existingSecret.key | string | `"connection"` | The key inside the kubernetes secret that holds the database connection URI |
| rucio_db.existingSecret.secretName | string | `"rucio-db"` | The name of the kubernetes secret storing the database connection URI. Its in use only if 'existingSecret.enabled: true' |
| safe_to_bootstrap_rucio | bool | `true` | This is a destructive operation, it will delete all data in the database |
| server.certificate.existingSecret.cert | string | `"tls.crt"` | The key inside the kubernetes secret that stores the TLS certificate |
| server.certificate.existingSecret.enabled | bool | `true` | Use an existing kubernetes (K8s) secret for certificates instead of creating new ones |
| server.certificate.existingSecret.key | string | `"tls.key"` | The key inside the kubernetes secret that stores the private key |
| server.certificate.existingSecret.secretName | string | `"rucio-server-manual-tc.local"` | The name of the kubernetes secret containing the TLS certificate and key |
| server.certificate.letsencrypt.email | string | `""` |  |
| server.certificate.letsencrypt.enabled | bool | `false` | Enables SSL/TLS certificate provisioning using Let's encrypt |
| server.rucioHost | string | `"rucio-server-manual-tc.local"` | The hostname of the Rucio server. It is used by clients and services to communicate with Rucio |
| storages | list | `["rucio-storage-1","rucio-storage-2","rucio-storage-3"]` | a list of storage element (RSE) hostnames names, for each RSE, one deployment and service are configured, two configmaps xrdconfig and xrd-entrypoint for those three storages |
| suffix_namespace | string | `"default"` | Specifies the Namespace suffix used for managing deployments in kubernetes |

