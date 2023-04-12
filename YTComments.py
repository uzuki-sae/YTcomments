import requests
import json
import sys

args = sys.argv


URL = 'https://www.googleapis.com/youtube/v3/'
# ここにAPI KEYを入力
API_KEY = 'AIzaSyCD_vIKS2v89k-xpb0GeEkJ3qAgnmHLv1M'
# ここにVideo IDを入力
VIDEO_ID = args[1]
vid = str(VIDEO_ID)
print(vid)
f = open(vid,'a')
def print_video_comment(no, video_id, next_page_token):
  params = {
    'key': API_KEY,
    'part': 'snippet',
    'videoId': video_id,
    'order': 'relevance',
    'textFormat': 'plaintext',
    'maxResults': 100,
  }
  if next_page_token is not None:
    params['pageToken'] = next_page_token
  response = requests.get(URL + 'commentThreads', params=params)
  resource = response.json()

  for comment_info in resource['items']:
    # コメント
    text = comment_info['snippet']['topLevelComment']['snippet']['textDisplay']
    # グッド数
    like_cnt = comment_info['snippet']['topLevelComment']['snippet']['likeCount']
    # 返信数
    reply_cnt = comment_info['snippet']['totalReplyCount']
    # ユーザー名
    user_name = comment_info['snippet']['topLevelComment']['snippet']['authorDisplayName']
    # Id
    parentId = comment_info['snippet']['topLevelComment']['id']
    return('{:0=4},{},{},{},{}'.format(no, text.replace('\r', '\n').replace('\n', ' '), like_cnt, user_name, reply_cnt))
    if reply_cnt > 0:
      cno = 1
      print_video_reply(no, cno, video_id, None, parentId)
    no = no + 1

  if 'nextPageToken' in resource:
    print_video_comment(no, video_id, resource["nextPageToken"])


def print_video_reply(no, cno, video_id, next_page_token, id):
  params = {
    'key': API_KEY,
    'part': 'snippet',
    'videoId': video_id,
    'textFormat': 'plaintext',
    'maxResults': 50,
    'parentId': id,
  }

  if next_page_token is not None:
    params['pageToken'] = next_page_token
  response = requests.get(URL + 'comments', params=params)
  resource = response.json()

  for comment_info in resource['items']:
    # コメント
    text = comment_info['snippet']['textDisplay']
    # グッド数
    like_cnt = comment_info['snippet']['likeCount']
    # ユーザー名
    user_name = comment_info['snippet']['authorDisplayName']

    return('{:0=4}-{:0=3},{},{},{}'.format(no, cno, text.replace('\r', '\n').replace('\n', ' '), like_cnt, user_name))
     
    cno = cno + 1

  if 'nextPageToken' in resource:
    print_video_reply(no, cno, video_id, resource["nextPageToken"], id)


# コメントを全取得する
video_id = VIDEO_ID
no = 1
x = print_video_comment(no, video_id, None)
print(x)
f.write(x)
f.close()



