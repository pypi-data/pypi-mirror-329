import matplotlib.pyplot as plt  #concern this is in colab context which is oldish

from sklearn.base import BaseEstimator, TransformerMixin

from sklearn.pipeline import Pipeline
import pandas as pd
from IPython.display import display
pd.set_option('mode.chained_assignment', None)  #https://pandas.pydata.org/pandas-docs/stable/user_guide/indexing.html#returning-a-view-versus-a-copy

import numpy as np
import math
import random
from sklearn.model_selection import train_test_split
from sklearn.impute import KNNImputer
from sklearn.preprocessing import MinMaxScaler

from sklearn.experimental import enable_halving_search_cv
from sklearn.model_selection import HalvingGridSearchCV
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import precision_score, recall_score, f1_score, accuracy_score

from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import f1_score#, balanced_accuracy_score, precision_score, recall_score
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegressionCV
from sklearn.ensemble import RandomForestClassifier

import warnings

class puddlesWarning(Warning):
  def __init__(self, message):
      self.message = message
  def __str__(self):
      return repr(self.message)
    
def up_ignore_warnings(yes_no):
  assert isinstance(yes_no, bool)
  if yes_no: warnings.filterwarnings("ignore", category=puddlesWarning)
  else: foo = warnings.filterwarnings("always", category=puddlesWarning)
  return None

up_ignore_warnings(False)  #start out with warnings

from random import sample, seed, choices
def the_claw():
  class_list = ['Smith', 'Jones']
  return sample(class_list,1)[0]

def hello():
  warnings.warn('Puddles says this is just for testing', puddlesWarning)
  print('Welcome to AI for Good')

def up_range(n):
  return list(range(n))

import builtins
import types

#use: @up_no_globals(globals())  #globals is function that returns *current* globals as dict
#DANGER DANGER: this fails on forward refs. Assumes helper functions all defined before main function. If not will get spurious error.
def up_no_globals(gfn:dict):

  def wrap(f):
    new_globals = {'__builtins__': builtins} 
    # removing keys from globals() storing global values in old_globals
    for key, val in gfn.items():
      if  callable(val):
          new_globals[key] = val
    new_f = types.FunctionType(f.__code__, globals=new_globals, argdefs=f.__defaults__)
    new_f.__annotations__ = f.__annotations__ # for some reason annotations aren't copied over
    return new_f

  return wrap

def up_lottery(student_list):
  random_students = random.sample(student_list, len(student_list))
  table_table = pd.DataFrame(columns=['Table'], index=random_students + ['Blank']*(20-len(student_list)))
  table_table['Table'] = [1]*4 + [2]*4 + [3]*4 + [4]*4 + [5]*4
  return table_table

def up_find_char(a_string, a_char):
  return a_string.find(a_char)
  
def up_get_table(url):
  assert isinstance(url, str), f':Puddles says: Expecting url to be string but is {type(url)} instead.'
  try:
    df = pd.read_csv(url)
  except:
    assert False, f'Puddles says: url is not a legal web site for a table. If using GitHub, make sure to get raw version of file.'
  return df.round(2)


def up_get_column(table, column_name):
  assert isinstance(table, pd.core.frame.DataFrame), f'Puddles says: Expecting a table but instead got a {type(table)}!'
  assert column_name in table.columns.to_list(),f'Puddles says: column_name {column_name} is unrecognized. Check spelling and case. Here are legal column names: {table.columns.to_list()}'

  return table[column_name].to_list()

def up_show_color(rgb_triple):
  assert isinstance(rgb_triple, list) or isinstance(rgb_triple, tuple), f'Puddles says: expecting a list but got {rgb_triple}.'
  assert len(rgb_triple)==3, f'Puddles says: expecting 3 itmes in the list but got {rgb_triple}.'
  assert all([isinstance(x, int) for x in rgb_triple]), f'Puddles says: expecting 3 ints but got {rgb_triple}.'

  plt.imshow([[tuple(rgb_triple)]])

def up_find_char(a_string, a_char):
  return a_string.find(a_char)
  
def up_plot_against(table, column1, column2):
  assert isinstance(table, pd.core.frame.DataFrame), f'Puddles says: expecting a pandas dataframe but instead got a {type(table)}!'
  assert column1 in table.columns, f'Puddles says: the first column {column1} is not legal. Check spelling and case. Here are legal columns: {table.columns.to_list()}'
  assert column2 in table.columns, f'Puddles says: the second column {column2} is not legal. Check spelling and case. Here are legal columns: {table.columns.to_list()}'

  if len(set(table[column1].to_list()))>20:
    print(f'Puddles warning: {column1} has more than 20 unique values. Likely to not plot well.')

  if len(set(table[column2].to_list()))>5:
    print(f'Puddles warning: {column2} has more than 5 unique values. Likely to not plot well.')

  df = pd.crosstab(table[column1], table[column2])
  ax = df.plot.bar(figsize=[15,8], grid=True)

  # Calculate group totals
  group_totals = df.sum(axis=1)

  # Calculate the width of each bar (this depends on the total number of bars in each group)
  bar_width = ax.patches[0].get_width()
  num_bars_per_group = len(df.columns)

  # Calculate and display percentages for each bar within its group
  for i, (index, row) in enumerate(df.iterrows()):
      for j, value in enumerate(row):
          # Calculate the percentage of the bar within its group
          percentage = (value / group_totals[index]) * 100

          # Calculate the x position for the label
          # Adjust the offset to center the label over each bar
          x_offset = j * bar_width - (num_bars_per_group * bar_width / 2) + bar_width / 2
          x = i + x_offset
          y = value

          # Display the percentage on the bar
          ax.text(x, y, f'{percentage:.1f}%', ha='center', va='bottom')

  plt.show()

