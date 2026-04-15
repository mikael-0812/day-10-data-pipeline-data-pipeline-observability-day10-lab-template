# Day 10 Lab: Data Pipeline & Data Observability


**Student ID:** AI20K-2A202600171
**Name:** Nguyen Khanh Huyen

---

## Mô tả

Bài lab này xây dựng một ETL pipeline đơn giản bằng Python để xử lý dữ liệu từ file JSON. Mục tiêu chính là đọc dữ liệu đầu vào, kiểm tra và loại bỏ các bản ghi không hợp lệ, chuẩn hóa dữ liệu, sau đó lưu kết quả ra file CSV.

Pipeline gồm 4 bước chính:

- **Extract**: Đọc dữ liệu từ file `raw_data.json`
- **Validate**: Loại bỏ các bản ghi không hợp lệ
- **Transform**: Chuẩn hóa category, tính giá giảm 10%, thêm thời gian xử lý
- **Load**: Lưu dữ liệu đã xử lý ra file `processed_data.csv`

Ngoài phần ETL, bài lab còn minh họa ảnh hưởng của chất lượng dữ liệu đến khả năng trả lời của AI agent thông qua việc so sánh giữa **clean data** và **garbage data**.

---

## Cách chạy

### Cài đặt thư viện
```bash
pip install pandas
```

### Chạy ETL Pipeline
```bash
python solution.py
```

### Chạy kiểm thử với dữ liệu sạch và dữ liệu rác
Sử dụng:
- `processed_data.csv` để đại diện cho dữ liệu sạch sau ETL
- `garbage_data.csv` để đại diện cho dữ liệu rác chưa qua xử lý

Mục đích là so sánh xem agent sẽ đưa ra kết quả khác nhau như thế nào khi đầu vào thay đổi về chất lượng.

---

## Cấu trúc thư mục

```bash
├── solution.py              # Script ETL chính
├── raw_data.json            # Dữ liệu đầu vào
├── processed_data.csv       # Dữ liệu sau khi ETL
├── garbage_data.csv         # Dữ liệu rác dùng để so sánh
├── experiment_report.md     # Báo cáo thí nghiệm
└── README.md                # File mô tả bài lab
```

---

## Kết quả sau khi chạy pipeline

Sau khi chạy ETL, dữ liệu được lọc và chỉ giữ lại các bản ghi hợp lệ. Trong kết quả thực tế:

- `processed_data.csv` còn **3 bản ghi hợp lệ**
- Các bản ghi còn lại là:
  - **Laptop** — giá 1200 — Electronics
  - **Chair** — giá 45 — Furniture
  - **Monitor** — giá 300 — Electronics

Ngoài ra, pipeline còn tạo thêm các cột:
- `discounted_price`
- `processed_at`

Những bản ghi có:
- `price <= 0`
- `category` rỗng hoặc thiếu

đều bị loại bỏ ở bước validation.

---

## So sánh clean data và garbage data

Trong `garbage_data.csv`, dữ liệu chứa nhiều vấn đề như:
- ID bị trùng
- Giá sai kiểu dữ liệu
- Dữ liệu thiếu
- Giá trị ngoại lai rất lớn như **Nuclear Reactor = 999999**

Nếu agent chỉ dùng dữ liệu rác để chọn sản phẩm điện tử có giá cao nhất, nó có thể đưa ra kết quả sai lệch. Ngược lại, với `processed_data.csv`, dữ liệu đã được làm sạch nên agent dễ đưa ra kết quả hợp lý hơn, cụ thể là chọn **Laptop** thay vì các giá trị bất thường.

---

## Ý nghĩa của bài lab

Bài lab cho thấy chất lượng dữ liệu đầu vào có ảnh hưởng trực tiếp đến độ tin cậy của hệ thống AI. Một agent có thể có logic đơn giản nhưng vẫn cho kết quả tốt nếu dữ liệu sạch. Ngược lại, khi dữ liệu có lỗi, thiếu hoặc chứa outlier, kết quả đưa ra sẽ rất dễ sai.

Vì vậy, bước **Validate** và **Transform** trong pipeline ETL là rất quan trọng. Đây không chỉ là bước tiền xử lý dữ liệu, mà còn là nền tảng giúp hệ thống AI hoạt động ổn định và đáng tin cậy hơn.
