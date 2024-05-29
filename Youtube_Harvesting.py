from googleapiclient.discovery import build
import pymongo
import pandas as pd
import streamlit as st
import mysql.connector


#*************************************************************************************************************************************************************************************
#Connecting API

def Api_connect():
  Api_Id = "AIzaSyD21kFVzRSqJkArl3QgcwcmCwcoe4ztqlo"

  api_service_name = "youtube"
  api_version = "v3"

  youtube = build(api_service_name, api_version, developerKey=Api_Id)

  return youtube
youtube = Api_connect()

#*************************************************************************************************************************************************************************************

#get channel information using channel_ids


def get_channel_info (channel_id):
  request= youtube.channels().list(
      part= "snippet, ContentDetails, statistics",
      id = channel_id)
  
  response=request.execute()
  
  for i in response ["items"]:
    data = dict(Channel_Name=i["snippet"]["title"],
                Channel_Id = i["id"],
                Subscribers=i["statistics"]["subscriberCount"],
                Views = i["statistics"]["viewCount"],
                Total_Videos = i["statistics"]["videoCount"],
                Channel_Description = i["snippet"]["description"],
                Playlist_ID = i["contentDetails"]["relatedPlaylists"]["uploads"]
                )
     
  return data
#*************************************************************************************************************************************************************************************
#get Video ids using channel ids

def get_videos_ids(channel_id):
  video_ids =[]
  response = youtube.channels().list(id=channel_id, part ='contentDetails').execute()
  Playlist_Id=response["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]

  next_page_token = None

  while True:
    response1=youtube.playlistItems().list(
                                          part='snippet',
                                          playlistId=Playlist_Id,
                                          maxResults=50,
                                          pageToken=next_page_token).execute()
    for i in range (len(response1["items"])):
      video_ids.append(response1["items"][i]["snippet"]["resourceId"]["videoId"])
    next_page_token=response1.get("nextPageToken")

    if next_page_token is None:
      break
  return video_ids

#*************************************************************************************************************************************************************************************
#get video information using video ids
def get_video_info(video_ids):


  Video_Data = []

  for video_id in video_ids:
    request=youtube.videos().list(
        part= "snippet, ContentDetails, statistics",
        id = video_id
    )
    response=request.execute()

    for item in response["items"]:
      data = dict(Channel_Name=item["snippet"]["channelTitle"],
                  Channel_Id = item["snippet"]["channelId"],
                  Video_Id =item["id"],
                  Title = item["snippet"]["title"],
                  Tags = item["snippet"].get("tags"),
                  Thumbnails = item ["snippet"]["thumbnails"]['default']['url'],
                  Description = item["snippet"].get("description"),
                  Published_date = item["snippet"]["publishedAt"],
                  Duration = item["contentDetails"]["duration"],
                  Views = item["statistics"].get("viewCount"),
                  Likes = item["statistics"].get("likeCount"),
                  Dislike = item["statistics"].get("dislike"),
                  Comments_Count = item["statistics"].get("commentCount"),
                  Favorite_Count = item ["statistics"]["favoriteCount"],
                  Definition = item ["contentDetails"]["definition"],
                  Caption_Status = item["contentDetails"]["caption"]

                  )
      Video_Data.append(data)
  return Video_Data
#*************************************************************************************************************************************************************************************

#get comment information
def get_comment_info(video_ids):
  Comment_data = []
  try:
    for i in video_ids:
      request = youtube.commentThreads().list(
        part = 'snippet',
        videoId = i,
        maxResults = 50
      )
      response = request.execute()
      for item in response ["items"]:
        data = dict(Comment_Id = item['snippet']["topLevelComment"]["id"],
                    Video_Id = item['snippet']['topLevelComment']["snippet"]["videoId"],
                    Comment_Text =item['snippet']['topLevelComment']["snippet"]["textDisplay"],
                    Comment_Author = item['snippet']['topLevelComment']["snippet"]["authorDisplayName"], 
                    Comment_Published = item['snippet']['topLevelComment']["snippet"]["publishedAt"])
        Comment_data.append(data)
  except:
    pass
  return Comment_data
#*************************************************************************************************************************************************************************************
#get all details and insert into mongo DB
def channel_details (channel_id):
  
  Channel_info = get_channel_info (channel_id)
  video_ids = get_videos_ids (channel_id)
  video_information = get_video_info (video_ids)
  Comment_details = get_comment_info(video_ids)
  
  #connect to mongo DB

  client=pymongo.MongoClient("mongodb://localhost:27017")

  db = client["Youtube_data"]
  coll1 = db["channel_details"]
  
  coll1.insert_one({"channel_information": Channel_info, "videoinfo":video_information, "Comment_info": Comment_details})
  return"upload completed successfully"


#*************************************************************************************************************************************************************************************#-----------------------------------------------------------------------------------------------------------------------------------------------------
#Connecting Mysql/ Creating tables/Inserting tables


mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="Password@123",
  database="Youtube_Harvesting"
)
#create database
mycursor = mydb.cursor()

