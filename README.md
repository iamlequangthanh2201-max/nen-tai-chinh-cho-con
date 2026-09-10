# Nền tài chính cho con

Nghiên cứu và thiết kế nội dung cho một cuốn sổ tay của người cha: xây nền tảng
tư duy và thói quen tài chính cho con trai, từ trong thai kỳ đến năm con 18 tuổi.

**Dự án riêng**, tách khỏi dự án nuôi dạy EQ (`../so-tay-nguoi-cha.html`), dù dùng
chung design system. Bản dựng thử: https://claude.ai/code/artifact/06f23c50-7c3d-4594-a13e-cf59440b9e0c

Con trai đầu lòng, dự sinh khoảng cuối 2026. Mọi mốc tuổi trong tài liệu quy ra
năm thật theo mốc đó.


## Trang web

Site tĩnh, không cần build tool, không phụ thuộc framework.

| File | Vai trò |
|---|---|
| `index.html` | Trang đã dựng — **sinh tự động, đừng sửa tay** |
| `styles.css` | Toàn bộ giao diện |
| `app.js` | Điều hướng, tìm kiếm, ba công cụ |
| `build.py` | Sinh `index.html` từ các file `.md` |
| `*.md` | Nội dung — **sửa ở đây** |

**Sửa nội dung rồi dựng lại**

```
python3 build.py
```

**Xem thử tại máy**

```
python3 -m http.server 4173
```

Rồi mở `http://localhost:4173`.

**Đưa lên GitHub Pages**

1. Tạo repo mới, đẩy toàn bộ thư mục này lên nhánh `main`.
2. Vào *Settings → Pages*, chọn *Deploy from a branch*, nhánh `main`, thư mục `/ (root)`.
3. Trang chạy ở `https://<tên-tài-khoản>.github.io/<tên-repo>/`.

Không cần `.nojekyll` vì trang không dùng thư mục bắt đầu bằng dấu gạch dưới.
Phông chữ lấy từ Google Fonts; mọi thứ còn lại nằm trong repo.

**Dữ liệu người dùng** — sổ mốc, sổ lì xì, giả định máy tính quỹ lưu trong
`localStorage` của trình duyệt, khoá `ntc-v1`. Không có máy chủ, không gửi đi đâu.

## Phạm vi

Trang này quản lý **tiền của con**. Tài chính gia đình (ngân sách, quỹ dự phòng,
ba con số của nhà) do công cụ khác của bố quản — không đưa vào đây để tránh
quản hai nơi rồi số liệu đá nhau.

## Khung: một nguyên tắc bao trùm, ba trụ

**BẢN GỐC** — Con sao chép cách bố sống với tiền, không sao chép lời bố giảng.
Ba trụ dưới đây đều đi qua đường truyền này.

| Trụ | Nghĩa | Đòi gì ở bố |
|---|---|---|
| **CON KỂ** | Con còn kể với bố, kể cả khi làm hỏng chuyện | Kiểm soát phản ứng của mình — không xoá hậu quả của con |
| **CON KHÔNG SO** | Con không đo giá trị mình và người khác bằng tiền | Ngôn ngữ trong nhà, không bù đắp bằng quà, không so sánh |
| **CON TỰ LO** | Con tự làm, tự sai, tự chịu — vì bố không theo con mãi | Giao quyền thật và chịu được việc nhìn con sai |

## Ba luật đã chốt

- **Luật khoảnh khắc** — con vừa làm hỏng chuyện, bố có ba giây để phản ứng:
  bảo vệ **Con kể** trước. Đúng cả khi có nợ, cờ bạc, tiêu tiền người khác.
- **Đích mười tám năm** — **Con không so** đứng trên **Con tự lo**. Thà con quản lý
  lỏng còn hơn con giỏi quản lý vì sợ thua bạn.
- **Trọng số theo tuổi** — **Con tự lo** được nâng lên ngang **Con kể** trong khoảng
  6–14 tuổi. Đó là cửa sổ duy nhất để nó mọc được.

## Phân biệt phải giữ cho sạch

Giữ **Con kể** = bố kiểm soát **phản ứng của chính mình** (giọng, câu đầu tiên,
có mắng hay không, có nhắc lại về sau hay không).
Nó **không** có nghĩa là xoá **hậu quả tự nhiên** — tiền mất là mất, đồ hỏng là hỏng,
hết tiền giữa kỳ là phải chờ. Hậu quả tự nhiên dạy **Con tự lo**, và không đe doạ
**Con kể** chút nào.

Hai cái chỉ đá nhau khi bố định *tạo thêm* một hậu quả nhân tạo — phạt, trừ tiền
tiêu vặt, siết quyền. Đúng lúc đó luật khoảnh khắc có hiệu lực: không tạo thêm.

## Bốn loại phản ứng

| Loại | Là gì | Dùng khi nào |
|---|---|---|
| Hậu quả tự nhiên | Tự nó xảy ra | Mặc định. Bố chỉ cần không xoá nó đi |
| Sửa chữa | Trả lại, xin lỗi, khắc phục — bố đi cùng, không làm thay | Khi có người khác bị thiệt |
| Ranh giới | Câu tuyên bố: việc này không được phép | Với việc nghiêm trọng |
| Hình phạt | Bố tạo ra đau để răn | **Loại khỏi hệ thống** — đây là thứ đóng cửa |

## Cấu trúc sáu chương

| File | Chương |
|---|---|
| `01-nen-mong.md` | Bản gốc · ba trụ · ranh giới cứng |
| `02-truoc-khi-sinh.md` | Sáu việc trước khi con ra đời |
| `03-lo-trinh.md` | Lộ trình 0–18 · tiền tiêu vặt · bảng bốn ô ưu tiên |
| `04-kich-ban.md` | 31 kịch bản, bốn nhóm tuổi và nhóm người lớn |
| `05-nghi-thuc-cong-cu.md` | Bốn nghi thức · ba công cụ |
| `06-tong-ket.md` | Nên làm · nên tránh · dấu hiệu |
| `07-tu-vung.md` | Bảng tra từ vựng kèm câu mẫu |

Mục lục trái, chuyển chương, ô tìm kiếm ở chương 04 và phụ lục từ vựng đều sinh tự động từ nội dung.

## Quy ước viết

- Giọng dứt khoát, mệnh lệnh, không rào đón. Không gán cho nghiên cứu điều nó
  không nói; phần "Cơ sở" để ngắn và đúng.
- Viết cho **cả hai vợ chồng cùng đọc**.
- Kịch bản theo sáu ô: *ba giây đầu · câu đầu tiên · đừng nói · nhánh theo phản ứng
  của con · sau đó · một dòng nghĩa*. Thêm ô *trước đó* khi phòng ngừa mới là chỗ
  quyết định.
- Mọi dòng viết ở dạng "nếu… thì…" khi có thể.
- Câu chờ vạn năng khi không nhớ nổi gì: **"Bố cần một phút, rồi mình nói tiếp."**
