# -*- coding: utf-8 -*-
"""BertBaisDetection.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1688kVH_LlZyoesYBMdYDS3oBQ1HSdEQR
"""
# Libraries
from audioop import bias
import os
import csv
import os.path
import json
import torch
import torch.nn as nn
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from transformers import BertModel, BertTokenizer, AdamW, get_linear_schedule_with_warmup
from torch.optim import lr_scheduler
import sys

import logging
logging.basicConfig(level=logging.ERROR)

import warnings
warnings.filterwarnings("ignore")

# Libraries and retreiving data
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

class Tokenize_dataset:
  """
  This class tokenizes the dataset using bert tokenizer
  """

  def __init__(self, text, targets, tokenizer, max_len):
    self.text = text
    self.tokenizer = tokenizer
    self.max_len = max_len
    self.targets = targets

  def __len__(self):
    return len(self.targets)

  def __getitem__(self, item):
    text = str(self.text[item])
    targets = self.targets[item]
    """
    Using encode_plus instead of encode as it helps to provide additional information that we need
    """
    inputs = self.tokenizer.encode_plus(
        str(text),
        add_special_tokens = True,
        max_length = self.max_len,
        pad_to_max_length = True
    )

    ids = inputs["input_ids"]
    mask = inputs["attention_mask"]
    token_type_ids = inputs["token_type_ids"]

    return {
        "ids": torch.tensor(ids, dtype=torch.long),
        "mask": torch.tensor(mask, dtype=torch.long),
        "token_type_ids": torch.tensor(token_type_ids, dtype=torch.long),
        "targets": torch.tensor(targets, dtype=torch.long)
    }

def loss_function(outputs, targets):
	"""
	This function defines the loss function we use in the model which since is multiclass is crossentropy
	"""
	return nn.CrossEntropyLoss()(outputs, targets)

def train_function(data_loader, model, optimizer, device):
  """
  Function defines the training that we will happen over the entire dataset
  """
  model.train()

  running_loss = 0.0
  """
  looping over the entire training dataset
  """
  for i, data in enumerate(data_loader):
    mask = data["mask"].to(device, dtype=torch.long)
    ids = data["ids"].to(device, dtype=torch.long)
    token_type_ids = data["token_type_ids"].to(device, dtype=torch.long)
    target = data["targets"].to(device, dtype=torch.long)
    optimizer.zero_grad()

    output = model(ids=ids, mask=mask, token_type_ids=token_type_ids)
    
    loss = loss_function(output, target)
    loss.backward()
    optimizer.step()
    """
    calculating loss and running loss
    """
    running_loss += loss.item()
    if i % 10 == 0 and i!=0:
      temp = f'Batch index = {i}\tRunning Loss = {running_loss/10}'
      print(temp)
      running_loss = 0.0

def eval_function(data_loader, model, device):
  """
  This function defines the loop over the dev set.
  """
  model.eval()
  correct_labels = 0
  tot = 0
  """
  no_grad as this is evaluation set and we dont want the model to update weights
  """
  with torch.no_grad():
    for i, data in enumerate(data_loader):
      mask = data["mask"].to(device, dtype=torch.long)
      ids = data["ids"].to(device, dtype=torch.long)
      token_type_ids = data["token_type_ids"].to(device, dtype=torch.long)
      targets = data["targets"].to(device, dtype=torch.long)
      outputs = model(ids=ids, mask=mask, token_type_ids=token_type_ids)

      max_probs, predicted = torch.max(outputs, 1)
      tot = tot + targets.size(0)
      correct_labels = correct_labels + torch.sum(predicted==targets)

      print(f"Batch Index: {i}\tPredicted: {predicted}\tTargets: {targets}")
    """
    basic metrics for accuracy calculation
    """
    accuracy = correct_labels / tot * 100
    print(accuracy)
  return accuracy

class CompleteModel(nn.Module):
  """
  The model architecture is defined here which is a fully connected layer + normalization on top of a BERT model
  """

  def __init__(self, bert):
    super(CompleteModel, self).__init__()
    self.bert = BertModel.from_pretrained(bert)
    self.drop = nn.Dropout(p=0.25)
    self.out = nn.Linear(self.bert.config.hidden_size, 2) # Number of output classes = 3, positive, negative and N(none)

  def forward(self, ids, mask, token_type_ids):
    _, pooled_output = self.bert(ids, attention_mask=mask, token_type_ids=token_type_ids, return_dict=False)
    output = self.drop(pooled_output)
    return self.out(output)

# def run():
#   training_set_path = os.path.join(currentDirPath, "SyllabiTrainData.csv")
#     #validation_set_path = '/content/drive/ColabNotebooks/dataset/dev/' + str(location) + '_' + str(aspect) + '.csv'
#   df_train = pd.read_csv(training_set_path)
#     #df_valid = pd.read_csv(validation_set_path)
      
#   df_train['target'] = df_train['target']
#    # df_valid['target'] = df_valid['target'].map(sentiment_mapping)
#   df_train = df_train.reset_index(drop=True)
#    # df_valid = df_valid.reset_index(drop=True)
#   tokenizer = BertTokenizer.from_pretrained(bert_model)
#   train_dataset = Tokenize_dataset(
#         text = df_train['text'].values,
#         targets = df_train['target'].values,
#         tokenizer = tokenizer,
#         max_len = train_maxlen
#   )
#   class_counts = []
#   for i in range(3):
#     class_counts.append(df_train[df_train['target']==i].shape[0])
#   print(f"Class Counts: {class_counts}")
      
