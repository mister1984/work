import vk
import pandas as pd
import datetime
from time import sleep
import re
import random as r
import requests, json
import vk_captchasolver as vc
import urllib.request
import json
from math import ceil as c 
def xlsx(mode):
    if mode == 'user_groups':
        df['id'] = ids
        df['link'] = links
        df['title'] = titles
        df['suggest_post'] = suggests
        df['members'] = members
        df['city'] = cities
        df.to_excel('user_groups.xlsx')
    elif mode == 'signer':
        df['signer'] = from_signers
        df.to_excel('signer.xlsx')
    elif mode == 'dead_bots':
        df['-name'] = names
        df['-phone'] = phones
        df['-password'] = passwords
        df['-id'] = ids
        df.to_excel('dead_bots.xlsx')
    elif mode == 'published_posts':
        df['name'] = names
        df['date'] = dates
        df['link'] = links
        df['post'] = posts
        df.to_excel('published_posts.xlsx')
    elif mode == 'dead_posts':
        df['link'] = links
        df['text'] = texts
        df.to_excel('dead_posts.xlsx')
    elif mode == 'last_messages':
        df['id'] = ids
        df['link'] = links
        df['title'] = titles
        df['response'] = responses
        df.to_excel('last_messages.xlsx')
    elif mode == 'statistic':
        df['city'] = cities
        df['sub_region'] = sub_regions
        df['region'] = regions
        df['link'] = links
        df['views'] = views
        df['members'] = members
        df['likes'] = likes
        df['comments'] = comments
        df['reposts'] = reposts
        df['date'] = dates
        df.to_excel('statistic.xlsx')
    elif mode == 'comments':
        df['link'] = links
        df.to_excel(df1['name'][n]+'-comments.xlsx')
    elif mode == 'groups_id':
        df['id'] = ids
        df.to_excel('group_ids.xlsx')
    elif mode == 'user_statistic':
        df['id'] = user_ids
        df['link'] = links
        df['name'] = names
        df.to_excel('user_statistic.xlsx')
def execute_main_commands(suggest=0, join=0, remove=0):
    def captcha_solver(mode, sid, img):
        print('Solving captcha ...')
        urllib.request.urlretrieve(img, 'code.jpg')
        captcha = vc.solve(image='code.jpg')
        sleep(5)
        if mode == 1: api.groups.join(group_id=i, captcha_sid=e.captcha_sid, captcha_key=captcha, v='5.199')
        elif mode == 2: api.wall.post(owner_id=-i, message=message, attachments=media_id, captcha_sid=e.captcha_sid, captcha_key=captcha, v='5.199')
        elif mode == 3: api.wall.delete(owner_id=-i, post_id=j['id'], captcha_sid=e.captcha_sid, captcha_key=captcha, v='5.199')
    try:
        if join == 1:
            join, mode = 1, 1
            api.groups.join(group_id=i, v='5.199')
            print('Joining: Id >>>', id, '<--> Row >>>', id+2)
        elif suggest == 1:
            suggest, mode = 1, 2
            api.wall.post(owner_id=-i, message=message, attachments=media_id, v='5.199')
            print('Posting: Id >>>', id, '<--> Row >>>', id+2)
        elif remove == 1:
            remove, mode = 1, 3
            api.wall.delete(owner_id=-i, post_id=j['id'], v='5.199')
            print('Removing: Id >>>', id, '<--> Row >>>', id+2)
    except vk.exceptions.VkAPIError as e:
        if e.code == 14:
            try: captcha_solver(mode=mode, sid=e.captcha_sid, img=e.captcha_img)
            except vk.exceptions.VkAPIError as e:
                    if e.code == 14:
                        try: captcha_solver(mode=mode, sid=e.captcha_sid, img=e.captcha_img)
                        except vk.exceptions.VkAPIError as e:
                            if e.code == 14:
                                try: captcha_solver(mode=mode, sid=e.captcha_sid, img=e.captcha_img)
                                except vk.exceptions.VkAPIError as e:
                                    if e.code == 14:
                                        try: captcha_solver(mode=mode, sid=e.captcha_sid, img=e.captcha_img)
                                        except vk.exceptions.VkAPIError as e:
                                            if e.code == 14: captcha_solver(mode=mode, sid=e.captcha_sid, img=e.captcha_img)
        else: print(e)
