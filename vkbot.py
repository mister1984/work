import vk
import pandas as pd
import datetime
from time import sleep
import re
import random as r
import requests

df1 = pd.read_excel('code/vk/bots.xlsx', sheet_name='credentials')
df2 = pd.read_excel('code/vk/bots.xlsx', sheet_name='message')
df3 = pd.read_excel('code/vk/bots.xlsx', sheet_name='groups1')
df4 = pd.read_excel('code/vk/bots.xlsx', sheet_name='join')
df5 = pd.read_excel('code/vk/bots.xlsx', sheet_name='comment')

n = int(input('Select number of bot >>> '))
access_token=str(df1['token'][n][45:265])
api = vk.API(access_token=access_token, v='5.199')           
bot = api.users.get(user_ids=df1['id'][n], v='5.199')
bot1 = bot[0]['first_name']+' '+bot[0]['last_name'] 
bot2 = bot[0]['first_name']

def write_to_excel():
    offset=0
    df = pd.DataFrame()
    ids, links, titles, members, cities, suggests, regions = [], [], [], [], [], [], []
    for i in range(5):
        mygroups = api.groups.get(user_id=int(df1['id'][n]), offset=offset, fields=['members_count', 'city', 'can_post', 'can_suggest'],  extended=1, v='5.199')
        offset+=1000
        for i in mygroups['items']:
            try:
                if i['members_count'] >= 1000 and i['id'] not in ids:
                    if i['can_post'] == 1: #or i['can_post'] == 1:
                        ids.append(i['id'])
                        links.append(r'https://vk.com/' + i['screen_name'])
                        titles.append(i['name'])
                        members.append(i['members_count'])
                        suggests.append(i['can_suggest'])
                        regions.append(df1['region'][n])
                        if 'city' in i: cities.append(i['city']['title'])
                        else: cities.append('-')
            except KeyError:
                print(KeyError)
    df['id'] = ids
    df['link'] = links
    df['title'] = titles
    df['members'] = members
    df['city'] = cities
    df['suggest_post'] = suggests
    df['region'] = regions
    print(len(ids))
    df.to_excel(df1['region'][n]+'.xlsx', sheet_name=df1['region'][n])
    session()

def groups():
    entry = int(input('1 >>> Join groups\n2 >>> Search groups\n3 >>> Leave groups\n>>> '))
    if entry == 1:
        last_id = int(input('Last id >>> '))
        for id, i in enumerate(df4['id']):
            if id >= last_id:
                try:
                    api.groups.join(group_id=i, v='5.199')
                    print('Id >>>', id, '<--> Row >>>', id+2)
                except vk.exceptions.VkAPIError as e:
                    if e.code == 15: print('You are already in this community!!!')
                    elif e.code == 14:
                        print(e.captcha_img)
                        captcha = input('Captcha code >>> ')
                        try:
                            api.groups.join(group_id=i, captcha_sid=e.captcha_sid, captcha_key=captcha, v='5.199') 
                            print('Id >>>', id, '<--> Row >>>', id+2)                   
                        except vk.exceptions.VkAPIError as e:
                            if e.code == 15: print('You are already in this community!!!')

                    elif e.code == 5:
                        print('Connect again!')
                        break
                    else: 
                        print(e)
                        break
        session()
    elif entry == 2:
        df0 = pd.read_excel('vk_search.xlsx')
        for id, query in enumerate(df0['word']):
            df = pd.DataFrame()
           # query = input('Query >>> ')
            search = api.groups.search(q=query.strip(), type='group', count=1000, v='5.199')
            ids1 = [i['id'] for i in search['items']]
            groups = api.groups.getById(group_ids=ids1, fields=['wall', 'can_suggest', 'members_count', 'city']) 
            ids, links, titles, members, cities, suggests, regions = [], [], [], [], [], [], []
            for i in groups['groups']:
                if i['wall'] != 0 and i['members_count'] >= 1000:
                    ids.append(i['id'])
                    links.append(r'https://vk.com/' + i['screen_name'])
                    titles.append(i['name'])
                    members.append(i['members_count'])
                    suggests.append(i['can_suggest'])
                    regions.append(query)
                    if 'city' in i: cities.append(i['city']['title'])
                    else: cities.append('-')
            df['id'] = ids
            df['link'] = links
            df['title'] = titles
            df['members'] = members
            df['city'] = cities
            df['suggest_post'] = suggests
            df['region'] = regions
            query = query.strip()
            df.to_excel(query+'.xlsx', sheet_name=query)
        session()
    elif entry == 3:
        mygroups = api.groups.get(user_id=int(df1['id'][n]), fields=['members_count', 'city', 'can_post', 'can_suggest'],  extended=1, v='5.199')
        for id, i in enumerate(mygroups['items']):
            api.groups.leave(group_id=i['id'], v='5.199')
            print(id)
        session()

