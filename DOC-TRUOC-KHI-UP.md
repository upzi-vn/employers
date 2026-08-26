# Đưa lên repo `upzi-vn/employers`

**Xoá file này trước khi upload** — nó chỉ là hướng dẫn.

Chỉ có **11 file**, không có ảnh, không có CSS mới.
Copy đè lên gốc repo, giữ nguyên đường dẫn. Không phải xoá file nào của repo.

---

## Giao diện giữ nguyên 100%

Không đụng tới bảng màu, font, hay bố cục. Trang `/writings` và các bài viết
nhìn **y hệt hiện tại**. Chỉ sửa những chỗ thật sự hỏng.

Hai file template bị sửa, và chỉ sửa đúng những dòng này:

- `writings.html` — thêm **một** điều kiện `{% if post.headline_stat %}`
  để thẻ Success Story không để lại ô trống khi đã gỡ số
- `_layouts/frame2.html` — thêm thẻ meta vào `<head>`, đổi 2 nút CTA,
  và thêm **một** rule CSS mới `.btn-ghost` cho nút phụ

---

## Các bước

1. Vào https://github.com/upzi-vn/employers
2. Bấm nút xám ghi **`main`** → gõ `fix-writings-content` →
   **Create branch: fix-writings-content from 'main'**
3. Kiểm tra nút đó giờ ghi `fix-writings-content`
4. **Add file → Upload files**
5. Giải nén zip, xoá file hướng dẫn này, rồi vào **bên trong** thư mục,
   `Ctrl+A`, kéo **nguyên khối** vào khung upload

   > Phải thấy cả biểu tượng thư mục `_posts`, `_layouts`, `_includes`
   > trong danh sách. Nếu chỉ thấy toàn file lẻ thì bạn đang đứng sai chỗ.

6. Gõ commit message → **Commit changes**
7. **Compare & pull request** → **Create pull request**
8. Chờ Vercel bình luận link xem thử → mở link, thêm `/writings`
9. Ưng thì **Merge pull request**

---

# Sửa những gì

## Ba lỗi đang nằm trên live

**1. Bài Success Story bán lẻ đang hiện văn bản mẫu cho công chúng.**
Tại `/insights/mo-rong-nguon-ung-vien-chuoi-ban-le/` người đọc đang thấy
*"Tiêu đề phần bài toán"*, *"Nội dung phần bài toán."*, *"Mô tả con số này."*.
Front matter có ghi chú nói bài này lẽ ra `published: false`, nhưng dòng đó
không hề tồn tại nên Jekyll vẫn đăng. **Đã viết nội dung thật.**

**2. Hai nút "Quay lại trang Insights" đang 404.**
Cả hai trỏ tới `/tips-insights.html` — trang này không còn trong repo.
Đã gỡ. Cũng khớp với yêu cầu: bài viết không dẫn ngược về trang writings.

**3. `README.md` và ghi chú trong `head-tracking.html` vẫn gọi tên
`tips-insights`.** Đã đổi thành `writings`.

## Nội dung

**Gỡ hết số khỏi 2 bài Success Story.** Cụ thể:

- Front matter: bỏ `headline_stat`, `headline_label`, `stats`
- Thân bài: bỏ khối `stat-box` và toàn bộ `results-section` chứa con số
- Thay bằng các khối định tính, **dùng lại đúng class `.solution-grid` có sẵn**
  nên nhìn vẫn thống nhất với phần còn lại của bài

Kết quả: thẻ trên `/writings` không còn ô *790 lượt xem · 19 hồ sơ*
và *1.290 · 34 · 150+*.

**Thêm bài còn thiếu:** Tại sao doanh nghiệp nên tuyển Intern.
Viết bằng đúng bộ class của layout hiện tại.

## CTA

Nav và cuối bài đổi từ `/#leadform` sang `/free-trial`, thêm nút phụ dẫn về
trang chủ. Tuỳ biến được theo từng bài qua `cta_heading` / `cta_lead`
trong front matter.

## SEO

Thêm `description`, `canonical`, thẻ OG và Twitter cho mọi bài.
Trước đó không có gì — dán link lên Facebook, LinkedIn hay Zalo ra một ô trắng.

`og:image` để trống có điều kiện. Khi chọn được ảnh thì thêm một dòng
`og_image: "/images/..."` vào front matter là xong, không phải sửa template.

---

# Cần bạn quyết

### Bài "Báo cáo xu hướng hành vi ứng viên 2026" đang tạm ẩn

Lý do: thân bài mới chỉ có một dòng *"Nội dung chi tiết của báo cáo..."*,
và hai con số **78%** / **3.5x** không ghi nguồn.

Cho hiện lại: xoá dòng `published: false` trong `_posts/2026-08-08-bao-cao-genz.md`.

---

# Ba việc phát hiện thêm, KHÔNG nằm trong gói này

**1. Số liệu trong 2 bài Insight chưa đối chiếu nguồn.**
Bài Gen Z có `60% / 50% / 62% / 46%` và `9% / 7%` ghi nguồn VnExpress.
Bài Xu hướng 2026 có `23,73% / 4,16% / 2,79% / 52,33% / 24,71% / 60,4%`
ghi nguồn khảo sát Navigos. Nên kiểm trước khi đẩy mạnh phát tán.

**2. Có một file ảnh hỏng trong repo.**
`images/event-fpt-officetour.jpg` chỉ nặng **2 byte** — file rỗng.
May là không trang nào dùng nó (các trang dùng bản `.png`), nên vô hại,
nhưng nên xoá cho sạch.

**3. Trang chủ đang tải ảnh rất nặng.**
`images/event-career-pathfinder.jpg` nặng **11,8 MB** (6000×4000) và
`images/event-htkd.jpg` nặng **12 MB** (6048×4024). Cả hai đang được
`index.html` dùng. Trên 3G thì gần như không tải nổi. Nên resize xuống
1600px, mỗi file sẽ còn khoảng 200 KB.
