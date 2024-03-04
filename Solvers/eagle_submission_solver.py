import numpy as np
from LSBSteg import decode
import requests

api_base_url = 'http://3.70.97.142:5000'
team_id='dMWFLvX'


def init_eagle(team_id):
    '''
    In this fucntion you need to hit to the endpoint to start the game as an eagle with your team id.
    If a sucessful response is returned, you will recive back the first footprints.

    return:
        Response:
        - footprints:  An array of three footprints represented as NumPy spectrograms.Each spectrogram is received as a list that
        should later be converted to a NumPy array using np.array().

    '''
    res = requests.post(api_base_url + '/eagle/start', json={'teamId': team_id})

    return res.json()

def select_channel(footprint):
    '''
    According to the footprint you recieved (one footprint per channel)
    you need to decide if you want to listen to any of the 3 channels or just skip this message.
    Your goal is to try to catch all the real messages and skip the fake and the empty ones.
    Refer to the documentation of the Footprints to know more what the footprints represent to guide you in your approach.       
    '''
    pass
  
def skip_msg(team_id):
    '''
    If you decide to NOT listen to ANY of the 3 channels then you need to hit the end point skipping the message.
    If sucessful request to the end point , you will expect to have back new footprints IF ANY.

    return:
        Response:
        - nextFootprint : The next chunk's footprints - an array of three footprints represented as NumPy spectrograms. 
        Each spectrogram is received as a list that should later be converted to a NumPy array using np.array(). 
        If the end of the message is reached, you will be notified that no more footprints exist and you should then end game.

        Example Response:
        If there exsist more footprints:
        {
        ”nextFootprint”:{”1”: spectrogram1, ”2”:spectrogram2, ”3”:spectrogram3 }
        }
        If no more footprint exist:
        ”End of message reached”

    '''
    res = requests.post(api_base_url + '/eagle/skip-message', json={'teamId': team_id})

    return res


    
  
def request_msg(team_id, channel_id):
    '''
    If you decide to listen to any of the 3 channels then you need to hit the end point of selecting a channel to hear on (1,2 or 3)

    return:
        Response:
        encodedMsg (numpy array): The requested message from the specified channel,
        in the form of a numpy array.
    '''
    res = requests.post(api_base_url + '/eagle/request-message', json={'teamId': team_id, 'channelId': channel_id})

    return res.json()

def submit_msg(team_id, decoded_msg):
    '''
    In this function you are expected to:
        1. Decode the message you requested previously
        2. call the api end point to send your decoded message  
    If sucessful request to the end point , you will expect to have back new footprints IF ANY.
    '''
    res = requests.post(api_base_url + '/eagle/submit-message', json={'teamId': team_id, 'decodedMsg': decoded_msg})

    return res
  
def end_eagle(team_id):
    '''
    Use this function to call the api end point of ending the eagle  game.
    Note that:
    1. Not calling this fucntion will cost you in the scoring function
    '''
    res = requests.post(api_base_url + '/eagle/end-game', json={'teamId': team_id})

    return res.text

def submit_eagle_attempt(team_id):
    '''
     Call this function to start playing as an eagle. 
     You should submit with your own team id that was sent to you in the email.
     Remeber you have up to 15 Submissions as an Eagle In phase1.
     In this function you should:
        1. Initialize the game as fox 
        2. Solve the footprints to know which channel to listen on if any.
        3. Select a channel to hear on OR send skip request.
        4. Submit your answer in case you listened on any channel
        5. End the Game
    '''
    pass


submit_eagle_attempt(team_id)
