# dpps

![Version: 0.0.0-dev](https://img.shields.io/badge/Version-0.0.0--dev-informational?style=flat-square) ![Type: application](https://img.shields.io/badge/Type-application-informational?style=flat-square) ![AppVersion: 0.0.0-dev](https://img.shields.io/badge/AppVersion-0.0.0--dev-informational?style=flat-square)

A Helm chart for the DPPS project

## Maintainers

| Name | Email | Url |
| ---- | ------ | --- |
| The DPPS Authors |  |  |

## Requirements

| Repository | Name | Version |
|------------|------|---------|
| oci://harbor.cta-observatory.org/dpps | bdms | v0.1.0 |
| oci://harbor.cta-observatory.org/dpps | cert-generator-grid | v0.2.3 |
| oci://harbor.cta-observatory.org/dpps | cvmfs | v0.1.0 |
| oci://harbor.cta-observatory.org/dpps | wms | v0.1.0 |

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| bdms.cert-generator-grid.enabled | bool | `true` |  |
| bdms.configure_test_setup | bool | `true` |  |
| bdms.database.default | string | `"postgresql://rucio:XcL0xT9FgFgJEc4i3OcQf2DMVKpjIWDGezqcIPmXlM@dpps-postgresql:5432/rucio"` |  |
| bdms.postgresql.global.postgresql.auth.database | string | `"rucio"` |  |
| bdms.postgresql.global.postgresql.auth.password | string | `"XcL0xT9FgFgJEc4i3OcQf2DMVKpjIWDGezqcIPmXlM"` |  |
| bdms.postgresql.global.postgresql.auth.username | string | `"rucio"` |  |
| bdms.rucio-daemons.config.database.default | string | `"postgresql://rucio:XcL0xT9FgFgJEc4i3OcQf2DMVKpjIWDGezqcIPmXlM@dpps-postgresql:5432/rucio"` |  |
| bdms.rucio-daemons.conveyorTransferSubmitterCount | int | `1` |  |
| bdms.rucio-server.authRucioHost | string | `"rucio-server.local"` |  |
| bdms.rucio-server.config.database.default | string | `"postgresql://rucio:XcL0xT9FgFgJEc4i3OcQf2DMVKpjIWDGezqcIPmXlM@dpps-postgresql:5432/rucio"` |  |
| bdms.rucio-server.exposeErrorLogs | bool | `false` |  |
| bdms.rucio-server.ftsRenewal.enabled | bool | `false` |  |
| bdms.rucio-server.httpd_config.grid_site_enabled | string | `"True"` |  |
| bdms.rucio-server.ingress.enabled | bool | `true` |  |
| bdms.rucio-server.ingress.hosts[0] | string | `"rucio-server.local"` |  |
| bdms.rucio-server.livenessProbe.initialDelaySeconds | int | `40` |  |
| bdms.rucio-server.livenessProbe.periodSeconds | int | `10` |  |
| bdms.rucio-server.livenessProbe.successThreshold | int | `1` |  |
| bdms.rucio-server.livenessProbe.timeoutSeconds | int | `15` |  |
| bdms.rucio-server.optional_config.RUCIO_CFG_BOOTSTRAP_USERPASS_IDENTITY | string | `"dpps"` |  |
| bdms.rucio-server.optional_config.RUCIO_CFG_BOOTSTRAP_USERPASS_PWD | string | `"secret"` |  |
| bdms.rucio-server.optional_config.RUCIO_CFG_BOOTSTRAP_X509_EMAIL | string | `"dpps-test@cta-observatory.org"` |  |
| bdms.rucio-server.optional_config.RUCIO_CFG_BOOTSTRAP_X509_IDENTITY | string | `"CN=DPPS User"` |  |
| bdms.rucio-server.optional_config.RUCIO_CFG_COMMON_EXTRACT_SCOPE | string | `"ctao_bdms"` |  |
| bdms.rucio-server.optional_config.RUCIO_CFG_POLICY_LFN2PFN_ALGORITHM_DEFAULT | string | `"ctao_bdms"` |  |
| bdms.rucio-server.optional_config.RUCIO_CFG_POLICY_PACKAGE | string | `"bdms_rucio_policy"` |  |
| bdms.rucio-server.readinessProbe.initialDelaySeconds | int | `40` |  |
| bdms.rucio-server.readinessProbe.periodSeconds | int | `10` |  |
| bdms.rucio-server.readinessProbe.successThreshold | int | `1` |  |
| bdms.rucio-server.readinessProbe.timeoutSeconds | int | `15` |  |
| bdms.rucio-server.replicaCount | int | `1` |  |
| bdms.rucio-server.service.name | string | `"https"` |  |
| bdms.rucio-server.service.port | int | `443` |  |
| bdms.rucio-server.service.protocol | string | `"TCP"` |  |
| bdms.rucio-server.service.targetPort | int | `443` |  |
| bdms.rucio-server.service.type | string | `"ClusterIP"` |  |
| bdms.rucio-server.useSSL | bool | `true` |  |
| bdms.safe_to_bootstrap_rucio | bool | `true` |  |
| cert-generator-grid.enabled | bool | `false` |  |
| cert-generator-grid.generatePreHooks | bool | `true` |  |
| cvmfs.enabled | bool | `false` |  |
| dev.client_image_tag | string | `nil` |  |
| dev.mount_repo | bool | `true` |  |
| dev.runAsGroup | int | `1000` |  |
| dev.runAsUser | int | `1000` |  |
| dev.run_tests | bool | `true` |  |
| dev.sleep | bool | `false` |  |
| dev.start_long_running_client | bool | `false` |  |
| image.pullPolicy | string | `"IfNotPresent"` |  |
| image.repository_prefix | string | `"harbor.cta-observatory.org/dpps/dpps"` |  |
| wms.cert-generator-grid.enabled | bool | `false` |  |
| wms.rucio.enabled | bool | `true` |  |
| wms.rucio.rucioConfig | string | `"dpps-bdms-rucio-config"` |  |

