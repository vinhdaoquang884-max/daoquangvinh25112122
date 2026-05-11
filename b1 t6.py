class QLCB:
    def __init__(self):
        self.ds: List[CanBo] = []

    def them_cb(self, cb: CanBo):
        self.ds.append(cb)
        # Tự động sắp xếp danh sách theo tên mỗi khi thêm mới (Dùng __lt__ bạn đã viết)
        self.ds.sort() 
        print(f" Đã thêm và sắp xếp: {cb.get_hoten()}")

    def hien_cb(self):
        if not self.ds:
            print("Danh sách trống!")
            return
        print(f"\n--- DANH SÁCH CÁN BỘ ({len(self.ds)} người) ---")
        for i, cb in enumerate(self.ds, 1):
            print(f"{i}. {cb}")

if __name__ == "__main__":
    qlcb = QLCB()
    
    while True:
        menu()
        try:
            chon = int(input(" Nhập lựa chọn: "))
        except ValueError:
            print(" Vui lòng nhập số!")
            continue

        if chon == 1:
            try:
                ht = input("Họ tên: ")
                t = int(input("Tuổi (18-65): "))
                gt = input("Giới tính: ")
                dc = input("Địa chỉ: ")
                
                print("Loại: 1.Công nhân | 2.Kỹ sư | 3.Nhân viên")
                loai = int(input("Chọn loại: "))

                if loai == 1:
                    bac = int(input("Bậc (1-10): "))
                    qlcb.them_cb(CongNhan(ht, t, gt, dc, bac))
                elif loai == 2:
                    nganh = input("Ngành: ")
                    qlcb.them_cb(KySu(ht, t, gt, dc, nganh))
                elif loai == 3:
                    cv = input("Công việc: ")
                    qlcb.them_cb(NhanVien(ht, t, gt, dc, cv))
                else:
                    print(" Loại không hợp lệ!")
            except (TuoiKhongHopLe, BacKhongHopLe) as e:
                print(f" Lỗi dữ liệu: {e}")
            except ValueError:
                print("Lỗi: Tuổi và Bậc phải là số!")

        elif chon == 2:
            ten = input("Nhập tên cần tìm: ")
            qlcb.tim_cb(ten)

        elif chon == 3:
            qlcb.hien_cb()

        elif chon == 4:
            print("Tạm biệt!")
            break
