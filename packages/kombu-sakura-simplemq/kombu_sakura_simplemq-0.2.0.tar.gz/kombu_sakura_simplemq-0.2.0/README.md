# Kombu Tramsport for Sakura Cloud SimpleMQ


## Install

```
pip install kombu-sakura-simplemq
```

### Quick overview

```python
from kombu import transport, Connection, Queue

transport.TRANSPORT_ALIASES["sakura-simplemq"] = "kombu_sakura_simplemq.transport:Transport"

with Connection("sakura-simplemq://:{}@".format("YOUR_SIMPLEMQ_API_KEY")) as conn:
    queue_name = "somequeue"
    queue = Queue(queue_name)
    queue.maybe_bind(conn)
    queue.declare()

    # メッセージ送信
    producer = conn.Producer()
    producer.publish(
        body="Hello, custom Transport!",
        routing_key=queue_name,
    )

    def handle_message(body, message):
        print(f"Received message: {body}")
        message.ack()

    # メッセージ受信
    with conn.Consumer(queue, callbacks=[handle_message]):
        while True:
            conn.drain_events(timeout=2)
```
