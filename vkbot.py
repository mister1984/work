import vk
import pandas as pd
import datetime
from time import sleep
import re
import random as r
import requests, json
import vk_captchasolver as vc
import urllib.request
from math import ceil as c 
def xlsx(mode):
    if mode == 'user_groups':
        df['id'] = ids
        df['link'] = links
        df['title'] = titles
        df['members'] = members
        df['city'] = cities
        df['suggest_post'] = suggests
        df['sub_region'] = sub_regions
        df['region'] = regions
        df.to_excel(f'{id} - user_groups.xlsx')
    elif mode == 'dead_bots':
        df['-region'] = regions
        df['-name'] = names
        df['-phone'] = phones
        df['-password'] = passwords
        df['-id'] = ids
        df['-token'] = tokens
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
        df['region'] = regions
        df.to_excel('dead_posts.xlsx')
    elif mode == 'last_messages':
        df['id'] = ids
        df['link'] = links
        df['title'] = titles
        df['response'] = responses
        df.to_excel('last_messages.xlsx')
    elif mode == 'statistic':
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
    elif mode == 'keyword':
        df['keyword'] = keywords
        df.to_excel('keyword.xlsx')
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
    df3 = pd.read_excel('code/vk/bots_vk.xlsx', sheet_name='groups')
    df4 = pd.read_excel('code/vk/bots_vk.xlsx', sheet_name='search')
    df6 = pd.read_excel('code/vk/bots_vk.xlsx', sheet_name='district')
    df8 = pd.read_excel('code/vk/bots_vk.xlsx', sheet_name='published_posts')
    df9 = pd.read_excel('code/vk/bots_vk.xlsx', sheet_name='dead_bots')
    access_token=str(df1['token'][n][45:265])
    api = vk.API(access_token=access_token, v='5.199')
    bot = api.users.get(user_ids=df1['id'][n], fields=['sex', 'bdate', 'city'], v='5.199')
    if bot[0]['sex'] == 1: 
        sex = 'Woman'
    if bot[0]['sex'] == 2:
        sex = 'Man'
    try: bot = bot[0]['first_name']+' '+bot[0]['last_name']+'\n'+sex+'\n'+str(bot[0]['bdate']+'\n'+str(bot[0]['city']['title'])+'\n'+str(df1['region'][n]))
    except KeyError:  bot = bot[0]['first_name']+' '+bot[0]['last_name']+'\n'+sex+'\n'+str(bot[0]['bdate']+'\n'+'No city'+'\n'+str(df1['region'][n]))
    message = df1['text'][n]
    try: media_id = df1['media_id'][n].split(',')
    except AttributeError: media_id = []
    try:
        groups_id = df1['groups_id'][n].split('-')
        next_id = int(groups_id[0])
        last_id = int(groups_id[1])
    except AttributeError: 
        next_id, last_id = -1, -1

    ids, links, titles, members, cities, suggests, regions, sub_regions, likes, reposts, views, comments, dates, posts, lst, numbers, names, phones, passwords, tokens, responses, my_ids, keywords = [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []
    offset = 0
    epoch = datetime.datetime.now().strftime('%s')
    end_time = int(epoch) - 864000
    entry = int(input(f'{bot}\n0 >>> exit\n1 >>> groups\n2 >>> posts\n3 >>> messages\n4 >>> users\n5 >>> settings\n>>> '))
    if entry == 0: exit()
    elif entry == 5:
        entry = int(input('1 >>> Change age\n2 >>> Change name\n3 >>> Change sex\n4 >>> Change city\n5 >>> Upload main photo\n6 >>> See main photo\n>>> '))
        if entry == 1:
            age = input('New age >>> ')
            api.account.saveProfileInfo(bdate=age, v='5.199')
        elif entry == 2:
            full_name = input('Full name >>> ')
            full_name.split(' ')
            first_name = full_name[0]
            last_name = full_name[1]
            api.account.saveProfileInfo(first_name=first_name, last_name=last_name, v='5.199')
        elif entry == 3:
            sex = int(input('1 >>> Female\n2 >>> Male\n>>> '))
            api.account.saveProfileInfo(sex=sex, v='5.199')
        elif entry == 4:
            city = input('City >>> ')
            city = api.database.getCities(q=city, v='5.199')
            city = city['items'][0]['id']
            api.account.saveProfileInfo(city_id=city, v='5.199')
        elif entry == 5:
            photo = api.photos.getOwnerPhotoUploadServer(owner_id=df1['id'][n] ,v='5.199')
            url = photo['upload_url']
            entry2 = input('Path to photo >>> ').strip("'")
            photo = requests.post(url, files={'file1':open(entry2, 'rb')})
            api.photos.saveOwnerPhoto(server=photo.json()['server'], hash=photo.json()['hash'], photo=photo.json()['photo']) 
        elif entry == 6:
            old_photo = api.photos.get(owber_id=df1['id'][n], album_id='profile', v='5.199')
            print(old_photo['items'][-1]['sizes'][-1]['url'])
            entry = int(input('1 >>> Remove old photo\n>>> '))
            if entry == 1: api.photos.delete(owner_id=df1['id'][n], photo_id=old_photo['items'][-1]['id'], v='5.199')
    elif entry == 4:
        entry = int(input('1 >>> remove friends\n2 >>> remove dead bot\n3 >>> friend request\n4 >>> like\n5 >>> join group\n7 >>> leave groups\n8 >>> repost\n9 >>> collect published posts\n>>> '))
        if entry == 4 or entry == 8:
            post = input('Link on post >>> ')
            post = post.split('wall')
            post = post[1].split('_')
            group_id = int(post[0])
            post_id = int(post[1])
            bots_id = input('Range bots >>> ').split('-')
            next_id = int(bots_id[0])
            last_id = int(bots_id[1])        
        elif entry == 3: 
            user_id = int(input('User id >>> '))
        elif entry == 5:
            group_id = int(input('Group id >>> '))
        for id, i in enumerate(df1['token']):
            try:
                access_token=str(df1['token'][id][45:265])
                api = vk.API(access_token=access_token, v='5.199')
                if entry == 1:
                    bots = [i for i in df1['id']]
                    my_friends = api.friends.get(user_id=int(df1['id'][id]), v='5.199')
                    for i in my_friends['items']:
                        if i in bots: api.friends.delete(user_id=i, v='5.199'), print('Removing >>> ', id)
                elif entry == 2:
                    try:
                        api.users.getInfo(user_ids=df1['id'][id], v='5.199')      
                    except vk.exceptions.VkAPIError as e:
                        if e.code == 5: 
                            print(id)
                            regions.append(df1['region'][id])
                            names.append(df1['name'][id])
                            phones.append(df1['phone'][id])
                            passwords.append(df1['password'][id])
                            ids.append(df1['id'][id])
                            tokens.append(df1['token'][id])
                elif entry == 3:
                    api.friends.add(user_id=user_id)
                    print(id)
                elif entry == 4:
                    if last_id >= id >= next_id:
                        print(id)
                        api.likes.add(type='post', owner_id=group_id, item_id=post_id), sleep(5)
                elif entry == 8:
                    if last_id >= id >= next_id:
                        print(id)
                        api.wall.repost(object='wall'+str(group_id)+'_'+str(post_id)), sleep(5)
                elif entry == 5:
                    api.groups.join(group_id=group_id, v='5.199')
                    print(id)
                elif entry == 7: 
                    mygroups = api.groups.get(user_id=int(df1['id'][n]), v='5.199')
                    for id1, i in enumerate(mygroups['items']):
                        if i['id'] not in [j for j in df1['id']]:
                            api.groups.leave(group_id=i['id'], v='5.199')
                            print(id1)
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
            except vk.exceptions.VkAPIError as e: print(id, e.message) 
        if entry == 2: xlsx('dead_bots')
        if entry == 9: xlsx('published_posts')
    if entry == 1:
        entry = int(input('0 >>> Excel\n1 >>> Leave\n2 >>> Search\n3 >>> Keyword\n5 >>> Sort\n6 >>> Fresh\n7 >>> Join special\n8 >>> Get group id\n>>> ')) 
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
                        regions.append('-')
                        sub_regions.append('-')
            xlsx('user_groups')
        elif entry == 8:
            df = pd.DataFrame()
            print(len(set(df3['link'])))
            print(len(list(df3['link'])))
            for id, i in enumerate(df3['link']): 
                i = i.split(r'vk.com/')
                i = i[-1]
                ids0 = api.groups.getById(group_id=i, v='5.199')
                for i in ids0['groups']:
                    ids.append(i['id'])
                    print(i['id'])
            df['id'] = ids
            df.to_excel('id.xlsx')
        elif entry == 3:
            for id, i in enumerate(df3['title']):
                if not isinstance(i, float):
                    i = ' '+i.lower()+' '
                    if 'женский' in i or 'мамочки' in i or 'мамы' in i or 'семья' in i or 'дети' in i: keywords.append('женский')
                    elif  'поиск' or 'пленные' in i or 'сво ' in i or 'чвк ' in i or 'сводки ' in i or 'армия' in i or 'мобилизация' in i or 'штурм ' in i or 'военкор' in i or 'война' in i: keywords.append('сво')
                    elif 'подслушано' in i or 'прослушано' in i: keywords.append('подслушано') 
                    elif 'чп ' in i or 'дтп ' in i or 'черный список ' in i or 'белый список ' in i or 'жесть ' in i or 'типичный ' in i or 'инцидент ' in i: keywords.append('другие')
                    elif 'news' in i or 'новости' in i: keywords.append('новости')
                    else: keywords.append('-')
            xlsx('keyword') 
        elif entry == 7:
            for i in range(5):
                mygroups = api.groups.get(user_id=int(df1['id'][n]), offset=offset, fields=['members_count', 'city', 'can_suggest'],  extended=1, v='5.199')
                for j in mygroups['items']: 
                    if j['id'] not in my_ids:
                        my_ids.append(j['id'])
                offset+=1000
            for id, i in enumerate(df7['id']):
                if i not in my_ids:
                    execute_main_commands(join=1)
        elif entry == 1:
            mygroups = api.groups.get(user_id=int(df1['id'][n]), fields=['can_suggest'],  extended=1, v='5.199')
            for id, j in enumerate(mygroups['items']):
                if j['can_suggest'] == 1:
                    api.groups.leave(group_id=j['id'], v='5.199')
                    print(id)
        elif entry == 5:
            for id, i in enumerate(df7['title']):
                try:
                    if 'халтура' not in i.lower() and 'работа' not in i.lower() and 'авторынок' not in i.lower() and 'знакомства' not in i.lower() and 'зароботок' not in i.lower() and 'магазин' not in i.lower() and 'фитнесс' not in i.lower() and df7['id'][id] not in ids:
                        ids.append(df7['id'][id])
                        links.append(df7['link'][id])
                        titles.append(df7['title'][id])
                        members.append(df7['members'][id])
                        suggests.append(df7['suggest_post'][id])
                        cities.append(df7['city'][id])
                        counter = False
                        for j in range(len(list(df6['city']))):
                            city = df6['city'][j]+' '    
                            if city.lower() in i.lower()+' ': 
                                regions.append(df6['region'][j])
                                sub_regions.append(df6['sub_region'][j])
                                counter = True
                                break               
                        if not counter:
                            regions.append(df7['region'][id])
                            sub_regions.append(df7['sub_region'][id])
                except: pass
            xlsx('user_groups')
        elif entry == 2:
            entry = int(input('1 >>> One groups\n2 >>> Many groups\n>>> '))
            if entry == 1:
                for id0, query0 in enumerate(df6['city']):
                    print(id0)
                    for id1, query1 in enumerate(df4['word']):
                        search = api.groups.search(q=str(query1+' '+query0), extended=1, fields=['can_suggest', 'members_count', 'city'], v='5.199')
                        for i in search['items']:
                            if i['members_count'] >= 1000 and query1.lower() in i['name'].lower() and i['id'] not in list(df3['id']) and i['id'] not in ids:
                                ids.append(i['id'])
                                links.append(r'https://vk.com/' + i['screen_name'])
                                titles.append(i['name'])
                                members.append(i['members_count'])
                                suggests.append(i['can_suggest'])
                                regions.append(df4['region'][id1])
                                sub_regions.append(df4['word'][id1])
                                if 'city' in i: cities.append(i['city']['title'])
                                else: cities.append('-')
            elif entry == 2:
                for id1, query in enumerate(df4['word']):
                    offset = 0
                    for j in range(2):
                        search = api.groups.search(q=str(query), extended=1, offset=offset,  count=500, fields=['can_suggest', 'members_count', 'city'], v='5.199')
                        ids1 = [i['id'] for i in search['items']]
                        offset += 500
                        if len(ids1) > 0:
                            groups = api.groups.getById(group_ids=ids1, fields=['can_suggest', 'members_count', 'city'], v='5.199')
                            for i in groups['groups']:
                                if i['members_count'] >= 1000 and query.lower() in i['name'].lower() and i['id'] not in list(df3['id']) and i['id'] not in ids:
                                    ids.append(i['id'])
                                    links.append(r'https://vk.com/' + i['screen_name'])
                                    titles.append(i['name'])
                                    members.append(i['members_count'])
                                    suggests.append(i['can_suggest'])
                                    regions.append(df4['region'][id1])
                                    sub_regions.append(df4['word'][id1])
                                    if 'city' in i: cities.append(i['city']['title'])
                                    else: cities.append('-')
            xlsx('user_groups') 
        elif entry == 6:
            for id, i in enumerate(df3['id']):
                try:
                    if last_id >= id >= next_id:
                        if id in range(0, 10000, 100): print(id)
                        last_post = api.wall.get(owner_id=-i, v='5.199')
                        if last_post['items'][2]['date'] >= end_time:
                            ids.append(df3['id'][id])
                            links.append(df3['link'][id])
                            titles.append(df3['title'][id])
                            members.append(df3['members'][id])
                            cities.append(df3['city'][id])
                            suggests.append(df3['suggest_post'][id])
                            regions.append(df3['region'][id])
                            sub_regions.append(df3['sub_region'][id]) 
                except (vk.exceptions.VkAPIError, IndexError) :
                    try:
                        execute_main_commands(join=1)
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
                    except (vk.exceptions.VkAPIError, IndexError): print('Check it', df7['link'][id])
            xlsx('user_groups')
    elif entry == 2:
        print(f'Sent with {len(media_id)} attachments!')
        selected_id = [id for id, i in enumerate(df3['id']) if df3['keyword'][id] == df1['keyword'][n]]
        #selected_id = [id for id, i in enumerate(df3['id']) if df3['region'][id] == df1['region'][n]]
        print(f'{min(selected_id)} <---> {max(selected_id)}')
        entry = int(input('2 >>> Upload photo\n3 >>> Suggest post\n5 >>> Comment on post\n6 >>> Find post\n7 >>> Statistic of post\n8 >>> Upload video\n>>> '))
        if entry == 7:        
            for i in df8['link']:
                if not isinstance(i, float):
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
                try:likes.append(j['likes']['count'])
                except:likes.append(0)
                try:reposts.append(j['reposts']['count'])
                except:reposts.append(0)
                try:views.append(j['views']['count'])
                except:views.append(0)
                try:comments.append(j['comments']['count'])
                except:comments.append(0)     
                dates.append(str(datetime.datetime.now())[:-7])  
                if abs(j['from_id']) in list(df3['id']):
                    for id, l in enumerate(df3['id']):
                        if abs(j['from_id']) == int(l):
                            regions.append(df3['region'][id])
                else:
                    regions.append('-')
            xlsx('statistic')
        elif entry == 2:
            server = api.photos.getWallUploadServer(v='5.199')
            url = server['upload_url']
            entry1 = int(input('Number of photos >>> '))
            for i in range(entry1):
                entry2 = input('Path to photo >>> ').strip("'")
                photo = requests.post(url, files={'file1':open(entry2, 'rb')})
                photo = photo.json()
                photo = api.photos.save(album_id=server['album_id'], server=photo['server'], photos_list=photo['photo'], hash=str(photo['hash']))
                print('photo'+str(photo[0]['owner_id'])+'_'+str(photo[0]['id'])) 
        elif entry == 8:
            server = api.video.save(v='5.199')
            url = server['upload_url']
            entry1 = int(input('Number of videos >>> '))
            for i in range(entry1):
                entry2 = input('Path to video >>> ').strip("'")
                video = requests.post(url, files={'file1':open(entry2, 'rb')})
                video = video.json()
                print('video'+str(video['owner_id'])+'_'+str(video['video_id']))
        elif entry == 3:
            if isinstance(message, float): print('Empty message!!!'), exit()
            mygroups = api.groups.get(user_id=int(df1['id'][n]), count=1000, v='5.199')
            mygroups = [i for i in mygroups['items']]
            for id, i in enumerate(df3['id']):
                if last_id >= id >= next_id and int(df3['id'][id]) not in mygroups:
                    execute_main_commands(join=1)
            for id, i in enumerate(df3['id']):
                if last_id >= id >= next_id:
                    try:
                        check_post = api.wall.get(owner_id=-i, filter='suggests', v='5.199')
                        if check_post['count'] != 0:
                            for j in check_post['items']:
                                execute_main_commands(remove=1)
                    except vk.exceptions.VkAPIError as e: print(e.message)
            for id, i in enumerate(df3['id']):
                if last_id >= id >= next_id:
                    execute_main_commands(suggest=1)
                    sleep(r.randint(10, 60))
        elif entry == 5:
            entry = int(input('1 >>> Target\n2 >>> Blind\n>>> '))
            entry = int(input('1 >>> Auto\n2 >>> Manual\n>>> '))
            if entry == 2:
                comment = df1['text'][n].split('$')
                c = r.randint(0, len(comment)-1)
     #       for i in df8['link']: 
    #            k = i.split('wall') 
   #             k = k[1] 
  #              ids.append(k)       
 #           published_posts = api.wall.getById(posts=ids, v='5.199')
#            for i0, i in enumerate(published_posts['items']):
            for i0, i in enumerate(df3['id']):
                if last_id >= i0 >= next_id:
                   
#                text = i['text']
#                group_id = i['from_id'] 
 #               post_id = i['id']
                    try:
                        last_post = api.wall.get(owner_id=-i, v='5.199')
                        last_post = last_post['items'][2]
                        group_id = last_post['from_id']
                        post_id = last_post['id']
                        if entry == 1: 
                            ai = requests.get(f'https://sharlock-mt6ud.ondigitalocean.app/app/AskSharlock?input={text}', headers={'token': 'f7c5cbd11024d1d27f7960d77389aab2'})
                            answer = ai.json()['response']
                            api.wall.createComment(owner_id=group_id, post_id=post_id, message=answer, attachments=media_id, v='5.199')
                        elif entry == 2: 
                            api.wall.createComment(owner_id=group_id, post_id=post_id, message=message, attachments=media_id, v='5.199')
                        comments = api.wall.getComments(owner_id=group_id, post_id=post_id, sort='desc', count=100, v='5.199')
                        for k in comments['items']:
                            if k['from_id'] == int(df1['id'][n]):
                                k1 = k['id']
                                print('https://vk.com/wall'+str(group_id)+'_'+str(post_id)+f'?reply={k1}')
                                links.append('https://vk.com/wall'+str(group_id)+'_'+str(post_id)+f'?reply={k1}')        
                        sleep(r.randint(10, 60))
                    except requests.exceptions.JSONDecodeError as e: print(e)
                    except vk.exceptions.VkAPIError as e: print(e.message)
            xlsx('comments')
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
                        except vk.exceptions.VkAPIError as e: print(e.code)
            xlsx('dead_posts')
