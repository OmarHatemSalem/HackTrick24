import operator

def solve_problem_solving_easy(input: tuple) -> list:
    """
    This function takes a tuple as input and returns a list as output.

    Parameters:
    input (tuple): A tuple containing two elements:
        - A list of strings representing a question.
        - An integer representing a key.

    Returns:
    list: A list of strings representing the solution to the problem.
    """

    words, n = input
    freq = {}
    for word in words:
        if word not in freq:
            freq[word] = 0
        freq[word] -= 1
    l = []
    for key, val in freq.items():
        l.append((val, key))
    l.sort()
    ans = [word for _, word in l[:n]]
    return ans

if __name__ == "__main__":
    input_problem_solving_easy = (['nile', 'sphinx', 'pharaoh', 'pharaoh','pharaoh', 'sphinx','pyramid','pharaoh','sphinx','sphinx'], 3)

    print(solve_problem_solving_easy(input_problem_solving_easy))