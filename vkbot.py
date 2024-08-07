import vk
import pandas as pd
import datetime
from time import sleep
import re
import random as r
import requests
from math import ceil as c

df1 = pd.read_excel('code/vk/bots.xlsx', sheet_name='credentials')
df2 = pd.read_excel('code/vk/bots.xlsx', sheet_name='message')
df3 = pd.read_excel('code/vk/bots.xlsx', sheet_name='groups')
df4 = pd.read_excel('code/vk/bots.xlsx', sheet_name='search')
df5 = pd.read_excel('code/vk/bots.xlsx', sheet_name='comment')
df6 = pd.read_excel('code/vk/bots.xlsx', sheet_name='district')
df7 = pd.read_excel('code/vk/bots.xlsx', sheet_name='raw_groups')
df8 = pd.read_excel('code/vk/bots.xlsx', sheet_name='published_posts')

n = int(input('Select number of bot >>> '))
access_token=str(df1['token'][n][45:265])
api = vk.API(access_token=access_token, v='5.199')           
bot = api.users.get(user_ids=df1['id'][n], v='5.199')
bot1 = bot[0]['first_name']+' '+bot[0]['last_name'] 
def groups():
    entry = int(input('0 >>> Excel\n1 >>> Join\n2 >>> Search\n3 >>> Leave\n5 >>> Sort\n6 >>> Fresh\n>>> '))
    df = pd.DataFrame()
    epoch = datetime.datetime.now().strftime('%s')
    end_time = int(epoch) - 864000
    ids, links, titles, members, cities, suggests, regions, new_regions, sub_regions, offset = [], [], [], [], [], [], [], [], [], 0
    if entry == 0:
        mygroups = api.groups.get(user_id=int(df1['id'][n]), v='5.199')
        for i in range(c(mygroups['count']/1000)):
            mygroups = api.groups.get(user_id=int(df1['id'][n]), offset=offset, fields=['members_count', 'city', 'can_suggest'],  extended=1, v='5.199')
            offset+=1000
            for i in mygroups['items']:
                for j in df4['word']:
                    try:
                        if i['members_count'] >= 1000 and i['can_suggest'] == 1 and j in str(i['name']):
                            ids.append(i['id'])
                            links.append(r'https://vk.com/' + i['screen_name'])
                            titles.append(i['name'])
                            members.append(i['members_count'])
                            suggests.append(i['can_suggest'])
                            regions.append(df1['region'][n])
                            if 'city' in i: cities.append(i['city']['title'])
                            else: cities.append('-')
                    except KeyError: print(KeyError)
    elif entry == 5:
        for i in range(0, len(list(df3['id']))):
            for id, j in enumerate(df6['city']):
                j = j[:-1]
                j = j.lower()
                if j in df3['title'][i].lower() and df3['id'][i] not in ids:
                    ids.append(df3['id'][i]) 
                    links.append(df3['link'][i])
                    titles.append(df3['title'][i])
                    members.append(df3['members'][i])
                    suggests.append(df3['suggest_post'][i])
                    cities.append(df3['city'][i])
                    regions.append(df3['region'][i])
                    new_regions.append(df6['region'][id])
                    break 
        for i1 in range(0, len(list(df3['id']))):
            if df3['id'][i1] not in ids:
                ids.append(df3['id'][i1]) 
                links.append(df3['link'][i1])
                titles.append(df3['title'][i1])
                members.append(df3['members'][i1])
                suggests.append(df3['suggest_post'][i1])
                cities.append(df3['city'][i1])
                regions.append(df3['region'][i1])
                new_regions.append('-')
        df['new_regions'] = new_regions
    elif entry == 1:
        mygroups = api.groups.get(user_id=int(df1['id'][n]), fields=['members_count', 'city', 'can_post', 'can_suggest'],  extended=1, v='5.199')
        last_id = int(input('Last id >>> '))
        for id, i in enumerate(df3['id']):
            if id >= last_id and df3['id'][id] not in [j['id'] for j in mygroups['items']] and df3['region'][id] == df1['region'][n]:
                try:
                    api.groups.join(group_id=i, v='5.199')
                    print('Id >>>', id, '<--> Row >>>', id+2)
                except vk.exceptions.VkAPIError as e:
                    if e.code == 14:
                        print(e.captcha_img)
                        captcha = input('Captcha code >>> ')
                        api.groups.join(group_id=i, captcha_sid=e.captcha_sid, captcha_key=captcha, v='5.199') 
                        print('Id >>>', id, '<--> Row >>>', id+2)                   
                    elif e.code == 5:
                        print('Connect again!')
                        break
                    elif e.code == 15: print(e.message)
                    else: 
                        print(e)
                        break
        session()
    elif entry == 2:
        entry = int(input('1 >>> One\n2 >>> Multiple\n>>> '))
        if entry == 1: 
            lst = ["подслушано", "черный список", "белый список", "ЧП", "ДТП", "типичний", "жесть", "бандитский"]
            for id, query in enumerate(df4['word']):
                print(id)
                query = query
                for j in lst:
                    search = api.groups.search(q=j+' '+query, extended=1, fields=['can_suggest', 'members_count', 'city'], v='5.199')
                    for i in search['items']:
                        if i['members_count'] >= 1000 and query in str(i['name']):
                            ids.append(i['id'])
                            links.append(r'https://vk.com/' + i['screen_name'])
                            titles.append(i['name'])
                            members.append(i['members_count'])
                            suggests.append(i['can_suggest'])
                            regions.append(query)
                            if 'city' in i: cities.append(i['city']['title'])
                            else: cities.append('-')
        elif entry == 2:
            for id, query in enumerate(df4['word']):
                query = query.strip()
                query = query
                search = api.groups.search(q=query, v='5.199')
                for j in range(3):
                    search = api.groups.search(q=query, offset=offset, extended=1, count=500, fields=['wall', 'can_suggest', 'members_count', 'city'], v='5.199')
                    ids1 = [i['id'] for i in search['items']]
                    offset += 500
                    print(len(ids1))
                    if len(ids1) > 0:
                        groups = api.groups.getById(group_ids=ids1, fields=['can_suggest', 'members_count', 'city'], v='5.199')
                        for i in groups['groups']:
                            if i['members_count'] >= 1000 and query.lower() in i['name'].lower():
                                ids.append(i['id'])
                                links.append(r'https://vk.com/' + i['screen_name'])
                                titles.append(i['name'])
                                members.append(i['members_count'])
                                suggests.append(i['can_suggest'])
                                regions.append(query)
                                if 'city' in i: cities.append(i['city']['title'])
                                else: cities.append('-')
    elif entry == 3:
        mygroups = api.groups.get(user_id=int(df1['id'][n]), v='5.199')
        if mygroups['count'] < 10:
            for id, i in enumerate(mygroups['items']):
                api.groups.leave(group_id=i['id'], v='5.199')
                print(id)
    elif entry == 6:
        entry = int(input('1 >>> From base\n2 >>> From YouScan\n>>> '))
        if entry == 1:
            for id, i in enumerate(df7['id']):
                try:
                    last_post = api.wall.get(owner_id=-i, v='5.199')
                    if last_post['items'][2]['date'] >= end_time:
                        ids.append(df7['id'][id])
                        links.append(df7['link'][id])
                        titles.append(df7['title'][id])
                        members.append(df7['members'][id])
                        cities.append(df7['city'][id])
                        suggests.append(df7['suggest_post'][id])
                        regions.append(df7['region'][id])
                        new_regions.append(df7['sub_region'][id]) 
                        print(id,' <--> ', id+2)
                except (vk.exceptions.VkAPIError, IndexError) : print('Check it', df3['link'][id])
            df['sub_region'] = new_regions 
        elif entry == 2:
            for i in df7['link']:
                i = i.split('_')
                links.append(i[0][20:])
            groups = api.groups.getById(group_ids=links,  v='5.199')
            for id, j in enumerate(groups['groups']):
                ids.append(j['id'])
                links.append(r'https://vk.com/' + j['screen_name'])
                titles.append(j['name'])
    #print(f"You have {mygroups['count']} groups!")
    df['id'] = ids
    df['link'] = links
    df['title'] = titles
    df['members'] = members
    df['city'] = cities
    df['suggest_post'] = suggests
    df['region'] = regions
    df.to_excel(bot1+'.xlsx')
    session()
