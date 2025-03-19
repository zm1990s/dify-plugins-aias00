# Elasticsearch Plugin

**Author:** [aias00](https://github.com/aias00)
**Version:** 0.0.1
**Type:** tool

## Description

The ElasticSearch Plugin allows users to write data into Elasticsearch.
![](./_assets/image.png)

## Features

- Write data into Elasticsearch and returns standard output and standard error

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| es_host | string | Yes | Hostname or IP address of the remote server |
| es_username | string | Conditional | Username for authentication |
| es_password | string | Conditional | Password for password authentication |
| index_name | string | Yes | Target index name in Elasticsearch |
| content | string | Yes | Content to write into Elasticsearch |

## Security Considerations

- Ensure you have permission to access the target server
- Sensitive information such as private keys and passwords should be kept secure
- Follow the principle of least privilege, granting only necessary execution permissions

## License

[MIT](./LICENSE)



