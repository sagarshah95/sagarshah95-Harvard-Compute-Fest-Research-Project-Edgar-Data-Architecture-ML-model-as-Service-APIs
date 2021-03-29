def sample_analyze_sentiment(text_content):
    """
    Analyzing Sentiment in a String
    Args:
      text_content The text content to analyze
    """
    # global df_sentimentScore
    global sentiment_score
    global sentiment_magnitude
    global sentence1
    global langue
    # print(text_content)
    client = language_v1.LanguageServiceClient()
    # text_content = 'I am so happy and joyful.'

    # Available types: PLAIN_TEXT, HTML
    type_ = language_v1.Document.Type.PLAIN_TEXT

    # Optional. If not specified, the language is automatically detected.
    # For list of supported languages:
    # https://cloud.google.com/natural-language/docs/languages
    language = "en"
    document = {"content": text_content, "type_": type_, "language": language}

    # Available values: NONE, UTF8, UTF16, UTF32
    encoding_type = language_v1.EncodingType.UTF8

    response = client.analyze_sentiment(request={'document': document, 'encoding_type': encoding_type})
    # Get overall sentiment of the input document
    # print(u"Document sentiment score: {}".format(response.document_sentiment.score))

    # Get sentiment for all sentences in the document

    for sentence in response.sentences:
        sent = (sentence.text.content)
        sn_score = (sentence.sentiment.score)
        # sn_magnitude = (sentence.sentiment.magnitude)
        # language1 = (response.language)
        sentence1.append(sent)
        sentiment_score.append(sn_score)
        # sentiment_magnitude.append(sn_magnitude)
        # langue.append(language1)
        # print(u"Sentence text: {}".format(sentence.text.content))

        # print(u"Sentence sentiment score: {}".format(sentence.sentiment.score))
        # print(u"Sentence sentiment magnitude: {}".format(sentence.sentiment.magnitude))

    # Get the language of the text, which will be the same as
    # the language specified in the request or, if not specified,
    # the automatically-detected language.
    # print(u"Language of the text: {}".format(response.language))


# [END language_sentiment_text]


def sentiment_main(passed_list):
    # import argparse

    # parser = argparse.ArgumentParser()
    # parser.add_argument("--text_content", type=str, default=["I am so happy and joyful.","Ifyou are bad I'm your dada"])
    # args = parser.parse_args()
    # label_list=["I am so happy and joyful.","Ifyou are bad I'm your dada","I am so happy and joyful.","Ifyou are bad I'm your dada"]
    # remove_stopwords()
    # processed_list=processed_list[0:5]
    for i in passed_list:
        # print(i)
        sample_analyze_sentiment(i)
        break


print('Google API Connection Established!!!')