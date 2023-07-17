import base64

from cloudevents.http import CloudEvent
import functions_framework


@functions_framework.cloud_event
def subscribe(cloud_event: CloudEvent) -> None:
    print(
        "Hello, " + base64.b64decode(cloud_event.data["message"]["data"]).decode() + "!"
    )