#   num_samples = sum(class_counts)
#   print(num_samples)
#   labels = df_train['target'].values
#   class_weights = []
#   for i in range(len(class_counts)):
#       if class_counts[i] != 0:
#           class_weights.append(num_samples/class_counts[i])
#       else:
#           class_weights.append(0)
#   weights = [class_weights[labels[i]] for i in range(int(num_samples))]
#   sampler = torch.utils.data.sampler.WeightedRandomSampler(torch.DoubleTensor(weights), int(num_samples))
#   train_data_loader = torch.utils.data.DataLoader(
#         train_dataset,
#         batch_size = batch_size,
#         shuffle = False,
#         sampler = sampler
#     )
#   #valid_dataset = Tokenize_dataset(
#     #    text = df_valid['text'].values,
#      #   targets = df_valid['sentiment'].values,
#     #   tokenizer = tokenizer,
#      #   max_len = dev_maxlen
#    # )
#    # valid_data_loader = torch.utils.data.DataLoader(
#     #    valid_dataset,
#      #   batch_size = batch_size,
#    #     shuffle = False
# #    )
#   device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
#   print(f"Device: {device}")
#   model = CompleteModel(bert_model).to(device)
#   optimizer = AdamW(model.parameters(), lr=learning_rate)
#   scheduler = lr_scheduler.StepLR(
#         optimizer,
#         step_size = 1,
#         gamma = 0.8
#     )
#   for epoch in range(epochs):
#     train_function(data_loader=train_data_loader, model=model, optimizer=optimizer, device=device)
#         #accuracy = eval_function(data_loader=valid_data_loader, model=model, device=device, location=location, aspect=aspect)
#   print("\nEpoch = "+ str(epoch))
#   print("\nLearning Rate = " + str(scheduler.get_lr()[0])+"\n")
#   scheduler.step()
#   torch.save(model, currentDirPath + '/'+ str(epoch) + '.bin')
  
# if __name__ == "__main__":
#   run()

# Test
def GeneralBertBiasDetection(currentDirPath):
  readData = os.path.join(currentDirPath, "SvmAndBERT/inputTestSyllabi/inputSyllabi.csv")
  data = pd.read_csv(readData)


  # The max sentence length used for fine-tuning model using dataset.
  train_maxlen = 140
  dev_maxlen = 140
  # The number of examples for training in one iteration
  batch_size = 16
  epochs = 10
  bert_model = 'bert-base-uncased'
  # Determine the step size at each iteration
  learning_rate = 3e-5
  MAX_LEN = 140

  tokenizer = BertTokenizer.from_pretrained(bert_model)
  device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

  df = pd.read_csv(readData)
  result = []
  idees = []
  model = torch.load(currentDirPath + "/SvmAndBERT/BERT/9.bin")
  for i in range(len(df)):
    id_test = df.loc[i, 'id']
    text = df.loc[i,'text']


    inputs = tokenizer.encode_plus(
            str(text),
            add_special_tokens = True,
            max_length = MAX_LEN,
            pad_to_max_length = True,
        )
    ids = torch.tensor(inputs["input_ids"], dtype=torch.long).unsqueeze(0)
    mask = torch.tensor(inputs["attention_mask"], dtype=torch.long).unsqueeze(0)
    token_type_ids = torch.tensor(inputs["token_type_ids"], dtype=torch.long).unsqueeze(0)

    ids = ids.to(device, dtype=torch.long)
    mask = mask.to(device, dtype=torch.long)
    token_type_ids = token_type_ids.to(device, dtype=torch.long)

  #model = models_set[f"{location}{aspect}"]
    outputs = model(ids=ids, mask=mask, token_type_ids=token_type_ids)
    prob_max, predicted = torch.max(outputs, 1)

    predicted = predicted.detach().cpu().numpy()

          # Add the predicted to the json only if it is not N(none)
          # Reverse mapping from numbers to sentiments
    idees.append(id_test)
    result.append(predicted[0])

  # Outputting Results
  print(idees)
  print(result)

  with open(currentDirPath + '/SvmAndBERT/inputTestSyllabi/inputSyllabi.csv', 'r') as csvfile:
    datareader = csv.reader(x.replace('\0', '') for x in csvfile)
    ct = 0
    with open(currentDirPath + '/SvmAndBERT/inputTestSyllabiResults/BiasInputSyllabi', 'w') as out_file:
        out_file.write(" ")
    with open(currentDirPath + '/SvmAndBERT/inputTestSyllabiResults/NotBiasInputSyllabi', 'w') as out_file:
      out_file.write(" ")

    next(datareader)
    for row in datareader:
      if(result[ct] == 1):
        with open(currentDirPath + '/SvmAndBERT/inputTestSyllabiResults/BiasInputSyllabi', 'a') as out_file:
          out_file.write(row[3] + '\n')
      else:
        with open(currentDirPath + '/SvmAndBERT/inputTestSyllabiResults/NotBiasInputSyllabi', 'a') as out_file:
          out_file.write(row[3] + '\n')
      ct += 1


  dt = pd.DataFrame(list(zip(idees, result)), columns = ['id', 'target'])
  # dt.to_csv('submissions.csv')

  # Calculating score
  biasCount = 0
  for i in range(len(result)):
    if result[i] == 1:
      biasCount += 1
      
  if(len(result) == 0):
    return "N/A"

  print("Bias Score: ", round(biasCount / len(result), 2), "%")
  return round(biasCount / len(result), 2)