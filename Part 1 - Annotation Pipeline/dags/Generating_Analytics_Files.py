def analytics_csv():
    import os
    import pandas as pd
    bucket = 'edgarteam3processedfiles'  # already created on S3
    csv_buffer = StringIO()

    ACCESS_KEY = 'AKIA5CUSOFRV64J75U7W'
    SECRET_KEY = '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'
    directory = r'/home/jayshil/PycharmProjects/EdgarPipeline/call_transcripts'
    df = pd.DataFrame(columns = ['Company','Revenue','Percent','Comments'])
    c = []
    r = []
    p = []
    co = []
    for filename in os.listdir(directory):
        print(filename)
        temp_list= []
        filepath=r'/home/jayshil/PycharmProjects/EdgarPipeline/call_transcripts'+'/'+str(filename)
        #print(filepath)
        f = open(filepath, "r")
        try:
            #with open(r'C:\Users\jaysh\Downloads\sec-edgar\sec-edgar\call_transcripts\AGEN') as f:
            data = f.readlines()
            matching = [s for s in data if "Revenue" in s]
            m2 = [s for s in data if "(" in s]
            m1 = matching[0].split("Revenue",1)[1]
            company = matching[0].split("(",1)[1].split(")",1)[0]
            comments = matching[0].split(')',1)[1].split(' ',1)[1].split('\n',1)[0]
            #print('Revenue is '+ m1.split("$",1)[1].split(' ',1)[0])
            #print('YoY Percentage Change is '+ m1.split('(',1)[1].split(' ',1)[0])
            #print('Company Name '+m2[0].split("(",1)[1].split(")",1)[0])
            matching = [s for s in data if "(" in s]
            company = matching[0].split("(",1)[1].split(")",1)[0]
            revenue = m1.split("$",1)[1].split(' ',1)[0]
            percent = m1.split('(',1)[1].split(' ',1)[0]
            c.append(company)
            r.append(revenue)
            p.append(percent)
            co.append(comments)
            #print(df)
        except:
            print("Revenue and Percentage Change not given")
        f.close()
    df['Company'] = c
    df['Revenue'] = r
    df['Percent'] = p
    df['Comments'] = co
    df.to_csv('/home/jayshil/PycharmProjects/EdgarPipeline/Edgar_analytics_csv.csv')
    df.to_csv(csv_buffer)
    s3_resource = boto3.resource('s3', aws_access_key_id=ACCESS_KEY,
                                 aws_secret_access_key=SECRET_KEY)
    s3_resource.Object(bucket, 'Edgar_analytics_csv.csv').put(Body=csv_buffer.getvalue())

print('Analytics Files Generated!!!!')