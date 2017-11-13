import copy
import csv
import json
import math

import requests

num = 10


def read():
    list = []
    f = open("data.csv")
    for row in csv.reader(f):
        list.append(row)
    f.close()
    return list


def metrica(list):
    users = []
    for j in range(0, len(list)):
        if j == num:
            users.append(0)
            continue
        uivi = 0
        ui = 0
        vi = 0
        for i in range(1, len(list[num])):
            if int(list[num][i]) > 0 and int(list[j][i]) > 0:
                uivi += int(list[num][i]) * int(list[j][i])
                ui += int(list[num][i]) * int(list[num][i])
                vi += int(list[j][i]) * int(list[j][i])
        ui = math.sqrt(ui)
        vi = math.sqrt(vi)
        res = uivi / (ui * vi)
        users.append(res)
    return users


def midMark(list):
    sum = 0
    cnt = 0
    for i in range(1, 31):
        if int(list[i]) != -1:
            sum += int(list[i])
            cnt += 1
    return sum / cnt


def product(allUsers, currentUser, dict, sims):
    answer = []
    for i in range(1, 31):
        if int(currentUser[i]) == -1:
            chisl = 0
            znamen = 0
            for x in dict:
                if int(allUsers[x][i]) != -1:
                    chisl += sims[x] * (int(allUsers[x][i]) - midMark(allUsers[x]))
                    znamen += abs(sims[x])
            ri = midMark(users[num]) + (chisl / znamen)
            answer.append(ri)
    return answer


def recomend(allUsers, currentUser, dict):
    nonWatch = {}
    for i in range(1, 31):
        if int(currentUser[i]) == -1:
            sred = 0
            for x in dict:
                sred += int(allUsers[x][i])
            sred /= len(dict)
            nonWatch[i] = sred
    return nonWatch


def readDays():
    list = []
    f = open("context.csv")
    for row in csv.reader(f):
        list.append(row)
    f.close()
    return list


if __name__ == '__main__':
    users = read()
    days = readDays()
    users = users[1:41]
    days = days[1:41]
    middleMark = midMark(users[num])
    sim = metrica(users)
    old = copy.deepcopy(sim)
    sim.sort(reverse=True)
    dict = {}
    for i in sim[:5]:
        dict[old.index(i)] = i
    answer = product(users, users[num], dict, sim)
    rec = recomend(users, users[num], dict)
    values = sorted(list(set(rec.values())), reverse=True)

    recFilm = 0
    for value in values:
        flag = 0
        for key in rec:
            if rec[key] == value and days[num][int(value)] != "-" and days[num][int(value)] != "Sun" and days[num][
                int(value)] != "Sat":
                recFilm = key
                flag = 1
                break
        if flag == 1:
            break

data = json.dumps({'user': num + 1, '1': {"movie 1": round(answer[0], 2),
                                          "movie 3": round(answer[1], 2),
                                          "movie 10": round(answer[2], 2),
                                          "movie 16": round(answer[3], 1),
                                          "movie 17": round(answer[4], 2),
                                          "movie 22": round(answer[5], 2)
                                          },
                   '2': {"movie " + str(recFilm): answer[1]}})
post = requests.post('https://cit-home1.herokuapp.com/api/rs_homework_1',
                     data=data,
                     headers={'content-type': 'application/json'})
print(post.status_code)
print(post.json())