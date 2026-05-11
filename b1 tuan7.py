import json
import csv
import sys
import os
from abc import ABC, abstractmethod

# Hỗ trợ tiếng Việt trên Windows
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# --- LAYER 1: MODELS (Đối tượng dữ liệu) ---

class CanBo(ABC):
    def __init__(self, ho_ten: str, tuoi: int, gioi_tinh: str, dia_chi: str):
        self.ho_ten = ho_ten
        self.tuoi = tuoi
        self.gioi_tinh = gioi_tinh
        self.dia_chi = dia_chi

    @abstractmethod
    def get_bac_luong(self) -> float:
        pass

    @abstractmethod
    def get_chi_tiet(self) -> dict:
        """Trả về thông tin đặc thù của từng loại cán bộ"""
        pass

    def to_dict(self) -> dict:
        data = {
            "loai": self.__class__.__name__,
            "ho_ten": self.ho_ten,
            "tuoi": self.tuoi,
            "gioi_tinh": self.gioi_tinh,
            "dia_chi": self.dia_chi
        }
        data.update(self.get_chi_tiet())
        return data

    def __str__(self):
        return f"{self.ho_ten:20} | {self.tuoi:2} tuổi | {self.gioi_tinh:5} | {self.dia_chi}"

class KySu(CanBo):
    def __init__(self, ho_ten, tuoi, gioi_tinh, dia_chi, nganh, nam_kn=0):
        super().__init__(ho_ten, tuoi, gioi_tinh, dia_chi)
        self.nganh = nganh
        self.nam_kn = float(nam_kn)

    def get_bac_luong(self) -> float:
        return self.nam_kn * 0.5 + 5.0

    def get_chi_tiet(self):
        return {"nganh": self.nganh, "nam_kn": self.nam_kn}

    def __str__(self):
        return f"[Kỹ sư] {super().__str__()} | Ngành: {self.nganh} ({self.nam_kn} năm KN)"

class CongNhan(CanBo):
    def __init__(self, ho_ten, tuoi, gioi_tinh, dia_chi, bac):
        super().__init__(ho_ten, tuoi, gioi_tinh, dia_chi)
        self.bac = int(bac)

    def get_bac_luong(self) -> float:
        return float(self.bac)

    def get_chi_tiet(self):
        return {"bac": self.bac}

    def __str__(self):
        return f"[C.Nhân] {super().__str__()} | Bậc: {self.bac}/7"

class NhanVien(CanBo):
    def __init__(self, ho_ten, tuoi, gioi_tinh, dia_chi, cong_viec):
        super().__init__(ho_ten, tuoi, gioi_tinh, dia_chi)
        self.cong_viec = cong_viec

    def get_bac_luong(self) -> float:
        return 3.0

    def get_chi_tiet(self):
        return {"cong_viec": self.cong_viec}

    def __str__(self):
        return f"[N.Viên] {super().__str__()} | Việc: {self.cong_viec}"

# --- LAYER 2: LOGIC QUẢN LÝ (Service Layer) ---

class QuanLyCanBo:
    # Mapping để khởi tạo đối tượng nhanh chóng từ Dict/JSON
    MAP_LOAI = {
        "KySu": KySu,
        "CongNhan": CongNhan,
        "NhanVien": NhanVien
    }

    def __init__(self):
        self.ds: list[CanBo] = []
        self.file_path = "database.json"

    def them_moi(self, can_bo: CanBo):
        self.ds.append(can_bo)
        print(f"✅ Đã thêm mới: {can_bo.ho_ten}")

    def xoa_theo_ten(self, ten: str):
        found = [cb for cb in self.ds if cb.ho_ten.lower() == ten.lower()]
        if not found:
            print(f"❌ Không tìm thấy cán bộ: {ten}")
            return
        for item in found:
            self.ds.remove(item)
        print(f"🗑️ Đã xóa {len(found)} cán bộ mang tên '{ten}'")

    def tim_kiem(self, tu_khoa: str):
        return [cb for cb in self.ds if tu_khoa.lower() in cb.ho_ten.lower()]

    def sap_xep_luong(self):
        return sorted(self.ds, key=lambda x: x.get_bac_luong(), reverse=True)

    # --- Persistence (Lưu trữ) ---
    def luu_du_lieu(self):
        try:
            with open(self.file_path, 'w', encoding='utf-8') as f:
                json.dump([cb.to_dict() for cb in self.ds], f, ensure_ascii=False, indent=4)
            print("💾 Đã lưu dữ liệu vào hệ thống.")
        except Exception as e:
            print(f"⚠️ Lỗi lưu file: {e}")

    def tai_du_lieu(self):
        if not os.path.exists(self.file_path): return
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.ds = []
                for item in data:
                    cls = self.MAP_LOAI.get(item.pop("loai"))
                    if cls: self.ds.append(cls(**item))
            print(f"📥 Đã tải {len(self.ds)} bản ghi.")
        except Exception as e:
            print(f"⚠️ Lỗi đọc file: {e}")

# --- LAYER 3: GIAO DIỆN (UI/CLI) ---

def main():
    ql = QuanLyCanBo()
    ql.tai_du_lieu()
    
    while True:
        print("\n" + "="*30)
        print(" QUẢN LÝ NHÂN SỰ v2.0 ")
        print("="*30)
        print("1. Xem danh sách\n2. Thêm mới\n3. Xóa\n4. Tìm kiếm\n5. Bảng lương Top-Down\n0. Thoát & Lưu")
        
        chon = input("\nNhập lựa chọn: ")
        
        if chon == "1":
            if not ql.ds: print("Danh sách đang trống.")
            for i, cb in enumerate(ql.ds, 1): print(f"{i}. {cb}")
            
        elif chon == "2":
            print("\nPhân loại: 1. Kỹ sư | 2. Công nhân | 3. Nhân viên")
            loai = input("Chọn: ")
            ten = input("Họ tên: ")
            tuoi = int(input("Tuổi: "))
            gt = input("Giới tính: ")
            dc = input("Địa chỉ: ")
            
            if loai == "1":
                nganh = input("Ngành đào tạo: ")
                kn = input("Số năm kinh nghiệm: ")
                ql.them_moi(KySu(ten, tuoi, gt, dc, nganh, kn))
            elif loai == "2":
                bac = input("Bậc lương (1-7): ")
                ql.them_moi(CongNhan(ten, tuoi, gt, dc, bac))
            elif loai == "3":
                viec = input("Công việc chính: ")
                ql.them_moi(NhanVien(ten, tuoi, gt, dc, viec))

        elif chon == "3":
            ten = input("Nhập tên chính xác cần xóa: ")
            ql.xoa_theo_ten(ten)

        elif chon == "4":
            ten = input("Nhập từ khóa tìm kiếm: ")
            kq = ql.tim_kiem(ten)
            print(f"Tìm thấy {len(kq)} kết quả:")
            for item in kq: print(f" -> {item}")

        elif chon == "5":
            print("\n--- DANH SÁCH THEO THỨ TỰ LƯƠNG GIẢM DẦN ---")
            for item in ql.sap_xep_luong():
                print(f"[{item.get_bac_luong():>4}] {item}")

        elif chon == "0":
            ql.luu_du_lieu()
            print("Tạm biệt!")
            break

if __name__ == "__main__":
    main()
