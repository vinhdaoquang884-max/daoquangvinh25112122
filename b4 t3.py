#con chó
class ConCho:
    def __init__(self, ten, mausac, giong, camxuc):
        self.ten = ten
        self.mausac = mausac
        self.giong = giong
        self.camxuc = camxuc
    
    def sua(self):
        print(f"{self.ten} dang sua")
    
    def vayduoi(self):
        print(f"{self.ten} dang vay duoi")
    
    def an(self):
        print(f"{self.ten} dang an")
    
    def chay(self):
        print(f"{self.ten} dang chay")

# oto
class Oto:
    def __init__(self, hang, kthuoc, mau, gia, tocdo):
        self.hang = hang
        self.kthuoc = kthuoc
        self.mau = mau
        self.gia = gia
        self.tocdo = tocdo
    
    def tangtoc(self, them):
        self.tocdo += them
        print(f"{self.hang} dang tang toc, toc do hien tai: {self.tocdo} km/h")
    
    def giamtoc(self, bot):
        self.tocdo -= bot
        if self.tocdo < 0:
            self.tocdo = 0  # Toc do khong duoc am
        print(f"{self.hang} dang giam toc, toc do hien tai: {self.tocdo} km/h")
    
    def dam(self):
        print(f"{self.hang} bi dam")
        self.tocdo = 0

#tai khoan ngan hang
class TaiKhoan:
    def __init__(self, tentk, stk, bank, sodu):
        self.tentk = tentk
        self.stk = stk
        self.bank = bank
        self.sodu = sodu
    
    def rut(self, tien):
        if tien > self.sodu:
            print("So du ko du de rut")
        else:
            self.sodu -= tien
            print(f"Rut thanh cong {tien} VND, so du con lai: {self.sodu}")
    
    def gui(self, tien):
        self.sodu += tien
        print(f"Gui thanh cong {tien} VND, so du con lai: {self.sodu}")
    
    def kiemtra(self):
        print(f"Tai khoan: {self.tentk}, So tai khoan: {self.stk}, Ngan hang: {self.bank}, So du: {self.sodu} VND")


def main():
    # Inp lop ConCho
    cho1 = ConCho("Lucky", "Vang", "Shiba", "Vui")
    cho1.sua()
    cho1.vayduoi()
    cho1.an()
    cho1.chay()
    print()
    
    # Inp lop Oto
    oto1 = Oto("Toyota", "Sedan", "Do", 500000000, 0)
    oto1.tangtoc(60)
    oto1.tangtoc(40)
    oto1.giamtoc(30)
    oto1.dam()
    print()
    
    # Inp lop TaiKhoan
    tk1 = TaiKhoan("Nguyen Bui Tu", "100021042007", "Techcombank", 100000000)
    tk1.kiemtra()
    tk1.rut(2000000)
    tk1.gui(5000000)
    tk1.kiemtra()


if __name__ == "__main__":
    main()