def up_table_subset(table, column_name, condition, value):
  assert isinstance(table, pd.core.frame.DataFrame), f'Puddles says: expecting a pandas dataframe but instead got a {type(table)}!'
  assert isinstance(condition, str), f'Puddles says: condition must be a string but is of type {type(condition)}'
  legal_conditions = {'equals':'==', 'not equals':'!=', '>':'>', '<':'<'}
  assert condition in legal_conditions.keys(), f'Puddles says: condition {condition} incorrect. Must be one of {list(legal_conditions.keys())}'
  assert column_name in table.columns, f'Puddles says: column_name {column_name} is not legal. Check spelling and case. Here are legal columns: {table.columns.to_list()}'
  if 'equals' not in condition and isinstance(value, str):
    assert False, f'Puddles says: expecting value to be a number but is string instead'

  if 'equals' in condition and value not in table[column_name].to_list():
      warnings.warn(f'Puddles warning: {value} does not appear in {column_name}',puddlesWarning)

  op = legal_conditions[condition]

  if isinstance(value,int) or isinstance(value,float):
    value = str(value)
  elif isinstance(value,str):
    value = f'"{value}"'
  else:
    assert False, f'Puddles says: tell Steve he has a bug with {value}'

  new_table = table.query(f'`{column_name}`' + op + value)
  if len(new_table)==0:
    warnings.warn(f'Puddles warning: the new table is empty',puddlesWarning)

  return new_table

def up_st_dev(a_list_of_numbers):
  assert isinstance(a_list_of_numbers, list), f'Puddles says: expecting a list but instead got a {type(a_list_of_numbers)}!'
  assert all([not isinstance(x,str) for x in a_list_of_numbers]), f'Puddles says: expecting a list of numbers but list includes a string!'

  st_dev = np.nanstd(a_list_of_numbers)  #ignores nans
  return st_dev

def up_drop_column(table, column_name):
  assert isinstance(table, pd.core.frame.DataFrame), f'Puddles says: Expecting a table but instead got a {type(table)}!'
  assert column_name in table.columns.to_list(),f'Puddles says: column_name {column_name} is unrecognized. Check spelling and case. Here are legal column names: {table.columns.to_list()}'

  return table.drop(columns=column_name)

def up_drop_nan_rows(table):
  assert isinstance(table, pd.core.frame.DataFrame), f'Puddles says: expecting a table but instead got a {type(table)}!'

  dropped_table = table.dropna(axis=0)
  return dropped_table.reset_index(drop=True)

def up_map_column(table, column_name, mapping_dict):
  assert isinstance(table, pd.core.frame.DataFrame), f'Puddles says: expecting a table but instead got a {type(table)}!'
  assert column_name in table.columns, f'Puddles says: column_name {column_name} is not legal. Check spelling and case. Here are legal columns: {table.columns.to_list()}'
  assert isinstance(mapping_dict, dict), f'Puddles says: expecting mapping_dict to be a dictionary but instead got a {type(mapping_dict)}!'

  column_values = table[column_name].to_list()
  mapping_keys = list(mapping_dict.keys())
  keys_unaccounted = set(mapping_keys).difference(set(column_values))
  if keys_unaccounted:
    warnings.warn(f'Puddles warning: these keys {keys_unaccounted} do not match any values in the column {column_name}.', puddlesWarning)

  values_unaccounted = set(column_values).difference(set(mapping_keys))
  if values_unaccounted:
    warnings.warn(f'Puddles warning: these values {values_unaccounted} are missing a mapping.', puddlesWarning)

  new_table = table.copy()
  with pd.option_context('future.no_silent_downcasting', True):
    new_table[column_name] = table[column_name].replace(mapping_dict).astype('int32')  #to avoid warning messages about downcasting

  return new_table

def up_get_column_types(table):
  assert isinstance(table, pd.core.frame.DataFrame), f'Puddles says: expecting a table but instead got a {type(table)}!'

  column_types = []
  for column in table.columns:
    col_list = up_get_column(table, column)
    unique = set(col_list)
    types = [type(x) for x in col_list if not pd.isnull(x)]
    if len(set(types))>1:
      value = [column, 'Mixed', 'Not good']
    else: 
      for item in col_list:
        if pd.isnull(item): continue
        d = type(item)
        if d==str and len(unique)<10:
          value = [column, d.__name__, unique]
        else:
          value = [column, d.__name__, '...']
        break
    column_types.append(value)

  return pd.DataFrame(column_types, columns=['Column', 'Type', 'Unique<10'])

def up_column_histogram(table, column_name):
  assert isinstance(table, pd.core.frame.DataFrame), f'Puddles says: expecting a table but instead got a {type(table)}!'
  assert column_name in table.columns, f'Puddles says: column_name {column_name} is not legal. Check spelling and case. Here are legal columns: {table.columns.to_list()}'
  assert all([not isinstance(x,str) for x in table[column_name]]), f'Puddles says: the column has string values. Can only plot numeric values.'
  
  table[column_name].plot(kind='hist', figsize=(15,8), grid=True, logy=True)
  
def up_clip_list(value_list, lower_boundary, upper_boundary):
  assert isinstance(value_list, list), f'Puddles says: Expecting a list but instead got a {type(value_list)}!'
  assert all([not isinstance(x,str) for x in value_list]), f'Puddles says: the list has string values. Can only clip numeric values.'
  assert lower_boundary<upper_boundary, f'Puddles says: lower_boundary must be less than upper_boundary!'

  upper_clipped = 0
  lower_clipped = 0
  new_list = []
  for item in value_list:
    if item>upper_boundary:
      value = upper_boundary
      upper_clipped+=1
    elif item<lower_boundary:
      value = lower_boundary
      lower_clipped+=1
    else:
      value = item
    new_list.append(value)
  print(f'Lower items clipped: {lower_clipped}')
  print(f'Upper items clipped: {upper_clipped}')
  return new_list


