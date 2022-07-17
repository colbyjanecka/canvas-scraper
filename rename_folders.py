import yaml
import sys
import os

with open("settings.conf", "r") as ymlfile:
    cfg = yaml.full_load(ymlfile)

courses_downloaded = []
with open(cfg["save_location"] + "course_list.txt", "r") as f:
  for line in f:
        course = line[:-1]
        courses_downloaded.append(course)

for i in range(len(courses_downloaded)):
    course_name = courses_downloaded[i]
    old_name = cfg["save_location"] + 'course_files_export (' + str(i) + ').zip'
    if(i == 0):
        old_name = cfg["save_location"] + "course_files_export.zip"
    new_name = cfg["save_location"] + str(course_name) + '.zip'

    os.rename(old_name, new_name)
