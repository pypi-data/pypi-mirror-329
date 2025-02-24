def merge_sort(massive: list) -> list:
    """Merge sort of the list[int]"""
    def merge(a: list, b: list):
        res = []
        i = 0
        j = 0
        while i < len(a) and j < len(b):
            if a[i] <= b[j]:
                res.append(a[i])
                i += 1
            else:
                res.append(a[j])
                j += 1
        res += a[i:] + b[j:]
        return res

    if len(massive) <= 1:
        return massive
    else:
        l = massive[:len(massive)//2]
        r = massive[len(massive)//2:]
    return (
        merge(merge_sort(l), merge_sort(r)))

def select_sort(massive: list) -> list:
    """Selection sort of the list[int]"""
    for i in range(len(massive)-1):
        x = massive[i]
        m = i
        for j in range(i+1, len(massive)):
            if massive[j] < x:
                x = massive[j]
                m = j
        massive[m], massive[i] = massive[i], massive[m]
    return massive

def insertion_sort(massive: list) -> list:
    """Insertion sort of the list[int]"""
    for i in range(1,len(massive)):
        temp = massive[i]
        j = i - 1
        while j >= 0 and temp < massive[j]:
            massive[j+1] = massive[j]
            j = j - 1
        massive[j+1] = temp
    return massive

def buble_sort(massive: list) -> list:
    """Buble sort of the list[int]"""
    for i in range(len(massive)-1):
        for j in range(len(massive)-i-1):
            if massive[j+1] < massive[j]:
                massive[j], massive[j+1] = massive[j+1], massive[j]
    return massive

def count_sort(massive: list) -> list:
    """Count sort of the list[int]"""
    from collections import defaultdict
    def mx(massive):
        max_element = massive[0]
        for i in range(len(massive)):
            if massive[i] > max_element:
                max_element = massive[i]
        return max_element

    def mn(massive):
        min_element = massive[0]
        for i in range(len(massive)):
            if massive[i] < min_element:
                min_element = massive[i]
        return min_element
    
    count = defaultdict(int)

    for i in massive:
        count[i] += 1
    result = []
    for j in range(mn(massive), (mx(massive)+1)):
        if count.get(j) is not None:
            for i in range(count.get(j)):
                result.append(j)
    return result

def quick_sort(massive):
    """Quick sort of the list[int]"""
    from random import choice

    if len(massive)<= 1:
        return massive
    else:
        q = choice(massive)
        l_nums = [n for n in massive if n < q]
        e_nums = [q]
        r_nums = [n for n in massive if n > q]
        return quick_sort(l_nums) + e_nums + quick_sort(r_nums)

def binary_search_left(element: int, massive: list) -> int:
    """Binary search of int element from left boundary"""
    left = -1
    right = len(massive)
    while right - left > 1:
        middle = (left + right) // 2
        if massive[middle] < element:
            left = middle
        else:
            right = middle
    return left + 1

def binary_search_right(element: int, massive: list) -> int:
    """Binary search of int element from right boundary"""
    left = -1
    right = len(massive)
    while right - left > 1:
        middle = (left + right) // 2
        if massive[middle] <= element:
            left = middle
        else:
            right = middle
    return right - 1

def to_base(number: int, base: int) -> str:
    """Converts int number to base<=36"""
    if base > 36:
        raise Exception('radix is greater than expected')
    ans = ''
    while number > 0:
        number, remainder = divmod(number, base)
        if remainder > 9:
            remainder = chr(ord('A') + remainder - 10)
        ans = str(remainder) + ans
    return ans

def to_int(number: str, base: int) -> int:
    """Converts str number to base<=36"""
    number = str(number)
    if base > 36:
        raise Exception('radix is greater than expected')
    table = {'A': 10, 'B': 11, 'C': 12, 'D': 13, 'E': 14, 'F': 15, 'G': 16, 'H': 17, 'I': 18, 'J': 19, 'K': 20, 'L': 21,
             'M': 22, 'N': 23, 'O': 24, 'P': 25, 'Q': 26, 'R': 27, 'S': 28, 'T': 29, 'U': 30, 'W': 32, 'X': 33, 'Y': 34,
             'Z': 35}
    s = 0
    for i in range(len(number)):
        if number[i].isalpha():
            a = int(len(number) - 1 - i)
            b = base ** a
            c = table.get(number[i])
            s += c * b
        else:
            a = int(len(number) - 1 - i)
            b = base ** a
            c = int(number[i])
            s += c * b
    return s

def max_index(massive: list) -> int:
    """Returns int index of the max element"""
    max_index = 0
    for i in range(len(massive)):
        if massive[i] > massive[max_index]:
            max_index = i
    return max_index

def min_index(massive: list) -> int:
    """Returns int index of the min element"""
    min_index = 0
    for i in range(len(massive)):
        if massive[i] < massive[min_index]:
            min_index = i
    return min_index

def arinc429_bnr_generator() -> None:
    """Function for generating ARINC429 messages through console \n 
BNR only, SDI as label extension"""
    message = ''

    print("""Select label:
    001 Distance to go
    012 Ground speed
    100 Selected radial on VOR
    101 Heading select
    102 Selected altitude
    104 Selected altitude rate
    105 QFU
    114 Selected airspeed/mach
    116 Cross track distance
    117 NAV vertical divation
    140 Flight director yaw command
    141 Flight director roll command
    142 Fast/slow indicator
    143 Fligth director pitch command
    162 ADF1
    173 Localizer
    205 Glide slope
    206 Indicated airspeed
    210 True airspeed
    212 Barometric altitude rate
    222 Omnibearing on VOR
    270 Alert and To-From bitfield
    312 Ground speed
    313 True track angle
    314 True heading
    320 Magnetic heading
    321 Ground speed
    324 Pitch angle
    325 Roll angle
    335 Track rate angle
    365 Inertial vertical velocity""")
    selected_label = input()
    if selected_label not in ['001', '012', '100', '101', '102', '104', '105', '114', '116', '117', '140', '141', '141', '142', '143', '162', '173', '205', '206', '210', '212', '222', '270', '312', '313', '314', '320', '321', '324', '325', '335', '365']:
        raise SystemExit("wrong label")
    label = str(bin(int(selected_label)))[2::]
    while len(label) < 10:
        label = '0' + label
    message += label

    print("enter data (must be less then 262143)")
    selected_data = bin(int(input()))[2::]
    if len(selected_data) > 18:
        raise SystemExit('selected data must be less then 262143')
    while len(selected_data) < 18:
        selected_data = '0' + selected_data
    message += selected_data

    print("""enter data sign (29th bit)
0 Plus, North, East, Right, To, Above
1 Minus, South, West, Left, From, Below""")
    selected_sign = input()
    if selected_sign != '0' and selected_sign != '1':
        raise SystemExit("wrong data sign")
    message += selected_sign

    print("""enter SSM
    00 Failure Warning
    01 No Computed Data
    10 Functional Test
    11 Normal Operation""")
    selected_ssm = input()
    if selected_ssm != '00' and selected_ssm != '01' and selected_ssm != '10' and selected_ssm != '11':
        raise SystemExit("wrong ssm")
    message += selected_ssm

    if message.count('1') % 2 == 0:
        message += '1'
        print("Selected parity 1")
    else:
        message += '0'
        print("Selected parity 0")

    print(message)

def otrezok_len_max():
    m = 0
    P = [i for i in range(12, 20)]
    Q = [i for i in range(5, 15)]
    for Amin in range(1, 101):
        for Amax in range(Amin + 1, 101):
            check = 1
            A = [i for i in range(Amin, Amax)]
            for x in range(1, 101):
                f = (((x in Q) <= (x in P)) and x in A) #формула; == - тождественно равно, <= - импликация
                if f == 1: #условие которое НЕ подходит
                    check = 0
                    break
            if check == 1:
                m = max(m, Amax - Amin)
    print(m)

def otrezok_len_min():
    m = 10**6
    P = [i for i in range(10, 28)]
    Q = [i for i in range(0, 12)]
    for Amin in range(1, 50):
        for Amax in range(Amin + 1, 50):
            check = 1
            A = [i for i in range(Amin, Amax)]
            for x in range(-300, 300):
                f = ((x not in A) <= (x not in P)) or (x in Q) #формула; == - тождественно равно, <= - импликация
                if f == 0: #условие которое НЕ подходит
                    check = 0
                    break
            if check == 1:
                m = min(m, Amax - Amin)
    print(m)
    
def otrezok_select():
    def is_formula_false(P, Q, A):
        P_set = set(range(P[0], P[1] + 1))
        Q_set = set(range(Q[0], Q[1] + 1))
        A_set = set(range(A[0], A[1] + 1))
        
        for x in range(min(min(P_set), min(Q_set), min(A_set)), max(max(Q_set), max(P_set), max(A_set))):
            if (x in P_set and x not in Q_set and x in A_set) == 1: #условие которое НЕ подходит
                return False
        return True

    def find_valid_A(P, Q, options):
        for A in options:
            if is_formula_false(P, Q, A):
                return A
        return None

    P = (5, 15)
    Q = (10, 20)
    options = [(0, 7), (8, 15), (15, 20), (7, 20)]
    A = find_valid_A(P, Q, options)
    print("Подходящий отрезок A:", A)
    
def yravnenie_max():
    for a in range(300, 1, -1): 
        k = 0
        for x in range(0, 300):
            for y in range(0, 300):
                if ((x < 3) <= (x * x <= a)) and ((y*y < a) <= (y <= 15)): #формула
                    k += 1
        if k == 90_000:
            print(a)
            break

def yravnenie_min():
    for a in range(-300, 300, 1): 
        k = 0
        for x in range(0, 300):
            for y in range(0, 300):
                if (((x<=5) <= (x*x < a)) and ((y*y<a) <= (y<7))) == 1: #формула
                    k += 1
        if k == 90_000:
            print(a)
            break
        
def yravnenie_how_much():
    c = 0
    for a in range(300, -300, -1): 
        k = 0
        for x in range(0, 300):
            for y in range(0, 300):
                if (((x<=5) <= (x*x < a)) and ((y*y<=a) <= (y<=8))) == 1: #формула
                    k += 1
        if k == 90_000:
            c += 1
    print(c)

def del_max():
    def f(x, A):
        return (not(x % A == 0) and (x % 21 == 0))<=(not(x%14==0)) #формула


    for A in range(10000, 0, -1):
        flag = True
        for x in range(1000):
            if not f(x, A):
                flag = False
        if flag:
            print(A)
            break

def del_min():
    def f(x, A):
        return (((x%A==0)and(not(x%16==0)))<=(x%32==0)) #формула


    for A in range(1, 10000, 1):
        flag = True
        for x in range(1000):
            if not f(x, A):
                flag = False
        if flag:
            print(A)
            break

def alph_what_word():
    a = {0: "А", 1: "К", 2: "Р", 3: "У"}
    k = 0
    for i in range(0, len(a)):
        for j in range(0, len(a)):
            for g in range(0, len(a)):
                for m in range(0, len(a)):
                    for n in range(0, len(a)):
                        k += 1
                        if k == 250: # на каком месте стоит (какое место в задании такое и писать)
                            print(a[i], a[j], a[g], a[m], a[n])

arinc429_bnr_generator()