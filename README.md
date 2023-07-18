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

### Attach Dead Letter

**Add retry**  
*this will ensure that the function carries on retrying if failed, this can be tested by triggering the function with "fail" message*
```shell
gcloud functions deploy demo-pubsub-function \
    --gen2 \
    --runtime=python311 \
    --region=europe-west2 \
    --source=./src \
    --entry-point=subscribe \
    --trigger-topic=demo-pubsub-topic \
    --retry
```

**Create dead-letter topic and subscription**
```shell
gcloud pubsub topics create demo-deadletter-topic
gcloud pubsub subscriptions create demo-deadletter-subscription --topic=demo-deadletter-topic
```

**Configure dead-letter**  
```shell
## fetch function information to get trigger name and then get the subscription id by getting trigger information  
trigger_name=$(gcloud functions describe demo-pubsub-function --region=europe-west2 --format='value(eventTrigger.trigger)')
trigger_subscription=$(gcloud eventarc triggers describe $trigger_name --location europe-west2 --format='value(transport.pubsub.subscription)')

## update the trigger subscription to attach the dead-letter topic to it
gcloud pubsub subscriptions update $trigger_subscription \
    --dead-letter-topic=demo-deadletter-topic

## assign the project pubsub service account publisher and subscriber role to the deadletter topic and trigger subscription
gcloud pubsub topics add-iam-policy-binding demo-deadletter-topic \
    --member="serviceAccount:service-<GCP_PROJECT_NUMBER>@gcp-sa-pubsub.iam.gserviceaccount.com" \
    --role="roles/pubsub.publisher"
gcloud pubsub subscriptions add-iam-policy-binding $trigger_subscription \
    --member="serviceAccount:service-<GCP_PROJECT_NUMBER>@gcp-sa-pubsub.iam.gserviceaccount.com" \
    --role="roles/pubsub.subscriber"
```

**Trigger the function to fail**  
*this will cause the code to raise an uncaught exception and exit the function, message should then end up in the dead-letter topic*
```shell
gcloud pubsub topics publish demo-pubsub-topic --message="fail"
```

**Check pubsub dead-letter for failed messages**  
*due to retry and backoff mechanism, this might take a couple of minutes to come through*
```shell
gcloud pubsub subscriptions pull demo-deadletter-subscription
```


**Prerequisite**  
Gcloud  
Python 3.10
