class Sieunhan:
    def __init__(self, ten, vukhi, mausac, sucmanh):
        self.ten = ten
        self.vukhi = vukhi
        self.mausac = mausac
        self.sucmanh = sucmanh

    def output(self):
        print(f"Ten: {self.ten} | Vu khi: {self.vukhi} | Mau sac: {self.mausac} | Suc manh: {self.sucmanh}")

def main():
    ds = []
    print("=== NHAP THONG TIN SIEU NHAN ===")

    while True:
        ten = input("Nhap ten (hoac 'exit'de thoat): ")

        if not ten:
            print("Ten khong duoc de trong. Vui long nhap lai.")
            continue

        if ten.isdigit():
            print("Ten khong duoc chua so. Vui lòn nhap lai.")
            continue

        if ten == "exit":
            break

        vukhi = input("Nhap vu khi: ")
        mausac = input("Nhap mau sac: ")
         
        try:
            sucmanh = int(input("Nhap suc manh (1-10): "))
            ds.append(Sieunhan(ten, vukhi, mausac, sucmanh))
        except ValueError:
            print("Suc manh phai la so nguyen. Vui long nhap lai.")
            continue
    
    print("\n=== DANH SACH SIEU NHAN ===")
    for sn in ds:
        sn.output()

if __name__ == "__main__":
    main()