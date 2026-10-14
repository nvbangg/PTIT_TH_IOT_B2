# Báo Cáo Thực Hành AMQP với Python & RabbitMQ

## 1. Môi trường & Broker sử dụng
- **Message Broker:** RabbitMQ Server (chạy tại `localhost`, cổng mặc định AMQP `5672`).
- **Ngôn ngữ lập trình:** Python 3.x
- **Thư viện AMQP:** `pika`
- **Cài đặt thư viện:**
  ```bash
  python -m pip install pika
  ```
- **Tải và cài đặt RabbitMQ:**
  - Erlang/OTP: [OTP Releases](https://github.com/erlang/otp/releases/tag/OTP-28.5.0.7)
  - RabbitMQ Server: [RabbitMQ Releases](https://github.com/rabbitmq/rabbitmq-server/releases/latest)

---

## 2. Bài 1: Gửi và nhận message cơ bản qua queue

### Mô tả
Mô phỏng mô hình giao tiếp cơ bản `Producer -> Queue -> Consumer` qua hàng đợi `iot_lab_queue`.
- **Producer (`producer_bai1.py`):** Gửi message chứa thông tin sinh viên và lời chào định kỳ 5 giây/lần.
- **Consumer (`consumer_bai1.py`):** Lắng nghe queue `iot_lab_queue` và in nội dung kèm thời gian nhận.

### Cách chạy
1. Khởi chạy Consumer (Terminal 1):
   ```bash
   python consumer_bai1.py
   ```
2. Khởi chạy Producer (Terminal 2):
   ```bash
   python producer_bai1.py
   ```

### Kết quả đạt được
- **Producer:**
  ```text
  Da gui message: Xin chao tu ung dung Python AMQP - B23DCCN067 - Nguyễn Văn Bằng
  ```
- **Consumer:**
  ```text
  Dang lang nghe queue: iot_lab_queue...
  Da nhan message: Xin chao tu ung dung Python AMQP - B23DCCN067 - Nguyễn Văn Bằng
  Thoi gian nhan: 20:30:15
  ```

---

## 3. Bài 2: Mô phỏng cảm biến IoT gửi dữ liệu môi trường

### Mục tiêu & Yêu cầu
- Mô phỏng thiết bị IoT gửi telemetry định kỳ mỗi 3 giây vào queue `sensor_data_queue`.
- Dữ liệu ở định dạng JSON:
  ```json
  {
    "device_id": "sensor01",
    "temperature": 29.5,
    "humidity": 62.1,
    "timestamp": "2026-10-14 20:35:00"
  }
  ```
- Consumer lắng nghe queue, bóc tách dữ liệu và đưa ra cảnh báo:
  - Nếu `temperature > 35`: in `"CANH BAO: Nhiet do cao"`
  - Nếu `humidity < 40`: in `"CANH BAO: Do am thap"`

### Các chương trình
- `sensor_producer_bai2.py`: Tạo dữ liệu ngẫu nhiên của các cảm biến (`sensor01`, `sensor02`, `sensor03`), gửi tuần hoàn 3 giây/lần ở định dạng JSON.
- `monitor_consumer_bai2.py`: Lắng nghe queue `sensor_data_queue`, parse JSON, hiển thị thông số và kiểm tra điều kiện kích hoạt cảnh báo.

### Cách chạy
1. Khởi chạy Monitoring Consumer trước (Terminal 1):
   ```bash
   python monitor_consumer_bai2.py
   ```
2. Khởi chạy Sensor Producer (Terminal 2):
   ```bash
   python sensor_producer_bai2.py
   ```
3. Nhấn `Ctrl + C` ở terminal tương ứng để dừng chương trình.

### Kết quả đạt được
- **Sensor Producer:**
  ```text
  [*] Sensor Producer da ket noi toi RabbitMQ (localhost)
  [*] Dang gui du lieu dinh ky moi 3s vao queue: sensor_data_queue (Nhan Ctrl+C de dung)...

  [2026-10-14 20:40:01] Da gui: {"device_id": "sensor01", "temperature": 36.4, "humidity": 38.9, "timestamp": "2026-10-14 20:40:01"}
  [2026-10-14 20:40:04] Da gui: {"device_id": "sensor02", "temperature": 28.2, "humidity": 65.4, "timestamp": "2026-10-14 20:40:04"}
  [2026-10-14 20:40:07] Da gui: {"device_id": "sensor03", "temperature": 37.8, "humidity": 52.0, "timestamp": "2026-10-14 20:40:07"}
  ```
- **Monitoring Consumer:**
  ```text
  [*] Monitoring Consumer da ket noi toi RabbitMQ (localhost)
  [*] Dang lang nghe queue: sensor_data_queue (Nhan Ctrl+C de thoat)...
  ===================================
  Device: sensor01
  Timestamp: 2026-10-14 20:40:01
  Temperature: 36.4
  Humidity: 38.9
  CANH BAO: Nhiet do cao
  CANH BAO: Do am thap
  -----------------------------------
  Device: sensor02
  Timestamp: 2026-10-14 20:40:04
  Temperature: 28.2
  Humidity: 65.4
  -----------------------------------
  Device: sensor03
  Timestamp: 2026-10-14 20:40:07
  Temperature: 37.8
  Humidity: 52.0
  CANH BAO: Nhiet do cao
  -----------------------------------
  ```
