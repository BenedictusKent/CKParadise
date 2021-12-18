import csv
import random

data = []
with open('drink_table_new.csv', newline='') as csvfile:
    rows = csv.reader(csvfile)
    for row in rows:
        data.append(row)

#print(data)


ingrs = []
with open('translation3.csv', newline='') as csvfile:
    rows = csv.reader(csvfile)
    for row in rows:
        ingrs.append(row)

temp_i = []
temp_o = []
for i in ingrs:
    for j in i:
        if '?' in j:
            j = j.replace('?', '')
        if j != '':
            temp_i.append(j)
    temp_o.append(temp_i)
    temp_i = []
ingrs = temp_o
ingrs.remove(ingrs[0])

#print(ingrs)
#print(len(ingrs))

dict = {}
for i in range(611):
    dict[data[i+1][0]] = ingrs[i]
#print(dict)

def choice(flavor, ingredient, piece):

    flavor_choice = []

    for i in data[0]:
        if i == flavor:
            flavor_id = data[0].index(i)
            for j in data:
                if j[flavor_id] == '1':
                    flavor_choice.append(j)
    #print(flavor_choice)
    #print('first= ', len(flavor_choice))

    ingredient_choice = []

    for i in data[0]:
        if i == ingredient:
            ingredient_id = data[0].index(i)
            for j in flavor_choice:
                if j[ingredient_id] == '1':
                    ingredient_choice.append(j)
    #print(ingredient_choice)
    #print('second= ', len(ingredient_choice))

    piece_choice = []

    if piece != '':
        for i in data[0]:
            if i == piece:
                piece_id = data[0].index(i)
                for j in ingredient_choice:
                    if j[piece_id] == '1':
                        piece_choice.append(j)
    else:
        piece_choice = ingredient_choice

    # print(piece_choice)
    #print('third= ', len(piece_choice), '\n')

    if len(piece_choice) > 0:

        result = piece_choice[random.randint(0, len(piece_choice)-1)] # 結果的屬性列
        #print(result)

        flavor = ''
        if result[1] == '1':
            flavor += '#酸 '
        if result[2] == '1':
            flavor += '#甜 '
        if result[3] == '1':
            flavor += '#重 '
        if result[4] == '1':
            flavor += '#苦 '

        #flavor = flavor[:-1]


        feature = ''
        if result[5] == '1':
            feature += '#果香 '
        if result[6] == '1':
            feature += '#濃醇香 '
        if result[7] == '1':
            feature += '#自然香 '
        if result[8] == '1':
            feature += '#純酒香 '

        #feature = feature[:-1]


        thing = ''
        if result[9] == '1':
            thing += '#蘋果 '
        if result[10] == '1':
            thing += '#葡萄 '
        if result[11] == '1':
            thing += '#莓果 '
        if result[12] == '1':
            thing += '#柑橘 '
        if result[13] == '1':
            thing += '#瓜類 '
        if result[14] == '1':
            thing += '#桃類 '
        if result[15] == '1':
            thing += '#檸檬萊姆 '
        if result[16] == '1':
            thing += '#台灣味 '
        if result[17] == '1':
            thing += '#熱帶水果 '
        if result[18] == '1':
            thing += '#綜合 '
        #if result[19] == '1':
            #thing += '#其他 '
        if result[20] == '1':
            thing += '#奶香 '
        if result[21] == '1':
            thing += '#咖啡 '
        if result[22] == '1':
            thing += '#巧克力 '
        if result[23] == '1':
            thing += '#堅果 '
        if result[24] == '1':
            thing += '#薑味 '
        if result[25] == '1':
            thing += '#藥草 '
        if result[26] == '1':
            thing += '#香料 '
        if result[27] == '1':
            thing += '#薄荷 '
        if result[28] == '1':
            thing += '#茶香 '

        #thing = thing[:-1]


        ingr = ''
        ingr_list = dict.get(result[0])
        for i in ingr_list:
            ingr = ingr + i + '\n\n'


        response = result[0] + '\n\n' + flavor + feature + thing + '\n\n\n\n' + ingr

    else:
        response = None

    return response

if __name__ == "__main__":
    print(choice('甜', '果香', '檸檬萊姆'))