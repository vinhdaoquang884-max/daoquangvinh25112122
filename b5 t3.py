class Point:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y


class Rectangle:
    def __init__(self, x=0, y=0, w=0, h=0):
        self.center = Point(x, y)
        self.width = w
        self.height = h
    
    def corners(self):
        half_w = self.width / 2.0
        half_h = self.height / 2.0
        return [
            Point(self.center.x - half_w, self.center.y - half_h),  # Goc tren trai
            Point(self.center.x + half_w, self.center.y - half_h),  # Goc tren phai
            Point(self.center.x + half_w, self.center.y + half_h),  # Goc duoi phai
            Point(self.center.x - half_w, self.center.y + half_h)   # Goc duoi trai
        ]


class Circle:
    def __init__(self, center, radius):
        self.center = center
        self.radius = radius


def dist2(a, b):
    """Tinh khoang cach binh phuong giua 2 diem (tranh sqrt de tang hieu suat)"""
    return (a.x - b.x) * (a.x - b.x) + (a.y - b.y) * (a.y - b.y)


def point_in_circle(p, c):
    """Kiem tra diem co nam trong hoac tren vong tron khong"""
    return dist2(p, c.center) <= c.radius * c.radius


def rect_in_circle(r, c):
    """Kiem tra hinh chu nhat co nam hoan toan trong vong tron khong"""
    for corner in r.corners():
        if not point_in_circle(corner, c):
            return False
    return True


def rec_circle_overlap(r, c):
    """Kiem tra hinh chu nhat co giao voi vong tron khong"""
    half_w = r.width / 2.0
    half_h = r.height / 2.0
    closest_x = max(r.center.x - half_w, min(c.center.x, r.center.x + half_w))
    closest_y = max(r.center.y - half_h, min(c.center.y, r.center.y + half_h))
    return dist2(Point(closest_x, closest_y), c.center) <= c.radius * c.radius


def main():
    # Vong tron tam (150, 150) ban kinh 75
    c = Circle(Point(150, 150), 75)
    p1 = Point(150, 100)
    p2 = Point(230, 100)  # p1 trong, p2 ngoai
    
    print(f"Diem p1 {'T' if point_in_circle(p1, c) else 'F'}")
    print(f"Diem p2 {'T' if point_in_circle(p2, c) else 'F'}")
    
    # r1 nho nam trong, r2 lon giao voi vong tron
    r1 = Rectangle(140, 90, 10, 10)
    r2 = Rectangle(100, 50, 300, 200)
    
    print(f"rect_in_circle(r1): {'T' if rect_in_circle(r1, c) else 'F'}")
    print(f"rect_circle_overlap(r2): {'T' if rec_circle_overlap(r2, c) else 'F'}")


if __name__ == "__main__":
    main()