def up_set_column(table, column_name, new_values):
  assert isinstance(table, pd.core.frame.DataFrame), f'Puddles says: Expecting a table but instead got a {type(table)}!'
  assert isinstance(new_values, list), f'Puddles says: Expecting a list but instead got a {type(new_values)}!'
  assert len(new_values)==len(table), f'Puddles says: length of list is {len(new_values)} but length of table is {len(table)}. Mismatch!'
  
  new_table = table.copy()
  new_table[column_name] = new_values
  if column_name not in table.columns.to_list():
    warnings.warn(f'Puddles warning: column_name {column_name} is not part of current table so adding new column.', puddlesWarning)
    new_cols = [column_name] + [col for col in new_table.columns if col != column_name] 
    new_table = new_table[new_cols]
  return new_table


def up_write_table(table, file_name):
  assert isinstance(table, pd.core.frame.DataFrame), f'Puddles says: Expecting a table but instead got a {type(table)}!'
  assert isinstance(file_name, str), f'Puddles says: Expecting file_name to be a string but got a {type(file_name)}!'

  if not file_name.endswith('.csv'): file_name += '.csv'
  table.to_csv(file_name, index=False)
  return None

def up_knn_probability(table, new_row, k):
  assert isinstance(table, pd.core.frame.DataFrame), f'Puddles says: expecting a pandas dataframe but instead got a {type(table)}!'
  assert table.isna().sum().sum()==0, f'Puddles says: table still contains NaN values.'
  for column in table.columns:
    col_list = up_get_column(table, column)
    assert not any([isinstance(x,str) for x in col_list]), f'Puddles says: column {column} contains string values.'
  assert isinstance(new_row, list), f'Puddles says: new_row must be a list but is of type {type(new_row)}'
  assert all([not isinstance(x,str) for x in new_row]), f'Puddles says: expecting a list of numbers but list includes a string!'
  assert isinstance(k, int), f'Puddles says: k must be an integer but is of type {type(k)}'
  assert k>0, f'Puddles says: k must be greater than 0'
  columns = table.columns
  assert len(new_row)==len(columns)-1, f'Puddles says: length of new_row should be {len(columns)-1} but is instead {len(new_row)}.'
  
  last_c = columns[len(columns)-1]
  feature_table = table.drop(columns=last_c)
  labels = table[last_c].to_list()
  assert all([x in [0,1] for x in labels]), f'Puddles says: the target column {last_c} should be binary. Reminder: the target column should be the last column in table.'
  from sklearn.neighbors import KNeighborsClassifier
  neigh = KNeighborsClassifier(n_neighbors=k)
  neigh.fit(feature_table.to_numpy(), labels)
  p = neigh.predict_proba([new_row])
  return p[0].tolist()

def up_knn_full(train_table, test_table, target_col, k):
  assert isinstance(train_table, pd.core.frame.DataFrame), f'Puddles says: expecting a pandas dataframe but instead got a {type(train_table)}!'
  assert isinstance(test_table, pd.core.frame.DataFrame), f'Puddles says: expecting a pandas dataframe but instead got a {type(test_table)}!'
  assert train_table.isna().sum().sum()==0, f'Puddles says: train_table still contains NaN values.'
  assert test_table.isna().sum().sum()==0, f'Puddles says: test_table still contains NaN values.'
  for column in train_table.columns:
    col_list = up_get_column(train_table, column)
    assert not any([isinstance(x,str) for x in col_list]), f'Puddles says: column {column} contains string values.'
  assert isinstance(k, int), f'Puddles says: k must be an integer but is of type {type(k)}'
  assert k>0, f'Puddles says: k must be greater than 0'
  assert k<=len(train_table), f'Puddles says: k must be <= length of train_table'
  assert all([x in [0,1] for x in up_get_column(train_table,target_col)]), f'Puddles says: the target column {target_col} should be binary.'

  from sklearn.neighbors import KNeighborsClassifier
  neigh = KNeighborsClassifier(n_neighbors=k)
  neigh.fit(train_table.drop(columns=target_col).to_numpy(), up_get_column(train_table,target_col))
  p = neigh.predict_proba(up_table_to_list(test_table.drop(columns=target_col)))
  return p.tolist()  #looks a little strange

def up_zip_lists(*args):
  assert args, f'Empty list not allowed'
  for lst in args:
    if not isinstance(lst, list):
      try:
        lst = list(lst)
      except:
        assert False, f'Puddles says: Expecting a list but instead got a {type(lst)}!'
  n = len(args[0])
  for lst in args[1:]:
    assert len(lst)==n, f'Puddles says: the lengths of the lists are not equal: {n}, {len(lst)}.'

  z = list(zip(*args))
  result = [list(tup)     for tup in z]
  return result

def up_scale_table(table):
  assert isinstance(table, pd.core.frame.DataFrame), f'Puddles says: expecting a table but instead got a {type(table)}!'
  num_columns = table.select_dtypes(include=np.number).columns.tolist()  #find columns that are numeric
  all_columns = table.columns.tolist()
  residue = set(all_columns) - set(num_columns)  #any columns that are not numeric?
  assert not residue, f'Puddles says: these columns contain strings {residue}'

  scaler = MinMaxScaler()
  df_scaled = pd.DataFrame(scaler.fit_transform(table), columns=table.columns)
  return df_scaled.round(2)

def up_apply_3sigma(table, column_name):
  assert isinstance(table, pd.core.frame.DataFrame), f'Puddles says: expected Dataframe but got {type(table)} instead.'
  assert column_name in table.columns.to_list(), f'Puddles says: unknown column {column_name}'
  assert not any([isinstance(v, str) for v in table[column_name].to_list()]), f'Puddles says: column_name contains strings.'

  df = table.copy()
  m = df[column_name].mean()
  sigma = df[column_name].std()
  df[column_name] = table[column_name].clip(lower=m-3*sigma, upper=m+3*sigma)
  return df.round(2)

