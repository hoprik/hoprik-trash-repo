import datetime
import os
import time
import apiStory

offset = datetime.timezone(datetime.timedelta(hours=3))
day = False
timeSend = {8: False, 16: False, 22: False}



while True:
    hour = datetime.datetime.now(offset).hour
    if hour in timeSend and not timeSend[hour]:
        if timeSend[hour] == 0 and day:
            day = False
        timeSend[hour] = True
        story_id = apiStory.update_story()
        story, author = apiStory.find_story(story_id)
        apiStory.main(story, author)
    if hour == 0 and not day:
        timeSend = {8: False, 16: False, 22: False}
        day = True
    print(hour)
    time.sleep(60)
