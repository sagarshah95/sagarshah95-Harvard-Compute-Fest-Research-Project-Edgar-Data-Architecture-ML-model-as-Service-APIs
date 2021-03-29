def convert_files_to_sent_list():
    directory = r'/home/jayshil/PycharmProjects/EdgarPipeline/call_transcripts'
    #content_list=[]
    #temp_list=[]
    global content_list
    for filename in os.listdir(directory):
        temp_list= []
        #filepath='call_transcripts'+'/'+str(filename)
        filepath=r'/home/jayshil/PycharmProjects/EdgarPipeline/call_transcripts'+'/'+str(filename)
        #print(filepath)
        f = open(filepath, "r")
        content=f.read()
        #print(content)
        temp_list=content.split(".")
        #print(temp_list)
        content_list=content_list+temp_list
        f.close()
    #print(content_list)


def remove_emptyrecords():
    while '' in content_list:
        content_list.remove('')
    #print(content_list)



def remove_punctuation():
    for i in content_list:
        re.sub('[^A-Za-z0-9]+', '', i)
    #print(content_list)


def remove_stopwords():
    #preprocessed_list=[]
    for i in content_list:
        from collections import Counter
        global stop_words
        #stop_words = nltk.download('stopwords')
        stop_words = stopwords.words('english')
        stopwords_dict = Counter(stop_words)
        sent = ' '.join([word for word in i.split() if word not in stopwords_dict])
        preprocessed_list.append(sent)
    print(preprocessed_list)
    return preprocessed_list
    #print(stopwords_dict)


print('PreProcessing Data Done!!!!!!!')