def up_build_decision_tree(table, depth):
  assert isinstance(table, pd.core.frame.DataFrame), f'Puddles says: expecting a pandas dataframe but instead got a {type(table)}!'
  assert table.isna().sum().sum()==0, f'Puddles says: table still contains NaN values.'
  for column in table.columns:
    col_list = up_get_column(table, column)
    assert not any([isinstance(x,str) for x in col_list]), f'Puddles says: column {column} contains string values.'
  
  assert isinstance(depth, int), f'Puddles says: depth must be an integer but is of type {type(depth)}'
  assert depth>0, f'Puddles says: depth must be greater than 0'
  columns = table.columns

  last_c = columns[len(columns)-1]
  feature_table = table.drop(columns=last_c)
  labels = table[last_c].to_list()
  assert all([x in [0,1] for x in labels]), f'Puddles says: the target column {last_c} should be binary. Reminder: the target column should be the last column in table.'

  from sklearn.tree import DecisionTreeClassifier
  clf = DecisionTreeClassifier(random_state=1234, max_depth=depth)
  clf.fit(feature_table, labels)
  import graphviz
  from sklearn import tree
  # DOT data
  dot_data = tree.export_graphviz(clf, out_file=None, 
                                  feature_names=feature_table.columns,  
                                  class_names=['No', 'Yes'],
                                  filled=True)

  # Draw graph
  graph = graphviz.Source(dot_data, format="png") 
  return graph

def up_get_random_rows(table, fraction, the_seed, bootstrap=False):
  assert isinstance(table, pd.core.frame.DataFrame), f'Puddles says: expecting a pandas dataframe but instead got a {type(table)}!'
  assert 0<fraction<=1, f'Puddles says: fraction must be 0<fraction<=1 but is {fraction}.'
  random_table = table.sample(frac=fraction, random_state=the_seed, replace=bootstrap)
  return random_table

def up_list_column_names(table):
  assert isinstance(table, pd.core.frame.DataFrame), f'Puddles says: expecting a pandas dataframe but instead got a {type(table)}!'
  return table.columns.to_list()

def up_product(value_list):
  assert isinstance(value_list, list)
  assert all([type(v)!=str for v in value_list])
  product = 1
  for v in value_list:
    product *= v
  return product

def up_table_to_list(table):
  return table.to_numpy().tolist()

def up_train_test_split(table, target, test_percentage):
  from sklearn.model_selection import train_test_split
  labels = up_get_column(table, target)
  train_X, test_X, train_y, test_y = train_test_split(table, labels, test_size=test_percentage, shuffle=True,
                                                random_state=1234, stratify=labels)
  return [train_X, test_X]

def up_metrics(zipped_list):
  tp = sum([1 if p==1 and a==1 else 0 for p,a in zipped_list])
  tn = sum([1 if p==0 and a==0 else 0 for p,a in zipped_list])
  fp = sum([1 if p==1 and a==0 else 0 for p,a in zipped_list])
  fn = sum([1 if p==0 and a==1 else 0 for p,a in zipped_list])

  precision = tp/(tp+fp) if (tp+fp)>0 else 0
  recall = tp/(tp+fn) if (tp+fn)>0 else 0
  f1 = 2*precision*recall/(precision+recall) if (precision+recall)>0 else 0
  accuracy = (tp+tn)/len(zipped_list)
  return {'Precision': precision, 'Recall': recall, 'F1': f1, 'Accuracy': accuracy}

def up_metrics_table(metrics_list):
  foo = pd.DataFrame(metrics_list)
  foo = foo.set_index('Threshold')
  foo = foo.round(2)
  foo = foo[['Precision', 'Recall', 'F1', 'Accuracy']]
  foo = foo.sort_index()
  #foo.insert(0, 'Threshold', foo.pop('Threshold'))
  return foo.round(2)

def up_plot_precision_v_recall(metrics_table):
  assert isinstance(metrics_table, pd.core.frame.DataFrame), f'Puddles says: expecting a pandas dataframe but instead got a {type(metrics_table)}!'
  assert metrics_table.index.name == 'Threshold', f'Expecting Threshold as index but got {metrics_table.index.name}'
  columns = metrics_table.columns.to_list()
  expected = ['Precision',	'Recall',	'F1',	'Accuracy']
  assert not set(expected) - set(columns), f"Puddles says: expecting columns {expected} but got {columns}"

  metrics_table['The Threshold'] = metrics_table.index
  import plotly.express as px
  metrics_table.sort_values(by='Precision', ascending=True, inplace=True)
  fig = px.line(
    data_frame=metrics_table,  
    x='Precision',
    y='Recall',
    title='Precision v. Recall curve',
    hover_data=['Accuracy', 'The Threshold', 'F1'])
  fig.update_traces(mode='markers+lines')
  fig.show()
  
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense, Activation, Dropout
import tensorflow as tf
from tensorflow import keras

import matplotlib.pyplot as plt

