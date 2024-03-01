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

    words, X = input
    freq = dict()
    for word in words:
        if not word in freq.keys():
            freq[word] = 1
        else:
            freq[word] += 1
    
    ans = list(freq.items())
    ans.sort(key=operator.itemgetter(1))

    return [x[0] for x in ans[-X:]]

if __name__ == "__main__":
    input_problem_solving_easy = (['nile', 'sphinx', 'pharaoh', 'pharaoh','pharaoh', 'sphinx','pyramid','pharaoh','sphinx','sphinx'], 2)

    print(solve_problem_solving_easy(input_problem_solving_easy))