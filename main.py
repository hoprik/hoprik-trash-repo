import datetime
import os
import time

import apiStory

offset = datetime.timezone(datetime.timedelta(hours=3))
day = False
timeSend = {8: False, 16: False, 22: False}


def update_story():
    with open("stories/story.txt", "r+") as f:
        story = 0
        try:
            story = int(f.read())
            f.write(str(story))
        except:
            f.write("1")
        return story


def find_story(story):
    files = os.listdir("stories")
    for i in files:
        file_id = i.split("-")[0]
        if story == file_id:
            return i, i.split("-")[1]
    return ""


while True:
    hour = datetime.datetime.now(offset).hour
    if hour in timeSend and not timeSend[hour]:
        if timeSend[hour] == 0 and day:
            day = False
        timeSend[hour] = True
        story_id, author = update_story()
        story = find_story(story_id)
        apiStory.main(story, author)
    if hour == 0 and not day:
        timeSend = {8: False, 16: False, 22: False}
        day = True
    print(hour)
    time.sleep(60)