def up_neural_net_old(train_table, test_table, architecture, target):
  assert isinstance(train_table, pd.core.frame.DataFrame), f'Puddles says: expecting train_table to be table but instead got a {type(train_table)}!'
  assert isinstance(test_table, pd.core.frame.DataFrame), f'Puddles says: expecting test_table to be table but instead got a {type(test_table)}!'
  assert isinstance(architecture, list) or isinstance(architecture, tuple), f'architecture is a list or tuple, the number of nodes per layer. Instead got {type(architecture)}'
  assert architecture, f'architecture cannot be the empty list'
  assert all([isinstance(x,int) and x>0 for x in architecture]), f'Puddles says: architecture must contain integers greater than 0'
  assert target in set(train_table.columns)
  assert target in set(test_table.columns)

  tf.keras.utils.set_random_seed(1234)  #need now for replication
  tf.config.experimental.enable_op_determinism()  #https://www.tensorflow.org/api_docs/python/tf/config/experimental/enable_op_determinism

  #np.random.seed(seed=1234)
  #tf.random.set_seed(1234)

  columns = up_list_column_names(train_table)
  new_train = train_table.drop(columns=target).to_numpy()
  labels = np.array(up_get_column(train_table, target))
  new_test = test_table.drop(columns=target).to_numpy()
  n = len(columns)-1

  metrics=tf.keras.metrics.BinaryAccuracy(
    name='binary_accuracy', dtype=None, threshold=0.5
  )
  loss=tf.keras.losses.BinaryCrossentropy(from_logits=False)
  learning_rate=.02

  l2_regu = tf.keras.regularizers.L2(0.01)  #weight regularization during gradient descent
  initializer = tf.keras.initializers.HeNormal(seed=1234)  #works best with Relu: https://machinelearningmastery.com/weight-initialization-for-deep-learning-neural-networks/

  early_stop_cb = tf.keras.callbacks.EarlyStopping(
    monitor='loss',
    min_delta=0,
    patience=5,  #Wait 5 epochs for loss to change - if no change, stop
    verbose=0
  )

  model = Sequential()

  #handle first hidden layer separately because of input_dim

  layer_units = architecture[0]
  layer_dropout = .2
  layer_act = 'relu'
  model.add(Dense(units=layer_units, activation=layer_act, activity_regularizer=l2_regu, kernel_initializer=initializer, input_dim=n))  #first hidden layer needs number of inputs
  model.add(Dropout(layer_dropout))

  for layer in architecture[1:]:
    layer_units = layer
    model.add(Dense(units=layer_units, activation=layer_act, activity_regularizer=l2_regu, kernel_initializer=initializer))
    model.add(Dropout(layer_dropout))
    
  #now output layer
  model.add(Dense(units=1, activation='sigmoid'))

  model.compile(optimizer=keras.optimizers.Adam(learning_rate=learning_rate),
              metrics=[metrics],
              loss=loss,
               )
  
  batch = 20
  epochs = 100
  training = model.fit(x=new_train,
                          y=labels,
                          batch_size=batch,
                          epochs=epochs,
                          verbose=0,
                          shuffle=True,   #this is new but should be controlled by setting seed
                          callbacks=[early_stop_cb])
  print(f'Finished training with {len(training.history["loss"])} epochs ...')
  '''
  plt.plot(training.history['binary_accuracy'])
  plt.title('model accuracy')
  plt.ylabel('accuracy')
  plt.xlabel('epoch')
  plt.show()
  '''
  np_predictions = model.predict(new_test)

  predictions = [[float(1-p[0]), float(p[0])] for p in np_predictions]
  print('Finished testing ...')
  return predictions

from tensorflow.keras.layers import Input
def up_neural_net(train_table, test_table, architecture, target):
  assert isinstance(train_table, pd.core.frame.DataFrame), f'Puddles says: expecting train_table to be table but instead got a {type(train_table)}!'
  assert isinstance(test_table, pd.core.frame.DataFrame), f'Puddles says: expecting test_table to be table but instead got a {type(test_table)}!'
  assert isinstance(architecture, list) or isinstance(architecture, tuple), f'architecture is a list or tuple, the number of nodes per layer. Instead got {type(architecture)}'
  assert architecture, f'architecture cannot be the empty list'
  assert all([isinstance(x,int) and x>0 for x in architecture]), f'Puddles says: architecture must contain integers greater than 0'
  assert target in set(train_table.columns)
  assert target in set(test_table.columns)

  tf.keras.backend.clear_session()

  tf.keras.utils.set_random_seed(1234)  #need now for replication
  tf.config.experimental.enable_op_determinism()  #https://www.tensorflow.org/api_docs/python/tf/config/experimental/enable_op_determinism

  np.random.seed(seed=1234)
  tf.random.set_seed(1234)

  columns = up_list_column_names(train_table)
  new_train = train_table.drop(columns=target).to_numpy()
  labels = np.array(up_get_column(train_table, target))
  new_test = test_table.drop(columns=target).to_numpy()
  n = len(columns)-1

  metrics=tf.keras.metrics.BinaryAccuracy(
    name='binary_accuracy', dtype=None, threshold=0.5
  )
  loss=tf.keras.losses.BinaryCrossentropy(from_logits=False)
  learning_rate=.02

  l2_regu = tf.keras.regularizers.L2(0.01)  #weight regularization during gradient descent
  initializer = tf.keras.initializers.HeNormal(seed=1234)  #works best with Relu: https://machinelearningmastery.com/weight-initialization-for-deep-learning-neural-networks/

  layer_act = 'leaky_relu'
  layer_dropout = .3

  monitor = 'binary_accuracy'
  mode = 'max'

  early_stopping = tf.keras.callbacks.EarlyStopping(monitor=monitor, mode=mode, patience=10, restore_best_weights=True)
  reduce_lr = tf.keras.callbacks.ReduceLROnPlateau(monitor=monitor, mode=mode, factor=0.5, patience=7, min_lr=1e-6, verbose=1)

  model = Sequential()

  #handle first hidden layer separately because of input_dim

  # Add an input layer
  model.add(Input(shape=(n,)))  # n is the number of input features

  for layer in architecture:
    layer_units = layer
    model.add(Dense(units=layer_units, activation=layer_act, activity_regularizer=l2_regu, kernel_initializer=initializer))
    model.add(Dropout(layer_dropout,seed=1234))

  #now output layer
  model.add(Dense(units=1, activation='sigmoid'))

  model.compile(optimizer=keras.optimizers.Adam(learning_rate=learning_rate),
              metrics=[metrics],
              loss=loss,
               )

  batch = 1
  epochs = 100
  training = model.fit(x=new_train,
                          y=labels,
                          batch_size=batch,
                          epochs=epochs,
                          verbose=0,
                          shuffle=True,   #this is new but should be controlled by setting seed
                          callbacks=[early_stopping, reduce_lr]
                       )
  print(f'Finished training with {len(training.history["loss"])} epochs ...')

  plt.plot(training.history['binary_accuracy'])
  plt.title('model accuracy')
  plt.ylabel('accuracy')
  plt.xlabel('epoch')
  plt.show()

  np_predictions = model.predict(new_test)

  predictions = [[float(1-p[0]), float(p[0])] for p in np_predictions]
  print('Finished testing ...')
  return predictions
  
