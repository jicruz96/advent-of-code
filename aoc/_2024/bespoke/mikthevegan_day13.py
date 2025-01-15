input, p1, p2, i, bnum = "data/day13.txt", 0, 0, 0, 10000000000000
currx: list[int] = []
curry: list[int] = []


def calcResult(
    x: list[int],
    y: list[int],
    bn: int,
    p1c: int,
    p2c: int,
) -> list[int]:
    X1, Y1, X2, Y2, div, p2Res, p1Res = (
        x[2],
        y[2],
        x[2] + bn,
        y[2] + bn,
        x[0] * y[1] - x[1] * y[0],
        0,
        0,
    )
    A1, B1, A2, B2 = (
        (X1 * y[1] - x[1] * Y1) / div,
        (x[0] * Y1 - X1 * y[0]) / div,
        (X2 * y[1] - x[1] * Y2) / div,
        (x[0] * Y2 - X2 * y[0]) / div,
    )
    p1Res = 3 * int(A1) + int(B1) if A1.is_integer() and B1.is_integer() else 0
    p2Res = 3 * int(A2) + int(B2) if A2.is_integer() and B2.is_integer() else 0
    return [p1Res + p1c, p2Res + p2c]


for k in open(input):
    if k.strip() == "":
        continue
    arr, i = ((k.replace("=", "+")).split(": ")[1]).split(", "), i + 1
    currx.append(int(arr[0].split("+")[1]))
    curry.append(int(arr[1].split("+")[1]))
    if i % 3 == 0:
        [p1, p2] = calcResult(currx, curry, bnum, p1, p2)
        currx = []
        curry = []

print("Part 1:", p1)
print("Part 2:", p2)
