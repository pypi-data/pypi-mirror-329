# DyffiClient

**DyffiClient** is a lightweight Python library for interacting with Dyffi-Bus via HTTP and WebSockets. It abstracts away the details of publishing messages and subscribing to topics, letting you focus on your application logic.

## Installation


```bash
pip install dyffi-client
```

## Usage

### 1. Create a Client

```python
from dyffi_bus_client import DyffiBusClient

# Initialize the client with the base URL of your pub/sub service
client = DyffiBusClient("http://127.0.0.1:8000")
```

### 2. Publish Messages

```python
message_id = client.publish("orders", {"order_id": 123, "customer": "Alice"})
print("Sent message with ID:", message_id)
```

- **`topic`**: The topic name to publish to.
- **`payload`**: A dictionary containing the message data.

### 3. Subscribe to a Topic

```python
def order_handler(message):
    print("Got Message:", message)
    print("Order ID:", message["payload"]["order_id"])

client.subscribe("orders", order_handler, blocking=False)
```

- **`topic`**: The topic name to subscribe to.
- **`handler`**: A callback function that receives the message as a Python dictionary.
- **`blocking=False`**: The subscription runs in a separate thread, so your main program can continue doing other things.  
  If you set `blocking=True`, the subscription loop will block the current thread until you stop it (e.g., with Ctrl+C).

### 4. Keep the Main Thread Alive (Optional)

If you used non-blocking subscriptions, you can call:

```python
client.listen()
```

This starts a simple loop that keeps your script running indefinitely. Press Ctrl+C to stop.

## Full Examples

### Example: Publishing

```python
from dyffi_bus_client import DyffiBusClient

client = DyffiBusClient("http://127.0.0.1:8000")

message_id = client.publish("orders", {"order_id": 123, "customer": "Alice"})
print("Sent message with ID:", message_id)
```

### Example: Subscribing to Multiple Topics

```python
from dyffi_bus_client import DyffiBusClient


def order_handler(message):
  print("Got Message:", message)
  print("Order ID:", message["payload"]["order_id"])


def topic_handler(message):
  print("Got Message:", message)


client = DyffiBusClient("http://127.0.0.1:8000")

# Subscribe to 'orders' in a non-blocking thread
client.subscribe("orders", order_handler, blocking=False)

# Subscribe to 'myTopic' in a blocking manner
client.subscribe("myTopic", topic_handler, blocking=True)
```

In this example:
- We listen to **orders** in a separate thread (non-blocking).
- We then subscribe to **myTopic** in blocking mode, so the program stays alive until we stop it.

## How It Works

- **`publish(topic, payload)`**  
  Sends an HTTP POST request to `<api_url>/publish` with the given topic and payload.
- **`subscribe(topic, handler, blocking=False)`**  
  Opens a WebSocket connection to `<api_url>/ws/<topic>` in a separate thread, calling `handler(message)` for every new message.  
  If `blocking=True`, it runs on the main thread until stopped.
- **`listen()`**  
  A simple blocking loop that keeps the main thread alive if you used non-blocking subscriptions.

## License

This library is provided under the [MIT License](LICENSE). Feel free to open issues or submit pull requests if you encounter any problems or have ideas for new features.
