'''
227 Basic Calculator II
https://leetcode.com/problems/basic-calculator-ii/description/

Given a string s which represents an expression, evaluate this expression and return its value. The integer division should truncate toward zero.

You may assume that the given expression is always valid. All intermediate results will be in the range of [-2^31, 2^31 - 1].

Note: You are not allowed to use any built-in function which evaluates strings as mathematical expressions, such as eval().

Example 1:
Input: s = "3+2*2"
Output: 7

Example 2:
Input: s = " 3/2 "
Output: 1

Example 3:
Input: s = " 3+5 / 2 "
Output: 5


Constraints:
1 <= s.length <= 3 * 105
s consists of integers and operators ('+', '-', '*', '/') separated by some number of spaces.
s represents a valid expression.
All the integers in the expression are non-negative integers in the range [0, 231 - 1].
The answer is guaranteed to fit in a 32-bit integer.

1. Compute using stack (sub-optimal):
The key idea is that we maintain the value of individual sub-expressions inside a stack instead of evaluating the expression so far (start to current).
Example:
s="3+2*2", result of sub-expressions = [3, 2*2]
s='32-4/2*5', result of sub-expressions = [32, -10]
s='32-4*8/2', result of sub-expressions = [32, -16]
s='32-4*8/2-6', result of sub-expressions = [32, -16, -6]

Step 1: Reading the string left to right and forming numbers digit by digit.
Step 2: Every time we hit an operator (or if we reach the end of string), we apply the last recorded operation using a stack and evaluate the sub-expression
Operator    Operation
+           push(+num)
-           push(-num)
*           push(pop*num)
*           push(pop/num)
Step 3: Then, when we are done with scanning the entire expression, we simply add the values of the individual sub-expressions by popping from the stack.

Example: Input s = "32 - 4*80/2"

Step 1: Pre-loop
i	c	num	op	stack  Remark
-   —	0	+	[]	   Init

Step 2: Loop
i	c	num	op	stack  Remark
0   3	3	+	[]	   Building num
1   2	32	+	[]	   Building num
2   -	0	-	[32]   op = + -> push = +1*num = 32, update: op=-, num=0
3   4	4	-	[32]   Building num
4   *	0	*	[32, -4] op = -, push = -1*num = -4, update: op=*, num=0
5	8	8	*	[32, -4] Building num
6	0	80	*	[32, -4] Building num
7	/	0	/	[32, -320] op=*, pop -4, push = pop*num = -320, update: op=/, num=0
8	2	2	/	[32, -320]	Building num (Loop ends)

Step 3: Post-Loop
—	2	2  /	[32, -160.0] op=., pop -160, push = pop/num = -320/2 = -160.0
-   -   -   -   -128         pop all values from stack and add

Time: O(N), Space: O(N)
https://youtu.be/Xh2vTslrnGw?t=2138

2. Compute using tail (optimal):
The key idea is that we maintain the value of the expression evaluated so far (start to current).
s="3+2*2", result = 3 (3) -> 5 (3+2) -> 7 (3+2*2)
s='32-4/2*5', result = 32 (32, tail=0) -> 28 (32-4, tail=-4) -> 30 (32-4/2, tail=-2) -> 22 (32-4/2*5, tail=-10)
s='32-4*8/2', result = 32 (32, tail=0) -> 28 (32-4, tail=-4) -> 0 (32-4*8, tail=--32) -> 16 (32-4*8/2, tail=-16)
Step 1: Reading the string left to right and forming numbers digit by digit.
Step 2: When we hit an operator, we apply the previous sign and adjust the *result obtained so far* based on precedence using a tail tracker. This lets us handle * and / immediately without a stack, by reversing the last number and applying the new operation.
operator        calc                            tail
+               prev calc + num                 +num
-               prev calc - num                 -num
*               prev calc - tail + tail*num     tail*num
/               prev calc - tail + tail/num     tail/num

https://youtu.be/Xh2vTslrnGw?t=189
Time: O(N), Space: O(1)

'''

def calculator_using_stack_1(s: str) -> int:
    ''' Time: O(N), Space: O(N) '''
    if not s:
        return 0
    N = len(s)
    stack = []
    # stack maintains the value of sub-expressions
    num =  0
    last_operator = '+'
    for i in range(N):
        c = s[i]
        if c == ' ':
            continue
        elif c.isdigit(): # digit
            num = num*10 + (ord(c) - ord('0'))
        else: # operator (reset num to 0 if c is an operator)
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

def calculator_using_stack_2(s: str) -> int:
    ''' Same as the stack solution stack_1 except that we
        avoid the repeating the operator code block for processing
        the last digit. But it's easier to follow the stack_1
        solution
        Time: O(N), Space: O(N)
    '''
    if not s:
        return 0
    N = len(s)
    stack = []
    # stack maintains the value of sub-expressions
    num, calc = 0, 0
    last_operator = '+'
    for i in range(N):
        c = s[i]
        if c.isdigit():
            num = num*10 + int(c)
        # Note we cannot use elif for the below condition because we want to process the last digit in both the above and below if-statements
        if (not c.isdigit() and c != ' ') or (i == N-1):
            # Why i == N-1? To process the last digit
            if last_operator == '+':
                stack.append(num)
            elif last_operator == '-':
                stack.append(-num)
            elif last_operator == '*':
                stack.append(stack.pop()*num)
            elif last_operator == '/':
                stack.append(int(stack.pop()/num))
            num = 0
            last_operator = c

    calc = 0
    while stack:
        calc = calc + stack.pop()
    return calc

def calculator_using_tail(s: str) -> int:
    ''' Time: O(N), Space: O(1) '''
    if not s:
        return 0
    N = len(s)
    num, calc, tail = 0, 0, 0
    # calc maintains the value of the expression evaluated so far
    last_operator = '+'
    for i in range(N):
        c = s[i]
        if c.isdigit():
            num = num*10 + int(c)
        # Note we cannot use elif for the below condition because we want to process the last digit in both the above and below if-statements
        if (not c.isdigit() and c != ' ') or (i == N-1):
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
        #print(f"num = {num}, last_operator = {last_operator}, calc = {calc}, tail = {tail}")
    return calc


def run_tests():
    tests = [("3+2*2", 7),
             ('32-4*80/2', -128), # back-to-back * and /
             (" 3+5 / 2 ", 5), # space handling
             ("14-3/2", 13), # divison of -ve numbers resuling in floats
             ('32-4/2*5', 22),
             ('32-4*8/2', 16),
             ('32-4*8/2-6', 10),
             ('32-4*8/2-6 ', 10),
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