def posts():
    entry = int(input('1 >>> Remove suggested post\n2 >>> Upload photo\n3 >>> Suggest post\n4 >>> Collect link on published post\n5 >>> Comment on post\n6 >>> Find post\n7 >>> Statistic of post\n8 >>> Upload video\n>>> '))
    if entry == 7:        
        ids = []
        df = pd.DataFrame()
        for i in df8['link']:
            k = i.split('wall')
            k = k[1]
            ids.append(k)       
        published_posts = api.wall.getById(posts=ids, v='5.199')
        links, likes, reposts, views, comments, dates, regions= [], [], [], [], [], [], [] 
        for j in published_posts['items']:
            for id, l in enumerate(df3['id']):
                if -j['from_id'] == int(l):
                    regions.append(df3['region'][id])
                    links.append('https://vk.com/wall'+str(j['from_id'])+'_'+str(j['id']))
                    likes.append(j['likes']['count'])
                    reposts.append(j['reposts']['count'])
                    views.append(j['views']['count'])
                    comments.append(j['comments']['count'])
                    dates.append(str(datetime.datetime.now())[:-7])
                
            if  -j['from_id'] not in list(df3['id']):
                print('https://vk.com/wall'+str(j['from_id'])+'_'+str(j['id']))
                regions.append('unknown')
                links.append('https://vk.com/wall'+str(j['from_id'])+'_'+str(j['id']))
                likes.append(j['likes']['count'])
                reposts.append(j['reposts']['count'])
                views.append(j['views']['count'])
                comments.append(j['comments']['count'])
                dates.append(str(datetime.datetime.now())[:-7])
        df = pd.DataFrame()
        df['region'] = regions
        df['link'] = links
        df['views'] = views
        df['likes'] = likes
        df['comments'] = comments
        df['reposts'] = reposts
        df['date'] = dates
        df.to_excel('statistic.xlsx')
        session()
    elif entry == 1:
        last_id = int(input('Last id >>> '))
        for id, i in enumerate(df3['id']):
            if df3['region'][id] == df1['region'][n]:
                if id >= last_id:
                    try:
                        check_post = api.wall.get(owner_id=-i, filter='suggests', v='5.199')
                        sleep(1)
                        print(id)
                    except vk.exceptions.VkAPIError as e: print(e.message)
                    if check_post['count'] != 0:
                        for j in check_post['items']:
                            try:
                                api.wall.delete(owner_id=-i, post_id=j['id'])
                                print('Id >>>', id, '<--> Row >>>', id+2)
                            except vk.exceptions.VkAPIError as e:
                                if e.code == 14:
                                    print(e.captcha_img)
                                    captcha = input('Captcha code >>> ')
                                    api.wall.delete(owner_id=-i, post_id=j['id'], captcha_sid=e.captcha_sid, captcha_key=captcha, v='5.199')
                                    print('Id >>>', id, '<--> Row >>>', id+2)

                                else: 
                                    print(e)
                                    break
        session()
    elif entry == 2:
        try:
            album = api.photos.getAlbums(owner_id=int(df1['id'][n]), v='5.199')
            album_id = album['items'][0]['id']
        except IndexError:
            album = api.photos.createAlbum(title='Разное', v='5.199')
            album = api.photos.getAlbums(owner_id=int(df1['id'][n]), v='5.199')
            album_id = album['items'][0]['id']
        server = api.photos.getUploadServer(album_id=album_id, v='5.199')
        url = server['upload_url']
        entry1 = int(input('Number of photos >>> '))
        for i in range(entry1):
            entry2 = input('Path to photo >>> ').strip("'")
            photo = requests.post(url, files={'file1':open(entry2, 'rb')})
            photo = photo.json()
            photo = api.photos.save(album_id=photo['aid'], server=photo['server'], photos_list=photo['photos_list'], hash=str(photo['hash']))
            print('photo'+str(photo[0]['owner_id'])+'_'+str(photo[0]['id'])) 
        exit()
    elif entry == 8:
        server = api.video.save(v='5.199')
        url = server['upload_url']
        entry1 = int(input('Number of videos >>> '))
        for i in range(entry1):
            entry2 = input('Path to video >>> ').strip("'")
            video = requests.post(url, files={'file1':open(entry2, 'rb')})
            video = video.json()
            print('video'+str(video['owner_id'])+'_'+str(video['video_id'])) 
     #   exit()
    elif entry == 3:
        message = df2['text'][n]
        photo1 = df2['photo_id1'][n]
        photo2 = df2['photo_id2'][n]
        last_id = int(input('Last id >>> '))
        for id, i in enumerate(df3['id']):
            if df3['region'][id] == df1['region'][n] and df3['suggest_post'][id] == 1:
                if id >= last_id:
                    try:
                        api.wall.post(owner_id=-i, message=message, attachments=[photo1, photo2], v='5.199')
                        print('Id >>>', id, '<--> Row >>>', id+2)
                    except vk.exceptions.VkAPIError as e:
                        if e.code == 214: 
                            try:
                                api.groups.join(group_id=i, v='5.199')
                                api.wall.post(owner_id=-i, message=message, attachments=[photo1, photo2], v='5.199')
                                print('Id >>>', id, '<--> Row >>>', id+2)
                            except vk.exceptions.VkAPIError as e:
                                if e.code == 14:
                                    try:
                                        print(e.captcha_img)
                                        captcha = input('Captcha code >>> ')
                                        api.groups.join(group_id=i, captcha_sid=e.captcha_sid, captcha_key=captcha, v='5.199')
                                        api.wall.post(owner_id=-i, message=message, attachments=[photo1, photo2], captcha_sid=e.captcha_sid, captcha_key=captcha, v='5.199')
                                        print('Id >>>', id, '<--> Row >>>', id+2)
                                    except: pass
                                elif e.code == 15:
                                    try:
                                        api.wall.post(owner_id=-i, message=message, attachments=[photo1, photo2], v='5.199')
                                        print('Id >>>', id, '<--> Row >>>', id+2)
                                    except: pass
                                elif e.code == 214:
                                    pass
                        elif e.code == 14:
                            print(e.captcha_img)
                            captcha = input('Captcha code >>> ')
                            api.wall.post(owner_id=-i, message=message, attachments=[photo1, photo2], captcha_sid=e.captcha_sid, captcha_key=captcha, v='5.199')
                            print('Id >>>', id, '<--> Row >>>', id+2)
                        elif e.code == 220: 
                            print('Too many recipient! Switch the bot!')
                            break
                        else: print(e)
    elif entry == 4:
        dates, links, posts = [], [], []
        for id, i in enumerate(df1['token']):
            try:
                access_token=str(df1['token'][id][45:265])
                api2 = vk.API(access_token=access_token, v='5.199') 
                df = pd.DataFrame()
                results = api2.notifications.get(count=100)
                for i in results['items']:
                    try:
                        if 'url' in i['action']:
                            if 'wall-' in i['action']['url'] and 'reply=' not in i['action']['url']:
                                dates.append(datetime.datetime.fromtimestamp(i['date']).strftime('%Y-%m-%d %H:%M:%S'))
                                links.append(i['action']['url'])
                                try: posts.append(i['text'])
                                except KeyError: posts.append('-')
                    except KeyError: pass
            except: pass
        df['date'] = dates
        df['link'] = links
        df['post'] = posts
        df.to_excel('published_posts.xlsx')

    elif entry == 5:
        h = int(input('Numbers of comments\n>>> '))
        t = r.randint(n, n+h-1)
        last_id = int(input('Last id >>> '))
        df = pd.DataFrame()
        links = []
        entry1 = '/home/m/1111.jpg' 
        #entry = input('Path to photo >>> ').strip("'")
        for id, i in enumerate(df8['link']):
            if id >= last_id: 
                #try:
                t = r.randint(n, n+h-1)
                link = i.split('wall')
                group = link[1].split('_')
                server = api.photos.getMessagesUploadServer(peer_id=df3['id'][n])
                url = server['upload_url']
                photo = requests.post(url, files={'file1':open(entry1, 'rb')})
                photo = photo.json()
                photo = api.photos.saveMessagesPhoto(photo=photo['photo'], server=photo['server'], hash=photo['hash'])
                c_photo1 = 'photo'+str(photo[0]['owner_id'])+'_'+str(photo[0]['id'])
                api.wall.createComment(owner_id=int(group[0]), post_id=int(group[1]), message='Hi', attachments=c_photo1, v='5.199')
                comments = api.wall.getComments(owner_id=int(group[0]), post_id=int(group[1]), sort='desc', count=100, v='5.199')
                print(id)
                for k in comments['items']:
                    if k['from_id'] == int(df1['id'][n]):
                        k1 = k['id']
                        print('https://vk.com/wall'+str(int(group[0]))+'_'+str(int(group[1]))+f'?reply={k1}')
                        links.append('https://vk.com/wall'+str(int(group))+'_'+str(int(link[1]))+f'?reply={k1}')
                sleep(3)
               # except vk.exceptions.VkAPIError as e:
                #    if e.code == 213: print(e.message)
                 #   elif e.code == 14:
                  #      print(e.captcha_img)
                   #     captcha = input('Captcha code >>> ')
                  #      api.wall.createComment(owner_id=int(group), post_id=int(link[1]), message=df5['text'][t], attachments=[df5['photo_id1'][n], df5['photo_id2'][n]], captcha_sid=e.captcha_sid, captcha_key=captcha, v='5.199') 
