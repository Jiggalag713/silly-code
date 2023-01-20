import hashlib
import json
import os
import datetime


def process_directory(dir_name, files):
    tmp_uniques = dict()
    for filename in files:
        fullpath = f'{dir_name}/{filename}'
        tmp_uniques.update({md5_file(fullpath): fullpath})
    return tmp_uniques


def md5_file(filename):
    with open(filename, "rb") as f:
        return hashlib.md5(f.read()).hexdigest()


start = datetime.datetime.now()
uniques = dict()
warns = list()
for step in os.walk('I:/'):
    if not step[1] and '$RECYCLE.BIN' not in step[0]:
        print(f'Now we process {step[0]} directory...')
        tmp_uniq = process_directory(step[0], step[2])
        for key in tmp_uniq.keys():
            if key in uniques:
                value = uniques.get(key)
                value.append(tmp_uniq.get(key))
                uniques.update({key: value})
                # print(f'[WARN] File {tmp_uniq.get(key)} duplicates file {uniques.get(key)}')
                # warns.append(f'[WARN] File {tmp_uniq.get(key)} duplicates file {uniques.get(key)}')
            else:
                uniques.update({key: [tmp_uniq.get(key)]})
                # uniques.update({key: tmp_uniq.get(key)})

warns = dict()
for key in uniques:
    if len(uniques.get(key)) > 1:
        warns.update({key: uniques.get(key)})
with open('warnings.txt', 'w') as f:
    f.write(json.dumps(warns, indent=4, ensure_ascii=False))




# with open('warnings.txt', 'w') as f:
#     for line in warns:
#         f.write(f'{line}\n')

print(f'Data processed in {datetime.datetime.now() - start}')
