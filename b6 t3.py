class Nhanvien:
    LUONG_MAX = 500000000.0  # Maximum salary constant
    
    def __init__(self, ten="", lcb=0, hsl=0):
        self.ten = ten
        self.luongcoban = lcb
        self.hesoluong = hsl
    
    def getTen(self):
        return self.ten
    
    def getLuongCoBan(self):
        return self.luongcoban
    
    def getHeSoLuong(self):
        return self.hesoluong
    
    def setTen(self, t):
        self.ten = t
    
    def setLuongCoBan(self, lcb):
        self.luongcoban = lcb
    
    def setHeSoLuong(self, hsl):
        self.hesoluong = hsl
    
    def tinhluong(self):
        """Tinh luong dua tren luong co ban va he so luong"""
        return self.luongcoban * self.hesoluong
    
    def inTTin(self):
        """In thong tin nhan vien"""
        print(f"Ten: {self.ten}")
        print(f"Luong co ban: {self.luongcoban}")
        print(f"He so luong: {self.hesoluong}")
        print(f"Luong: {self.tinhluong()}")
    
    def tangluong(self, delta):
        """Tang luong voi kiem tra dieu kien"""
        if delta <= 0:
            print("Delta phai > 0!")
            return False
        
        luongHienTai = self.tinhluong()
        luongMoi = luongHienTai + delta  # Tinh luong moi sau khi tang
        
        if luongMoi > Nhanvien.LUONG_MAX:
            print(f"Khong the tang luong! Luong moi vuot LUONG_MAX ({int(Nhanvien.LUONG_MAX)}).")
            return False
        
        # Giu nguyen heSoLuong, dieu chinh luongCoBan theo luong moi
        self.luongcoban = luongMoi / self.hesoluong
        print(f"Tang luong thanh cong. Luong moi: {int(self.tinhluong())}")
        return True


def main():
    nv = Nhanvien("TieuKy", 1000000, 2.5)
    nv.inTTin()
    
    print("\n=== TANG LUONG ===")
    nv.tangluong(2000000)  # Tang 2 trieu
    
    print("\n=== THONG TIN SAU KHI TANG LUONG ===")
    nv.inTTin()


if __name__ == "__main__":
    main()