#                    else : print(e.message)
       # df['link'] = links
       # df.to_excel(df3['name'][n]+'-comments.xlsx')

    elif entry == 6:
        df = pd.DataFrame()
        banned_bots = [k for k in df1['id']]
        links, texts, regions = [], [], []
        last_id = int(input('Last id >>> '))
        for id, i in enumerate(df3['id']):
            if df3['suggest_post'][id] == 1:
                if id >= last_id:
                    try:
                        get_post = api.wall.get(owner_id=-i, extended=1,  v='5.199')
                        for j in get_post['items']:
                            if 'signer_id' in j:
                                if j['signer_id'] in banned_bots:
                                    print(f'https://vk.com/wall-{i}_{j["id"]}')
                                    print(j['text'])
                                    links.append(f'https://vk.com/wall-{i}_{j["id"]}')
                                    texts.append(j['text'])
                                    regions.append(df3['region'][id])
                        print(id)
                    except vk.exceptions.VkAPIError as e:
                        if e.code == 15: pass
        df['link'] = links
        df['text'] = texts
        df['region'] = regions
        df.to_excel('published_posts.xlsx')
def messages():
    entry = int(input('1 >>> Get last message\n2 >>> Remove all messages\n3 >>> Send message to admins\n4 >>> Send message to user\n5 >>> Get message from specific ids\n>>> ')) 
    results = api.messages.getConversations(count=200, v='5.199')
    if entry == 1:
        df = pd.DataFrame()
        region = df1['region'][n]
        ids, links, titles, responses = [], [], [], []
        for id, i in enumerate(results['items']):
            if re.search(r'\d', i['last_message']['text']):
                group = api.groups.getById(group_id=i['conversation']['peer']['local_id'], v='5.199')
                ids.append(group['groups'][0]['id'])
                links.append(str(r'https://vk.com/'+str(group['groups'][0]['screen_name'])))
                titles.append(group['groups'][0]['name'])
                responses.append(i['last_message']['text'])
                print(id)
                sleep(1)
        df['id'] = ids
        df['link'] = links
        df['title'] = titles       
        df['response'] = responses
        df.to_excel(region+'.xlsx', sheet_name=region)
    elif entry == 2:
        for id, i in enumerate(results['items']):
            api.messages.deleteConversation(peer_id=i['conversation']['peer']['id'], v='5.199')
            print(id)
            sleep(1)
    elif entry == 3:
        name = df1['region'][n]
        message = df2['text'][n]
        df = pd.read_excel('prices.xlsx', sheet_name=name)
        last_id = int(input('Last id >>> '))
        for id, i in enumerate(df['id']):
            if id >= last_id:
                try:
                    api.messages.send(peer_id=-i, random_id=0, message=message, v='5.199')
                    print('Id >>>', id, '<--> Row >>>', id+2)
                    sleep(5)
                except vk.exceptions.VkAPIError as e:
                    if e.code == 7:
                        print('Cannot contact!')
    elif entry == 4: 
        print('Under development!!!')

    elif entry == 5:
        df = pd.DataFrame()
        region = df1['region'][n]
        ids, links, titles, responses = [], [], [], []
        specific_ids = pd.read_excel('prices.xlsx', sheet_name=region)
        for id, i in enumerate(results['items']):
            if i['conversation']['peer']['local_id'] in list(specific_ids['id']) and i['last_message']['from_id'] != int(df1['id'][n]) :
                group = api.groups.getById(group_id=i['conversation']['peer']['local_id'], v='5.199')
                ids.append(group['groups'][0]['id'])
                links.append(str(r'https://vk.com/'+str(group['groups'][0]['screen_name'])))
                titles.append(group['groups'][0]['name'])
                responses.append(i['last_message']['text'])
                print(id)
                sleep(1)
        df['id'] = ids
        df['link'] = links
        df['title'] = titles       
        df['response'] = responses
        df.to_excel(region+'1.xlsx', sheet_name=region)
