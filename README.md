# Gen2 Cloud function Pubsub

**Create pubsub topic**
```shell
gcloud pubsub topics create my-pubsub-topic
```

**Deploy function**

```shell
gcloud functions deploy my-pubsub-function \
    --gen2 \
    --runtime=python311 \
    --region=europe-west2 \
    --source=./src \
    --entry-point=subscribe \
    --trigger-topic=my-pubsub-topic
```

**Trigger the function to pass**  
*function will run and print the greeting*
```shell
gcloud pubsub topics publish my-topic --message="World"
```

**Trigger the function to fail**  
*this will cause the code to raise an uncaught exception and exit the function*
```shell
gcloud pubsub topics publish my-topic --message="fail"
```

**Read logs**
```shell
gcloud beta functions logs read my-pubsub-function --gen2
```

**Prerequisite**  
Gcloud  
Python 3.10
