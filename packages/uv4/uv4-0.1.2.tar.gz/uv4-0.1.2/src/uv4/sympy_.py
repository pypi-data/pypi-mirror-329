import sympy

from math import ceil


u = [
    0xFFFCB933BD6FAD37AA2D162D1A594001,
    0xFFF97272373D413259A46990580E213A,
    0xFFF2E50F5F656932EF12357CF3C7FDCC,
    0xFFE5CACA7E10E4E61C3624EAA0941CD0,
    0xFFCB9843D60F6159C9DB58835C926644,
    0xFF973B41FA98C081472E6896DFB254C0,
    0xFF2EA16466C96A3843EC78B326B52861,
    0xFE5DEE046A99A2A811C461F1969C3053,
    0xFCBE86C7900A88AEDCFFC83B479AA3A4,
    0xF987A7253AC413176F2B074CF7815E54,
    0xF3392B0822B70005940C7A398E4B70F3,
    0xE7159475A2C29B7443B29C7FA6E889D9,
    0xD097F3BDFD2022B8845AD8F792AA5825,
    0xA9F746462D870FDF8A65DC1F90E061E5,
    0x70D869A156D2A1B890BB3DF62BAF32F7,
    0x31BE135F97D08FD981231505542FCFA6,
    0x9AA508B5B7A84E1C677DE54F3E99BC9,
    0x5D6AF8DEDB81196699C329225EE604,
    0x2216E584F5FA1EA926041BEDFE98,
    0x48A170391F7DC42444E8FA2,
]

x = sympy.symbols('x')
g = (sympy.S(str(2**128)) / sympy.S('10001/10000') ** (2 ** (x - 1)))

a = [0 for _ in range(21)]

PREC = 1000

a[0] = g.evalf(PREC, subs={x: sympy.S(' 0.0')})
a[1] = g.evalf(PREC, subs={x: sympy.S(' 1.0')})
a[2] = g.evalf(PREC, subs={x: sympy.S(' 2.0')})
a[3] = g.evalf(PREC, subs={x: sympy.S(' 3.0')})
a[4] = g.evalf(PREC, subs={x: sympy.S(' 4.0')})
a[5] = g.evalf(PREC, subs={x: sympy.S(' 5.0')})
a[6] = g.evalf(PREC, subs={x: sympy.S(' 6.0')})
a[7] = g.evalf(PREC, subs={x: sympy.S(' 7.0')})
a[8] = g.evalf(PREC, subs={x: sympy.S(' 8.0')})
a[9] = g.evalf(PREC, subs={x: sympy.S(' 9.0')})
a[10] = g.evalf(PREC, subs={x: sympy.S('10.0')})
a[11] = g.evalf(PREC, subs={x: sympy.S('11.0')})
a[12] = g.evalf(PREC, subs={x: sympy.S('12.0')})
a[13] = g.evalf(PREC, subs={x: sympy.S('13.0')})
a[14] = g.evalf(PREC, subs={x: sympy.S('14.0')})
a[15] = g.evalf(PREC, subs={x: sympy.S('15.0')})
a[16] = g.evalf(PREC, subs={x: sympy.S('16.0')})
a[17] = g.evalf(PREC, subs={x: sympy.S('17.0')})
a[18] = g.evalf(PREC, subs={x: sympy.S('18.0')})
a[19] = g.evalf(PREC, subs={x: sympy.S('19.0')})
a[20] = g.evalf(PREC, subs={x: sympy.S('20.0')})

for i in range(20):
    b = int(ceil(a[i]))
    print("| $h_{{{3}}}(1)$ | `0x{0:x}` | `0x{1:x}` | ${2:d}$|".format(b, u[i], u[i] - b, i))
