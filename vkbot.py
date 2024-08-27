import vk
import pandas as pd
import datetime
from time import sleep
import re
import random as r
import requests
import vk_captchasolver as vc
import urllib.request
from math import ceil as c

df1 = pd.read_excel('code/vk/bots.xlsx', sheet_name='credentials')
df2 = pd.read_excel('code/vk/bots.xlsx', sheet_name='message')
df3 = pd.read_excel('code/vk/bots.xlsx', sheet_name='groups')
df4 = pd.read_excel('code/vk/bots.xlsx', sheet_name='search')
df5 = pd.read_excel('code/vk/bots.xlsx', sheet_name='comment')
df6 = pd.read_excel('code/vk/bots.xlsx', sheet_name='district')
df7 = pd.read_excel('code/vk/bots.xlsx', sheet_name='raw_groups')
df8 = pd.read_excel('code/vk/bots.xlsx', sheet_name='published_posts')
df9 = pd.read_excel('code/vk/bots.xlsx', sheet_name='dead_bots')
n = int(input('Select number of bot >>> '))
access_token=str(df1['token'][n][45:265])
api = vk.API(access_token=access_token, v='5.199')           
bot = api.users.get(user_ids=df1['id'][n], v='5.199')
bot1 = bot[0]['first_name']+' '+bot[0]['last_name'] 
df = pd.DataFrame()
save_as = 'code.jpg'

ids, links, titles, members, cities, suggests, regions, sub_regions, likes, reposts, views, comments, dates, posts = [], [], [], [], [], [], [], [], [], [], [], [], [], []

def xlsx():
    df['id'] = ids
    df['link'] = links
    df['title'] = titles
    df['members'] = members
    df['city'] = cities
    df['suggest_post'] = suggests
    df['sub_region'] = sub_regions 
    df['region'] = regions
    df.to_excel(bot1+'.xlsx')

def captcha_solver(image=''):
    global captcha
    captcha = vc.solve(image=save_as)
    return captcha

def download_image(url, save_as):
    urllib.request.urlretrieve(url, save_as)

