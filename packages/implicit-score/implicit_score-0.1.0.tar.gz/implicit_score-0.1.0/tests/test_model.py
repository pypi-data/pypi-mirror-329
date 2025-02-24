import impscore  # Assuming `impscore` is your package name.


def test_infer_single():
    sentence = ["I have to leave now. Talk to you later.", "You must find a new place and move out by the end of this month."]
    model = impscore.load_model()
    imp_scores, prag_embs, sem_embs = model.infer_single(sentence)
    print(imp_scores)

def test_compare_two_sentences():
    """
    Test the helper method compare_two_sentences on two sample strings.
    """
    # If you want to test the class method directly, you might need to
    # access the global model. For example, do something like:
    model = impscore.load_model()

    sentence_batch = [
        ["I have to leave now. Talk to you later.", "I can't believe we've talked for so long."],
        ["You must find a new place and move out by the end of this month.",
         "Maybe exploring other housing options could benefit us both?"]
    ]

    s1 = ["I have to leave now. Talk to you later.", "You must find a new place and move out by the end of this month."]
    s2 = ["I can't believe we've talked for so long.", "Maybe exploring other housing options could benefit us both?"]
    print(s1)
    print(s2)
    imp_score1, imp_score2, prag_distance = model.infer_pairs(s1, s2)
    print(imp_score1, imp_score2, prag_distance)
