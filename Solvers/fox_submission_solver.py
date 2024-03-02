import requests
import numpy as np
from LSBSteg import encode
from riddle_solvers import riddle_solvers
import random
import string
from PIL import Image

api_base_url = 'http://3.70.97.142:5000'
team_id='dMWFLvX'

def init_fox(team_id):
    '''
    In this fucntion you need to hit to the endpoint to start the game as a fox with your team id.
    If a sucessful response is returned, you will recive back the message that you can break into chunkcs
      and the carrier image that you will encode the chunk in it.
    
    return:
        Response:
        - msg (string): The secret message.
        - carrier_image (array): The carrier image to use, presented as a NumPy array.

    '''
    res = requests.post(api_base_url + '/fox/start', json={'teamId': team_id})

    return res.json()
  

def generate_message_array(message, image_carrier, fake_budget=0):  
    '''
    In this function you will need to create your own startegy. That includes:
        1. How you are going to split the real message into chunkcs
        2. Include any fake chunks
        3. Decide what 3 chuncks you will send in each turn in the 3 channels & what is their entities (F,R,E)
        4. Encode each chunck in the image carrier  
    '''
    # The message has a fixed length of 20 chars, divide it into 20 chunks
    real_messages = []
    # Encode the chunks in the carrier image
    for i in range(20):
        real_messages.append(encode(image_carrier, message[i]))

    # Generate the fake messages
    fake_messages = []
    no_fake_messages = min(fake_budget, 12)
    for i in range(no_fake_messages):
        fake_messages.append(''.join(random.choices(string.ascii_lowercase, k=20)))

    # Generate the message array along with the entities
    message_array = []
    entities = []

    i = 0
    for i in range(no_fake_messages):
        message_array.append([fake_messages[i], image_carrier, real_messages[i]])
        entities.append(['F', 'E', 'R'])
    
    while(i < 20):
        message_array.append([image_carrier, real_messages[i], image_carrier])
        entities.append(['E', 'R', 'E'])
        i += 1

    return message_array, entities

def get_riddle(team_id, riddle_id):
    '''
    In this function you will hit the api end point that requests the type of riddle you want to solve.
    use the riddle id to request the specific riddle.
    Note that: 
        1. Once you requested a riddle you cannot request it again per game. 
        2. Each riddle has a timeout if you didnot reply with your answer it will be considered as a wrong answer.
        3. You cannot request several riddles at a time, so requesting a new riddle without answering the old one
          will allow you to answer only the new riddle and you will have no access again to the old riddle. 
    
    return:
        Response:
        - test_case : A test case for the requested riddle - the format of which depends on the riddle as specified in the riddle details documented.

    '''
    res = requests.post(api_base_url + '/fox/get-riddle', json={'teamId': team_id, 'riddleId': riddle_id})
    return res.json()

def solve_riddle(team_id, solution):
    '''
    In this function you will solve the riddle that you have requested. 
    You will hit the API end point that submits your answer.
    Use te riddle_solvers.py to implement the logic of each riddle.

    return:
        Response:
        - budget_increase: The amount the budget has increased.
        - total_budget: The current total budget.
        - status: Indicating success or failure of the solution.
    '''
    res = requests.post(api_base_url + '/fox/solve-riddle', json={'teamId': team_id, 'solution': solution})
    return res.json()

def send_message(team_id, messages, message_entities=['F', 'E', 'R']):
    '''
    Use this function to call the api end point to send one chunk of the message. 
    You will need to send the message (images) in each of the 3 channels along with their entites.
    Refer to the API documentation to know more about what needs to be send in this api call. 

    return:
        Response:
        - status: success or failure of sending the message.
    '''
    res = requests.post(api_base_url + '/fox/send-message', json={'teamId': team_id, 'messages': messages, 'messageEntities': message_entities})
    return res.json()
   
def end_fox(team_id):
    '''
    Use this function to call the api end point of ending the fox game.
    Note that:
    1. Not calling this fucntion will cost you in the scoring function
    2. Calling it without sending all the real messages will also affect your scoring fucntion
      (Like failing to submit the entire message within the timelimit of the game).

    return:
        Response:
        - return text (string): Text indicating the score and whether it's a new high score.

    '''
    res = requests.post(api_base_url + '/fox/end-game', json={'teamId': team_id})
    return res

def submit_fox_attempt(team_id):
    '''
     Call this function to start playing as a fox. 
     You should submit with your own team id that was sent to you in the email.
     Remeber you have up to 15 Submissions as a Fox In phase1.
     In this function you should:
        1. Initialize the game as fox 
        2. Solve riddles 
        3. Make your own Strategy of sending the messages in the 3 channels
        4. Make your own Strategy of splitting the message into chunks
        5. Send the messages 
        6. End the Game
    Note that:
        1. You HAVE to start and end the game on your own. The time between the starting and ending the game is taken into the scoring function
        2. You can send in the 3 channels any combination of F(Fake),R(Real),E(Empty) under the conditions that
            2.a. At most one real message is sent
            2.b. You cannot send 3 E(Empty) messages, there should be atleast R(Real)/F(Fake)
        3. Refer To the documentation to know more about the API handling 
    '''

  #   Start the game as a fox
    response = init_fox(team_id)
    print("Init fox response: ", response)

    msg = response['msg']
    carrier_image = response['carrier_image']

    carrier_image = np.array(carrier_image)

    fake_budget = 0

    # # Get the riddle
    # riddle_res = get_riddle(team_id, 'problem_solving_easy')
    # print("Riddle response (easy): ", riddle_res)
    # test_case = riddle_res['test_case']

    # # Solve the riddle
    # solution = riddle_solvers['problem_solving_easy'](test_case)
    # solution_res = solve_riddle(team_id, str(solution))
    # print("Testcase Solution: ", solution)
    # print("Solution response: ", solution_res)
    # if solution_res['status'] == 'success':
    #     fake_budget = solution_res['total_budget']

    # print("Fake budget: ", fake_budget)
    # Get the riddle
    riddle_res = get_riddle(team_id, 'problem_solving_medium')
    test_case = riddle_res['test_case']

    print("Riddle response(medium): ", riddle_res)
    # Solve the riddle
    solution = riddle_solvers['problem_solving_medium'](test_case)
    solution_res = solve_riddle(team_id, str(solution))

    print("Testcase Solution: ", solution)
    print("Solution response: ", solution_res)

    if solution_res['status'] == 'success':
        fake_budget = solution_res['total_budget']

    print("Fake budget: ", fake_budget)

    # # Get the riddle
    # riddle_res = get_riddle(team_id, 'problem_solving_hard')
    # test_case = riddle_res['test_case']

    # print("Riddle response(hard): ", riddle_res)

    # # Solve the riddle
    # solution = riddle_solvers['problem_solving_hard'](test_case)
    # solution_res = solve_riddle(team_id, str(solution))

    # print("Testcase Solution: ", solution)
    # print("Solution response: ", solution_res)

    # if solution_res['status'] == 'success':
    #     fake_budget = solution_res['total_budget']

    # print("Fake budget: ", fake_budget)

    # Get the message array
    message_array, entities = generate_message_array(msg, carrier_image, fake_budget)

    # Send the messages
    for i in range(0, len(message_array)):
        print(message_array[i], entities[i])

    # End the game
    end_res = end_fox(team_id)
    print("End response: ", end_res)



submit_fox_attempt(team_id)