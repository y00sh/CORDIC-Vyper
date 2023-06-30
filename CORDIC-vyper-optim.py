import boa
from decimal import Decimal
from decimal import ROUND_DOWN

boa.env.enable_gas_profiling()

srce = """
@external
@view
def trig(angle: decimal) -> (decimal, decimal):
    ALPHA: decimal[35] = [45.0, 26.5650511771, 14.0362434679, 7.125016349, 3.576334375, 1.7899106082, 0.8951737102, 0.4476141709, 0.2238105004, 0.1119056771, 0.0559528919, 0.0279764526, 0.0139882271, 0.0069941137, 0.0034970569, 0.0017485284, 0.0008742642, 0.0004371321, 0.0002185661, 0.000109283, 0.0000546415, 0.0000273208, 0.0000136604, 0.0000068302, 0.0000034151, 0.0000017075, 0.0000008538, 0.0000004269, 0.0000002134, 0.0000001067, 0.0000000534, 0.0000000267, 0.0000000133, 0.0000000067, 0.0000000033] 

    target_angle: decimal = angle % 90.0
    #x: uint256 = 10_000_000_000_000    # 10**13  
    x: uint256 = 100_000_000_000_000_000_000 # 10**20
    temp_x: uint256 = 0
    y: uint256 = 0    # sine
    theta: decimal = 0.0  #degrees

    for i in range(35):  #35
        if theta < target_angle:
            temp_x = x - (y >> i) # since y needs the original x for the calc , too bad no more simult assignment
            y = y + (x >> i)
            x = temp_x
            theta = theta + ALPHA[i]
        else:
            temp_x = x + (y >> i) # since y needs the original x for the calc 
            y = y - (x >> i)
            x = temp_x
            theta = theta - ALPHA[i]
    # multiply back in the cos(alpha)
    #cos: decimal = convert(x, decimal) / 16467602581210.6549123463
    #sin: decimal = convert(x, decimal) / 16467602581210.6549123463
    cos: decimal = convert(x, decimal) / 164676025812106549123.4637838099
    sin: decimal = convert(x, decimal) / 164676025812106549123.4637838099
    
    
    #modify the sign +/- depending on the quadrant of given angle 
    if angle < 90.0:
        # First quadrant
        return cos, sin
    elif angle < 180.0:
        # Second quadrant
        return -cos, sin
    elif angle < 270.0:
        # Third quadrant
        return -cos, -sin
    else:
        # Fourth quadrant
        return cos, -sin
    
    return cos, sin

"""
ww = boa.loads(srce)
x = Decimal('235')
ww.trig(x)
#ww.line_profile().summary()
ww._computation.get_gas_used()
