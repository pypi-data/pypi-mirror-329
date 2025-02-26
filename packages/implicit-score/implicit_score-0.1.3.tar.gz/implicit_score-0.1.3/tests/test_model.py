import impscore  # Assuming `impscore` is your package name.


def test_infer_single():
    sentence = ["I have to leave now. Talk to you later.", "I can't believe we've talked for so long."]
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

    sentence_pairs = [
        ["I have to leave now. Talk to you later.", "I can't believe we've talked for so long."],
        ["You must find a new place and move out by the end of this month.",
         "Maybe exploring other housing options could benefit us both?"]
    ]

    s1_list = [pair[0] for pair in sentence_pairs]
    s2_list = [pair[1] for pair in sentence_pairs]

    imp_score1, imp_score2, prag_distance = model.infer_pairs(s1_list, s2_list)
    print(imp_score1, imp_score2, prag_distance)