def get_paricipants():
    name = input('Link of group >>> ')
    name = str(name[15:])
    df = pd.DataFrame()
    ids, links, names, surnames, cities = [], [], [], [], [] 
    group = api.groups.getById(group_id=name, fields=['members_count'], extended=1, v='5.199') 
    group_id = group['groups'][0]['id']
    try:
        offset = 0
        while True:
            participats = api.groups.getMembers(group_id=group_id, offset=offset, count=1000, fields='city, can_write_private_message', v='5.199')
            if  offset >= group['groups'][0]['members_count']: break
            for i in participats['items']:
                if i['can_write_private_message']:
                    ids.append(i['id'])
                    links.append('https://vk.com/id' + str(i['id']))
                    names.append(i['first_name'])
                    surnames.append(i['last_name'])
                    if 'city' in i: cities.append(i['city']['title'])
                    else: cities.append('-')
            offset += 1000
            print(offset)
        df['id'] = ids
        df['link'] = links
        df['name'] = names
        df['surname'] = surnames
        df['city'] = cities
        df.to_excel('paricipants.xlsx')
    except vk.exceptions.VkAPIError as e:
        if e.code == 15:
            print('Hide group!')
        else: print(e)


def friends():
    bots = [i for i in df1['id']]
    my_friends = api.friends.get(user_id=int(df1['id'][n]), v='5.199')
    for i in my_friends['items']:
        if i in bots:
            api.friends.delete(user_id=i, v='5.199')
            print('Removing >>> ', i)
    session()
