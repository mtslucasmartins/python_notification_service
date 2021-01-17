# Python Notification Service

A simple service application to send WebPush API Notifications.

### Examples

#### Getting persisted notifications
```shell
curl -v "https://<>/api/v1/notifications?username=lucas@ottimizza.com.br&application_id=ottimizza " \
  -H 
  -H 
  -o /dev/null

```



## Installation

This project's official image is available at [DockerHub](https://hub.docker.com/r/mtslucasmartins/python_notification_service).
```bash
$ docker pull mtslucasmartins/python_notification_service:latest
```

Run the image:

```bash
$ docker run -d mtslucasmartins/python_notification_service:latest
```


## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)