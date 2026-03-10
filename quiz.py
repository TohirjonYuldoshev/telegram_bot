from database import save_result

def finish_quiz(user_id, score):
    save_result(user_id, score)