import pandas as pd
import numpy as np
from io import StringIO
import math
import ast
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import statistics
from sklearn import preprocessing
from sklearn.preprocessing import StandardScaler
from scipy import stats
import matplotlib.pyplot as plt
import ruptures as rpt


import plotly.express as px

# Famous Players
nba_1 = pd.read_csv("/Users/dannysimon/Documents/QARIK/OPUS/src/nba_kingjames.csv", index_col=[0])
nba_1 = nba_1.append(pd.read_csv("/Users/dannysimon/Documents/QARIK/OPUS/src/nba_damianlillard.csv", index_col=[0]), ignore_index = True)
nba_1 = nba_1.append(pd.read_csv("/Users/dannysimon/Documents/QARIK/OPUS/src/nba_giannis_an34_ygtrece.csv", index_col=[0]), ignore_index = True)
nba_1 = nba_1.append(pd.read_csv("/Users/dannysimon/Documents/QARIK/OPUS/src/nba_kyrieirving_EasyMoneySniper_jharden13_cp3_zo.csv", index_col=[0]), ignore_index = True)
nba_1 = nba_1.append(pd.read_csv("/Users/dannysimon/Documents/QARIK/OPUS/src/nba_stephencurry30_russwest44.csv", index_col=[0]), ignore_index = True)
nba_1 = nba_1.append(pd.read_csv("/Users/dannysimon/Documents/QARIK/OPUS/src/nba_new_players_jordan_poole_jokicnikolaofficial_melo.csv", index_col=[0]), ignore_index = True)
nba_1 = nba_1.append(pd.read_csv("/Users/dannysimon/Documents/QARIK/OPUS/src/nba_new_players_jamorant_anthony.csv", index_col=[0]), ignore_index = True)
nba_1['posts'] = [ast.literal_eval(x) for x in nba_1['posts']]
nba_final_df = nba_1


import plotly.express as px


