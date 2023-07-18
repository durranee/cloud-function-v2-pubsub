# Gen2 Cloud function Pubsub

This simple cloud function gets triggered on a pubsub message and prints a greeting. If the message passed is "fail", the function code will raise an exception which will force the function to exit ungracefully.
After configuring the dead-letter, every run that fails to complete will be retried and will end up in the dead-letter topic once the retries are exhausted.

### Deploy Cloud Function  

**Create pubsub topic**
```shell
gcloud pubsub topics create demo-pubsub-topic
```

**Deploy function**

```shell
gcloud functions deploy demo-pubsub-function \
    --gen2 \
    --runtime=python311 \
    --region=europe-west2 \
    --source=./src \
    --entry-point=subscribe \
    --trigger-topic=demo-pubsub-topic
```

**Trigger the function to pass**  
*function will run and print the greeting*
```shell
gcloud pubsub topics publish demo-pubsub-topic --message="World"
```

**Trigger the function to fail**  
*this will cause the code to raise an uncaught exception and exit the function*
```shell
gcloud pubsub topics publish demo-pubsub-topic --message="fail"
```

**Read logs**
```shell
gcloud beta functions logs read  demo-pubsub-function --region=europe-west2 --gen2
```
