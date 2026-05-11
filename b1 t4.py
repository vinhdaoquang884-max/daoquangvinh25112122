class NhanVien:
    LUONG_MAX = 500000000.0
    
    def __init__(self, ten="", lcb=0, hsl=0):
        self.ten = ten
        self.luongcoban = lcb
        self.hesoluong = hsl
    
    # Getter
    def getTen(self):
        return self.ten
    
    def getLuongCoBan(self):
        return self.luongcoban
    
    def getHeSoLuong(self):
        return self.hesoluong
    
    # Setter
    def setTen(self, t):
        self.ten = t
    
    def setLuongCoBan(self, lcb):
        self.luongcoban = lcb
    
    def setHeSoLuong(self, hsl):
        self.hesoluong = hsl
    
    def tinhluong(self):
        return self.luongcoban * self.hesoluong
    
    def tangluong(self, delta):
        hsmoi = self.hesoluong + delta
        luongmoi = self.luongcoban * hsmoi
        if luongmoi > self.LUONG_MAX:
            print(f"Khong the tang luong! Luong moi vuot LUONG_MAX ({self.LUONG_MAX:.0f}).")
            return False
        self.hesoluong = hsmoi
        return luongmoi <= self.LUONG_MAX
    
    def inTTin(self):
        print(f"Ten: {self.ten}")
        print(f"Luong co ban: {self.luongcoban}")
        print(f"He so luong: {self.hesoluong}")
        print(f"Luong: {self.tinhluong()}")


if __name__ == "__main__":
    nv = NhanVien("Bui Tu", 1000000, 2.5)
    nv.inTTin()
    print("\n=== TANG LUONG ===")
    nv.tangluong(2.0)  # Tang 2 he so luong
    print("\n=== THONG TIN SAU KHI TANG LUONG ===")
    nv.inTTin()