def news():
    entry = int(input('1 >>> Youscan\n2 >>> News\n>>> '))
    if entry == 1:
        df0 = pd.read_excel('links.xlsx')
        df = pd.DataFrame()
        h = int(input('Numbers of comments\n>>> '))
        links = [] 
         
    if entry == 2:
        df = pd.DataFrame()
        links = []
        epoch = datetime.datetime.now().strftime('%s')
        start_time = int(epoch) - 36000
        end_time = int(epoch) - 7000
        h = int(input('Numbers of comments\n>>> '))
        news  = api.newsfeed.search(q='news', start_time=start_time, end_time=end_time, count=200, v='5.199')
        for i in news['items']:
            try:
                if 'views' in i:
                    if i['comments']['can_post'] == 1 and i['views']['count'] >= 1000:
                        t = r.randint(n, n+h-1)
                        api.wall.createComment(owner_id=i['owner_id'], post_id=i['id'], message=df5['text'][t], attachments=[df5['photo_id1'][n], df5['photo_id1'][n]], v='5.199')
                        comments = api.wall.getComments(owner_id=i['owner_id'], count=100, sort='desc', post_id=i['id'], v='5.199')
                        sleep(1)
                        for k in comments['items']:
                            if k['from_id'] == int(df1['id'][n]):
                                k1 = k['id']
                                print(id,' <--> ',id+2, 'https://vk.com/wall'+str(i['owner_id'])+'_'+str(i['id'])+f'?reply={k1}')
                                links.append('https://vk.com/wall'+str(i['owner_id'])+'_'+str(i['id'])+f'?reply={k1}')
                                break
                        sleep(10)
            except vk.exceptions.VkAPIError as e:
                if e.code == 213: pass        
        df['link'] = links