def df_maker_1(df, ma, momentum, entity):
  df_entity_posts = df.loc[df.insta_handle == entity]['posts'].item()
  df_entity_posts.reverse()

  df_list = []
  df_nan_list = []
  df_nan_2_list = []
  
  value_list = []
  value_list_nan = []
  value_list_nan_2 = []

  momentum_value = 0
  momentum_value_nan = ma
  
  count = 0
  index_count = 1
  for post in df_entity_posts:
    _, values = zip(*post.items())
    if (values[0]['type'] == 'photo') and (values[0]['post_date'] > '2020-05-10'):  # 2020-04-20
      df_dict = {}
      try:
        value_list.append(values[0]['likes'])
        if count >= momentum:
          df_dict['momentum'] = values[0]['likes'] - value_list[momentum_value]
          momentum_value += 1
        else:
          df_dict['momentum'] = np.nan 
        count += 1
        df_dict['index'] = index_count
        df_dict['insta_handle'] = entity
        df_dict['date'] = values[0]['post_date']
        df_dict['date_month'] = values[0]['post_date']
        df_dict['likes'] = values[0]['likes']
        df_list.append(df_dict)
      except:
        likes_got = statistics.mean(value_list)
        value_list.append(likes_got)
        if count >= momentum:
          df_dict['momentum'] = likes_got - value_list[momentum_value]
          momentum_value += 1
        else:
          df_dict['momentum'] = np.nan 
        count += 1
        df_dict['insta_handle'] = entity
        df_dict['date'] = values[0]['post_date']
        df_dict['date_month'] = values[0]['post_date']
        df_dict['likes'] = likes_got
        df_list.append(df_dict)

  df_new = pd.DataFrame(df_list).sort_values(by=['date'])
  df_new['date'] = pd.to_datetime(df_new['date'])
  df_new['date_month'] = pd.to_datetime(df_new['date_month'])
  df_new = df_new.set_index('date')

  df_ma = df_new.copy()
  df_ma['likes'] = df_ma['likes'].rolling(window=ma, min_periods = 10).mean() #

  df_resample = df_new.copy()
  df_resample = df_resample.groupby('insta_handle').resample('D').mean().fillna(0)
  df_resample['likes'] = df_resample['likes'].rolling(window=ma).mean()
  df_resample = df_resample.reset_index()


  df_resample_nan = df_new.copy()
  df_resample_nan = df_resample_nan.groupby('insta_handle').resample('D').mean().fillna(0)
  # print(df_resample_nan.head(20))
  # df_resample_nan['likes'] = df_resample_nan['likes'].rolling(window=ma).mean()
  df_resample_nan = df_resample_nan.reset_index()

  count_nan = 0
  for index, row in df_resample_nan.iterrows():
    df_nan_dict = {}
    value_list_nan.append(row['likes'])

    df_nan_dict['date'] = row['date']
    df_nan_dict['insta_handle'] = entity
    if count_nan >= ma:
      df_nan_dict['likes'] = (np.nan if (sum(value_list_nan[-(ma+1):])) == 0 else (sum(value_list_nan[-(ma+1):]))) / ma
      df_nan_dict['likes_nan'] = (np.nan if sum(value_list_nan[-(ma+1):]) == 0 else sum(value_list_nan[-(ma+1):])) / (1 if (ma - value_list_nan[-(ma+1):].count(0)) == 0 else (ma - value_list_nan[-(ma+1):].count(0)))  # ma+1 or just ma
    else:
      df_nan_dict['likes'] = np.nan
      df_nan_dict['likes_nan'] = np.nan

    count_nan += 1
    df_nan_list.append(df_nan_dict)
  df_resample_nan_2 = pd.DataFrame(df_nan_list).sort_values(by=['date'])
  df_resample_nan_2['date'] = pd.to_datetime(df_resample_nan_2['date'])

  count_nan_2 = 0
  for index, row_2 in df_resample_nan_2.iterrows():
    df_nan_2_dict = {}
    value_list_nan_2.append(row_2['likes_nan'])

    df_nan_2_dict['date'] = row_2['date']  
    df_nan_2_dict['insta_handle'] = entity
    df_nan_2_dict['likes'] = row_2['likes']
    df_nan_2_dict['likes_nan'] = row_2['likes_nan']
    if (count_nan_2 >= (momentum+ma)):
      if not math.isnan(value_list_nan_2[-(momentum+momentum+1)]):
        df_nan_2_dict['momentum_absolute'] = row_2['likes_nan'] - value_list_nan_2[-(momentum+momentum+1)]
        # print(entity, row_2['date']  ,row_2['likes_nan'], value_list_nan_2[-(momentum+momentum+1)])
        df_nan_2_dict['momentum_relative'] = (row_2['likes_nan'] - ((0 if ((math.isnan(value_list_nan_2[-(momentum+momentum+1)])) or (value_list_nan_2[-(momentum+momentum+1)] == 0))  else value_list_nan_2[-(momentum+momentum+1)]))) / ((1 if ((math.isnan(value_list_nan_2[-(momentum+momentum+1)])) or (value_list_nan_2[-(momentum+momentum+1)] == 0))  else value_list_nan_2[-(momentum+momentum+1)]))
        momentum_value_nan += 1
    else:
      df_nan_2_dict['momentum_absolute'] = np.nan 
      df_nan_2_dict['momentum_relative'] = np.nan

    count_nan_2 += 1
    value_list_nan_2.append(row_2['likes_nan'])
    df_nan_2_list.append(df_nan_2_dict)
  df_resample_nan_3 = pd.DataFrame(df_nan_2_list).sort_values(by=['date'])
  df_resample_nan_3['date'] = pd.to_datetime(df_resample_nan_3['date'])


  df_grouped = df_new.groupby([(df_new.date_month.dt.year), (df_new.date_month.dt.month)]).agg('count')

  return df_new, df_ma, df_resample, df_resample_nan_2, df_resample_nan_3, df_grouped

