class Point:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
    
    def inp(self):
        print("Nhap x va y: ", end="")
        x, y = map(int, input().split())
        self.x = x
        self.y = y
    
    def out(self):
        print(f"Toa do: ({self.x}, {self.y})", end="")
    
    def getX(self):
        return self.x
    
    def getY(self):
        return self.y


class LineSegment:
    def __init__(self, d1=None, d2=None, x1=None, y1=None, x2=None, y2=None):
        # Default constructor: d1(8,5), d2(1,0)
        if d1 is None and d2 is None and x1 is None:
            self.d1 = Point(8, 5)
            self.d2 = Point(1, 0)
        # Constructor with two Point objects
        elif isinstance(d1, Point) and isinstance(d2, Point):
            self.d1 = Point(d1.getX(), d1.getY())
            self.d2 = Point(d2.getX(), d2.getY())
        # Constructor with four integers
        elif isinstance(d1, int) and isinstance(d2, int) and isinstance(x1, int) and isinstance(y1, int):
            self.d1 = Point(d1, d2)
            self.d2 = Point(x1, y1)
        # Copy constructor
        elif isinstance(d1, LineSegment):
            self.d1 = Point(d1.d1.getX(), d1.d1.getY())
            self.d2 = Point(d1.d2.getX(), d1.d2.getY())
    
    def inp(self):
        print("Nhap toa do cho diem d1:")
        self.d1.inp()
        print("Nhap toa do cho diem d2:")
        self.d2.inp()
    
    def out(self):
        print("Doan thang: d1", end="")
        self.d1.out()
        print(" - d2", end="")
        self.d2.out()
        print()


if __name__ == "__main__":
    seg1 = LineSegment()
    print("Mac dinh: ", end="")
    seg1.out()
    
    a = Point(2, 3)
    b = Point(5, 7)
    seg2 = LineSegment(a, b)
    print("2 Point: ", end="")
    seg2.out()
    
    seg3 = LineSegment(1, 1, 4, 4)
    print("4 int: ", end="")
    seg3.out()
    
    seg4 = LineSegment(seg3)
    print("Sao chep: ", end="")
    seg4.out()