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
    sentences = [s[0] for s in db.query(Sentences.sentence).filter(Sentences.word_id == word.id).all()]
    return word.word, sentences


def get_random_sentences(db, user_id):
    sentences = [s[0] for s in db.query(Sentences.sentence).filter(Sentences.owner_id == user_id).all()]
    random.shuffle(sentences)
    original_sentence = sentences[0]
    splitted_sentence = sentences[0].rstrip('.').split()
    random.shuffle(splitted_sentence)
    return original_sentence, splitted_sentence


def get_random_quiz_word_and_choices(db, user_id):
    all_words = db.query(Words).filter(Words.owner_id == user_id).all()
    if len(all_words) < 4:
        return None, []

    random.shuffle(all_words)
    correct_word = all_words[0]
    wrong_choices = [w.meaning for w in all_words[1:4]]

    choices = wrong_choices + [correct_word.meaning]
    random.shuffle(choices)
    return correct_word.word, choices

