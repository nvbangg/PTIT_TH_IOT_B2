import json
import random
import time
from datetime import datetime
import pika

BROKER = "localhost"
QUEUE = "sensor_data_queue"
DEVICE_IDS = ["sensor01", "sensor02", "sensor03"]


def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=BROKER))
    channel = connection.channel()

    # Đảm bảo queue tồn tại
    channel.queue_declare(queue=QUEUE)
    print(f"[*] Sensor Producer da ket noi toi RabbitMQ ({BROKER})")
    print(f"[*] Dang gui du lieu dinh ky moi 3s vao queue: {QUEUE} (Nhan Ctrl+C de dung)...\n")

    try:
        while True:
            # Sinh ngẫu nhiên nhiệt độ (20.0 - 42.0°C) và độ ẩm (30.0 - 85.0%)
            # Giá trị này bao phủ các ngưỡng cảnh báo: temp > 35 và humidity < 40
            payload = {
                "device_id": random.choice(DEVICE_IDS),
                "temperature": round(random.uniform(20.0, 42.0), 1),
                "humidity": round(random.uniform(30.0, 85.0), 1),
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }

            message_body = json.dumps(payload, ensure_ascii=False)
            channel.basic_publish(
                exchange="",
                routing_key=QUEUE,
                body=message_body.encode("utf-8"),
                properties=pika.BasicProperties(
                    content_type="application/json",
                    delivery_mode=pika.DeliveryMode.Transient
                )
            )

            print(f"[{payload['timestamp']}] Da gui: {message_body}")
            time.sleep(3)

    except KeyboardInterrupt:
        print("\n[!] Dung Sensor Producer")
    finally:
        if connection.is_open:
            connection.close()


if __name__ == "__main__":
    main()