#*************************************************************************************************************************************************************************************
#Channel details

def Channel_Table (channel_name):
  mycursor.execute ('''create table if not exists Channel (Channel_Name varchar(100),
                                                                  Channel_Id varchar (100) primary key,
                                                                  Subscribers bigint,
                                                                  Views bigint,
                                                                  Total_Videos int,
                                                                  Channel_Description text,
                                                                  Playlist_ID varchar (80))''')

  client=pymongo.MongoClient("mongodb://localhost:27017")
  db=client["Youtube_data"]   
  coll1 = db['channel_details']



  sql= "SELECT * FROM channel"
  mycursor.execute(sql)
  table= mycursor.fetchall()
  mydb.commit()

  chann_list= []
  chann_list2= []
  df_all_channels= pd.DataFrame(table)

  chann_list.append(df_all_channels[0])
  for i in chann_list[0]:
      chann_list2.append(i)
  

  if channel_name in chann_list2:
      exists= f"Your Provided Channel {channel_name} is Already exists"        
      return exists
  
  else:

      ch_list = []
      coll1=db["channel_details"]
      coll1= coll1.find_one({"channel_information.Channel_Name":channel_name})
      ch_list.append(coll1["channel_information"])

      df = pd.DataFrame(ch_list)
      Channeldetails = []
      for index in df.index:
        row = df.loc[index].values
        row = tuple([str(d) for d in row])
        Channeldetails.append(row)


        channel = "insert into Channel values (%s, %s,%s,%s,%s,%s,%s )"
        mycursor.executemany(channel,Channeldetails)
        mydb.commit()
#*************************************************************************************************************************************************************************************
#video details
def Video_Table (channel_name):
  mycursor.execute('''create table if not exists videos(Channel_Name varchar (100),
                                                    Channel_Id varchar(100),
                                                    Video_Id  varchar (30),
                                                    Title  varchar (200),
                                                    Tags text,
                                                    Thumbnails varchar (250),
                                                    Description text,
                                                    Published_date varchar (250),
                                                    Duration varchar (50),
                                                    Views varchar (50),
                                                    Likes varchar (50),
                                                    Dislikes varchar (50),
                                                    Comments_Count varchar (50),
                                                    Favorite_Count varchar (50),
                                                    Definition varchar (20),
                                                    Caption_Status varchar (50))''')
  #Video details
  V_list = []
  db=client["Youtube_data"]   
  coll1 = db['channel_details']

  for coll in coll1.find_one({"channel_information.Channel_Name":channel_name},{"_id":0})["videoinfo"]:
    V_list.append(coll)

  df1 = pd.DataFrame(V_list)

  df1['Published_date']=pd.to_datetime(df1['Published_date'])


  videodata = []
  for index in df1.index:
      row = df1.loc[index].values
      row = tuple([str(d) for d in row])
      videodata.append(row)

  videos_list = "insert into videos values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
  mycursor.executemany(videos_list,videodata)
  mydb.commit()

#*************************************************************************************************************************************************************************************                                                                         
                                                                            
