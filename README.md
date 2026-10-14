# Báo Cáo Thực Hành AMQP với Python & RabbitMQ

## 1. Môi trường & Broker sử dụng
- **Message Broker:** RabbitMQ Server (chạy tại `localhost:5672`).
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

### Mục tiêu & Mô tả
- Làm quen với mô hình `Producer -> Queue -> Consumer` trong AMQP.
- Queue sử dụng: `iot_lab_queue` (kết nối broker `localhost:5672`).
- **Producer (`producer_bai1.py`):** Gửi message chứa thông tin sinh viên và lời chào định kỳ 5 giây/lần.
- **Consumer (`consumer_bai1.py`):** Lắng nghe queue `iot_lab_queue`, nhận và in nội dung kèm mốc thời gian nhận.

### Cách chạy
1. Đảm bảo RabbitMQ server đang hoạt động.
2. Khởi chạy Consumer (Terminal 1):
   ```bash
   python consumer_bai1.py
   ```
3. Khởi chạy Producer (Terminal 2):
   ```bash
   python producer_bai1.py
   ```
4. Producer gửi mỗi 5 giây. Nhấn `Ctrl + C` ở từng terminal để dừng chương trình.

### Kết quả chạy thực tế
- **Producer (`producer_bai1.py`):**
  ```text
  Da gui message: Xin chao tu ung dung Python AMQP - B23DCCN067 - Nguyễn Văn Bằng
  Da gui message: Xin chao tu ung dung Python AMQP - B23DCCN067 - Nguyễn Văn Bằng
  Da gui message: Xin chao tu ung dung Python AMQP - B23DCCN067 - Nguyễn Văn Bằng
  Da gui message: Xin chao tu ung dung Python AMQP - B23DCCN067 - Nguyễn Văn Bằng

  Ket thuc Producer
  ```
- **Consumer (`consumer_bai1.py`):**
  ```text
  Dang lang nghe queue: iot_lab_queue...
  Da nhan message: Xin chao tu ung dung Python AMQP - B23DCCN067 - Nguyễn Văn Bằng
  Thoi gian nhan: 21:00:44

  Da nhan message: Xin chao tu ung dung Python AMQP - B23DCCN067 - Nguyễn Văn Bằng
  Thoi gian nhan: 21:00:49

  Da nhan message: Xin chao tu ung dung Python AMQP - B23DCCN067 - Nguyễn Văn Bằng
  Thoi gian nhan: 21:00:54

  Da nhan message: Xin chao tu ung dung Python AMQP - B23DCCN067 - Nguyễn Văn Bằng
  Thoi gian nhan: 21:00:59

  Ket thuc Consumer
  ```

---

## 3. Bài 2: Mô phỏng cảm biến IoT gửi dữ liệu môi trường

### Mục tiêu & Mô tả
- Mô phỏng thiết bị IoT gửi dữ liệu telemetry định kỳ qua AMQP.
- Queue sử dụng: `sensor_data_queue`.
- **Producer (`sensor_producer_bai2.py`):** Mô phỏng cảm biến gửi dữ liệu môi trường định kỳ 3 giây/lần dưới định dạng JSON (`device_id`, `temperature`, `humidity`, `timestamp`). Giá trị nhiệt độ và độ ẩm được sinh ngẫu nhiên bao phủ các ngưỡng cảnh báo.
- **Consumer (`monitor_consumer_bai2.py`):** Lắng nghe dữ liệu telemetry từ queue, phân tích thông số và kiểm tra điều kiện phát cảnh báo:
  - Nếu `temperature > 35`: Cảnh báo `"CANH BAO: Nhiet do cao"`
  - Nếu `humidity < 40`: Cảnh báo `"CANH BAO: Do am thap"`

### Cách chạy
1. Khởi chạy Monitoring Consumer trước (Terminal 1):
   ```bash
   python monitor_consumer_bai2.py
   ```
2. Khởi chạy Sensor Producer (Terminal 2):
   ```bash
   python sensor_producer_bai2.py
   ```
3. Nhấn `Ctrl + C` ở từng terminal để dừng chương trình.

