import requests

team_id='dMWFLvX'

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


message = 'Keep moving forward.'
print(len(message))
   
chunk1 = message[:7]
chunk2 = message[7:14]
chunk3 = message[14:]

print(len(chunk1))
print(chunk1)

print(len(chunk2))
print(chunk2)

print(len(chunk3))
print(chunk3)