def up_lower_string_list(string_list):
  result = [c.lower() for c in string_list]
  return result

def up_build_bow(table, text_column, target_column):
  import spacy
  from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
  import string
  from spacy.lang.en import English
  from spacy.lang.en.stop_words import STOP_WORDS
  nlp = spacy.load('en')

  punctuations = string.punctuation
  stop_words = spacy.lang.en.stop_words.STOP_WORDS
  parser = English()

  def spacy_tokenizer(sentence):

      # Creating our token object which is used to create documents with linguistic annotations
      mytokens = parser(sentence)
      
      # lemmatizing each token and converting each token in lower case
      # Note that spaCy uses '-PRON-' as lemma for all personal pronouns lkike me, I etc
      mytokens = [ word.lemma_.lower().strip() if word.lemma_ != "-PRON-" else word.lower_ for word in mytokens ]
      
      # Removing stop words
      mytokens = [ word for word in mytokens if word not in stop_words and word not in punctuations]
      
      # Return preprocessed list of tokens
      return mytokens   

  the_text = up_get_column(table, text_column)
  cleaned = [text.strip().lower() for text in the_text]
  vectorizer = CountVectorizer(tokenizer = spacy_tokenizer, ngram_range = (1,1))
  the_bow = vectorizer.fit_transform(cleaned)
  data = the_bow.toarray()
  columns = list(vectorizer.get_feature_names_out())
  bow_table = pd.DataFrame(data, columns=columns)
  bow_table.insert(len(columns), f'__{target_column}__', up_get_column(table, target_column))
  
  return bow_table

def up_check_paths(path_list):
  assert any([c for c,v in path_list]), f'Puddles says: all paths false'
  assert sum([c for c,v in path_list])==1, f'Puddles says: more than one path true: {path_list}'
  for i,[c,v] in enumerate(path_list):
    if c:
      print(f'Path {i+1} is True {v}')
      break
  return None

def stats_please(*, table):
  assert isinstance(table, pd.core.frame.DataFrame), f'Puddles says: expecting a pandas dataframe but instead got a {type(table)}!'
  return table.describe(include='all').T

#PARSONS test

# Import necessary components from ipywidgets

from ipywidgets import Dropdown, Layout, VBox, HBox, Button, HTML as HTMLWidget, Output
from IPython.display import display, clear_output, HTML
from IPython import get_ipython
import random
import traceback
import sys

#This version has lots of hints. Problem is student can try all combinations easily by blind search.

def setup_code_exercise(statement_indent_pairs, distractors=[], the_globals={}):
      # Initialize the info text and button
    info_text = '''The goal is to get to all green code and all green comments.<br>
    Green code signifies a needed statement in the correct order.<br>
    Red code signifies a needed statement but not in correct order.<br>
    Comments are focused on indentation and are self-explanatory.<br>
    Purple code signifies a statement that is not part of the solution and potentially can cause errors.<br>
    Click 'Info' button to toggle visibility.<br>
    '''
    info_display = HTMLWidget(value="")  # Initially hidden

    # Function to toggle the info display
    def toggle_info(btn):
        info_display.value = "" if info_display.value else info_text

    info_button = Button(description="Info")
    info_button.on_click(toggle_info)

    # Prepare the statements and options
    all_statements = [pair[0] for pair in statement_indent_pairs] + distractors
    scrambled_statements = random.sample(all_statements, len(all_statements))

    # Initialize widgets
    order_dropdowns = [Dropdown(options=['Select a statement'] + scrambled_statements, description=f'Statement {i+1}:', layout=Layout(width='auto')) for i in range(len(statement_indent_pairs))]
    indentation_dropdowns = [Dropdown(options=[f'Select indentation level for statement {i+1}', 'No indentation', 'One level', 'Two levels'], description=f'Indentation {i+1}:', layout=Layout(width='auto'), disabled=True) for i in range(len(statement_indent_pairs))]

    # Mapping to check if a statement is correct and its expected position
    correct_order_map = {stmt: i for i, (stmt, _) in enumerate(statement_indent_pairs)}
    
    def on_statement_change(change):
        index = order_dropdowns.index(change.owner)
        selected_statement = change.new
        # Enable indentation selection for correctly positioned statements
        is_correct_and_positioned = selected_statement in correct_order_map and correct_order_map[selected_statement] == index
        indentation_dropdowns[index].disabled = not is_correct_and_positioned
        update_code_display(None)

    def update_code_display(change):
        clear_output(wait=True)
        #display(VBox(order_dropdowns + indentation_dropdowns))
        display(info_button, info_display, VBox(order_dropdowns + indentation_dropdowns))
        
        code_display_html = "<br><strong>Current Code Configuration:</strong><br><hr>"
        for i, (order_dropdown, indent_dropdown) in enumerate(zip(order_dropdowns, indentation_dropdowns)):
            if order_dropdown.value == 'Select a statement':
                statement_display = f"<em># Statement {i+1} not selected</em>"
                indent_feedback = ""
                indent_visual = ""
            else:
                statement_color = "purple" if order_dropdown.value in distractors else "red"
                if order_dropdown.value in correct_order_map and correct_order_map[order_dropdown.value] == i:
                    statement_color = "green"
                
                statement_display = f"<span style='color:{statement_color};'><strong>{order_dropdown.value}</strong></span>"
                
                # Only apply indentation visual if indentation has been selected
                if indent_dropdown.value != f'Select indentation level for statement {i+1}':
                    indent_levels = ['No indentation', 'One level', 'Two levels']
                    selected_indent_level = indent_levels.index(indent_dropdown.value)
                    indent_visual = '&nbsp;' * 4 * selected_indent_level
                    correct_indent_level = statement_indent_pairs[correct_order_map[order_dropdown.value]][1] if statement_color == "green" else 0
                    indent_feedback_color = "green" if correct_indent_level == selected_indent_level else "red"
                    indent_feedback = f"<span style='color:{indent_feedback_color};'>&nbsp;&nbsp;# {'Correct indentation' if correct_indent_level == selected_indent_level else 'Incorrect indentation'}</span>"
                else:
                    indent_feedback = "<span style='color:gray;'>&nbsp;&nbsp;# Indentation missing</span>"
                    indent_visual = ""
            
            code_line_html = f"{indent_visual}{statement_display}{indent_feedback}<br>"
            code_display_html += code_line_html
        
        display(HTML(code_display_html))

    # Attach event listeners
    for dropdown in order_dropdowns:
        dropdown.observe(on_statement_change, names='value')
    for dropdown in indentation_dropdowns:
        dropdown.observe(update_code_display, names='value')

    update_code_display(None)  # Initial display