def plot_maker_1(df, ma, momentum, entity = False):
  if entity:
    df_new, df_ma, df_resample, df_resample_nan_2, df_resample_nan_3, df_grouped = df_maker_1(df, ma, momentum, entity)

    fig_1 = px.line(df_new, x=df_new.index, y="likes", title='Instagram Post Likes VS Date')
    fig_1.show()

    fig_2 = px.line(df_ma, x=df_ma.index, y="likes", title='Instagram Post Likes VS Date (RMA - post focused)')
    fig_2.show()
    
    fig_3 = px.line(df_resample, x='date', y="likes", title='Instagram Post Likes VS Date (RMA - Time focused)')
    fig_3.show()

    fig_4 = px.line(df_ma, x='date_month', y="momentum", title='Instagram Post Likes VS Date (momentum - post focused)')
    fig_4.show()

    fig_4_b = px.line(df_resample, x='date', y="momentum", title='Instagram Post Likes VS Date (momentum - Time focused)')
    fig_4_b.show()

    fig_5 = px.line(df_resample_nan_2, x='date', y="likes_nan", title='Instagram Post Likes VS Date (RMA - considers nan, Time period focused)')
    fig_5.show()

    fig_6 = px.histogram(df_ma, x="date_month", y="likes",
             color='insta_handle', barmode='group', title='Month-Wise Total Like received',
             height=400)
    fig_6.show()

    fig_7 = px.line(df_resample_nan_3, x='date', y="momentum_absolute", title='Instagram Post Likes VS Date (Absolute Momentum)')
    fig_7.show()

    fig_8 = px.line(df_resample_nan_3, x='date', y="momentum_relative", title='Instagram Post Likes VS Date (Relative Momentum)')
    fig_8.show()

  else:
    df_new, df_ma, df_resample, df_resample_nan_2, df_resample_nan_3, df_grouped = df_maker_1(df, ma, momentum, 'kingjames') # change entity? jordan_poole. kingjames
    entities = df.insta_handle.unique()
    for entity in entities[1:]:
        df_new_e, df_ma_e, df_resample_e, df_resample_nan_2_e, df_resample_nan_3_e, df_grouped_e = df_maker_1(df, ma, momentum, entity)
        df_new = df_new.append(df_new_e)
        df_ma = df_ma.append(df_ma_e)
        df_resample = df_resample.append(df_resample_e)
        df_resample_nan_2 = df_resample_nan_2.append(df_resample_nan_2_e)
        df_resample_nan_3 = df_resample_nan_3.append(df_resample_nan_3_e)
        df_grouped = df_grouped.append(df_resample_e)
    fig_1 = px.line(df_new, x='date_month', y='likes', color = 'insta_handle',
                  hover_data={"date_month": "|%B %d, %Y"},
                  title='Instagram Post Likes VS Date')
    fig_1.update_xaxes(
        dtick="M1",
        tickformat="%b\n%Y")
    fig_1.show()

    fig_2 = px.line(df_ma, x='date_month', y='likes', color = 'insta_handle',
                  hover_data={"date_month": "|%B %d, %Y"},
                  title='Instagram Post Likes VS Date (RMA - post focused)')
    fig_2.update_xaxes(
        dtick="M1",
        tickformat="%b\n%Y")
    fig_2.show()

    fig_3 = px.line(df_resample, x='date', y='likes', color = 'insta_handle',
                  hover_data={"date": "|%B %d, %Y"},
                  title='Instagram Post Likes VS Date (RMA - Time period focused)')
    fig_3.update_xaxes(
        dtick="M1",
        tickformat="%b\n%Y")
    fig_3.show()

    fig_4 = px.line(df_ma, x='date_month', y='momentum', color = 'insta_handle',
                  hover_data={"date_month": "|%B %d, %Y"},
                  title='Instagram Post Likes VS Date (momentum - post focused)')
    fig_4.update_xaxes(
        dtick="M1",
        tickformat="%b\n%Y")
    fig_4.show()

    fig_4_b = px.line(df_resample, x='date', y='momentum', color = 'insta_handle',
                  hover_data={"date": "|%B %d, %Y"},
                  title='Instagram Post Likes VS Date (momentum - Time focused)')
    fig_4_b.update_xaxes(
        dtick="M1",
        tickformat="%b\n%Y")
    fig_4_b.show()

    fig_5 = px.line(df_resample_nan_2, x='date', y='likes_nan', color = 'insta_handle',
                  hover_data={"date": "|%B %d, %Y"},
                  title='Instagram Post Likes VS Date (RMA - considers nan, Time focused)')
    fig_5.update_xaxes(
        dtick="M1",
        tickformat="%b\n%Y")
    fig_5.show()

    fig_6 = px.histogram(df_ma, x="date_month", y="likes",
             color='insta_handle', barmode='group',
             title='Month-Wise Total Like received',
             height=400)
    fig_6.show()

    fig_7 = px.line(df_resample_nan_3, x='date', y='momentum_absolute', color = 'insta_handle',
              hover_data={"date": "|%B %d, %Y"},
              title='Instagram Post Likes VS Date ((Absolute Momentum))')
    fig_7.update_xaxes(
        dtick="M1",
        tickformat="%b\n%Y")
    fig_7.show()

    fig_8 = px.line(df_resample_nan_3, x='date', y='momentum_relative', color = 'insta_handle',
              hover_data={"date": "|%B %d, %Y"},
              title='Instagram Post Likes VS Date ((Relative Momentum))')
    fig_8.update_xaxes(
        dtick="M1",
        tickformat="%b\n%Y")
    fig_8.show()

    import pandas as pd
    import plotly.graph_objects as go
    from plotly.offline import iplot
    from plotly.subplots import make_subplots

    for entity_x in df_resample_nan_2.insta_handle.unique().tolist():
      df_resample_nan_2_entity =  df_resample_nan_2.loc[df_resample_nan_2.insta_handle == entity_x]
      df_resample_nan_3_entity =  df_resample_nan_3.loc[df_resample_nan_3.insta_handle == entity_x]
      # dict for the dataframes and their names
      dfs = {"Moving Average" : df_resample_nan_2_entity, "Relative Momentum": df_resample_nan_3_entity}

      # plot the data
      fig = go.Figure()
      fig = make_subplots(specs=[[{"secondary_y": True}]])

      for i in dfs:
        if i == 'Moving Average':
          fig.add_trace(go.Scatter(x = dfs[i]["date"],
                                        y = dfs[i]["likes_nan"], 
                                        name = i), secondary_y=False)
        elif i == 'Relative Momentum':
          fig.add_trace(go.Scatter(x = dfs[i]["date"],
                                        y = dfs[i]["momentum_relative"], 
                                        name = i), secondary_y=True)
      # Add figure title
      fig.update_layout(
          title_text=f"{entity_x}"
      )

      # Set x-axis title
      fig.update_xaxes(title_text="xaxis title")

      # Set y-axes titles
      fig.update_yaxes(title_text= f"Rolling Moving Average ({ma} Days)", secondary_y=False)
      fig.update_yaxes(title_text= f"Relative Momentum ({momentum} frame)", secondary_y=True)

      fig.show()
      try:
        points=np.array(dfs[i]["likes_nan"])
        #Changepoint detection with window-based search method
        model = "l2"  
        algo = rpt.Window(width=40, model=model).fit(points)
        my_bkps = algo.predict(n_bkps=10)
        rpt.show.display(points, my_bkps, figsize=(40, 7))
        plt.title('Change Point Detection: Window-Based Search Method')
        plt.show()

        points=np.array(df_new.loc[df_new.insta_handle==entity_x]["likes"])
        #Changepoint detection with window-based search method
        model = "l2"  
        algo = rpt.Window(width=40, model=model).fit(points)
        my_bkps = algo.predict(n_bkps=10)
        rpt.show.display(points, my_bkps, figsize=(40, 7))
        plt.title('Change Point Detection: Window-Based Search Method')
        plt.show()
      except:
        pass
    print(entities)

    return df_resample_nan_3



momentum_frame = 30
rolling_movinge_average_frame = 90
# nba_final_df = pd.read_csv("/Users/dannysimon/Documents/QARIK/OPUS/src/nba_final_df.csv")
#Give a instahandle id in entity to see player focused plots, else keep it as false
entity = False
# entity = 'kingjames'

# Run this function
# Give Entity a insta handle value to plot individually
momentum_df_1 = plot_maker_1(nba_final_df, rolling_movinge_average_frame, momentum_frame,entity)
sdbadsb