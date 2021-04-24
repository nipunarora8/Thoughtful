from textblob import TextBlob

f=open("example.txt",'r')
data=f.read()

tb=TextBlob(data)

print("Overall sentiment is: ",tb.sentiment)

print("Line wise sentiment:-")
for sentence in tb.sentences:
    print(sentence,TextBlob(str(sentence)).sentiment)