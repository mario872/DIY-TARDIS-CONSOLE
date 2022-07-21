import glowbit

matrix = glowbit.matrix4x4()

for x in range(4):
    for y in range(4):
        c = matrix.wheel(36*(x, y))
        matrix.pixelSetXY(x, y, c)

matrix.pixelsShow()