### Kết quả chạy thực tế
- **Sensor Producer (`sensor_producer_bai2.py`):**
  ```text
  [*] Sensor Producer da ket noi toi RabbitMQ (localhost)
  [*] Dang gui du lieu dinh ky moi 3s vao queue: sensor_data_queue (Nhan Ctrl+C de dung)...

  [2026-10-14 20:40:01] Da gui: {"device_id": "sensor01", "temperature": 36.4, "humidity": 38.9, "timestamp": "2026-10-14 20:40:01"}
  [2026-10-14 20:40:04] Da gui: {"device_id": "sensor02", "temperature": 28.2, "humidity": 65.4, "timestamp": "2026-10-14 20:40:04"}
  [2026-10-14 20:40:07] Da gui: {"device_id": "sensor03", "temperature": 37.8, "humidity": 52.0, "timestamp": "2026-10-14 20:40:07"}
  ```
- **Monitoring Consumer (`monitor_consumer_bai2.py`):**
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

---

## 4. Bài 3: Mô phỏng hệ thống điều phối cảnh báo IoT với Exchange

### Mục tiêu & Mô tả
- Làm quen với `Exchange` và `Routing Key` trong AMQP để định tuyến message tới đúng consumer tương ứng theo mức độ cảnh báo.
- Exchange sử dụng: `iot_alert_exchange` (loại `direct`).
- **Producer (`alert_producer_bai3.py`):** Gửi cảnh báo tới exchange với các routing key:
  - `info`: Thông tin trạng thái bình thường (không có consumer nhận).
  - `warning`: Cảnh báo mức cảnh giác.
  - `critical`: Cảnh báo mức nguy cấp.
- **Warning Consumer (`warning_consumer_bai3.py`):** Tạo queue `warning_queue`, bind với `iot_alert_exchange` bằng routing key `warning`, in cảnh báo và ghi log ra file `alerts.log`.
- **Critical Consumer (`critical_consumer_bai3.py`):** Tạo queue `critical_queue`, bind với `iot_alert_exchange` bằng routing key `critical`, in cảnh báo và ghi log ra file `alerts.log`.

### Cách chạy
Khởi chạy các Consumer trước để sẵn sàng nhận cảnh báo từ Producer:
1. Khởi chạy Warning Consumer (Terminal 1):
   ```bash
   python warning_consumer_bai3.py
   ```
2. Khởi chạy Critical Consumer (Terminal 2):
   ```bash
   python critical_consumer_bai3.py
   ```
3. Khởi chạy Alert Producer (Terminal 3):
   ```bash
   python alert_producer_bai3.py
   ```

### Kết quả chạy thực tế
- **Alert Producer (`alert_producer_bai3.py`):**
  ```text
  [producer] Da gui [info]: Nhiet do phong may binh thuong
  [producer] Da gui [warning]: Nhiet do phong may vuot nguong warning
  [producer] Da gui [critical]: Cam bien kho lanh mat ket noi critical
  ```
- **Warning Consumer (`warning_consumer_bai3.py`):**
  ```text
  [warning_queue] Dang cho canh bao 'warning'. Nhan CTRL+C de thoat.
  [warning_queue] Da nhan: Nhiet do phong may vuot nguong warning
  ```
- **Critical Consumer (`critical_consumer_bai3.py`):**
  ```text
  [critical_queue] Dang cho canh bao 'critical'. Nhan CTRL+C de thoat.
  [critical_queue] Da nhan: Cam bien kho lanh mat ket noi critical
  ```
- **File nhật ký cảnh báo (`alerts.log`):**
  ```text
  [warning_queue] Da nhan: Nhiet do phong may vuot nguong warning
  [critical_queue] Da nhan: Cam bien kho lanh mat ket noi critical
  ```
- *(Lưu ý: Message `info` không hiển thị ở consumer nào do không có queue nào bind với routing key này, phản ánh đúng cơ chế định tuyến Direct Exchange).*

---

## 5. Tổng kết danh mục file nộp bài
| Bài | File chương trình | Vai trò |
|---|---|---|
| **Bài 1** | `producer_bai1.py` | Gửi message chào mừng định kỳ vào queue |
| | `consumer_bai1.py` | Lắng nghe và hiển thị message kèm thời gian |
| **Bài 2** | `sensor_producer_bai2.py` | Sinh ngẫu nhiên và gửi telemetry JSON mỗi 3s |
| | `monitor_consumer_bai2.py` | Nhận telemetry, phân tích và phát hiện cảnh báo |
| **Bài 3** | `alert_producer_bai3.py` | Gửi cảnh báo đa mức qua direct exchange |
| | `warning_consumer_bai3.py` | Nhận và ghi log cảnh báo mức warning |
| | `critical_consumer_bai3.py` | Nhận và ghi log cảnh báo mức critical |
| **Tài liệu**| `README.md` | Báo cáo chi tiết môi trường, cách chạy và kết quả |