def posts():
    entry = int(input('1 >>> Remove suggested post\n2 >>> Upload photo\n3 >>> Suggest post\n4 >>> Collect link on published post\n5 >>> Comment on post\n6 >>> Find post\n>>> '))
    if entry == 1:
        last_id = int(input('Last id >>> '))
        for id, i in enumerate(df3['id']):
            if df3['region'][id] == df1['region'][n]:
                if id >= last_id:
                    check_post = api.wall.get(owner_id=-i, filter='suggests', v='5.199')
                    sleep(1)
                    print(id)
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
                           # print('Access to wall denied', df3['link'][id])
                            try:
                                api.groups.join(group_id=i, v='5.199')
                                api.wall.post(owner_id=-i, message=message, attachments=[photo1, photo2], v='5.199')
                                print('Id >>>', id, '<--> Row >>>', id+2)

                            except vk.exceptions.VkAPIError as e:
                                if e.code == 14:
                                    print(e.captcha_img)
                                    captcha = input('Captcha code >>> ')
                                    api.groups.join(group_id=i, captcha_sid=e.captcha_sid, captcha_key=captcha, v='5.199')
                                    api.wall.post(owner_id=-i, message=message, attachments=[photo1, photo2], captcha_sid=e.captcha_sid, captcha_key=captcha, v='5.199')
                                    print('Id >>>', id, '<--> Row >>>', id+2)
                        elif e.code == 14:
                            print(e.captcha_img)
                            captcha = input('Captcha code >>> ')
                            api.wall.post(owner_id=-i, message=message, attachments=[photo1, photo2], captcha_sid=e.captcha_sid, captcha_key=captcha, v='5.199')
                            print('Id >>>', id, '<--> Row >>>', id+2)
                        elif e.code == 220: 
                            print('Too many recipient! Switch the bot!')
                            break
                        else: 
                            print(e)
                            break
    elif entry == 4:
        df = pd.DataFrame()
        results = api.notifications.get(count=100)
        dates, links, posts = [], [], []
        for i in results['items']:
            try:
                if 'url' in i['action']:
                    if 'wall-' in i['action']['url']:
                        dates.append(datetime.datetime.fromtimestamp(i['date']).strftime('%Y-%m-%d %H:%M:%S'))
                        links.append(i['action']['url'])
                        try: posts.append(i['text'])
                        except KeyError: posts.append('-')
            except KeyError: pass
        df['date'] = dates
        df['link'] = links
        df['post'] = posts
        df.to_excel(f'published_posts-{df1["name"][n]}.xlsx', sheet_name=df1['name'][n])

    elif entry == 5:
        h = int(input('Numbers of comments\n>>> '))
        t = r.randint(n, n+h-1)
        df = pd.read_excel('kyrgyz(comment).xlsx')
        last_id = int(input('Last id >>> '))
        df0 = pd.DataFrame()
        links = []
        for id, i in enumerate(df['id']):
            if id >= last_id:
                try:
                    get_post = api.wall.get(owner_id=-i, v='5.199')
                    if get_post['count'] > 1:
                        j = get_post['items'][1]['id']
                        api.wall.createComment(owner_id=-i, post_id=j, message=df5['text'][t], v='5.199')
                        print(id, '<-->', id+2)
                        sleep(1)
                        comments = api.wall.getComments(owner_id=-i, post_id=j, v='5.199')
                        for k in comments['items']:
                            if k['from_id'] == int(df1['id'][n]):
                                k1 = k['id']
                                links.append(f'https://vk.com/wall-{i}_{j}?reply={k1}')
                        sleep(3)
                except vk.exceptions.VkAPIError as e:
                    if e.code == 213:
                        pass
        df0['link'] = links
        df0.to_excel(df1['name'][n]+'-comments.xlsx')

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

