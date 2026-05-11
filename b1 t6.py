from abc import ABC, abstractmethod
from typing import List
import sys


class TuoiKhongHopLe(ValueError):
    def __init__(self, tuoi: int):
        super().__init__(f"Tuoi {tuoi} khong hop le")


class BacKhongHopLe(ValueError):
    def __init__(self, bac: int):
        super().__init__(f"Bac {bac} khong hop le")


class CanBo(ABC):
    def __init__(self, ht: str = "", t: int = 0, gt: str = "", dc: str = ""):
        if t < 18 or t > 65:
            raise TuoiKhongHopLe(t)
        self.hoten = ht
        self.tuoi = t
        self.gioitinh = gt
        self.diachi = dc

    def get_hoten(self) -> str:
        return self.hoten

    def get_gioitinh(self) -> str:
        return self.gioitinh

    def get_diachi(self) -> str:
        return self.diachi

    def get_tuoi(self) -> int:
        return self.tuoi

    def set_hoten(self, ht: str):
        self.hoten = ht

    def set_gioitinh(self, gt: str):
        self.gioitinh = gt

    def set_diachi(self, dc: str):
        self.diachi = dc

    def set_tuoi(self, t: int):
        if t < 18 or t > 65:
            raise TuoiKhongHopLe(t)
        self.tuoi = t

    @abstractmethod
    def mota(self) -> str:
        pass

    def __lt__(self, other: 'CanBo') -> bool:
        return self.hoten < other.hoten

    def ghi_file(self) -> str:
        return f"{self.hoten};{self.tuoi};{self.gioitinh};{self.diachi};{self.mota()}\n"

    def __str__(self) -> str:
        return f"Ho ten: {self.hoten} | Tuoi: {self.tuoi} | Gioi tinh: {self.gioitinh} | Dia chi: {self.diachi} | {self.mota()}"


class CongNhan(CanBo):
    def __init__(self, ht: str = "", t: int = 0, gt: str = "", dc: str = "", b: int = 0):
        super().__init__(ht, t, gt, dc)
        if b < 1 or b > 10:
            raise BacKhongHopLe(b)
        self.bac = b

    def get_bac(self) -> int:
        return self.bac

    def set_bac(self, b: int):
        if b < 1 or b > 10:
            raise BacKhongHopLe(b)
        self.bac = b

    def mota(self) -> str:
        return f"Cong nhan bac {self.bac}"


class KySu(CanBo):
    def __init__(self, ht: str = "", t: int = 0, gt: str = "", dc: str = "", ndt: str = ""):
        super().__init__(ht, t, gt, dc)
        self.nganh = ndt

    def mota(self) -> str:
        return f"Ky su nganh {self.nganh}"


class NhanVien(CanBo):
    def __init__(self, ht: str = "", t: int = 0, gt: str = "", dc: str = "", cv: str = ""):
        super().__init__(ht, t, gt, dc)
        self.congviec = cv

    def mota(self) -> str:
        return f"Nhan vien cong viec {self.congviec}"


class QLCB:
    def __init__(self):
        self.ds: List[CanBo] = []

    def them_cb(self, cb: CanBo):
        self.ds.append(cb)
        print("DEBUG: Đã thêm cán bộ ->", cb)

    def tim_cb(self, ten: str):
        for cb in self.ds:
            if cb.get_hoten() == ten:
                print("DEBUG: Tìm thấy cán bộ ->", cb)
                return
        print(f"Khong tim thay can bo: {ten}")

    def hien_cb(self):
        if not self.ds:
            print("Danh sach trong!")
            return
        print("DEBUG: Danh sách cán bộ hiện tại:")
        for cb in self.ds:
            print(cb)

    def thoat(self):
        self.ds.clear()
        print("DEBUG: Danh sách đã được xóa.")


def menu():
    print("\n===== MENU =====")
    print("1. Them can bo")
    print("2. Tim kiem can bo theo ten")
    print("3. Hien thi thong tin ve danh sach can bo")
    print("4. Thoat")


if __name__ == "__main__":
    try:
        n = int(input("Nhap so luong can bo: "))
    except ValueError:
        print("Nhap sai! Vui long nhap so nguyen.")
        sys.exit()

    qlcb = QLCB()

    while True:
        menu()
        try:
            chon = int(input("Nhap lua chon: "))
            print("DEBUG: Lua chon =", chon)
        except ValueError:
            print("Vui long nhap so nguyen!")
            continue

        if chon == 1:
            ht = input("Nhap ho ten: ")
            try:
                t = int(input("Nhap tuoi: "))
            except ValueError:
                print("Tuoi phai la so nguyen!")
                continue
            gt = input("Nhap gioi tinh: ")
            dc = input("Nhap dia chi: ")

            print("Chon loai can bo:")
            print("1. Cong nhan")
            print("2. Ky su")
            print("3. Nhan vien")
            try:
                loai = int(input("Nhap lua chon: "))
            except ValueError:
                print("Lua chon phai la so nguyen!")
                continue

            try:
                if loai == 1:
                    bac = int(input("Nhap bac cong nhan: "))
                    qlcb.them_cb(CongNhan(ht, t, gt, dc, bac))
                elif loai == 2:
                    nganh = input("Nhap nganh dao tao: ")
                    qlcb.them_cb(KySu(ht, t, gt, dc, nganh))
                elif loai == 3:
                    cv = input("Nhap cong viec: ")
                    qlcb.them_cb(NhanVien(ht, t, gt, dc, cv))
                else:
                    print("Lua chon khong hop le.")
            except (TuoiKhongHopLe, BacKhongHopLe) as e:
                print(f"Loi: {e}")

        elif chon == 2:
            ten = input("Nhap ten can bo can tim: ")
            qlcb.tim_cb(ten)

        elif chon == 3:
            qlcb.hien_cb()

        elif chon == 4:
            qlcb.thoat()
            print("Thoát chương trình...")
            sys.exit()

        else:
            print("Lua chon khong hop le.")