def groups():
    entry = int(input('0 >>> Excel\n1 >>> Join\n2 >>> Search\n3 >>> Leave\n5 >>> Sort\n6 >>> Fresh\n7 >>> Join special\n>>> ')) 
    offset = 0
    epoch = datetime.datetime.now().strftime('%s')
    end_time = int(epoch) - 864000
    if entry == 0:
        for i in range(5):
            mygroups = api.groups.get(user_id=int(df1['id'][n]), offset=offset, fields=['members_count', 'city', 'can_suggest'],  extended=1, v='5.199')
            offset+=1000
            for i in mygroups['items']:
                if i['members_count'] >= 1000 and i['can_suggest'] == 1 and i['id'] not in ids and i['id'] not in list(df3['id']):
                    ids.append(i['id'])
                    links.append(r'https://vk.com/' + i['screen_name'])
                    titles.append(i['name'])
                    members.append(i['members_count'])
                    suggests.append(i['can_suggest'])
                    if 'city' in i: cities.append(i['city']['title'])
                    else: cities.append('-')
                    regions.append('-')
                    sub_regions.append('-')
        xlsx()
    elif entry == 5:
        for id, i in enumerate(df7['title']):
            if 'халтура' not in i.lower() and 'работа' not in i.lower() and 'авторынок' not in i.lower():
                ids.append(df7['id'][id])
                links.append(df7['link'][id])
                titles.append(df7['title'][id])
                members.append(df7['members'][id])
                suggests.append(df7['suggest_post'][id])
                cities.append(df7['city'][id])
                counter = False
                for j in range(len(list(df6['city']))):
                    city = df6['city'][j]    
                    if city in i.title(): 
                        regions.append(df6['region'][j])
                        sub_regions.append(df6['sub_region'][j])
                        counter = True
                        break               
                if not counter: 
                    regions.append(df7['region'][id])
                    sub_regions.append(df7['sub_region'][id])

        xlsx()
    elif entry == 1:
        lst = []
        for i in range(5):
            mygroups = api.groups.get(user_id=int(df1['id'][n]),offset=offset, v='5.199')
            lst += mygroups['items']
            offset += 1000

        next_id = int(input('Next id >>> '))
        for id, i in enumerate(df3['id']):
            #if id >= next_id and int(df3['id'][id]) not in lst and 'жесть'.title() in df3['title'][id].title() or 'ЧП' in df3['title'][id]:
            if id >= next_id and int(df3['id'][id]) not in lst and df3['region'][id] == df1['region'][n]:
                try:
                    api.groups.join(group_id=i, v='5.199')
                    print('Id >>>', id, '<--> Row >>>', id+2)
                except vk.exceptions.VkAPIError as e:
                    if e.code == 14:
                        try:
                            print('Solving captcha ...')
                            download_image(e.captcha_img, save_as) 
                            code = captcha_solver(save_as)
                            sleep(5)
                            api.groups.join(group_id=i, captcha_sid=e.captcha_sid, captcha_key=code, v='5.199') 
                            print('Id >>>', id, '<--> Row >>>', id+2)             
                        except vk.exceptions.VkAPIError as e:
                            if e.code == 14:
                                try:
                                    print('Solving captcha ...')
                                    download_image(e.captcha_img, save_as) 
                                    code = captcha_solver(save_as)
                                    sleep(5)
                                    api.groups.join(group_id=i, captcha_sid=e.captcha_sid, captcha_key=code, v='5.199') 
                                    print('Id >>>', id, '<--> Row >>>', id+2)
                                except vk.exceptions.VkAPIError as e:
                                    if e.code == 14:
                                        try:
                                            print('Solving captcha ...')
                                            download_image(e.captcha_img, save_as)
                                            code = captcha_solver(save_as)
                                            sleep(5)
                                            api.groups.join(group_id=i, captcha_sid=e.captcha_sid, captcha_key=code, v='5.199')
                                            print('Id >>>', id, '<--> Row >>>', id+2)
                                        except vk.exceptions.VkAPIError as e:
                                            if e.code == 14:
                                                print('Solving captcha ...')
                                                download_image(e.captcha_img, save_as)
                                                code = captcha_solver(save_as)
                                                sleep(5)
                                                api.groups.join(group_id=i, captcha_sid=e.captcha_sid, captcha_key=code, v='5.199')
                                                print('Id >>>', id, '<--> Row >>>', id+2)
                    else: print(e)
    elif entry == 2:
        entry = int(input('1 >>> One\n2 >>> Multiple\n>>> '))
        if entry == 1: 
            lst = [""]
            for id, query in enumerate(df4['word']):
                print(id)
                query = str(query)
                for j in lst:
                    search = api.groups.search(q=str(j+' '+query), extended=1, fields=['can_suggest', 'members_count', 'city'], v='5.199')
                    for i in search['items']:
                        if i['members_count'] >= 100 and query.lower() in str(i['name']).lower() and i['id'] not in list(df3['id']):
                            ids.append(i['id'])
                            links.append(r'https://vk.com/' + i['screen_name'])
                            titles.append(i['name'])
                            members.append(i['members_count'])
                            suggests.append(i['can_suggest'])
                            if 'city' in i: cities.append(i['city']['title'])
                            else: cities.append('-')
                            regions.append(df4['region'][id])
                            sub_regions.append('-')
            xlsx()
        elif entry == 2:
            for id, query in enumerate(df4['word']):
                search = api.groups.search(q=query, v='5.199')
                for j in range(2):
                    search = api.groups.search(q=query, extended=1, offset=offset,  count=500, fields=['wall', 'can_suggest', 'members_count', 'city'], v='5.199')
                    ids1 = [i['id'] for i in search['items']]
                    offset += 500
                    if len(ids1) > 0:
                        groups = api.groups.getById(group_ids=ids1, fields=['can_suggest', 'members_count', 'city'], v='5.199')
                        for i in groups['groups']:
                            if i['members_count'] >= 1000 and query.lower() in i['name'].lower() and i['id'] not in list(df3['id']):
                                ids.append(i['id'])
                                links.append(r'https://vk.com/' + i['screen_name'])
                                titles.append(i['name'])
                                members.append(i['members_count'])
                                suggests.append(i['can_suggest'])
                                regions.append(df4['region'][id])
                                sub_regions.append('-')
                                if 'city' in i: cities.append(i['city']['title'])
                                else: cities.append('-')
            xlsx()
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
                    if id in range(0, 1000, 100): print(id)
                    last_post = api.wall.get(owner_id=-i, v='5.199')
                    if last_post['items'][2]['date'] >= end_time:
                        ids.append(df7['id'][id])
                        links.append(df7['link'][id])
                        titles.append(df7['title'][id])
                        members.append(df7['members'][id])
                        cities.append(df7['city'][id])
                        suggests.append(df7['suggest_post'][id])
                        regions.append(df7['region'][id])
                        sub_regions.append(df7['sub_region'][id]) 
                except (vk.exceptions.VkAPIError, IndexError) : print('Check it', df7['link'][id])
            xlsx()
        elif entry == 2:
            for i in df7['link']:
                i = i.split('_')
                links.append(i[0][20:])
            groups = api.groups.getById(group_ids=links,  v='5.199')
            for id, j in enumerate(groups['groups']):
                ids.append(j['id'])
                links.append(r'https://vk.com/' + j['screen_name'])
                titles.append(j['name'])
    session()