def Comment_Table (channel_name):                                                                
  mycursor.execute('''create table if not exists comments (Comment_Id varchar (50),
                                                  Video_ID varchar(100),
                                                  Comment_Text text ,
                                                  Comment_Author varchar (50),
                                                  Comment_Published varchar (50))''')
  #Comments

  db=client["Youtube_data"]   
  coll1 = db['channel_details']

  cmtlist = []
  for coll in coll1.find_one({"channel_information.Channel_Name":channel_name},{"_id":0})["Comment_info"]:
    cmtlist.append(coll)

  df2 = pd.DataFrame(cmtlist)

  Commentdetails = []
  for index in df2.index:
      row = df2.loc[index].values
      row = tuple([str(d) for d in row])
      Commentdetails.append(row)

  cmt_list = "insert into comments values (%s,%s,%s,%s,%s)" 
  mycursor.executemany(cmt_list,Commentdetails)
  mydb.commit()


def tables(channel_name):
  ch = Channel_Table(channel_name)
  if ch:
    st.write (ch)
    Video_Table(channel_name)
    Comment_Table(channel_name)
  return "Tables Created Successfully"


#*************************************************************************************************************************************************************************************

client=pymongo.MongoClient("mongodb://localhost:27017")

def show_channels_table():
    ch_list=[]
    db=client["Youtube_data"]
    coll1=db["channel_details"]
    for ch_data in coll1.find({},{"_id":0,"channel_information":1}):
        ch_list.append(ch_data["channel_information"])
    df=st.dataframe(ch_list)

    return df

def show_videos_table():
    vi_list=[]
    db=client["Youtube_data"]
    coll1=db["channel_details"]
    for vi_data in coll1.find({},{"_id":0,"videoinfo":1}):
        for i in range(len(vi_data["videoinfo"])):
            vi_list.append(vi_data["videoinfo"][i])
    df2=st.dataframe(vi_list)

    return df2

def show_comments_table():
    com_list=[]
    db=client["Youtube_data"]
    coll1=db["channel_details"]
    for com_data in coll1.find({},{"_id":0,"Comment_info":1}):
        for i in range(len(com_data["Comment_info"])):
            com_list.append(com_data["Comment_info"][i])
    
    df3 =st.dataframe(com_list)
    return df3

#*************************************************************************************************************************************************************************************-----------------------------------------------------------------------------------------------------
if st.button ("Yout tube data harvesting"):
    st.header("Skill Take Away")
    st.caption("Python Scripting, Data Collection, MongoDB, API Integration, Data Management using MongoDB and SQL")
#*************************************************************************************************************************************************************************************-----------------------------------------------------------------------------------------------------------------------------------------
client=pymongo.MongoClient("mongodb://localhost:27017")
channel_id=st.text_input("Enter the channel ID")

if st.button("collect and store data"):
    ch_ids=[]

    db=client["Youtube_data"]
    coll1=db["channel_details"]
    for ch_data in coll1.find({},{"_id":0,"channel_information":1}):
        ch_ids.append(ch_data["channel_information"]["Channel_Id"])

    if channel_id in ch_ids:
        st.success("Channel id is already exists")

    else:
        insert=channel_details(channel_id)
        st.success(insert)

#*************************************************************************************************************************************************************************************---------------------------------------------------------------------------------------------------------------------------------------------------
client=pymongo.MongoClient("mongodb://localhost:27017")
db=client["Youtube_data"] 

all_channels= []
coll1=db["channel_details"]
for ch_data in coll1.find({},{"_id":0,"channel_information":1}):
  all_channels.append(ch_data["channel_information"]["Channel_Name"])
unique_channel= st.selectbox("Select the Channel",all_channels)

#*************************************************************************************************************************************************************************************=========================================================================================================================================================
if st.button("Migrate to Sql"):
    Table=tables(unique_channel)
    st.success(Table)

show_table=st.radio("SELECT THE TABLE FOR VIEW",("CHANNELS","VIDEOS","COMMENTS"))

if show_table=="CHANNELS":
    show_channels_table()

elif show_table=="VIDEOS":
    show_videos_table()

elif show_table=="COMMENTS":
    show_comments_table()


#*************************************************************************************************************************************************************************************


#SQL Connection

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="Password@123",
  database="Youtube_Harvesting"
)
mycursor = mydb.cursor(buffered=True)                                                                     #since i had issue i have added buffered=True)

question=st.selectbox("Select your question",("1. All the channel names",
                                              "2. channels with most number of videos",
                                              "3. 10 most viewed videos",
                                              "4. comments in each videos",
                                              "5. Videos with higest likes",
                                              "6. likes of all videos",
                                              "7. views of each channel",
                                              "8. videos published in the year of 2022",
                                              "9. average duration of all videos in each channel",
                                              "10. videos with highest number of comments",
                                              "11. compare all channels"))