def parsons_quiz_1():
  statement_indent_pairs = [
      ("numbers = [1, 2, 3, 4, 5]", 0),
      ("for number in numbers:", 0),
      ("if number % 2 == 0:", 1),
      ('print(f"{number} is even")', 2),
      ("else:", 1),
      ('print(f"{number} is odd")', 2),
  ]
  distractors = [
      "print('This is a distractor.')",
      "unused_var = 0"
  ]
  setup_code_exercise(statement_indent_pairs, distractors)

#Below is version with no hints, other than number of necessary statements

def setup_simplified_code_exercise(statement_indent_pairs, distractors=[], the_globals={}):
    info_text = '''Fill in code for all the statements.<br>
    Select indentation for each statement.<br>
    When finished, click the Run Code button to see results. Note this button is inactive until all statements and indentation chosen.<br>
    If you do not get the correct result, fix the bug(s) - easier said than done in some cases!<br>
    Note the error messages are brief. You may get more detailed messages by copying the code into a new cell and running that cell.<br>
    Click 'Info' button to toggle visibility.<br>
    '''
    info_display = HTMLWidget(value="")  # Initially hidden

    def toggle_info(btn):
        info_display.value = info_text if info_display.value == "" else ""

    info_button = Button(description="Info")
    info_button.on_click(toggle_info)

    # Prepare statements for the exercise
    all_statements = [pair[0] for pair in statement_indent_pairs] + distractors
    scrambled_statements = random.sample(all_statements, len(all_statements))

    # Create dropdown widgets for statement ordering and indentation levels
    order_dropdowns = [Dropdown(options=['Select a statement'] + scrambled_statements, description=f'Statement {i+1}:', layout=Layout(width='auto')) for i in range(len(statement_indent_pairs))]
    indentation_dropdowns = [Dropdown(options=['Select indentation level', 'No indentation', 'One level', 'Two levels'], description=f'Indentation {i+1}:', layout=Layout(width='auto')) for i in range(len(statement_indent_pairs))]
    pairs = [HBox([order_dropdown, indent_dropdown]) for order_dropdown, indent_dropdown in zip(order_dropdowns, indentation_dropdowns)]

    run_button = Button(description="Run Code", disabled=True)  # Initially disabled
    code_output = Output()  # Output widget to display code execution results

    def check_run_button_activation():
        # Enable the "Run Code" button only if all statements and indentations are selected
        all_statements_selected = all(dropdown.value != 'Select a statement' for dropdown in order_dropdowns)
        all_indentations_selected = all(dropdown.value != 'Select indentation level' for dropdown in indentation_dropdowns)
        run_button.disabled = not (all_statements_selected and all_indentations_selected)

    def run_code(btn):
      # Assemble the selected code
      assembled_code = "\n".join(
          "    " * ['No indentation', 'One level', 'Two levels'].index(indent_dropdown.value) + order_dropdown.value
          for order_dropdown, indent_dropdown in zip(order_dropdowns, indentation_dropdowns)
          if order_dropdown.value != 'Select a statement' and indent_dropdown.value != 'Select indentation level'
      )
      
      # Create a clean execution context by default - can override if want outside context
      clean_globals = the_globals.copy()
      
      with code_output:
          clear_output()
          try:
              # Execute the assembled code in the clean context
              exec(assembled_code, clean_globals)
              # Optionally, print something like "Code executed successfully" if needed
          except Exception as e:
            #print("\nAn error occurred:\n")
            #traceback.print_exc()
            
            # Capture the exception details
            exc_type, exc_value, exc_traceback = sys.exc_info()
            #print(f'{exc_type=}, {exc_value=}, {exc_traceback=}')
            # Format the traceback
            traceback_details = traceback.format_exception(exc_type, exc_value, exc_traceback)[2:]  #skip over first 2
            #print(f'{traceback_details=}')
            k = traceback_details[0].find('line')
            if k != -1:
              msg1 = traceback_details[0][k:]
              k = msg1.find(",")
              msg1 = msg1[:k] + '\n' if k != -1 else msg1
            else:
              msg1 = traceback_details[0]
            msg2 = ' ' + traceback_details[1] + '\n'
            msg3 = ' ' + traceback_details[-1]
            # Optionally, process 'traceback_details
            error_message = ''.join(msg1+msg2+msg3)
            # Optionally, process 'error_message' to customize the display
            print("\nAn error occurred:\n", error_message)

    run_button.on_click(run_code)

    def update_display(change):
        clear_output(wait=True)
        #display(info_button, info_display, VBox(order_dropdowns + indentation_dropdowns), run_button, code_output)
        
        code_display_html = "<br><strong>Current Code Configuration:</strong><br><hr>"
        for i, (order_dropdown, indent_dropdown) in enumerate(zip(order_dropdowns, indentation_dropdowns)):
            if order_dropdown.value != 'Select a statement':
                indent_visual = "&nbsp;" * 4 * ['No indentation', 'One level', 'Two levels'].index(indent_dropdown.value) if indent_dropdown.value != 'Select indentation level' else ""
                code_line = f"{indent_visual}<span style='color:blue;'>{order_dropdown.value}</span>"
                if indent_dropdown.value == 'Select indentation level':
                    code_line += " <span style='color:gray;'># Missing indentation</span>"
            else:
                code_line = f"<em># Statement {i+1} not selected</em>"
            code_display_html += code_line + "<br>"
        code_display_html += "<hr>"
      
        display(info_button, info_display)
        display(HTML(code_display_html))
        display(VBox(pairs + [run_button]), code_output)
        check_run_button_activation()  # Update "Run Code" button activation status

    # Attach event listeners to widgets for dynamic updates
    for dropdown in order_dropdowns + indentation_dropdowns:
        dropdown.observe(update_display, names='value')

    update_display(None)  # Initial display setup

