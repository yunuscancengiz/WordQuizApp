import random
from ..models import Words, Sentences, CorrectIncorrect


def get_random_word_and_sentences(db, user_id: int):
    wrong_words = db.query(Words).join(CorrectIncorrect).filter(
        Words.owner_id == user_id,
        CorrectIncorrect.owner_id == user_id,
        CorrectIncorrect.is_last_time_correct == False
    ).all()

    if wrong_words and random.random() < 0.7:
        selected_list = wrong_words
    else:
        selected_list = db.query(Words).filter(Words.owner_id == user_id).all()

    if not selected_list:
        return None, []

    random.shuffle(selected_list)
    word = selected_list[0]
    sentences = db.query(Sentences.sentence).filter(Sentences.word_id == word.id).all()
    sentence_list = [s[0] for s in sentences]

    return word.word, sentence_list