if question=="1. All the channel names":
    query1='''select channel_name from channel'''
    mycursor.execute(query1)
    mydb.commit()
    t1=mycursor.fetchall()
    df=pd.DataFrame(t1)
    st.write(df)


elif question=="2. channels with most number of videos":
    query2='''select channel_name as channelname,total_videos as no_videos from channel
                order by total_videos desc'''
    mycursor.execute(query2)
    mydb.commit()
    t2=mycursor.fetchall()
    df2=pd.DataFrame(t2,columns=["channel name","No of videos"])
    st.write(df2)

elif question=="3. 10 most viewed videos":
    query3='''select views as views,channel_name as channelname,title as videotitle from videos 
                where views is not null order by views desc limit 10'''
    mycursor.execute(query3)
    mydb.commit()
    t3=mycursor.fetchall()
    df3=pd.DataFrame(t3,columns=["views","channel name","videotitle"])
    st.write(df3)

elif question=="4. comments in each videos":
    query4='''select comments_count as no_comments,title as videotitle from videos where comments_count is not null'''
    mycursor.execute(query4)
    mydb.commit()
    t4=mycursor.fetchall()
    df4=pd.DataFrame(t4,columns=["no of comments","videotitle"])
    st.write(df4)

elif question=="5. Videos with higest likes":
    query5='''select title as videotitle,channel_name as channelname,likes as likecount
                from videos where likes is not null order by likes desc'''
    mycursor.execute(query5)
    mydb.commit()
    t5=mycursor.fetchall()
    df5=pd.DataFrame(t5,columns=["videotitle","channelname","likecount"])
    st.write(df5)

elif question=="6. likes of all videos":
    query6='''select likes as likecount,title as videotitle from videos'''
    mycursor.execute(query6)
    mydb.commit()
    t6=mycursor.fetchall()
    df6=pd.DataFrame(t6,columns=["likecount","videotitle"])
    st.write(df6)

elif question=="7. views of each channel":
    query7='''select channel_name as channelname ,views as totalviews from channel'''
    mycursor.execute(query7)
    mydb.commit()
    t7=mycursor.fetchall()
    df7=pd.DataFrame(t7,columns=["channel name","totalviews"])
    st.write(df7)

elif question=="8. videos published in the year of 2022":
    query8='''select title as video_title,published_date as videorelease,channel_name as channelname from videos
                where extract(year from published_date)=2022'''
    mycursor.execute(query8)
    mydb.commit()
    t8=mycursor.fetchall()
    df8=pd.DataFrame(t8,columns=["videotitle","published_date","channelname"])
    st.write(df8)

elif question=="9. average duration of all videos in each channel":
    query9='''select channel_name as channelname,AVG(duration) as averageduration from videos group by channel_name'''
    mycursor.execute(query9)
    mydb.commit()
    t9=mycursor.fetchall()
    df9=pd.DataFrame(t9,columns=["channelname","averageduration"])

    T9=[]
    for index,row in df9.iterrows():
        channel_title=row["channelname"]
        average_duration=row["averageduration"]
        average_duration_str=str(average_duration)
        T9.append(dict(channeltitle=channel_title,avgduration=average_duration_str))
    df1=pd.DataFrame(T9)
    st.write(df1)

elif question=="10. videos with highest number of comments":
    query10='''select title as videotitle, channel_name as channelname,comments_count as comments from videos where comments_count is not null order by comments desc'''
    mycursor.execute(query10)
    mydb.commit()
    t10=mycursor.fetchall()
    df10=pd.DataFrame(t10,columns=["video title","channel name","comments"])
    st.write(df10)

elif question=="11. compare all channels":
   query11 = '''select Channel_Name, Subscribers, Views, Total_Videos from channel'''
   mycursor.execute(query11)
   mydb.commit()
   t11=mycursor.fetchall()
   df11=pd.DataFrame(t11,columns=["Channel Name","Total Subscription","Total Views", "Total Videos"])
   st.write(df11)
    
#*************************************************************************************************************************************************************************************