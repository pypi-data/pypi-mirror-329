from xctype import *


def test():
    a = U32()
    print(a, a.size())
    a.val = 32
    print(a, a.size())
    b = U16()
    print(b, b.size())
    b.val = 16
    print(b, b.size())

    s = make_struct('only_primitive_struct_auto', a=U32(), b=U16())()
    print(s, s.size())
    ba = bytearray()
    ba += a.to_bytes()
    ba += b.to_bytes()
    s.from_bytes(ba)
    print(s, s.size())
    s.m_a = 0xAA
    print(s)
    s.m_a = 0x10203040
    print(s)

    # exit()

    array = Array(elem_class=U16, num_elem=3)
    print(array, array.size())
    array.from_bytes(ba)
    print(array, array.size())

    s = make_struct('struct_with_array_auto', a=U16(), b=Array(elem_class=U16, num_elem=2))()
    print(s, s.size())
    print(s.to_str(deep=True))
    s.from_bytes(ba)
    print(s, s.size())
    print(s.to_str(deep=True))
    asize = symbols('asize')
    array = Array(elem_class=U16, num_elem=asize)
    print(array, array.size())

    members_t = make_array(elem_cls=U16, n_elem=int_symbol('size', granularity=2) / 2)
    struct_with_var_len_array_auto_class = make_struct(
        'struct_with_var_len_array_auto', size=U16(), members=members_t()
    )
    s = struct_with_var_len_array_auto_class()
    ssize = s.size()
    print(s, s.size())
    print(s.to_str(deep=True))
    ba = bytearray()
    size = U16(8)
    ba += size.to_bytes()
    for i in range(0, size // 2):
        e = U16()
        e.val = i
        ba += e.to_bytes()
    s.from_bytes(ba)
    print(s, s.size())
    print(s.to_str(deep=True))
    print(s.m_size)
    print(s.m_size.size())
    print(s.m_members)
    a = U8(1)
    print(type(a), a)
    test = [1 + a, a + 1, 1 - a, a - 1, a - 2, a - 256, a - 257, a - 258, 0 - a, 256 - a]
    for e in test:
        print(type(e), e)
    print(s, s.offsets)

    struct_bit_size = make_struct('struct_bit_size', flag0=Bool(), flag1=Bool())
    s = struct_bit_size()
    print(s, s.bit_size(), s.size())
    c = U64()
    print(c, c.bit_size(), c.size())

    s = struct_with_var_len_array_auto_class()
    print(s.to_c_typedef(tab='    '))
    print(s.gen_check_against_c())
    print(s.m_members.__class__)
    with open('main.c', 'w') as f:
        print(gen_check_against_c_main([struct_with_var_len_array_auto_class], tab='    '), file=f)