def uniq_groups():
    df000 = pd.read_excel('suggested_groups.xlsx')
    links0 = []
    for i in df000['link']:
        i = i.split('_')
        links0.append(i[0][20:])
    links0 = set(links0)
   # links0 = set([str(i[15:]) for i in df000['link']])
    ids1, links1, titles1, members1, cities1, suggests1, regions1 = [], [], [], [], [], [], []
    groups = api.groups.getById(group_ids=links0, fields=['members_count', 'city', 'can_suggest'], extended=1, v='5.199')
    for id, j in enumerate(groups['groups']):
            ids1.append(j['id'])
            links1.append(r'https://vk.com/' + j['screen_name'])
            titles1.append(j['name'])
            try:
                members1.append(j['members_count'])
                suggests1.append(j['can_suggest'])
            except KeyError:
                members1.append('0')
                suggests1.append('-')

            if 'city' in j: cities1.append(j['city']['title'])
            else: cities1.append('-')
    df00 = pd.DataFrame()
    df00['id'] = ids1
    df00['link'] = links1
    df00['title'] = titles1
    df00['members'] = members1
    df00['city'] = cities1
    df00['suggest_post'] = suggests1
    df00.to_excel('groups for adding.xlsx') 
    ids, links, titles, members, cities, suggests, regions = [], [], [], [], [], [], []
    df = pd.DataFrame()
    df0 = pd.read_excel('groups for adding.xlsx')
    for id, i in enumerate(df0['id']):
        if i not in list(df3['id']):
            ids.append(i)
            links.append(df0['link'][id])
            titles.append(df0['title'][id])
            members.append(df0['members'][id])
            suggests.append(df0['suggest_post'][id])
            regions.append(df1['region'][n])
            cities.append(df0['city'][id])
    df['id'] = ids
    df['link'] = links
    df['title'] = titles
    df['members'] = members
    df['city'] = cities
    df['suggest_post'] = suggests
    df['region'] = regions
    df.to_excel('new_groups_for_vk.xlsx')

def friends():
    bots = [i for i in df1['id']]
    my_friends = api.friends.get(user_id=int(df1['id'][n]), v='5.199')
    for i in my_friends['items']:
        if i in bots:
            api.friends.delete(user_id=i, v='5.199')
            print('Removing >>> ', i)
def news():
    entry = int(input('1 >>> Youscan\n2 >>> News\n>>> '))
    if entry == 1:
        df0 = pd.read_excel('links.xlsx')
        df = pd.DataFrame()
        h = int(input('Numbers of comments\n>>> '))
        links = [] 
        last_id = int(input('Last id >>> '))
        for id, i in enumerate(df0['link']):
            if id >= last_id: 
                try:
                    t = r.randint(n, n+h-1)
                    link = i.split('_')
                    group = link[0][19:]
                    api.wall.createComment(owner_id=int(group), post_id=int(link[1]), message=df5['text'][t], attachments=df5['photo_id1'][t], v='5.199')
                    comments = api.wall.getComments(owner_id=int(group), post_id=int(link[1]), v='5.199')
                    sleep(1)
                    for k in comments['items']:
                        if k['from_id'] == int(df1['id'][n]):
                            k1 = k['id']
                            print(id,' <--> ',id+2, 'https://vk.com/wall'+str(int(group))+'_'+str(int(link[1]))+f'?reply={k1}')
                            links.append('https://vk.com/wall'+str(int(group))+'_'+str(int(link[1]))+f'?reply={k1}')
                    sleep(10)
                except vk.exceptions.VkAPIError as e:
                    if e.code == 213: pass
        df['link'] = links
        df.to_excel('comments.xlsx')       
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
                        api.wall.createComment(owner_id=i['owner_id'], post_id=i['id'], message=df5['text'][t], attachments=df5['photo_id1'][t], v='5.199')
                        comments = api.wall.getComments(owner_id=i['owner_id'], post_id=i['id'], v='5.199')
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
            
def session():
    print(f'{bot1}\n0 >>> write_to_excel\n1 >>> groups\n2 >>> posts\n3 >>> messages\n4 >>> get_paricipants\n5 >>> uniq_groups\n6 >>> remove_friend\n7 >>> news')
    entry = int(input('>>> '))
    if entry == 0: write_to_excel()
    elif entry == 1: groups()
    elif entry == 2: posts()
    elif entry == 3: messages()
    elif entry == 4: get_paricipants()
    elif entry == 5: uniq_groups()
    elif entry == 8:
        df0 = pd.DataFrame()
        df1 = pd.read_excel('all.xlsx')
        ids, links, titles, members, cities, suggests, regions = [], [], [], [], [], [], []
        for id1, i in enumerate(df1['id']):
            if i in list(df3['id']):
                for id2, j in enumerate(df3['id']):
                    if i == j:
                        ids.append(i)
                        links.append(df1['link'][id1])
                        titles.append(df1['title'][id1])
                        members.append(df1['members'][id1])
                        suggests.append(df1['suggest_post'][id1])
                        regions.append(df3['region'][id2])
                        cities.append(df1['city'][id1])
            else:
                ids.append(i)
                links.append(df1['link'][id1])
                titles.append(df1['title'][id1])
                members.append(df1['members'][id1])
                suggests.append(df1['suggest_post'][id1])
                regions.append('unkown')
                cities.append(df1['city'][id1])
        df0['id'] = ids
        df0['link'] = links
        df0['title'] = titles
        df0['members'] = members
        df0['city'] = cities
        df0['suggest_post'] = suggests
        df0['region'] = regions
        df0.to_excel('groups0.xlsx')
    

                    

       # lst = list(df['id'])
       # print(len(lst))
       # print(len(set(lst)))

    elif entry == 6: friends()
    elif entry == 7: news()

             

session()

