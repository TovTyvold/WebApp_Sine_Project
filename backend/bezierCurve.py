from math import sqrt
import envelope


def bOfT(p0, p1, p2, t):
    x0, y0 = p0
    x1, y1 = p1
    x2, y2 = p2

    x = (1-t)*(1-t)*x2 + 2*(1-t)*t*x1 + t*t*x0
    y = (1-t)*(1-t)*y2 + 2*(1-t)*t*y1 + t*t*y0

    return (x, y)


def tOfX(p0, p1, p2, x):
    x0, y0 = p0
    x1, y1 = p1
    x2, y2 = p2

    a = (x2 - 2*x1 + x0) #will be 0 if it becomes straight line
    b = (-2*x2 + 2*x1)
    c = (x2 - x)

    return (-b - sqrt(b*b - 4*a*c)) / (2*a) if a != 0 else -c/b


def bOfX(p0, p1, p2, x):
    return bOfT(p0, p1, p2, tOfX(p0, p1, p2, x))


def func(p0, p1, p2):
    def get(x):
        if x < p0[0]:
            return p0[1]
        elif x >= p2[0]:
            return p2[1]
        else:
            return bOfT(p0, p1, p2, tOfX(p0, p1, p2, x))[1]

    return get
    #return lambda x: bOfT(p0, p1, p2, tOfX(p0, p1, p2, x))[1] if p0[0] < x and x <= p2[0] else 0


#return lambda
def composite(points, xsamples):
    funcs = []

    for i in range(1, len(points), 2):
        funcs.append(func(points[i-1], points[i], points[i+1]))

    yvalues = []
    for x in xsamples:
        val = 0
        for f in funcs:
            val += f(x)

        yvalues.append(val)

    return yvalues


def compositeFunc(points, dim=3):
    def get(x:float) -> float:
        i = 1
        while True:
            px, _ = points[i-1]
            nx, _ = points[i+1]

            if px <= x and x < nx:
                #found the correct point trio
                break

            if i+2 < len(points):
                i += 2
            else:
                break

        # print(points[i-1], points[i], points[i+1])
        return func(points[i-1], points[i], points[i+1])(x)
    return get


def compositeOn(points, xsamples):
    return [compositeFunc(points)(x) for x in xsamples]

if __name__ == "__main__":
    smpls = 10
    secnds = 4
    xpoints = [i/smpls for i in range(int(smpls*secnds))]
    ypoints = compositeOn([(0, 0), (0.2, 0.5), (0.4, 1), (0.9, 0.8200000000000001), (1.4, 0.64), (2.3499999999999996, 0.64), (3.3, 0.64), (3.5465, 0.32), (3.7929999999999997, 0)], xpoints)
    for x,y in zip(xpoints, ypoints):
        print(x, ",", y)