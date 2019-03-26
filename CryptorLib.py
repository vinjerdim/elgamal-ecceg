def is_prime(n) : 
    if n <= 1 :
        return False
    if n <= 3 :
        return True
  
    if (n % 2 == 0 or n % 3 == 0) : 
        return False
  
    i = 5
    while(i * i <= n) : 
        if (n % i == 0 or n % (i + 2) == 0) : 
            return False
        i = i + 6
    return True

def gcd(a, b):
    if (a == 0):
        return b
    return gcd(b % a, a)

def modular_pow(x, y, m) : 
    if (y == 0) : 
        return 1
          
    p = modular_pow(x, y // 2, m) % m 
    p = (p * p) % m 
  
    if(y % 2 == 0) : 
        return p  
    else :  
        return ((x * p) % m) 

def modular_inv(a, m) : 
    g = gcd(a, m)

    if (g != 1) : 
        return -1
    else : 
        return modular_pow(a, m - 2, m)

class EllipticCurve():
    def __init__(self, a, b, p) :
        self.a = a
        self.b = b
        self.p = p
    
    def evaluate(self, x) :
        return ((x ** 3) + self.a * x + self.b) % self.p
    
    def get_point(self, x) :
        y_square = self.evaluate(x)

        result = list()
        for i in range(self.p) :
            if (i ** 2 % self.p) == y_square :
                result.append((x, i))
        
        return result
    
    

    def gradient(self, point1, point2=None) :
        if point2 != None :
            top = point1[1] - point2[1]
            bottom = point1[0] - point2[0]
            if bottom < 0 :
                bottom = -bottom; top = -top
        else :
            top = 3 * point1[0] ** 2 + self.a
            bottom = 2 * point1[1]
        
        if bottom == 0 :
            return None
            
        return (top * modular_inv(bottom, self.p)) % self.p

    def add(self, point1, point2) :
        if point1 == point2 :
            g = self.gradient(point1)
        else :
            g = self.gradient(point1, point2)

        if g == None :
            return None

        x = (g ** 2 - point1[0] - point2[0]) % self.p
        y = (g * (point1[0] - x) - point1[1]) % self.p
        return x, y

    def subtract(self, point1, point2) :
        point2 = (point2[0], -point2[1] % self.p)
        return self.add(point1, point2)

    def multiply(self, k, point) :
        result = point
        for i in range(1, k) :
            result = self.add(result, point)
            if result == None:
                return None
        return result

    def encode(self, m) :
        k = 10
        for i in range(1, k):
            x = m * k + i
            point = self.get_point(x)
            if (self.get_point(x) != []):
                return point[0]
        return None
    
    def decode(self, point) :
        k = 10
        x = point[0]
        return (x - 1) // k
    
    def get_basis(self) :
        result = None
        for i in range(self.p) :
            points = self.get_point(i)
            if points != [] :
                return points[0]
        return result
