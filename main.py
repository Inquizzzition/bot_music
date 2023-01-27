import pandas as pd
import vk_api
import copy
import data as dt
import time
from time import sleep
from yandex_music import Client
open_browser = True

client = Client(dt.YaToken).init()
print('Yandex connect success')

vk_session = vk_api.VkApi(dt.vknumber, dt.vkpass)
vk_session.auth()
vk = vk_session.get_api()
print('VK connect success')

queue = copy.copy(client.queues_list())
track_second = copy.copy(time.time())
paused = False
laststatus = 'temp'

def setstatus(status):
    vk.status.set(text=status)
    sleep(1)
    vk.messages.send(user_id=dt.vkid, message='updated')
    sleep(1)

while(True):
    queue = copy.copy(client.queues_list())
    try:
        last_queue = client.queue(queue[0].id)
        last_track_id = last_queue.get_current_track()
        last_track = last_track_id.fetch_track()
        newstatus = last_track.title + ' | ' + ', '.join(last_track.artists_name())
        if laststatus != newstatus:
            laststatus = newstatus
            setstatus('Слушает Yadex Music: ' + newstatus)
            track_second = copy.copy(time.time())
            paused = False
        else:
            if abs(time.time()-track_second) > 301 and not paused:
                paused = True
                setstatus('')
                sleep(10)

    except:
        continue