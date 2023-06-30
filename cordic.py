import math
from math import cos, pi, atan, degrees
from decimal import Decimal, getcontext, Context
ctx = Context(prec=11)

scale = Decimal(1e10)


# =============================================================================
# # create lookup tables

# A = [Decimal(2**-j) for j in range(0, 35)]  # from 1 to 34, length of 34
# print(A)
# # take inverse tangent of values
# A = [ctx.create_decimal(str(atan(float(a)))) for a in A]
# #print(A[0])

# k = []
# for i in range(len(A) - 1):
#     if i == 0:
#         k.append(cos(A[i]))
#     k.append(k[i] * cos(A[i + 1]))
# print(f'k={k}')

# # convert from radians to degrees
# A = [ctx.create_decimal(str(degrees(float(a)))) for a in A]
# # we have out final list A to use in our code 
# print(f'A={A}')

# =============================================================================

A=[Decimal('1'), Decimal('0.5'), Decimal('0.25'), Decimal('0.125'), Decimal('0.0625'), Decimal('0.03125'), Decimal('0.015625'), Decimal('0.0078125'), Decimal('0.00390625'), Decimal('0.001953125'), Decimal('0.0009765625'), Decimal('0.00048828125'), Decimal('0.000244140625'), Decimal('0.0001220703125'), Decimal('0.00006103515625'), Decimal('0.000030517578125'), Decimal('0.0000152587890625'), Decimal('0.00000762939453125'), Decimal('0.000003814697265625'), Decimal('0.0000019073486328125'), Decimal('9.5367431640625E-7'), Decimal('4.76837158203125E-7'), Decimal('2.384185791015625E-7'), Decimal('1.1920928955078125E-7'), Decimal('5.9604644775390625E-8'), Decimal('2.98023223876953125E-8'), Decimal('1.490116119384765625E-8'), Decimal('7.450580596923828125E-9'), Decimal('3.7252902984619140625E-9'), Decimal('1.86264514923095703125E-9'), Decimal('9.31322574615478515625E-10'), Decimal('4.656612873077392578125E-10'), Decimal('2.3283064365386962890625E-10'), Decimal('1.16415321826934814453125E-10'), Decimal('5.82076609134674072265625E-11')]

alpha=[Decimal('45.0'), Decimal('26.565051177077994'), Decimal('14.036243467926479'), Decimal('7.125016348901798'), Decimal('3.576334374997351'), Decimal('1.7899106082460694'), Decimal('0.8951737102110744'), Decimal('0.4476141708605531'), Decimal('0.22381050036853808'), Decimal('0.1119056770662069'), Decimal('0.055952891893803675'), Decimal('0.027976452617003676'), Decimal('0.013988227142265016'), Decimal('0.006994113675352919'), Decimal('0.003497056850704011'), Decimal('0.0017485284269804495'), Decimal('0.0008742642136937803'), Decimal('0.00043713210687233457'), Decimal('0.00021856605343934784'), Decimal('0.00010928302672007149'), Decimal('0.00005464151336008544'), Decimal('0.000027320756680048934'), Decimal('0.000013660378340025243'), Decimal('0.000006830189170012719'), Decimal('0.0000034150945850063712'), Decimal('0.0000017075472925031871'), Decimal('8.537736462515938E-7'), Decimal('4.2688682312579694E-7'), Decimal('2.1344341156289847E-7'), Decimal('1.0672170578144923E-7'), Decimal('5.336085289072462E-8'), Decimal('2.668042644536231E-8'), Decimal('1.3340213222681154E-8'), Decimal('6.670106611340577E-9'), Decimal('3.3350533056702886E-9')]

k=[0.7071067811865476, 0.6324555320336759, 0.6135719910778964, 0.6088339125177524, 0.6076482562561683, 0.607351770141296, 0.6072776440935261, 0.6072591122988928, 0.6072544793325625, 0.6072533210898753, 0.6072530315291345, 0.607252959138945, 0.6072529410413973, 0.6072529365170104, 0.6072529353859136, 0.6072529351031395, 0.6072529350324459, 0.6072529350147725, 0.6072529350103542, 0.6072529350092496, 0.6072529350089735, 0.6072529350089044, 0.6072529350088872, 0.6072529350088829, 0.6072529350088818, 0.6072529350088816, 0.6072529350088814, 0.6072529350088814, 0.6072529350088814, 0.6072529350088814, 0.6072529350088814, 0.6072529350088814, 0.6072529350088814, 0.6072529350088814, 0.6072529350088814]

def cordic(angle):
    # first fold the angle to under 180degrees
    # if angle>180:
    #     angle = angle % 180
    # print(angle)
    # if angle > 90:
    #     angle = 180 - angle
    angle = angle % 90
    print(angle)
    
    # starting unit vector
    x = Decimal(1.0) 
    y = Decimal(0.0)
    theta = Decimal(0.0)
    
    #for i in alpha:
    for i in range(34):  #35
        if theta < angle:
            print(f"A list {A[i]} for {i}")
            print(f"existing x:{x} y:{y}")
            temp_x = x - (y*A[i]) # since y needs the original x for the calc 
            y = y + (x*A[i])
            x = temp_x
            theta = theta + alpha[i]
        else:
            temp_x = x + (y*A[i]) # since y needs the original x for the calc 
            y = y - (x*A[i])
            x = temp_x
            theta = theta - alpha[i]
        print(f"theta:{theta} {i}")
        print(f"x:{x}")
        print(f"y:{y}")
    x = x * Decimal(0.607252935008)
    y = y * Decimal(0.607252935008)
    print(f"final x:{x}")    
    print(f"final y:{y}")
    return theta

cordic(55)




