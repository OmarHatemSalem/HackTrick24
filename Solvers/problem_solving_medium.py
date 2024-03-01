import operator

# def generate_str(s: str, n: int) -> str:
#     return n*s

def solve_problem_solving_medium(input: str) -> str:
    """
    This function takes a string as input and returns a string as output.

    Parameters:
    input (str): A string representing the input data.

    Returns:
    str: A string representing the solution to the problem.
    """

    ans = ''
    stack = []

    amount = ''
    word = ''
    new = False
    for char in input:
        print(char, ": ", word, " ", amount)
        if char.isdigit() and not new:
            amount += char
        elif char.isdigit() and new:
            stack.append((word, int(amount)))              
           
            amount = char
            word = ''
            new = False
        elif char.isalpha():
            word += char
        elif char == '[':
            new = True
        elif char == ']':
            if amount != '' and word != '': 
                stack.append((word, int(amount)))              
            
                amount = ''
                word = ''
                new = False
                
            
            new = False
            top = stack.pop()
            ans = top[1] * (top[0] + ans)
        # print(f"ans = {ans}")




    return ''

if __name__ == "__main__":
    input_problem_solving_medium = '3[d1[e2[l]]]'

    print(solve_problem_solving_medium(input_problem_solving_medium))
