import json
import csv
import sys
from abc import ABC, abstractmethod

# Hỗ trợ tiếng Việt trên Windows
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# BASE CLASS & SUBCLASSES
class CanBo(ABC):
    """Lớp cơ sở cho cán bộ"""

    def __init__(self, hoTen: str, tuoi: int, gioiTinh: str, diaChi: str):
        self.hoTen = hoTen
        self.tuoi = tuoi
        self.gioiTinh = gioiTinh
        self.diaChi = diaChi

    def __str__(self):
        return f"{self.hoTen} | {self.tuoi} tuổi | {self.gioiTinh} | {self.diaChi}"

    @abstractmethod
    def get_thong_tin_chuyen_mon(self) -> str:
        """Trả về thông tin chuyên môn (bậc/năm kinh nghiệm/công việc)"""
        pass

    @abstractmethod
    def get_bac_luong(self) -> float:
        """Trả về bậc lương để so sánh"""
        pass

    def to_dict(self) -> dict:
        """Chuyển đối tượng sang dictionary"""
        return {
            "hoTen": self.hoTen,
            "tuoi": self.tuoi,
            "gioiTinh": self.gioiTinh,
            "diaChi": self.diaChi,
            "loai": self.__class__.__name__,
            "thongTin": self.get_thong_tin_chuyen_mon()
        }

    @staticmethod
    def from_dict(data: dict) -> "CanBo":
        """Khởi phục đối tượng từ dictionary dựa vào trường 'loai'"""
        loai = data.get("loai", "")
        thongTin = data.get("thongTin", "")

        if loai == "KySu":
            return KySu(
                data["hoTen"], data["tuoi"],
                data["gioiTinh"], data["diaChi"],
                thongTin
            )
        elif loai == "CongNhan":
            return CongNhan(
                data["hoTen"], data["tuoi"],
                data["gioiTinh"], data["diaChi"],
                thongTin
            )
        elif loai == "NhanVien":
            return NhanVien(
                data["hoTen"], data["tuoi"],
                data["gioiTinh"], data["diaChi"],
                thongTin
            )
        else:
            raise ValueError(f"Loại cán bộ không hợp lệ: {loai}")


class KySu(CanBo):
    """Kỹ sư - có thêm ngành"""

    def __init__(self, hoTen: str, tuoi: int, gioiTinh: str, diaChi: str, nganh: str):
        super().__init__(hoTen, tuoi, gioiTinh, diaChi)
        self.nganh = nganh

    def get_thong_tin_chuyen_mon(self) -> str:
        return self.nganh

    def get_bac_luong(self) -> float:
        # Kỹ sư: năm kinh nghiệm * 0.5 + 5
        try:
            nam = float(self.nganh)
            return nam * 0.5 + 5
        except ValueError:
            return 5.0

    def __str__(self):
        return f"[KySu] {super().__str__()} | Ngành: {self.nganh}"


class CongNhan(CanBo):
    """Công nhân - có thêm bậc (1-10)"""

    def __init__(self, hoTen: str, tuoi: int, gioiTinh: str, diaChi: str, bac: str):
        super().__init__(hoTen, tuoi, gioiTinh, diaChi)
        self.bac = bac

    def get_thong_tin_chuyen_mon(self) -> str:
        return self.bac

    def get_bac_luong(self) -> float:
        try:
            return float(self.bac)
        except ValueError:
            return 1.0

    def __str__(self):
        return f"[CongNhan] {super().__str__()} | Bậc: {self.bac}"


class NhanVien(CanBo):
    """Nhân viên - có thêm công việc"""

    def __init__(self, hoTen: str, tuoi: int, gioiTinh: str, diaChi: str, congViec: str):
        super().__init__(hoTen, tuoi, gioiTinh, diaChi)
        self.congViec = congViec

    def get_thong_tin_chuyen_mon(self) -> str:
        return self.congViec

    def get_bac_luong(self) -> float:
        # Nhân viên: cố định 3.0
        return 3.0

    def __str__(self):
        return f"[NhanVien] {super().__str__()} | Công việc: {self.congViec}"