def posts():
    entry = int(input('1 >>> Remove suggested post\n2 >>> Upload photo\n3 >>> Suggest post\n4 >>> Collect link on published post\n5 >>> Comment on post\n6 >>> Find post\n7 >>> Statistic of post\n8 >>> Upload video\n>>> '))
    regions, links, views, members, likes, comments, reposts, dates = [], [], [], [], [], [], [], []
    if entry == 7:        
        for i in df8['link']:
            k = i.split('wall')
            k = k[1]
            ids.append(k)       
        published_posts = api.wall.getById(posts=ids, v='5.199')
        for j in published_posts['items']:
            group = api.groups.getById(group_id=abs(j['from_id']), fields='members_count', v='5.199')
            group_members = group['groups'][0]['members_count']
            try: members.append(group_members)
            except KeyError: members.append('-')
            links.append('https://vk.com/wall'+str(j['from_id'])+'_'+str(j['id']))
            likes.append(j['likes']['count'])
            reposts.append(j['reposts']['count'])
            views.append(j['views']['count'])
            comments.append(j['comments']['count'])
            dates.append(str(datetime.datetime.now())[:-7])  
            if abs(j['from_id']) in list(df3['id']):
                for id, l in enumerate(df3['id']):
                    if abs(j['from_id']) == int(l):
                        regions.append(df3['region'][id])
            else:
                regions.append('unknown') 
        df['region'] = regions
        df['link'] = links
        df['views'] = views
        df['members'] = members
        df['likes'] = likes
        df['comments'] = comments
        df['reposts'] = reposts
        df['date'] = dates
        df.to_excel('statistic.xlsx')
        session()
    elif entry == 1:
        next_id = int(input('Next id >>> '))
        for id, i in enumerate(df3['id']):
           # if 'жесть'.title() in df3['title'][id] or 'ЧП' in df3['title'][id]: 
            if df3['region'][id] == df1['region'][n]:
                if id >= next_id:
                    try:
                        check_post = api.wall.get(owner_id=-i, filter='suggests', v='5.199')
                        sleep(0.5)
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
                                else: print(e)
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
        exit()
    elif entry == 3:
        message = df2['text'][n]
        try: media_id = df2['media_id'][n].split(',')
        except AttributeError: media_id = []
        if isinstance(message, float): print('Empty message!!!'), exit()
        print(f'Sent with {len(media_id)} attachments!') 
        next_id = int(input('Next id >>> '))
        for id, i in enumerate(df3['id']):
           # if 'жесть'.title() in df3['title'][id] or 'ЧП' in df3['title'][id]:
            if df3['region'][id] == df1['region'][n] and df3['suggest_post'][id] == 1:
                if id >= next_id:
                    try:
                        api.wall.post(owner_id=-i, message=message, attachments=media_id, v='5.199')
                        print('Id >>>', id, '<--> Row >>>', id+2)
                    except vk.exceptions.VkAPIError as e:
                        if e.code == 214: 
                            try:
                                api.groups.join(group_id=i, v='5.199')
                                api.wall.post(owner_id=-i, message=message, attachments=media_id, v='5.199')
                                print('Id >>>', id, '<--> Row >>>', id+2)
                            except vk.exceptions.VkAPIError as e:
                                if e.code == 14:
                                    try:
                                        print('Solving captcha ...')
                                        download_image(e.captcha_img, save_as)
                                        code = captcha_solver(save_as)
                                        sleep(5)
                                        api.wall.post(owner_id=-i, message=message, attachments=media_id, captcha_sid=e.captcha_sid, captcha_key=code, v='5.199')
                                        print('Id >>>', id, '<--> Row >>>', id+2)
                                    except: pass
                                elif e.code == 15:
                                    try:
                                        api.wall.post(owner_id=-i, message=message, attachments=media_id, v='5.199')
                                        print('Id >>>', id, '<--> Row >>>', id+2)
                                    except: pass
                                elif e.code == 214:
                                    pass
                        elif e.code == 14:
                            print('Solving captcha ...')
                            download_image(e.captcha_img, save_as)
                            code = captcha_solver(save_as)
                            sleep(5)
                            try:
                                api.wall.post(owner_id=-i, message=message, attachments=media_id, captcha_sid=e.captcha_sid, captcha_key=code, v='5.199')
                                print('Id >>>', id, '<--> Row >>>', id+2)
                            except vk.exceptions.VkAPIError as e:
                                if e.code == 14:
                                    print('Solving captcha ...')
                                    download_image(e.captcha_img, save_as)
                                    code = captcha_solver(save_as)
                                    sleep(5)
                                    try:
                                        api.wall.post(owner_id=-i, message=message, attachments=media_id, captcha_sid=e.captcha_sid, captcha_key=code, v='5.199')
                                        print('Id >>>', id, '<--> Row >>>', id+2)
                                    except vk.exceptions.VkAPIError as e:
                                        if e.code == 14:
                                            print('Solving captcha ...')
                                            download_image(e.captcha_img, save_as)
                                            code = captcha_solver(save_as)
                                            sleep(5)
                                            api.wall.post(owner_id=-i, message=message, attachments=media_id, captcha_sid=e.captcha_sid, captcha_key=code, v='5.199')
                        elif e.code == 220: 
                            print('Too many recipient! Switch the bot!')
                            exit()
                        else: print(e)
    elif entry == 4:
        dates, links, posts = [], [], []
        for id, i in enumerate(df1['token']):
            try:
                access_token=str(df1['token'][id][45:265])
                api2 = vk.API(access_token=access_token, v='5.199') 
                results = api2.notifications.get(count=100, v='5.199')
                for i in results['items']:
                    try:
                        if 'url' in i['action']:
                            if 'wall-' in i['action']['url'] and 'reply=' not in i['action']['url']:
                                dates.append(datetime.datetime.fromtimestamp(i['date']).strftime('%Y-%m-%d %H:%M'))
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
        next_id = int(input('Next id >>> '))
        last_id = int(input('Last id >>> '))
        links = []
        try: media_id = df5['media_id'][n].split(',')
        except AttributeError: media_id = []
        for id, i in enumerate(df8['link']):
            if last_id >= id >= next_id and 'reply=' not in i: 
                try:
                    t = r.randint(n, n+h-1)
                    link = i.split('wall')
                    group = link[1].split('_')
                    api.wall.createComment(owner_id=int(group[0]), post_id=int(group[1]), message=df5['text'][t], attachments=media_id, v='5.199')
                    comments = api.wall.getComments(owner_id=int(group[0]), post_id=int(group[1]), sort='desc', count=100, v='5.199')
                    for k in comments['items']:
                        if k['from_id'] == int(df1['id'][n]):
                            k1 = k['id']
                            print('https://vk.com/wall'+str(int(group[0]))+'_'+str(int(group[1]))+f'?reply={k1}')
                            links.append('https://vk.com/wall'+str(int(group[0]))+'_'+str(int(link[1]))+f'?reply={k1}')
                    sleep( r.randint(20, 90))
                except vk.exceptions.VkAPIError as e:
                    if e.code == 213: print(e.message)
                    elif e.code == 14:
                        print('Solving captcha ...')
                        download_image(e.captcha_img, save_as) 
                        code = captcha_solver(save_as)
                        sleep(5)
                        api.wall.createComment(owner_id=int(group[0]), captcha_sid=e.captcha_sid, captcha_key=code, post_id=int(group[1]), message=df5['text'][t], attachments=media_id, v='5.199')
                        comments = api.wall.getComments(owner_id=int(group[0]), post_id=int(group[1]), sort='desc', count=100, v='5.199')
                        for k in comments['items']:
                            if k['from_id'] == int(df1['id'][n]):
                                k1 = k['id']
                                print('https://vk.com/wall'+str(int(group[0]))+'_'+str(int(group[1]))+f'?reply={k1}')
                                links.append('https://vk.com/wall'+str(int(group[0]))+'_'+str(int(link[1]))+f'?reply={k1}')
                                sleep( r.randint(20, 90))
                            else : print(e.message)
        df['link'] = links
        df.to_excel(df1['name'][n]+'-comments.xlsx')
    elif entry == 6:
        for id, k in enumerate(df9['id']):
            for id1, i in enumerate(df3['id']):
                if df9['region'][id] == df3['region'][id1]:
                    try:
                        get_post = api.wall.get(owner_id=-i, extended=1,  v='5.199')
                        for j in get_post['items']:
                            if 'signer_id' in j:
                                if k == j['signer_id']:
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
        df.to_excel('dead_posts.xlsx')
