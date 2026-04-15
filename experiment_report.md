# Experiment Report: Ảnh hưởng của chất lượng dữ liệu đến AI Agent


**Student ID:** AI20K-2A202600171
**Name:** Nguyen Khanh Huyen
**Date:** 15/04/2026

---

## 1. Kết quả thí nghiệm

Chạy pipeline ETL để tạo file `processed_data.csv`, sau đó so sánh khi agent làm việc với hai bộ dữ liệu: dữ liệu sạch sau ETL và dữ liệu rác ban đầu.

| Kịch bản | Kết quả quan sát được | Độ chính xác (1-10) | Ghi chú |
|----------|------------------------|---------------------|--------|
| Clean Data (`processed_data.csv`) | Bộ dữ liệu còn 3 bản ghi hợp lệ: Laptop (1200), Chair (45), Monitor (300). Nếu agent chọn sản phẩm điện tử có giá cao nhất thì kết quả là **Laptop**. | 10 | Kết quả hợp lý vì dữ liệu đã được làm sạch, chỉ giữ lại các bản ghi đúng định dạng và có ý nghĩa. |
| Garbage Data (`garbage_data.csv`) | Bộ dữ liệu có 5 bản ghi, trong đó xuất hiện **Nuclear Reactor** giá 999999, giá trị bất thường và không thực tế. Nếu agent chọn sản phẩm điện tử giá cao nhất thì rất dễ chọn **Nuclear Reactor** thay vì Laptop. | 2 | Kết quả sai lệch mạnh do dữ liệu rác chứa outlier, dữ liệu thiếu và sai kiểu. |

---

## 2. Phân tích và nhận xét

### Tại sao agent trả lời sai khi dùng Garbage Data?

Khi đọc file `garbage_data.csv`, có thể thấy dữ liệu đầu vào chứa nhiều vấn đề nghiêm trọng về chất lượng.

Thứ nhất, có **ID bị trùng lặp**. Cụ thể, ID `1` xuất hiện cho cả `Laptop` và `Banana`. Điều này làm cho việc định danh sản phẩm không còn đáng tin cậy, đặc biệt nếu hệ thống cần tra cứu hoặc gom nhóm theo ID.

Thứ hai, có **sai kiểu dữ liệu** ở cột giá. Bản ghi `Broken Chair` có giá là `"ten dollars"` thay vì một giá trị số. Nếu hệ thống hoặc agent cần so sánh giá, bản ghi này có thể gây lỗi hoặc bị hiểu sai trong quá trình xử lý.

Thứ ba, bộ dữ liệu có **giá trị ngoại lai rất lớn**. Sản phẩm `Nuclear Reactor` có giá `999999` và thuộc category `electronics`. Nếu agent chỉ áp dụng logic đơn giản như “chọn sản phẩm điện tử có giá cao nhất”, thì nó gần như chắc chắn sẽ chọn bản ghi này. Về mặt kỹ thuật, điều đó có thể đúng theo dữ liệu đầu vào, nhưng về mặt thực tế thì đây là một kết quả vô lý.

Thứ tư, có **dữ liệu thiếu**. Bản ghi `Ghost Item` có `id` rỗng, `category` rỗng và giá bằng `0`. Đây là bản ghi không hợp lệ nhưng vẫn tồn tại trong dữ liệu rác. Nếu không có bước validation, những dòng như vậy sẽ đi thẳng vào hệ thống và làm giảm chất lượng đầu ra.

Ngược lại, sau khi chạy ETL, file `processed_data.csv` chỉ còn lại 3 bản ghi hợp lệ:
- Laptop — giá 1200 — Electronics  
- Chair — giá 45 — Furniture  
- Monitor — giá 300 — Electronics  

Ngoài ra, dữ liệu còn được bổ sung thêm:
- `discounted_price`
- `processed_at`

Trong bộ dữ liệu sạch này, nếu agent cần chọn sản phẩm điện tử có giá cao nhất thì đáp án đúng sẽ là **Laptop**, vì đây là bản ghi hợp lệ và có giá cao hơn `Monitor`. Điều này cho thấy khi dữ liệu đầu vào đã được kiểm tra và làm sạch, cùng một logic đơn giản của agent vẫn có thể cho ra kết quả đúng và đáng tin cậy hơn rất nhiều.

---

## 3. Kết luận

Qua thí nghiệm này, em đồng ý với nhận định rằng **chất lượng dữ liệu quan trọng hơn rất nhiều so với việc chỉ tối ưu prompt hoặc logic trả lời của agent**.

Trong bộ dữ liệu sạch, agent có thể đưa ra kết quả đúng vì dữ liệu đầu vào đã được kiểm soát. Trong khi đó, ở bộ dữ liệu rác, chỉ cần xuất hiện một vài bản ghi bất thường như giá trị ngoại lai, dữ liệu thiếu hoặc sai kiểu, agent đã có thể bị dẫn đến một kết quả sai lệch hoàn toàn.

Bài lab này cho thấy bước **Validate** và **Transform** trong ETL không chỉ là bước phụ trợ, mà là thành phần cốt lõi để đảm bảo hệ thống AI hoạt động ổn định. Nếu dữ liệu đầu vào không được làm sạch, thì dù prompt có viết tốt hay agent có được thiết kế hợp lý, kết quả cuối cùng vẫn rất dễ sai. Vì vậy, đầu tư vào dữ liệu sạch là điều kiện nền tảng để xây dựng một hệ thống AI đáng tin cậy.