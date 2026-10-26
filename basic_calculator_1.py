'''
224 Basic Calculator I
https://leetcode.com/problems/basic-calculator/description/

Given a string s representing a valid expression, implement a basic calculator to evaluate it, and return the result of the evaluation.

Note: You are not allowed to use any built-in function which evaluates strings as mathematical expressions, such as eval().


Example 1:

Input: s = "1 + 1"
Output: 2

Example 2:

Input: s = " 2-1 + 2 "
Output: 3

Example 3:

Input: s = "(1+(4+5+2)-3)+(6+8)"
Output: 23


Constraints:
1 <= s.length <= 3 * 105
s consists of integers and operators ('+', '-', '*', '/') separated by some number of spaces.
s represents a valid expression.
'+' is not used as a unary operation (i.e., "+1" and "+(2 + 3)" is invalid).
'-' could be used as a unary operation (i.e., "-1" and "-(2 + 3)" is valid).
There will be no two consecutive operators in the input.
Every number and running calculation will fit in a signed 32-bit integer.

1. Compute using stack (sub-optimal):
Similar to Basic Calculator 2 (LC 227) except that at each opening parenthesis '(', we make a recursive call to start a new calculator (hence, start a new local stack). At each closing parenthesis ')', we pop the elements of the local stack and sum them.
Time: O(N), Space: O(N)
https://youtu.be/cBZ7mu8_WXI?t=1598

2. Compute using tail (optimal):
Similar to Basic Calculator 2 (LC 227) except that at each opening parenthesis '(', we make a recursive call to start a new calculator (hence, start a new local stack). At each closing parenthesis ')', we pop the elements of the local stack and sum them.
Time: O(N), Space: O(N)

'''

def calculator_using_stack_1(s: str) -> int:
    ''' Time: O(N), Space: O(N) '''
    def dfs(s: str) -> int:
        nonlocal i
        if not s:
            return 0
        N = len(s)
        stack = []
        # stack maintains the value of sub-expressions
        num =  0
        last_operator = '+'
        while i < N:
            c = s[i]
            i += 1

            if c == ' ':
                continue

            if c.isdigit(): # digit
                num = num*10 + (ord(c) - ord('0'))
            elif c == '(':
                num = dfs(s) # '(' = start a new calculator
            elif c == ')':
                break

            if (not c.isdigit() and c != '('):
                # reset num to 0 if c is an operator
                # '(' is not an operator, it is a new calculator
                if last_operator == '+':
                    stack.append(num)
                elif last_operator == '-':
                    stack.append(-num)
                elif last_operator == '*':
                    x = stack.pop()
                    y = num
                    stack.append(x*y)
                elif last_operator == '/':
                    x = stack.pop()
                    y = num
                    stack.append(int(x/y))
                num = 0
                last_operator = c

        # process the last digit
        if last_operator == '+':
            stack.append(num)
        elif last_operator == '-':
            stack.append(-num)
        elif last_operator == '*':
            x = stack.pop()
            y = num
            stack.append(x*y)
        elif last_operator == '/':
            x = stack.pop()
            y = num
            stack.append(int(x/y))

        calc = 0
        while stack:
            calc += stack.pop()
        return calc

    if not s:
        return 0
    i = 0
    calc = dfs(s)
    return calc


def calculator_using_stack_2(s: str) -> int:
    ''' Same as the stack solution stack_1 except that we
            avoid the repeating the operator code block for processing
            the last digit. But it's easier to follow the stack_1
            solution
        Time: O(N), Space: O(N)
    '''
    def dfs(s: str) -> int:
        nonlocal i
        if not s:
            return 0
        N = len(s)
        stack = []
        # stack maintains the value of sub-expressions
        num =  0
        last_operator = '+'
        while i < N:
            c = s[i]
            i += 1
            if c.isdigit(): # digit
                num = num*10 + (ord(c) - ord('0'))
            elif c == '(':
                num = dfs(s) # '(' = start a new calculator

            if (not c.isdigit() and c != '(' and c != ' ') or i == N or c == ')':
                # reset num to 0 if c is an operator
                # '(' is not an operator
                if last_operator == '+':
                    stack.append(num)
                elif last_operator == '-':
                    stack.append(-num)
                elif last_operator == '*':
                    x = stack.pop()
                    y = num
                    stack.append(x*y)
                elif last_operator == '/':
                    x = stack.pop()
                    y = num
                    stack.append(int(x/y))
                num = 0
                last_operator = c

            if c == ')':
                break

        calc = 0
        while stack:
            calc += stack.pop()
        return calc

    if not s:
        return 0
    i = 0
    calc = dfs(s)
    return calc


def calculator_using_tail(s: str) -> int:
    ''' Time: O(N), Space: O(N) '''
    def dfs(s):
        nonlocal i
        if not s:
            return 0
        N = len(s)
        num, calc, tail = 0, 0, 0
        # calc maintains the value of the expression evaluated so far
        last_operator = '+'
        while i < N:
            c = s[i]
            i += 1
            if c.isdigit():
                num = num*10 + int(c)
            elif c == '(':
                num = dfs(s) # '(' = start a new calculator

            # Note we cannot use elif for the below condition because we want to process the last digit in both the above and below if-statements
            if (not c.isdigit() and c != ' ') or (i == N) or c == ')':
                if last_operator == '+':
                    calc = calc + num # new calc <-- prev calc + prev num
                    tail = +num
                elif last_operator == '-':
                    calc = calc - num
                    tail = -num
                elif last_operator == '*':
                    calc = calc - tail + tail*num
                    tail = tail*num
                elif last_operator == '/':
                    calc = calc - tail + int(tail/num)
                    tail = int(tail/num)
                num = 0
                last_operator = c

            if c == ')':
                return calc

        return calc

    if not s:
        return 0
    i = 0
    calc = dfs(s)
    return calc

def run_tests():
    tests = [("2 + 3 - (2+3 - (2+1))", 3),
             ("2 + 3 - (2+3 - (2+1)) - 4", -1),
             ("2 + 3 - (2+3 * ((2+1))) - 4", -10),
             ("(1+(4+5+2)-3)+(6+8)", 23),
             ("(1+(4+5+2)-3)*(6+8)", 126),
             (" 2-1 + 2 ", 3),
             (" (3+(5 / 2)) ", 5),
    ]
    for test in tests:
        expr, ans = test[0], test[1]
        print(f"\nExpression = {expr}")
        for method in ['stack_1', 'stack_2', 'tail']:
            if method == 'stack_1':
                result = calculator_using_stack_1(expr)
            elif method == 'stack_2':
                result = calculator_using_stack_2(expr)
            elif method == 'tail':
                result = calculator_using_tail(expr)
            print(f"Method {method}: result = {result}")
            passed = (ans == result)
            assert passed == True, f"Test case failed"
            print(f"Pass: {passed}")
    print(f"\nDONE")

run_tests()