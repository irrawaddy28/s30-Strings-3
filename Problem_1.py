'''
273 Integer to English words
https://leetcode.com/problems/integer-to-english-words/description/

Convert a non-negative integer num to its English words representation.

Example 1:
Input: num = 123
Output: "One Hundred Twenty Three"

Example 2:
Input: num = 12345
Output: "Twelve Thousand Three Hundred Forty Five"

Example 3:
Input: num = 1234567
Output: "One Million Two Hundred Thirty Four Thousand Five Hundred Sixty Seven"

Constraints:
0 <= num <= 2^31 - 1

Solution:
1. numberToWords1(): Split the number into 3-digit chunks from right to left and process each chunk separately. Eg 1,234,567 is split into  567, then 234, then 1.
Each chunk is converted into words using simple rules defined in a magic function. In the magic function, handle small numbers directly, combine tens and ones, or add “Hundred” if needed.
Then join the word parts with proper labels like "Thousand" or "Million", clean up spaces, and that's our final sentence.

https://youtu.be/Xh2vTslrnGw?t=3191

Time: O(1), Space: O(1) (since no. of digits in the number is finite)

2. numberToWords2(): This is similar to the Solution #1 except that we dont need to call the magic function recursively.

Time: O(1), Space: O(1)

'''
below_20 = ["", "One ", "Two ", "Three ", "Four ", "Five ", "Six ", "Seven ", "Eight ", "Nine ", "Ten ", "Eleven ", "Twelve ", "Thirteen ", "Fourteen ", "Fifteen ", "Sixteen ", "Seventeen ", "Eighteen ", "Nineteen "]

tens = ["", "Ten ", "Twenty ", "Thirty ", "Forty ", "Fifty ", "Sixty ", "Seventy ", "Eighty ", "Ninety "]

thousands = ["", "Thousand ", "Million ", "Billion "]
def numberToWords1(num):
    def magic(num):
        if num == 0:
            return ""
        elif num < 20:
            return below_20[num]
        elif num < 100:
            return tens[num//10] + below_20[num%10]
        else:
            return below_20[num//100] + "Hundred " + magic(num%100)

    if num == 0:
        return "Zero"
    result = ""
    i = 0
    while num > 0:
        if num % 1000 != 0:
            result = magic(num % 1000) + thousands[i] + result
        i += 1
        num = num // 1000
    return result.strip()

def numberToWords2(num):
    def magic(num):
        result = ""
        if num > 99:
            result += below_20[num // 100]
            result += "Hundred "
            num = num % 100

        if 20 <= num <= 99:
            result += tens[num // 10]
            num = num % 10

        result += below_20[num]
        return result

    if num == 0:
       return "Zero"
    result = ""
    i = 0
    while num != 0:
        r = num % 1000
        remainder_word = magic(r)
        if i > 0 and r != 0:
            remainder_word += thousands[i]
        result = remainder_word + result
        i += 1
        num = num // 1000

    result = result.strip()
    return result


def run_numberToWords():
    tests = [0, 8, 13, 25, 100, 123, 999, 1234, 12234, 25346, 100000, 120245, 154123, 4000000, 1000452, 1234567, 4154123, 123456789, 2123456789, 4000000000]
    for num in tests:
        print(f"\nnum = {num}")
        for method in [1,2]:
            if method == 1:
                words1 = numberToWords1(num)
                print(f"Method {method}: Number in Words = {words1}") # verify ans manually
            elif method == 2:
                words2 = numberToWords2(num)
                print(f"Method {method}: Number in Words = {words2}") # verify ans manually
        match = (words1 == words2)
        print(f"Match: {match}")
        if not match:
            return


run_numberToWords()