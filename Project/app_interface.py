import torch
import torch.nn as nn
from transformers import get_linear_schedule_with_warmup
import pygame
from tkinter import *
from transformers import AutoModel
from torch.utils.data import Dataset, DataLoader
from transformers import AutoModel, AutoTokenizer
import numpy as np
import pandas as pd
from time import sleep
phobert = AutoModel.from_pretrained("vinai/phobert-base-v2")
class CommentDataset(Dataset):
    def __init__(self, df, tokenizer, max_len=30):
        self.df = df
        self.max_len = max_len
        self.tokenizer = tokenizer

    def __len__(self):
        return len(self.df)

    def __getitem__(self, index):
        row = self.df.iloc[index]
        text, label = self.get_input_data(row)
        encoding = self.tokenizer.encode_plus(
            text,
            truncation=True,
            add_special_tokens=True,
            max_length=self.max_len,
            padding='max_length',
            return_attention_mask=True,
            return_token_type_ids=False,
            return_tensors='pt',
        )

        return {
            'text': text,
            'input_ids': encoding['input_ids'].flatten(),
            'attention_masks': encoding['attention_mask'].flatten(),
            'targets': torch.tensor(label, dtype=torch.long),
        }

    def get_input_data(self, row):
        text = row['Comment']
        label = row['Label']
        return text, label
class CommentClassifier(nn.Module):
    def __init__(self, n_classes):
        super(CommentClassifier, self).__init__()
        self.bert = phobert#AutoModel.from_pretrained("vinai/phobert-base")
        self.drop = nn.Dropout(p=0.3)
        self.fc = nn.Linear(self.bert.config.hidden_size, n_classes)
        nn.init.normal_(self.fc.weight, std=0.02)
        nn.init.normal_(self.fc.bias, 0)

    def forward(self, input_ids, attention_mask):
        last_hidden_state, output = self.bert(
            input_ids=input_ids,
            attention_mask=attention_mask,
            return_dict=False # Dropout will errors if without this
        )

        x = self.drop(output)
        x = self.fc(x)
        return x
tokenizer = AutoTokenizer.from_pretrained("vinai/phobert-base-v2")
model = CommentClassifier(n_classes = 3)
model.load_state_dict(torch.load('./phobert.pth'))
model.eval()
def RemoveStopwords(data):
    data_check = []
    link_vn_stopword = './/vietnamese-stopwords.txt'
    stop_words = set(line.strip() for line in open(link_vn_stopword, encoding="utf8"))
    sen_new = ""
    sen_temp = data.split()
    for word in sen_temp:
        if (word not in stop_words):
            sen_new += word + " "
    return sen_new

def punctuation_removal(data):
    character = ['\'','.',',','-',':','"','!','~','?',']','*']
    character = set(character)
    new_ = ""
    for i in data:
        if i not in character:
            new_ += i
    return new_
def Predict(text):
    text = RemoveStopwords(text)
    text = punctuation_removal(text)
    d = {
        'index' : ["0"],
        'Id' : [1],
        'Label' : [2],
        'Comment' : [text]
    }
    df = []
    df.append(d)
    df = pd.DataFrame(d)
    te_ = CommentDataset(df, tokenizer, max_len = 30)
    te_1 = DataLoader(te_, batch_size=1)

    with torch.no_grad():
        data_loader = te_1
        for dat in data_loader:
            input_ids = dat['input_ids']
            attention_mask = dat['attention_masks']
            outputs = model(
                input_ids=input_ids,
                attention_mask=attention_mask
            )
            _, pred = torch.max(outputs, dim=1)
            sup = pred[0]
    return sup
def CreateResultWindow():
    text_to_check = inputText.get("1.0",END)
    ns = "Wrong"
    a = Predict(text_to_check)
    if (a == 2):
        ans = "Very Toxic"
    elif(a == 1):
        ans = "Toxic"
    else:
        ans = "Non-Toxic"
    result = Tk()
    result.geometry('300x100+200+100')
    result.title("Result!!")
    Label(result, text=ans).pack(ipadx=10, ipady=10)
    Label(result, text='Thanks for using!!!', justify=CENTER).pack(ipadx=10, ipady=10)
    inputText.delete('1.0', END)
    
    app.mainloop()

app = Tk()
app.title("IS THIS COMMENT TOXIC")
app.geometry('640x480+100+100')
instruction = "1.Write the text you want to check\n2.Press the \"check\" button\n3.Wait a minute "
label = Label(app, text = instruction, justify=LEFT).pack(ipadx=10, ipady=10)

inputText = Text(app)
inputText.place(x=10, y=115, height=30,width=200)
inputText.pack()
Button(app, text='Check', command=CreateResultWindow).pack()
app.mainloop()