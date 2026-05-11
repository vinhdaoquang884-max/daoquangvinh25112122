from math import gcd
from functools import total_ordering
from typing import List

class MauSoBangKhong(Exception):
    """Raised when denominator equals 0."""
    pass

@total_ordering
class PhanSo:
    """Phân số với đầy đủ operator overloading và magic methods."""

    def __init__(self, tu: int, mau: int):
        if mau == 0:
            raise MauSoBangKhong("Mẫu số không được bằng 0!")
        if mau < 0:
            tu, mau = -tu, -mau
        self._tu = int(tu)
        self._mau = int(mau)

    @property
    def tu(self) -> int:
        return self._tu

    @tu.setter
    def tu(self, value: int):
        self._tu = int(value)

    @property
    def mau(self) -> int:
        return self._mau

    @mau.setter
    def mau(self, value: int):
        if value == 0:
            raise MauSoBangKhong("Mẫu số không được bằng 0!")
        if value < 0:
            self._tu = -self._tu
            self._mau = -int(value)
        else:
            self._mau = int(value)

    def is_toi_gian(self) -> bool:
        return gcd(abs(self._tu), self._mau) == 1

    def toi_gian(self) -> "PhanSo":
        g = gcd(abs(self._tu), self._mau)
        return PhanSo(self._tu // g, self._mau // g)

    def _gia_tri(self) -> float:
        return self._tu / self._mau

    def __add__(self, other: "PhanSo") -> "PhanSo":
        tu  = self._tu * other._mau + other._tu * self._mau
        mau = self._mau * other._mau
        return PhanSo(tu, mau).toi_gian()

    def __sub__(self, other: "PhanSo") -> "PhanSo":
        tu  = self._tu * other._mau - other._tu * self._mau
        mau = self._mau * other._mau
        return PhanSo(tu, mau).toi_gian()

    def __mul__(self, other: "PhanSo") -> "PhanSo":
        return PhanSo(self._tu * other._tu,
                      self._mau * other._mau).toi_gian()

    def __truediv__(self, other: "PhanSo") -> "PhanSo":
        if other._tu == 0:
            raise ZeroDivisionError("Không thể chia cho phân số bằng 0!")
        return PhanSo(self._tu * other._mau,
                      self._mau * other._tu).toi_gian()

    def __eq__(self, other) -> bool:
        if not isinstance(other, PhanSo):
            return NotImplemented
        a = self.toi_gian()
        b = other.toi_gian()
        return a._tu == b._tu and a._mau == b._mau

    def __lt__(self, other) -> bool:
        if not isinstance(other, PhanSo):
            return NotImplemented
        return self._gia_tri() < other._gia_tri()

    def __hash__(self) -> int:
        tg = self.toi_gian()
        return hash((tg._tu, tg._mau))

    def __str__(self) -> str:
        tg = self.toi_gian()
        if tg._mau == 1:
            return str(tg._tu)
        return f"{tg._tu}/{tg._mau}"

    def __repr__(self) -> str:
        return f"PhanSo({self._tu}, {self._mau})"

# Nhập phân số từ bàn phím
def nhap_phan_so(thu_tu: int) -> PhanSo:
    while True:
        try:
            print(f"  Phân số {thu_tu}:")
            tu  = int(input("    Tử số : "))
            mau = int(input("    Mẫu số: "))
            return PhanSo(tu, mau)
        except MauSoBangKhong as e:
            print(f"    ✘ {e} — nhập lại.")
        except ValueError:
            print("    ✘ Vui lòng nhập số nguyên.")

# Demo
def demo():
    print("═"*55)
    print("  DEMO – Phép tính phân số")
    print("═"*55)

    ps1 = PhanSo(1, 2)
    ps2 = PhanSo(1, 3)
    ps3 = PhanSo(2, 4)
    ps4 = PhanSo(3, 1)
    ps5 = PhanSo(-5, 6)

    print(f"\n  ps1 = {repr(ps1)}  →  {ps1}")
    print(f"  ps2 = {repr(ps2)}  →  {ps2}")
    print(f"  ps3 = {repr(ps3)}  →  {ps3}  (tối giản = ps1)")
    print(f"  ps4 = {repr(ps4)}  →  {ps4}  (mẫu = 1 → hiện số nguyên)")
    print(f"  ps5 = {repr(ps5)}  →  {ps5}")

    print(f"\n  {'─'*50}")
    print("  Phép toán:")
    print(f"    ps1 + ps2 = {ps1} + {ps2} = {ps1 + ps2}")
    print(f"    ps1 - ps2 = {ps1} - {ps2} = {ps1 - ps2}")
    print(f"    ps1 * ps2 = {ps1} × {ps2} = {ps1 * ps2}")
    print(f"    ps1 / ps2 = {ps1} ÷ {ps2} = {ps1 / ps2}")

    print(f"\n  {'─'*50}")
    print("  So sánh:")
    print(f"    ps1 == ps3 : {ps1 == ps3}")
    print(f"    ps1 >  ps2 : {ps1 > ps2}")
    print(f"    ps5 <  ps2 : {ps5 < ps2}")

    print(f"\n  {'─'*50}")
    print("  is_toi_gian():")
    print(f"    ps1 (1/2)  : {ps1.is_toi_gian()}")
    print(f"    PhanSo(4,6): {PhanSo(4,6).is_toi_gian()}")

    print(f"\n  {'─'*50}")
    print("  set() loại trùng :")
    tap_hop = {ps1, ps2, ps3, ps4, ps5}
    print(f"    {{{', '.join(str(p) for p in tap_hop)}}}  ({len(tap_hop)} phần tử)")

    print(f"\n  {'─'*50}")
    print("  Test MauSoBangKhong:")
    try:
        PhanSo(1, 0)
    except MauSoBangKhong as e:
        print(f"    ✘ {e}")

# Ứng dụng nhập dãy phân số
def ung_dung():
    print("\n" + "═"*55)
    print("  ỨNG DỤNG – Nhập dãy phân số")
    print("═"*55)

    try:
        n = int(input("  Nhập số lượng phân số: "))
    except ValueError:
        print("  ✘ Không hợp lệ.")
        return

    ds: List[PhanSo] = []
    for i in range(1, n + 1):
        ds.append(nhap_phan_so(i))

    print("\n  Dạng tối giản:")
    for ps in ds:
        tg = ps.toi_gian()
        print(f"    {repr(ps):20s}  →  {tg}")

    print("\n  Sắp xếp tăng dần:")
    for ps in sorted(ds):
        print(f"    {ps}")

if __name__ == "__main__":
    demo()
    print("\n" + "─"*55)
    chay = input("  Chạy ứng dụng nhập phân số? (y/n): ").strip().lower()
    if chay == "y":
        ung_dung()