while True:
    n = int(input('Select number of bot >>> '))
    if n == -1: exit()
    df = pd.DataFrame()
    df1 = pd.read_excel('code/vk/bots_vk.xlsx', sheet_name='credentials')
    df2 = pd.read_excel('code/text/data.xlsx', sheet_name='регіон')
    df3 = pd.read_excel('code/vk/bots_vk.xlsx', sheet_name='groups')
    df4 = pd.read_excel('code/vk/bots_vk.xlsx', sheet_name='users')
    df5 = pd.read_excel('code/text/data.xlsx', sheet_name='special_words')
    df8 = pd.read_excel('code/vk/bots_vk.xlsx', sheet_name='published_posts')
    df9 = pd.read_excel('code/vk/bots_vk.xlsx', sheet_name='dead_bots')
    df10 = pd.read_excel('code/vk/bots_vk.xlsx', sheet_name='team_bots')
    access_token=str(df1['token'][n][45:265])
    api = vk.API(access_token=access_token, v='5.199')
    bot = api.users.get(user_ids=df1['id'][n], fields=['sex', 'bdate', 'city'], v='5.199')
    if bot[0]['sex'] == 1: 
        sex = 'Woman'
    elif bot[0]['sex'] == 2:
        sex = 'Man'
    try: bot = bot[0]['first_name']+' '+bot[0]['last_name']+'\n'+sex+'\n'+str(bot[0]['bdate']+'\n'+str(bot[0]['city']['title']))
    except KeyError:  bot = bot[0]['first_name']+' '+bot[0]['last_name']+'\n'+sex+'\n'+str(bot[0]['bdate']+'\n'+'No city')
    message = df1['text'][n]
    try: media_id = df1['media_id'][n].split('$')
    except AttributeError: media_id = []
    try:
        next_id, last_id = int(df1['next_id'][n])-2, int(df1['last_id'][n])-2
    except (AttributeError, ValueError): 
        next_id, last_id = -1, -1
    print(f'You have {len(media_id)} attachments!')
    ids, links, titles, members, cities, suggests, regions, sub_regions, likes, reposts, views, comments, dates, posts, lst, numbers, names, phones, passwords, tokens, responses, my_ids, keywords, texts, user_ids, from_signers, types = [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []
    offset = 0
    epoch = datetime.datetime.now().strftime('%s')
    end_time = int(epoch) - 864000
    entry = int(input(f'{bot}\n0 >>> exit\n1 >>> groups\n2 >>> posts\n3 >>> messages\n4 >>> users\n5 >>> settings\n6 >>> suggest post\n7 >>> friends\n>>> '))
    if entry == 0: exit()
    elif entry == 5:
        entry1 = int(input('1 >>> Change age\n2 >>> Change name\n3 >>> Change sex\n4 >>> Change city\n5 >>> Upload main photo\n6 >>> See main photo\n>>> '))
        if entry1 == 1:
            age = input('New age >>> ')
            api.account.saveProfileInfo(bdate=age, v='5.199')
        elif entry1 == 2:
            full_name = input('Full name >>> ').split(' ')
            first_name = full_name[0]
            last_name = full_name[1]
            api.account.saveProfileInfo(first_name=first_name, last_name=last_name, v='5.199')
        elif entry1 == 3:
            sex = int(input('1 >>> Female\n2 >>> Male\n>>> '))
            api.account.saveProfileInfo(sex=sex, v='5.199')
        elif entry1 == 4:
            city = input('City >>> ')
            city = api.database.getCities(q=city, v='5.199')
            city = city['items'][0]['id']
            api.account.saveProfileInfo(city_id=city, v='5.199')
        elif entry1 == 5:
            photo = api.photos.getOwnerPhotoUploadServer(owner_id=int(df1['id'][n]) ,v='5.199')
            url = photo['upload_url']
            entry2 = input('Path to photo >>> ').strip("'")
            photo = requests.post(url, files={'file1':open(entry2, 'rb')})
            api.photos.saveOwnerPhoto(server=photo.json()['server'], hash=photo.json()['hash'], photo=photo.json()['photo']) 
            new_photo = api.photos.get(owber_id=int(df1['id'][n]), album_id='profile', v='5.199')
            print(new_photo['items'][-1]['sizes'][-1]['url'])
        elif entry1 == 6:
            old_photo = api.photos.get(owber_id=int(df1['id'][n]), album_id='profile', v='5.199')
            print(old_photo['items'][-1]['sizes'][-1]['url'])
            entry = int(input('1 >>> Remove old photo\n>>> '))
            if entry1 == 1: api.photos.delete(owner_id=df1['id'][n], photo_id=old_photo['items'][-1]['id'], v='5.199')
    elif entry == 4:
        entry = int(input('1 >>> remove friends\n2 >>> check dead bots\n3 >>> friend request\n4 >>> like\n5 >>> join group\n7 >>> leave groups\n8 >>> repost\n9 >>> collect published posts\n>>> '))
        bots_id = input('Range bots >>> ').split('-')
        next_id = int(bots_id[0])
        last_id = int(bots_id[-1])  
        if entry == 4 or entry == 8:
            type_entry = input('Type >>> ')
            if type_entry != 'post':
                post = input('Link on media >>> ')
                post = post.split(f'z={type_entry}')
                post = post[1].split('_')
                group_id = int(post[0])
                post_id = int(post[1])
            else:
                post = input('Link on post >>> ')
                post = post.split('wall')
                post = post[1].split('_')
                group_id = int(post[0])
                post_id = int(post[1])      
        elif entry == 3: 
            user_id = int(input('User id >>> '))
        elif entry == 5:
            group_id = int(input('Group id >>> '))
        if entry == 2:
            for id, i in enumerate(df9['phone']):
                try:
                    api = vk.UserAPI(user_login=str(i), user_password=str(df9['password'][id]), v='5.199')
                    print(api.users.get(user_ids=int(df9['id'][id])))
                except vk.exceptions.VkAuthError as e:
                    print(id, e)
            exit()
        for id, i in enumerate(df1['token']):
            if last_id >= id >= next_id:
                try:
                    access_token=str(df1['token'][id][45:265])
                    api = vk.API(access_token=access_token, v='5.199')
                    if entry == 1:
                        bots = [i for i in df1['id']]
                        my_friends = api.friends.get(user_id=int(df1['id'][id]), v='5.199')
                        for i in my_friends['items']:
                            if i in bots: api.friends.delete(user_id=i, v='5.199'), print('Removing >>> ', id)
                    elif entry == 3: api.friends.add(user_id=user_id)
                    elif entry == 4: api.likes.add(type=type_entry, owner_id=group_id, item_id=post_id), sleep(5)
                    elif entry == 8: api.wall.repost(object='wall'+str(group_id)+'_'+str(post_id)), sleep(5)
                    elif entry == 5: api.groups.join(group_id=group_id, v='5.199')
                    elif entry == 7: 
                        mygroups = api.groups.get(user_id=int(df1['id'][n]), v='5.199')
                        for id1, i in enumerate(mygroups['items']):
                            if i['id'] not in [j for j in df1['id']]: api.groups.leave(group_id=i['id'], v='5.199'), print(id1)
                    elif entry == 9:
                            results = api.notifications.get(count=100, v='5.199')
                            for i in results['items']:
                                try:
                                    if 'url' in i['action']:
                                        if 'wall-' in i['action']['url'] and 'reply=' not in i['action']['url']:
                                            if i['action']['url'] not in [j.strip() for j in df8['link_used']]: 
                                                names.append(df1['name'][id])
                                                dates.append(datetime.datetime.fromtimestamp(i['date']).strftime('%Y-%m-%d %H:%M'))
                                                links.append(i['action']['url'])
                                                try: posts.append(i['text'])
                                                except KeyError: posts.append('-')
                                except KeyError: pass
                    print(id)
                except vk.exceptions.VkAPIError as e: print(id, e.message) 
        if entry == 2: xlsx('dead_bots')
        elif entry == 9: xlsx('published_posts')
    elif entry == 1:
        entry = int(input('0 >>> Excel\n1 >>> Leave\n2 >>> Search\n3 >>> Get group info\n6 >>> Fresh\n7 >>> Join special\n8 >>> Get group id\n>>> ')) 
        if entry == 0:
            for i in range(5):
                mygroups = api.groups.get(user_id=int(df1['id'][n]), offset=offset, fields=['members_count', 'city', 'can_suggest'],  extended=1, v='5.199')
                offset+=1000
                for i in mygroups['items']:
                    if i['members_count'] >= 1000 and i['id'] not in ids and i['id'] not in list(df3['id']):
                        ids.append(i['id'])
                        links.append(r'https://vk.com/' + i['screen_name'])
                        titles.append(i['name'])
                        members.append(i['members_count'])
                        suggests.append(i['can_suggest'])
                        if 'city' in i: cities.append(i['city']['title'])
                        else: cities.append('-')
            xlsx('user_groups')
        elif entry == 3:
            for id, i in enumerate(df3['id']):
                if last_id >= id >= next_id:
                    my_ids.append(i)
            s= 0
            f = 500
            for j in range(c((last_id-next_id)/500)):
                print(len(my_ids[s:f]))
                groups = api.groups.getById(group_ids=my_ids[s:f], fields=['members_count', 'city', 'can_suggest'], v='5.199')
                for i in groups['groups']:
                    if i['members_count'] >= 1000 and i['id'] not in ids:
                        ids.append(i['id'])
                        links.append(r'https://vk.com/' + i['screen_name'])
                        titles.append(i['name'])
                        members.append(i['members_count'])
                        suggests.append(i['can_suggest'])
                        if 'city' in i: cities.append(i['city']['title'])
                        else: cities.append('-')
                s += 500
                f += 500
            xlsx('user_groups')
        elif entry == 8:
            for id, i in enumerate(df3['link']):
                if last_id >= id >= next_id:
                    i = i.split(r'vk.com/')
                    i = i[-1]
                    ids0 = api.groups.getById(group_id=i, v='5.199')
                    for i in ids0['groups']:
                        ids.append(i['id'])
                        print(i['id'])
            xlsx('groups_id')
        elif entry == 7:
            for i in range(5):
                mygroups = api.groups.get(user_id=int(df1['id'][n]), offset=offset, fields=['members_count', 'city', 'can_suggest'],  extended=1, v='5.199')
                for j in mygroups['items']: 
                    if j['id'] not in my_ids:
                        my_ids.append(j['id'])
                offset+=1000
            for id, i in enumerate(df3['id']):
                if last_id >= id >= next_id and i not in my_ids:
                    execute_main_commands(join=1)
        elif entry == 1:
            mygroups = api.groups.get(user_id=int(df1['id'][n]), fields=['can_suggest'],  extended=1, v='5.199')
            for id, j in enumerate(mygroups['items']):
                api.groups.leave(group_id=j['id'], v='5.199')
                print(id)
        elif entry == 2:
            entry = int(input('1 >>> Group and city\n2 >>> 1000 groups\n>>> '))
            print(*[(id, i.split('$')[0]) for id, i in enumerate(df5['word'])], sep='\n')
            word = int(input('>>> '))
            for lst0 in df5['word'][word:word+1]:
                lst0 = lst0.split('$')
                for query0 in lst0:
                    if entry == 1:
                        for lst1 in df2['регіон']:
                            lst1 = lst1.split('$')
                            for query1 in lst1:
                                search = api.groups.search(q=str(query0+' '+query1), type='group',  extended=1, fields=['can_suggest', 'members_count', 'city', 'is_closed', 'wall'], v='5.199')
                                print(query0+' '+query1)
                                for i in search['items']:
                                    if i['members_count'] >= 500 and i['id'] not in [int(i) for i in df3['id']] and i['id'] not in ids and i['is_closed'] == 0 and i['wall'] == 2:
                                        ids.append(i['id'])
                                        links.append('https://vk.com/' + i['screen_name'])
                                        titles.append(i['name'])
                                        members.append(i['members_count'])
                                        suggests.append(i['can_suggest'])
                                        if 'city' in i: cities.append(i['city']['title'])
                                        else: cities.append('-')
                    elif entry == 2:
                        search = api.groups.search(q=query0, extended=1, offset=0, type='group', count=1000, sort=0, fields=['can_suggest', 'members_count', 'city', 'is_closed', 'wall'], v='5.199')
                        print(query0, '\ntotal: ', search['count'], ', per query:',len(search['items']))
                        for i in search['items']:
                            if i['members_count'] >= 500 and query0.lower() in i['name'].lower() and i['id'] not in list(df3['id']) and i['is_closed'] == 0 and i['wall'] == 2 and i['id'] not in ids:
                                ids.append(i['id'])
                                links.append(r'https://vk.com/' + i['screen_name'])
                                titles.append(i['name'])
                                members.append(i['members_count'])
                                suggests.append(i['can_suggest'])
                                if 'city' in i: cities.append(i['city']['title'])
                                else: cities.append('-')
            xlsx('user_groups') 
        elif entry == 6:
            for id, i in enumerate(df3['id']):
                try:
                    if last_id >= id >= next_id:
                        if id in range(0, 100000, 100): print(id)
                        last_post = api.wall.get(owner_id=-i, v='5.199')
                        signers = [j['signer_id'] for j in last_post['items'] if 'signer_id' in j]
                        if last_post['items'][2]['date'] >= end_time and len(signers) > 0: from_signers.append(1)
                        elif last_post['items'][2]['date'] >= end_time and len(signers) == 0: from_signers.append(0)
                        elif last_post['items'][2]['date'] < end_time: from_signers.append(-1)
                        else: from_signers.append(-2)
                except (vk.exceptions.VkAPIError, IndexError):
                    try:
                        if last_id >= id >= next_id:
                            if id in range(0, 100000, 100): print(id)
                            execute_main_commands(join=1)
                            last_post = api.wall.get(owner_id=-i, v='5.199')
                            signers = [j['signer_id'] for j in last_post['items'] if 'signer_id' in j]
                            if last_post['items'][2]['date'] >= end_time and len(signers) > 0: from_signers.append(1)
                            elif last_post['items'][2]['date'] >= end_time and len(signers) == 0: from_signers.append(0)
                            elif last_post['items'][2]['date'] < end_time: from_signers.append(-1)
                            else: from_signers.append(-2) 
                    except (vk.exceptions.VkAPIError, IndexError): 
                        print('Check it', df3['link'][id])
                        from_signers.append(-3) 
            xlsx('signer')
    elif entry == 2:
        entry = int(input('1 >>> Upload media\n2 >>> Search news\n5 >>> Comment on post\n6 >>> Find post\n7 >>> Statistic of post\n9 >>> User statistic\n>>> '))
        if entry == 7 or entry == 9:
            data = [n for n in df10['id']]
            type = int(input('1 >>> Post\n2 >>> Video\n>>> '))
            for id1, i in enumerate(df8['link']):
                try:
                    if not isinstance(i, float):
                        if entry == 9:
                            if type == 1:
                                i = i.strip()
                                k = i.split('wall')
                                l = k[1].split('_')
                                info = api.wall.getComments(owner_id=l[0], extended=1, post_id=l[1], need_likes=1,count=100)
                                for i in info['profiles']:
                                    if i['id'] not in user_ids and i['id'] not in data:
                                        names.append(str(i['first_name'])+' '+str(i['last_name']))
                                        links.append('https://vk.com/id'+str(i['id'])) 
                                        types.append('comment')
                                        user_ids.append(i['id'])
                                info = api.likes.getList(type='post', owner_id=l[0], item_id=l[1], extended=1, count=1000)
                                for i in info['items']:
                                    if i['id'] not in user_ids and i['id'] not in data:
                                        names.append(str(i['first_name'])+str(i['last_name']))
                                        links.append('https://vk.com/id'+str(i['id']))
                                        types.append('like')
                                        user_ids.append(i['id'])
                            elif type == 2:
                                i = i.strip()
                                k = i.split('video')
                                l = k[1].split('_') 
                                offset = 0
                                info = api.likes.getList(type='video', owner_id=l[0], item_id=l[1])
                                for m in range(c(info['count']/1000)):
                                    info = api.likes.getList(type='video', owner_id=l[0], item_id=l[1], offset=offset, extended=1, count=1000)
                                    offset += 1000
                                    for i in info['items']:
                                        if i['id'] not in user_ids and i['id'] not in [n for n in df10['id']]:
                                            names.append(str(i['first_name'])+' '+str(i['last_name']))
                                            links.append('https://vk.com/id'+str(i['id']))
                                            types.append('like')
                                            user_ids.append(i['id'])
                        elif entry == 7:
                            i = i.strip()
                            k = i.split('wall')
                            k = k[1]
                            published_posts = api.wall.getById(posts=str(k).strip(), extended=1, v='5.199')
                            for j in published_posts['items']:
                                group = api.groups.getById(group_id=abs(j['from_id']), fields='members_count', v='5.199')
                                try: 
                                    group_members = group['groups'][0]['members_count']
                                    members.append(group_members)
                                except KeyError: members.append('-')
                                try:links.append('https://vk.com/wall'+str(j['owner_id'])+'_'+str(j['id']))
                                except: links.append('-')
                                try:likes.append(j['likes']['count'])
                                except:likes.append(0)
                                try:reposts.append(j['reposts']['count'])
                                except:reposts.append(0)
                                try:views.append(j['views']['count'])
                                except:views.append(0)
                                try:comments.append(j['comments']['count'])
                                except:comments.append(0)     
                                dates.append(str(datetime.datetime.now())[:-7])
                                c = False
                                for id, l in enumerate(df3['id']):
                                    if abs(j['owner_id']) == int(l):
                                        cities.append(df3['city'][id])
                                        sub_regions.append(df3['sub_region'][id])
                                        regions.append(df3['region'][id])
                                        c = True
                                        break
                                if not c:
                                    cities.append('-')
                                    sub_regions.append('-')
                                    regions.append('-')
                        print(id1)
                except vk.exceptions.VkAPIError as e: print(e.message)
            if entry == 7: xlsx('statistic')
            elif entry == 9: xlsx('user_statistic') 
        elif entry == 1:
            medias = []
            media = input('Path to media >>> ').split("$")
            for i in range(len(media)):
                try:
                    media_type = re.search(r'[.]{1}[aA-zZ]+\d*', str(media[i])).group(0)
                    if media_type.lower() in ['.jpeg', '.jpg', '.png', '.img']:
                        server = api.photos.getWallUploadServer(v='5.199')
                        url = server['upload_url']
                        photo = requests.post(url, files={'file1':open(media[i], 'rb')})
                        photo = photo.json()
                        photo = api.photos.save(album_id=server['album_id'], server=photo['server'], photos_list=photo['photo'], hash=str(photo['hash']))
                        medias.append('photo'+str(photo[0]['owner_id'])+'_'+str(photo[0]['id'])) 
                    elif media_type.lower() in ['.mp4', '.m4v', '.f4v', '.lrv', '.webm']:    
                        server = api.video.save(v='5.199')
                        url = server['upload_url']
                        video = requests.post(url, files={'file1':open(media[i], 'rb')})
                        video = video.json()
                        medias.append('video'+str(video['owner_id'])+'_'+str(video['video_id']))
                    elif media_type in ['.mp3']:
                        server = api.audio.getUploadServer()
                        url = server['upload_url']
                        audio =  requests.post(url, files={'file1':open(media[i], 'rb')})
                        audio = audio.json()
                        audio.update({'artist': 'noname','title': 'noname',})
                        audio = api.audio.save(server=audio['server'], audio=audio['audio'])
                        medias.append('audio'+audio['ads']['content_id'])
                except vk.exceptions.VkAPIError as e: print(e.code)
            print(*medias, sep='$')
        elif entry == 5:
            entry_type = int(input('1 >>> Target\n2 >>> Blind\n>>> '))
            entry = int(input('1 >>> Auto\n2 >>> Manual\n>>> '))
            if entry == 2:
                comment = df1['text'][n].split('$')
                c = r.randint(0, len(comment)-1)
            if entry_type == 1:
                base = []
                for i in df8['link']:
                    if not isinstance(i, float):
                        k = i.split('wall') 
                        k = k[1]
                        base.append(k)
            elif entry_type == 2:
                base = df3['id']
            for i0, i in enumerate(base):
                if last_id >= i0 >= next_id:
                    try:
                        if entry_type == 1:
                            group_id = i.split('_')[0]
                            post_id = i.split('_')[1]
                        elif entry_type == 2:
                            last_post = api.wall.get(owner_id=-i, v='5.199')
                            last_post = last_post['items'][2]
                            group_id = last_post['from_id']
                            post_id = last_post['id']
                        if entry == 1:
                            posts = api.wall.getById(posts=1, v='5.199')
                            text = posts['items'][0]['text']
                            ai = requests.get(f'https://sharlock-mt6ud.ondigitalocean.app/app/AskSharlock?input={text}', headers={'token': 'f7c5cbd11024d1d27f7960d77389aab2'})
                           # ai = requests.get(f'https://sharlock-mt6ud.ondigitalocean.app/app/AskSharlock?input={text}&count=5', headers={'token': 'f7c5cbd11024d1d27f7960d77389aab2'})
                            answer = ai.json()
                            print(answer)
                            exit()
                            api.wall.createComment(owner_id=group_id, post_id=post_id, message=answer, attachments=media_id, v='5.199')
                        elif entry == 2: 
                            api.wall.createComment(owner_id=group_id, post_id=post_id, message=message, attachments=media_id, v='5.199')
                        comments = api.wall.getComments(owner_id=group_id, post_id=post_id, sort='desc', count=100, v='5.199')
                        for k in comments['items']:
                            if k['from_id'] == int(df1['id'][n]):
                                k1 = k['id']
                                print('https://vk.com/wall'+str(group_id)+'_'+str(post_id)+f'?reply={k1}')
                                links.append('https://vk.com/wall'+str(group_id)+'_'+str(post_id)+f'?reply={k1}')        
                        sleep(r.randint(5, 10))
                    except requests.exceptions.JSONDecodeError as e: print(e)
                    except vk.exceptions.VkAPIError as e: print(e.message)
            xlsx('comments')
        elif entry == 2:
            end_time = 3600
            q = input('Query >>> ')
            for j in range(23):
                news = api.newsfeed.search(q=q, count=200, end_time=str(int(epoch)-end_time), v='5.199')
                for i in news['items']:
                    if 'views' in i and i['views']['count'] > 500 and i['comments']['can_post'] == 1 and 'https://vk.com/wall'+str(i['from_id'])+'_'+str(i['id']) not in links:
                        links.append('https://vk.com/wall'+str(i['from_id'])+'_'+str(i['id']))
                        print('https://vk.com/wall'+str(i['from_id'])+'_'+str(i['id']))
                end_time += 3600
        elif entry == 6:
            for id, k in enumerate(df8['group_id']):
                try:
                    k = int(k)
                    get_post = api.wall.get(owner_id=-k, extended=1,  v='5.199')
                    for j in get_post['items']:
                        try:
                            if ' '+df8['text'][id].lower().strip()+' ' in ' '+j['text'].lower().strip()+' ':
                                links.append(f'https://vk.com/wall-{k}_{j["id"]}')
                                texts.append(str(j['text']))
                            elif len(j['attachments']) > 0:
                                try:
                                    media_lst = df8['media'][id].split('$')
                                except: 
                                    media_lst = []
                                for i in media_lst:
                                    i0 = re.search(r'[a-zA-Z]+', i).group(0)
                                    for l in j['attachments']:
                                        if i0 == l['type']:
                                            i1 = int(re.search(r'-*[0-9]+', i).group(0))
                                            i2 = int(re.search(r'_[0-9]+', i).group(0)[1:])
                                            if i1 == l[f'{i0}']['owner_id'] and i2 == l[f'{i0}']['id']:
                                                links.append(f'https://vk.com/wall-{k}_{j["id"]}')
                                                texts.append(str(j['text']))
                                                print(f'https://vk.com/wall-{k}_{j["id"]}')
                            elif 'signer_id' in j:
                                if df8['user_id'][id] == j['signer_id']:
                                    links.append(f'https://vk.com/wall-{k}_{j["id"]}')
                                    texts.append(str(j['text']))
                        except vk.exceptions.VkAPIError as e: print(e.code)
                    print(id)
                except vk.exceptions.VkAPIError as e: print(e.code)
                except ValueError as e: pass 
            xlsx('dead_posts')
    elif entry == 3:    
        entry = int(input('1 >>> Get last message\n2 >>> Remove all messages\n3 >>> Send message to admins\n4 >>> Send message to user\n>>> ')) 
        results = api.messages.getConversations(count=200, v='5.199')
        if entry == 1:
            for id, i in enumerate(results['items']):
                group = api.groups.getById(group_id=i['conversation']['peer']['local_id'], v='5.199')
                ids.append(group['groups'][0]['id'])
                links.append(str(r'https://vk.com/'+str(group['groups'][0]['screen_name'])))
                titles.append(group['groups'][0]['name'])
                responses.append(i['last_message']['text'])
                print(id)
            xlsx('last_messages')
        elif entry == 2:
            for id, i in enumerate(results['items']):
                api.messages.deleteConversation(peer_id=i['conversation']['peer']['id'], v='5.199')
                print(id)
                sleep(0.1)
        elif entry == 3:
            next_id = int(input('Next id >>> '))
            last_id = int(input('Last id >>> '))
            for id, i in enumerate(df3['id']):
                if last_id >= id >= next_id:
                    try:
                        api.messages.send(peer_id=-i, random_id=0, message=message, v='5.199')
                        print('Id >>>', id, '<--> Row >>>', id+2)
                        sleep(5)
                    except vk.exceptions.VkAPIError as e: print(e.code)
        elif entry == 4: print('Under development!!!')
    elif entry == 6:
        if isinstance(message, float): print('Empty message!!!'), exit()
        mygroups = []
        for  i in range(5):
            try:
                mygroups0 = api.groups.get(user_id=int(df1['id'][n]), offset=offset, count=1000, v='5.199')
                mygroups += [i for i in mygroups0['items'] if i not in mygroups]
                offset += 1000
            except vk.exceptions.VkAPIError as e: print(e.message)
            except json.decoder.JSONDecodeError as e: print(e)
        for id, i in enumerate(df3['id']):
            if last_id >= id >= next_id and int(df3['id'][id]) not in mygroups:
                try:
                    execute_main_commands(join=1)
                except vk.exceptions.VkAPIError as e: print(e.message)
                except json.decoder.JSONDecodeError as e: print(e)
        for id, i in enumerate(df3['id']):
            if last_id >= id >= next_id:
                try:
                    check_post = api.wall.get(owner_id=-i, filter='suggests', v='5.199')
                    if check_post['count'] != 0:
                        for j in check_post['items']:
                            execute_main_commands(remove=1)
                except vk.exceptions.VkAPIError as e: print(e.message)
                except json.decoder.JSONDecodeError as e: print(e)
        for id, i in enumerate(df3['id']):
            if last_id >= id >= next_id:
                try:
                    execute_main_commands(suggest=1)
                    ids.append(i)
                    user_ids.append(df1['id'][n])
                    texts.append(message)
                except vk.exceptions.VkAPIError as e: print(e.message)
                except json.decoder.JSONDecodeError as e: print(e)
                #sleep(r.randint(1, 60))
        df['group_id'] = ids
        df['user_id'] = user_ids
        df['text'] = texts
        df['media'] = [df1['media_id'][n] for t in range(len(ids))]
        normal_time = str(datetime.datetime.now())[:10]
        df.to_excel(f"code/vk/history/{normal_time} - {df1['name'][n]}.xlsx")
    elif entry == 7:
        entry = int(input('1 >>> Users from requests\n2 >>> User from base\n3 >>> Users from suggested\n4 >>> Remove friends\n5 >>> Remove followers\n>>> '))
        if entry == 1:
            base = api.friends.getRequests(count=1000, out=0, sort=0, need_viewed=1)
            base = [i for i in base['items']] 
            base1 = api.friends.getRequests(count=1000, out=1, sort=0)
        elif entry == 2:
            base = df4['id']
            base1 = api.friends.getRequests(count=1000, out=1, sort=0)
            base1 = [i for i in base1['items']]
        elif entry == 3:
            base = api.friends.getSuggestions(v='5.199')
            base = [i['id'] for i in base['items']]
            base1 = api.friends.getRequests(count=1000, out=1, sort=0)
        elif entry == 4:
            base = api.friends.get(user_id=int(df1['id'][n]), v='5.199')
            base = [i for i in base['items']]
        elif entry == 5:
            base = api.friends.getRequests(count=1000, out=0, sort=0, need_viewed=1)
            base = [i for i in base['items']]
        for id, i in enumerate(base):
#            if last_id >= id >= next_id:
            try:
                if entry in [1, 2, 3]:
                    if i not in base1:
                        api.friends.add(user_id=i, v='5.199')
                        print(id+2)
                    if entry == 2: sleep(r.randint(1150, 1200))
                elif entry == 4: api.friends.delete(user_id=i)
                elif entry == 5: api.account.ban(owner_id=i)
                #print(id)
            except vk.exceptions.VkAPIError as e:
                if e.code == 9: print(id, '>>>',e.message), exit()
                else: print(id, '>>>',e.message) 
