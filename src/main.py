import base64

from cloudevents.http import CloudEvent
import functions_framework


@functions_framework.cloud_event
def subscribe(cloud_event: CloudEvent) -> None:
    message = base64.b64decode(cloud_event.data["message"]["data"]).decode()
    if message == "fail":
        raise Exception("I was told to fail")
    else:
        print(
            "Hello, " + base64.b64decode(cloud_event.data["message"]["data"]).decode() + "!"
        )

