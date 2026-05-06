import math

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def input(self):
        self.x, self.y = map(int, input("Nhap x va y: ").split())

    def output(self):
        print(f"Toa do: ({self.x}, {self.y})")

    def doixungquagocO(self):
        return Point(-self.x, -self.y)

    def khoangcachdenO(self):
        return math.sqrt(self.x * self.x + self.y * self.y)

    @staticmethod
    def khoangcach2diem(a, b):
        return math.sqrt((a.x - b.x) ** 2 + (a.y - b.y) ** 2)


def main():
    p1 = Point(3, 4)
    p1.output()

    p2 = p1.doixungquagocO()
    print("Doi xung qua goc O -> ", end="")
    p2.output()

    print(f"Khoang cach den O -> {p1.khoangcachdenO()}")

    p3 = Point(6, 8)
    print(f"Khoang cach tu p1 den p3: {Point.khoangcach2diem(p1, p3)}")


if __name__ == "__main__":
    main()