#        df.to_excel('comments.xlsx')
    elif entry == 3:
        df0 = pd.read_excel('links.xlsx')
        print(len(list(df0['link'])))
        print(len(set(df0['link'])))

def session():
    print(f'{bot1}\n0 >>> write_to_excel\n1 >>> groups\n2 >>> posts\n3 >>> messages\n4 >>> get_paricipants\n5 >>> uniq_groups\n6 >>> remove_friend\n7 >>> news')
    entry = int(input('>>> '))
    if entry == 1: groups()
    elif entry == 2: posts()
    elif entry == 3: messages()
    elif entry == 4: get_paricipants()
    elif entry == 5: uniq_groups()
    elif entry == 6: friends()
    elif entry == 7: news()
    elif entry == 10:
        last_id = int(input('Last id >>> '))
        for id, i in enumerate(df1['token']):
            if id >= last_id:
                print(id)
                access_token=str(df1['token'][id][45:265])
                api = vk.API(access_token=access_token, v='5.199')
                post = api.wall.get(owner_id=-52468701, count=14, v='5.199')
                for i in post['items'][1:]: 
                    api.wall.repost(object='wall'+str(-52468701)+'_'+str(i['id']))
                    sleep(5)
                    print(i['id'])
                    api.likes.add(type='post', owner_id=-52468701, item_id=i['id'])
                    sleep(5)
    elif entry == 11:
        last_id = int(input('Last id >>> '))
        for id, i in enumerate(df1['token']):
            if id >= last_id:
                print(id)
                access_token=str(df1['token'][id][45:265])
                api = vk.API(access_token=access_token, v='5.199') 
                try: 
                    api.likes.add(type='comment', owner_id=-202415347, item_id=73887)
                    sleep(1)
                except vk.exceptions.VkAPIError as e: 
                    if e.code == 5: pass
session()