def parsons_raw_quiz_1():
  statement_indent_pairs = [
      ("numbers = [1, 2, 3, 4, 5]", 0),
      ("for number in numbers:", 0),
      ("if number % 2 == 0:", 1),
      ('print(f"{number} is even")', 2),
      ("else:", 1),
      ('print(f"{number} is odd")', 2),
  ]
  distractors = [
      "print('This is a distractor.')",
      "unused_var = 0"
  ]
  setup_simplified_code_exercise(statement_indent_pairs, distractors)

#week 3 review
def parsons_demo():
  statement_indent_pairs = [
    ('a_list = [4, 5, 9, 0]', 0),
    ('for item in a_list:', 0),
    ("print(f'{item=}')  #[4,5,9,0]", 1),
  ]
  distractors = [
  ]
  setup_simplified_code_exercise(statement_indent_pairs, distractors)
  
#week 3 review
def parsons_loop_1():
  statement_indent_pairs = [
    ('current_list = [4, 5, -7, -8, 9, 0]', 0),
    ('new_list = []', 0),
    ('for item in current_list:', 0),
    ('if item >= 0:', 1),
    ('new_list += [item]', 2),
    ("print(f'{new_list=}')  #[4,5,9,0]", 0),
  ]
  distractors = [
  ]
  setup_simplified_code_exercise(statement_indent_pairs, distractors)

#week 3 review
def parsons_loop_2():
  statement_indent_pairs = [
    ("list_a = ['a', 'b', 'c']", 0),
    ("list_b = [1, 2, 3]", 0),
    ('zipped = []', 0),
    ('for i in range(len(list_a)):', 0),
    ('zipped += [[list_a[i], list_b[i]]]', 1),
    ("print(f'{zipped=}')  #[['a', 1], ['b', 2], ['c', 3]]", 0)
  ]
  distractors = [
  'for item2 in list_b:',
  'zipped += [item1, item2]',
  'for item1 in list_a:',
  'zipped += [list_a[i], list_b[i]]',
  'for i in range(4):',
  'zipped = [[]]'
  ]
  setup_simplified_code_exercise(statement_indent_pairs, distractors)

#parsons version - chapter 4 - need to call with globals()
def parsons_loop_3(globals={}):
  statement_indent_pairs = [
    ('for k in k_list:',0),
    ('probs = up_knn_probability(neighbors_table, newbie_row, k)',1),
    ('prediction = 1 if probs[1]>=.5 else 0',1),
    ("print(f'{k=}, {actual_outcome=}, {prediction=}, {probs=}')",1),
  ]
  distractors = [
  'for k in range(101):',
  'probs = up_knn_probability(neighbors_table, newbie_row, K)',
  'prediction = 1 if probs[0]>=.5 else 0',
  'prediction = 1 if prbs[1]>=.5 else 0',
  ]
  setup_simplified_code_exercise(statement_indent_pairs, distractors, globals)

#parsons version chapter 4
def parsons_loop_4():
  statement_indent_pairs = [
    ('a_list = [4,5,6]',0),
    ('b_list = [1,2,3]',0),
    ('added_list = []',0),
    ('zipped_list = up_zip_lists(a_list,b_list)', 0),
    ('for x,y in zipped_list:',0),
    ('added_list += [x+y]',1),
    ('added_list = [x+y for x,y in zipped_list]', 0),
    ('pass', 0),
    ("print(f'{added_list=}')",0),
  ]
  distractors = [

  ]
  setup_simplified_code_exercise(statement_indent_pairs, distractors, {'up_zip_lists':up_zip_lists})

#parsons version - chapter 4 - need to call with globals()
def parsons_nested(globals={}):
  statement_indent_pairs = [
    ('for thresh in thresholds:',0),
    ("print(f'{thresh=}')",1),
    ('for prob in middle_probs:',1),
    ("prediction = 1 if prob >= thresh else 0",2),
    ("print(f'{prediction=}, {prob=}')",2),
    ("print()",1),
  ]
  distractors = [

  ]
  setup_simplified_code_exercise(statement_indent_pairs, distractors, globals)
  
#parsons version chapter 9 - need to call with globals()
def parsons_loop_5(globals={}):
  statement_indent_pairs = [
    ('for n in number_trees:',0),
    ('clf = RandomForestClassifier(n_estimators=n, max_depth=2, random_state=1234)',1),
    ('clf.fit(X, y)', 1),
    ("probs = clf.predict_proba(fire_table[-10:].drop(columns='fire'))",1),
    ('pos_probs = [p for n,p in probs]', 1),
    ('predictions = [1 if p>=.5 else 0 for p in pos_probs]',1),
    ('accuracy = sum([p==row[-1] for p,row in up_zip_lists(predictions, last10_rows)])/len(predictions)',1),
    ("print(f'{n=}, {accuracy=}')", 1),
  ]
  distractors = [

  ]
  setup_simplified_code_exercise(statement_indent_pairs, distractors, globals)