# quan ly can bo
class QuanLyCanBo:
    """Lớp quản lý danh sách cán bộ với CRUD và CLI"""

    def __init__(self):
        self.ds: list[CanBo] = []
        self.file_json = "canbo.json"
        self.file_csv = "canbo.csv"

    # CRUD Operations
    def them(self, canbo: CanBo) -> bool:
        """Thêm cán bộ vào danh sách"""
        try:
            self.ds.append(canbo)
            self.luu_json()
            print(f"✓ Đã thêm: {canbo.hoTen}")
            return True
        except Exception as e:
            print(f"Lỗi khi thêm: {e}")
            return False

    def xoa(self, hoTen: str) -> bool:
        """Xóa cán bộ theo họ tên"""
        for i, cb in enumerate(self.ds):
            if cb.hoTen.lower() == hoTen.lower():
                da_xoa = self.ds.pop(i)
                self.luu_json()
                print(f"✓ Đã xóa: {da_xoa.hoTen}")
                return True
        print(f"Không tìm thấy: {hoTen}")
        return False

    def tim_theo_ten(self, hoTen: str) -> list[CanBo]:
        """Tìm cán bộ theo họ tên (không phân biệt hoa thường)"""
        ket_qua = [cb for cb in self.ds if hoTen.lower() in cb.hoTen.lower()]
        return ket_qua

    def tim_theo_loai(self, loai: str) -> list[CanBo]:
        """Tìm cán bộ theo loại (KySu/CongNhan/NhanVien)"""
        ket_qua = [cb for cb in self.ds if type(cb).__name__ == loai]
        return ket_qua

    def top3_luong_cao(self) -> list[CanBo]:
        """Trả về 3 cán bộ có bậc lương cao nhất"""
        sorted_ds = sorted(self.ds, key=lambda cb: cb.get_bac_luong(), reverse=True)
        return sorted_ds[:3]

    def hien_thi_danh_sach(self):
        """Hiển thị toàn bộ danh sách"""
        if not self.ds:
            print("Danh sách trống.")
            return
        print(f"\n{'='*70}")
        print(f"Tổng số: {len(self.ds)} cán bộ")
        print(f"{'='*70}")
        for i, cb in enumerate(self.ds, 1):
            print(f"{i}. {cb}")

    # JSON Operations
    def luu_json(self, ten_file: str = None) -> bool:
        """Lưu danh sách ra file JSON"""
        try:
            file = ten_file or self.file_json
            with open(file, 'w', encoding='utf-8') as f:
                json.dump([cb.to_dict() for cb in self.ds], f,
                         ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"Lỗi lưu JSON: {e}")
            return False

    def tai_json(self, ten_file: str = None) -> bool:
        """Tải danh sách từ file JSON"""
        try:
            file = ten_file or self.file_json
            with open(file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.ds = [CanBo.from_dict(d) for d in data]
            print(f"✓ Đã tải {len(self.ds)} cán bộ từ {file}")
            return True
        except FileNotFoundError:
            print(f"File {file} chưa tồn tại, bắt đầu danh sách mới.")
            self.ds = []
            return True
        except json.JSONDecodeError as e:
            print(f"Lỗi định dạng JSON: {e}")
            return False
        except Exception as e:
            print(f"Lỗi khi tải: {e}")
            return False

    # --- CSV Operations ---
    def doc_csv(self, ten_file: str = None) -> bool:
        """Đọc dữ liệu từ file CSV"""
        try:
            file = ten_file or self.file_csv
            with open(file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    try:
                        # Validate dữ liệu
                        hoTen = row['hoTen'].strip()
                        tuoi = int(row['tuoi'].strip())
                        gioiTinh = row['gioiTinh'].strip()
                        diaChi = row['diaChi'].strip()
                        loai = row['loai'].strip()
                        thongTin = row['thongTin'].strip()

                        # Tạo đối tượng từ CSV
                        canbo = CanBo.from_dict({
                            "hoTen": hoTen,
                            "tuoi": tuoi,
                            "gioiTinh": gioiTinh,
                            "diaChi": diaChi,
                            "loai": loai,
                            "thongTin": thongTin
                        })
                        self.ds.append(canbo)

                    except ValueError as e:
                        print(f"Lỗi ValueError ở dòng: {row} - {e}")
                    except KeyError as e:
                        print(f"Thiếu trường {e} ở dòng: {row}")

            print(f"✓ Đã đọc {len(self.ds)} cán bộ từ {file}")
            return True

        except FileNotFoundError:
            print(f"File {file} không tồn tại.")
            return False
        except Exception as e:
            print(f"Lỗi đọc CSV: {e}")
            return False

    # --- CLI Menu ---

    def menu(self):
        """Chạy chương trình CLI"""
        print("\n" + "="*60)
        print("   HỆ THỐNG QUẢN LÝ CÁN BỘ")
        print("="*60)

        # Thử tải JSON trước
        if not self.tai_json():
            # Nếu không có JSON, thử đọc CSV
            print("Đang thử đọc từ CSV...")
            self.doc_csv()

        while True:
            self._hien_thi_menu()
            try:
                chon = input("\nChọn: ").strip()
                if not self._xu_ly_menu(chon):
                    break
            except KeyboardInterrupt:
                print("\n\nĐã thoát. Tự động lưu...")
                self.luu_json()
                break
            except EOFError:
                break

    def _hien_thi_menu(self):
        print("""
┌─────────────────────────────────────────┐
│           MENU QUẢN LÝ CÁN BỘ           │
├─────────────────────────────────────────┤
│  1. Xem danh sách                       │
│  2. Thêm cán bộ                         │
│  3. Xóa cán bộ                          │
│  4. Tìm theo họ tên                     │
│  5. Tìm theo loại (KySu/CN/NV)          │
│  6. Top 3 lương cao nhất                │
│  7. Lưu (JSON)                          │
│  8. Tải từ CSV                          │
│  0. Thoát                               │
└─────────────────────────────────────────┘""")

    def _xu_ly_menu(self, chon: str) -> bool:
        """Xử lý lựa chọn menu, trả về False nếu thoát"""
        if chon == "1":
            self.hien_thi_danh_sach()

        elif chon == "2":
            self._nhap_them_canbo()

        elif chon == "3":
            hoTen = input("Nhập họ tên cần xóa: ").strip()
            self.xoa(hoTen)

        elif chon == "4":
            hoTen = input("Nhập họ tên cần tìm: ").strip()
            ket_qua = self.tim_theo_ten(hoTen)
            self._hien_ket_qua(ket_qua, f"Tìm '{hoTen}'")

        elif chon == "5":
            print("Loại: KySu | CongNhan | NhanVien")
            loai = input("Nhập loại: ").strip()
            ket_qua = self.tim_theo_loai(loai)
            self._hien_ket_qua(ket_qua, f"Tìm loại '{loai}'")

        elif chon == "6":
            top3 = self.top3_luong_cao()
            self._hien_ket_qua(top3, "Top 3 lương cao nhất")

        elif chon == "7":
            if self.luu_json():
                print("✓ Lưu thành công!")

        elif chon == "8":
            self.doc_csv()

        elif chon == "0":
            self.luu_json()
            print("Đã lưu và thoát!")
            return False

        else:
            print("Lựa chọn không hợp lệ!")

        return True

    def _nhap_them_canbo(self):
        """Hướng dẫn nhập thông tin và thêm cán bộ"""
        print("\n--- Thêm Cán Bộ ---")
        print("Loại: 1=KySu | 2=CongNhan | 3=NhanVien")

        try:
            loai = input("Chọn loại: ").strip()

            hoTen = input("Họ tên: ").strip()
            tuoi = int(input("Tuổi: ").strip())
            gioiTinh = input("Giới tính: ").strip()
            diaChi = input("Địa chỉ: ").strip()

            if loai == "1":
                nganh = input("Ngành: ").strip()
                canbo = KySu(hoTen, tuoi, gioiTinh, diaChi, nganh)
            elif loai == "2":
                bac = input("Bậc (1-10): ").strip()
                canbo = CongNhan(hoTen, tuoi, gioiTinh, diaChi, bac)
            elif loai == "3":
                congViec = input("Công việc: ").strip()
                canbo = NhanVien(hoTen, tuoi, gioiTinh, diaChi, congViec)
            else:
                print("Loại không hợp lệ!")
                return

            self.them(canbo)

        except ValueError as e:
            print(f"Lỗi: Tuổi phải là số nguyên! ({e})")
        except Exception as e:
            print(f"Lỗi nhập liệu: {e}")

    def _hien_ket_qua(self, ket_qua: list, tieu_de: str):
        """Hiển thị kết quả tìm kiếm"""
        print(f"\n--- {tieu_de} ---")
        if not ket_qua:
            print("Không có kết quả.")
        else:
            print(f"Tìm thấy {len(ket_qua)} kết quả:")
            for cb in ket_qua:
                print(f"  • {cb}")


if __name__ == "__main__":
    qlcb = QuanLyCanBo()
    qlcb.menu()