def messages():
    entry = int(input('1 >>> Get last message\n2 >>> Remove all messages\n3 >>> Send message to admins\n4 >>> Send message to user\n5 >>> Get message from specific ids\n>>> ')) 
    results = api.messages.getConversations(count=200, v='5.199')
    if entry == 1:
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
        next_id = int(input('Next id >>> '))
        for id, i in enumerate(df['id']):
            if id >= next_id:
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
        region = df1['region'][n]
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

def users():
    entry = int(input('1 >>> friends\n2 >>> remove dead bot\n3 >>> friend request\n4 >>> like and repost\n5 >>> join group\n6 >>> remove suggested posts\n>>> '))
    numbers, regions, names, phones, passwords, ids, tokens, channels = [], [], [], [], [], [], [], []
    numbers0, regions0, names0, phones0, passwords0, ids0, tokens0, channels0 = [], [], [], [], [], [], [], []
    df = pd.DataFrame()
    for id, i in enumerate(df1['token']):
        try:
            access_token=str(df1['token'][id][45:265])
            api = vk.API(access_token=access_token, v='5.199')
            if entry == 1:
                bots = [i for i in df1['id']]
                my_friends = api.friends.get(user_id=int(df1['id'][id]), v='5.199')
                for i in my_friends['items']:
                    if i in bots: api.friends.delete(user_id=i, v='5.199'), print('Removing >>> ', i)
            elif entry == 2:
                try:
                    api.users.getInfo(user_ids=df1['id'][id], v='5.199')
                    numbers0.append(df1['n'][id])
                    regions0.append(df1['region'][id])
                    names0.append(df1['name'][id])
                    phones0.append(df1['phone'][id])
                    passwords0.append(df1['password'][id])
                    ids0.append(df1['id'][id])
                    tokens0.append(df1['token'][id])
                    channels0.append(df1['channels'][id])       
                except vk.exceptions.VkAPIError as e:
                    if e.code == 5: 
                        print(id)
                        numbers.append(df1['n'][id])
                        regions.append(df1['region'][id])
                        names.append(df1['name'][id])
                        phones.append(df1['phone'][id])
                        passwords.append(df1['password'][id])
                        ids.append(df1['id'][id])
                        tokens.append(df1['token'][id])
                        channels.append(df1['channels'][id])
            elif entry == 3:
                user_id = int(input('User id >>> '))
                api.friends.add(user_id=user_id)
                print(id)
            elif entry == 4:
                entry1 = int(input('1 >>> Like\n2 >>> Repost\n>>> '))
                group_id = int(input('Group id >>> '))
                post_id = int(input('Post id >>> '))
                next_id = int(input('Next id >>> '))
                if id >= next_id:
                    print(id)
                    if entry1 == 1: api.likes.add(type='post', owner_id=group_id, item_id=post_id), sleep(5)
                    elif entry1 == 2: api.wall.repost(object='wall'+str(group_id)+'_'+str(post_id)), sleep(5)
            elif entry == 5:
                group_id = int(input('Group id >>> '))
                api.groups.join(group_id=group_id, v='5.199')
                print(id)
                sleep(1)
            elif entry == 6:
                for id, i in enumerate(df3['id']):
           # if 'жесть'.title() in df3['title'][id] or 'ЧП' in df3['title'][id]:
                    if df3['region'][id] == df1['region'][id]:
                        try:
                            check_post = api.wall.get(owner_id=-i, filter='suggests', v='5.199')
                            sleep(0.5)
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
                                else: print(e)
        except vk.exceptions.VkAPIError as e: print(e.message)   
#    df['n'] = numbers0
#    df['region'] = regions0
#    df['name'] = names0
#    df['phone'] = phones0
#    df['password'] = passwords0
#    df['id'] = ids0
#    df['token'] = tokens0
#    df['channels'] = channels0
    df['-n'] = numbers
    df['-region'] = regions
    df['-name'] = names
    df['-phone'] = phones
    df['-password'] = passwords
    df['-id'] = ids
    df['-token'] = tokens
    df['-channels'] = channels
    df.to_excel('dead_bots.xlsx')

    session()
def session():
    entry = int(input(f'{bot1}\n1 >>> groups\n2 >>> posts\n3 >>> messages\n4 >>> users\n>>> '))
    if entry == 1: groups()
    elif entry == 2: posts()
    elif entry == 3: messages()
    elif entry == 4: users()
session()


