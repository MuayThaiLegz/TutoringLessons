from classCal import Calculator

def assertCaltest():
    calculator = Calculator()
    assert calculator.add(2, 3) == 8, "Addition result is incorrect"
    assert calculator.subtract(5, 3) == 2, "Subtraction result is incorrect"

if __name__ == '__main__':
    assertCaltest()
    