import requests
import numpy as np
from LSBSteg import encode
from riddle_solvers import riddle_solvers
import random
import string
from PIL import Image
from transformers import pipeline

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
        - carrier_image (list): The carrier image to use, convert it to numpy array.

    '''
    res = requests.post(api_base_url + '/fox/start', json={'teamId': team_id})

    return res.json()
  

def generate_message_array(message, image_carrier):  
    '''
    In this function you will need to create your own startegy. That includes:
        1. How you are going to split the real message into chunkcs
        2. Include any fake chunks
        3. Decide what 3 chuncks you will send in each turn in the 3 channels & what is their entities (F,R,E)
        4. Encode each chunck in the image carrier  
    '''
    message_array = []
    entities = []

    chunk1 = message[:7]
    chunk2 = message[7:14]
    chunk3 = message[14:]
    # Encode the real message
    encoded_real1 = encode(image_carrier, chunk1)
    encoded_real1_list = encoded_real1.tolist()

    encoded_real2 = encode(image_carrier, chunk2)
    encoded_real2_list = encoded_real2.tolist()

    encoded_real3 = encode(image_carrier, chunk3)
    encoded_real3_list = encoded_real3.tolist()

    # Encode an empty message
    encoded_empty1 = encode(image_carrier, "")
    encoded_empty1_list = encoded_empty1.tolist()


    # Generate the message array
    message_array.append([encoded_real1_list, encoded_empty1_list, encoded_empty1_list])
    entities.append(['R', 'F', 'F'])

    message_array.append([encoded_real2_list, encoded_empty1_list, encoded_empty1_list])
    entities.append(['R', 'F', 'F'])

    message_array.append([encoded_real3_list, encoded_empty1_list, encoded_empty1_list])
    entities.append(['R', 'F', 'F'])
    


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
    res = requests.post(api_base_url + '/fox/send-message', json={'teamId': team_id, 'messages': messages, 'message_entities': message_entities})
    return res.json()

def get_remaining_attempts(team_id):
    '''
    Use this function to call the api end point to get the remaining attempts for the fox and eagle.
    You can use this function to know how many attempts you have left.

    return:
        Response:
        - remaining_attempts: The number of attempts remaining.
    '''
    res = requests.post('http://13.53.169.72:5000/attempts/student', json={'teamId': team_id})
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
    # vqa_pipeline = pipeline("visual-question-answering")
    fake_budget = 0

  #   Start the game as a fox
    response = init_fox(team_id)

    msg = response['msg']
    carrier_image = response['carrier_image']

    carrier_image = np.array(carrier_image)

    # Problem Solving Easy Riddle

    riddle_res = get_riddle(team_id, 'problem_solving_easy')
    test_case = riddle_res['test_case']
    solution = riddle_solvers['problem_solving_easy'](test_case)
    solution_res = solve_riddle(team_id, solution)

    # Problem Solving Medium Riddle
   
    riddle_res = get_riddle(team_id, 'problem_solving_medium')
    test_case = riddle_res['test_case']
    solution = riddle_solvers['problem_solving_medium'](test_case)
    solution_res = solve_riddle(team_id, solution)

    # Problem Solving Hard Riddle

    riddle_res = get_riddle(team_id, 'problem_solving_hard')
    test_case = riddle_res['test_case']
    solution = riddle_solvers['problem_solving_hard'](test_case)
    solution_res = solve_riddle(team_id, solution)

    # Computer Vision Easy Riddle

    # riddle_res = get_riddle(team_id, 'cv_easy')
    # test_case = riddle_res['test_case']
    # try:
    #     solution = riddle_solvers['cv_easy'](test_case)
    #     solution_res = solve_riddle(team_id, solution)
    # except:
    #     print("cv_easy failed")

    # Computer Vision Hard Riddle

    # riddle_res = get_riddle(team_id, 'cv_hard')
    # test_case = riddle_res['test_case']
    # try:
    #     extracted_question, image = test_case
    #     image = np.asarray(image, dtype=np.uint8)
    #     image = Image.fromarray(image)
    #     ans = vqa_pipeline(image, extracted_question, top_k=1)
    #     solution = int(ans[0]['answer'])
    #     solution_res = solve_riddle(team_id, solution)
    #     print("Went to the model successfully")
    # except:
    #     solution_res = solve_riddle(team_id, 2)
    #     print("cv_hard failed")

    # if solution_res['status'] == 'success':
    #     print("CV Hard Riddle Solved Successfully")

    # sec Medium Riddle
    # riddle_res = get_riddle(team_id, 'sec_medium_stegano')
    # test_case = riddle_res['test_case']
    # try:
    #     image = np.asarray(test_case, dtype=np.uint8)
    #     solution = riddle_solvers['sec_medium_stegano'](image)
    #     solution_res = solve_riddle(team_id, solution)
    #     print("Sec Medium Riddle Entered Try Block")
    # except:
    #     print("Sec Medium Riddle Failed")
    

    


    # Sec Hard Riddle

    riddle_res = get_riddle(team_id, 'sec_hard')
    test_case = riddle_res['test_case']
    solution = riddle_solvers['sec_hard'](test_case)
    solution_res = solve_riddle(team_id, solution)


    fake_budget = solution_res['total_budget']

    print("Fake budget: ", fake_budget)


    # Get the message array
    message_array, entities = generate_message_array(msg, carrier_image)

    # Send the messages
    # send_message(team_id, message_array[0], entities[0])

    for i in range(0, len(message_array)):
        message = message_array[i]
        entity = entities[i]

        send_res = send_message(team_id, message, entity)

    # End the game
    end_res = end_fox(team_id)
    # print("End response: ", end_res)

    print("End Response Body: ", end_res.text)

     # Get the remaining attempts
    # attempts_res = get_remaining_attempts(team_id)
    # print("Attempts response: ", attempts_res)



submit_fox_attempt(team_id)