# Mẫu tin nhắn / văn bản xin phép sử dụng CV

> Dùng cho thành viên C khi liên hệ bạn bè xin CV phục vụ dự án thi.
> Bằng chứng đồng ý (screenshot tin nhắn / email reply) lưu tại `data/consent/` — **không** commit
> lên GitHub public.

---

## Mẫu 1 — Tin nhắn ngắn (Messenger / Zalo)

```
Chào [tên bạn],

Mình đang tham gia Cuộc thi Sáng tạo trẻ Quốc gia về AI 2026 (Bảng C — ứng dụng
AI). Đội mình làm sản phẩm "trợ lý nghề nghiệp" giúp sinh viên đối chiếu CV với
tin tuyển dụng và nhận gợi ý cải thiện CV.

Mình muốn xin phép được sử dụng CV của bạn làm dữ liệu mẫu (sample data) cho
sản phẩm. Mình cam kết:

✅ ẨN DANH HOÀN TOÀN trước khi sử dụng — xoá tên, SĐT, email, địa chỉ, ảnh và
   mọi thông tin định danh cá nhân.
✅ Chỉ dùng cho mục đích nghiên cứu/thi — không chia sẻ, không thương mại.
✅ File CV gốc không được lưu trong repo công khai — chỉ lưu bản đã ẩn danh.
✅ Bạn có quyền từ chối hoặc yêu cầu xoá bất cứ lúc nào.

Nếu bạn đồng ý, bạn chỉ cần:
1. Gửi file CV cho mình (PDF hoặc DOCX).
2. Reply xác nhận "Đồng ý cho sử dụng CV đã ẩn danh cho mục đích thi."

Cảm ơn bạn rất nhiều! 🙏
```

---

## Mẫu 2 — Email (chính thức hơn, dùng khi cần)

```
Tiêu đề: Xin phép sử dụng CV (ẩn danh) — Dự thi AI Sáng tạo trẻ 2026

Chào [tên bạn],

Mình là [tên], sinh viên [trường/khoa], hiện đang tham gia Cuộc thi Sáng tạo trẻ
Quốc gia về AI 2026 (Bảng C) với đề tài "Trợ lý nghề nghiệp cá nhân hóa cho
người trẻ Việt Nam". Sản phẩm sử dụng AI để chấm điểm độ phù hợp giữa CV và tin
tuyển dụng, từ đó gợi ý cải thiện CV cho sinh viên.

Để huấn luyện và đánh giá hệ thống, đội mình cần một tập CV mẫu. Mình viết email
này để xin phép được sử dụng CV của bạn, với các cam kết sau:

1. ẨN DANH HOÀN TOÀN: Trước khi đưa vào hệ thống, mình sẽ xoá toàn bộ thông tin
   cá nhân (họ tên, SĐT, email, địa chỉ, ảnh, link mạng xã hội). Tên được thay
   bằng mã ẩn danh (ví dụ: "Ứng viên A").
2. MỤC ĐÍCH DUY NHẤT: Chỉ phục vụ nghiên cứu và thi — không dùng cho mục đích
   thương mại hay chia sẻ công khai.
3. FILE GỐC KHÔNG CÔNG KHAI: CV gốc chỉ lưu cục bộ để xử lý ẩn danh, không được
   commit vào repo hay chia sẻ ra ngoài nhóm.
4. QUYỀN RÚT LẠI: Bạn có thể yêu cầu xoá CV khỏi tập dữ liệu bất cứ lúc nào.

Nếu bạn đồng ý, xin bạn:
- Gửi file CV (PDF hoặc DOCX) reply email này.
- Ghi rõ: "Tôi đồng ý cho sử dụng CV đã ẩn danh cho mục đích nghiên cứu và thi."

Nếu bạn không muốn, mình hoàn toàn tôn trọng, không ảnh hưởng gì cả.

Cảm ơn bạn rất nhiều!

[Tên]
[SĐT / email liên hệ]
```

---

## Hướng dẫn lưu bằng chứng đồng ý

1. Screenshot / forward email reply có nội dung đồng ý.
2. Đặt tên file: `consent_<mã_ứng_viên>.png` hoặc `.pdf` (ví dụ: `consent_A.png`).
3. Lưu vào `data/consent/` — thư mục này **KHÔNG** được commit lên GitHub public.
4. Trong `data/DATA_SOURCES.md`, cập nhật bảng D2 (số lượng, nguồn).

## Checklist ẩn danh trước khi lưu CV vào repo

- [ ] Xoá họ tên → thay bằng "Ứng viên X"
- [ ] Xoá số điện thoại
- [ ] Xoá email cá nhân → thay bằng `candidate_X@example.com`
- [ ] Xoá địa chỉ cụ thể (số nhà, đường, phường)
- [ ] Xoá ảnh đại diện
- [ ] Xoá link mạng xã hội cá nhân (Facebook, LinkedIn cá nhân)
- [ ] Đổi tên file: `cv_sample_<mã>.pdf`
- [ ] Kiểm tra lại toàn bộ nội dung — không còn thông tin định danh
