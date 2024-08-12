import json

from broker.middleware import KafkaMiddleware
from broker.topics import Topics
from networks.model_types import srgan_x2_image_processor

consumer = KafkaMiddleware.get_consumer(client_id="image_enhance_service", group_id="enhance_x2")
consumer.subscribe([Topics.image_enhance.value])
middleware = KafkaMiddleware(service_name="image_enhance_service")

if __name__ == '__main__':
    try:
        while True:
            try:
                msg = consumer.poll(1.0)
                if msg is None:
                    continue
                data = json.loads(msg.value().decode("utf-8"))
                if data is not None:
                    print("started image enhance")
                    print(data)
                    print("path from message: " + data['path_to_picture'])
                    result_path = srgan_x2_image_processor.update(path_to_picture=data['path_to_picture'])
                    middleware.send_message(topic=Topics.bot_response,
                                            message={"result_path": result_path,
                                                     "send_to": data['message_from']})
                    print("image enhanced successfully. Pending...")
            except Exception as e:
                print(f"Error deserializing message: {e}")
                continue
    finally:
        consumer.close()
