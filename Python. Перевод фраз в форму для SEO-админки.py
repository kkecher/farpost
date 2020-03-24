with open ('res_полные_вводы2.txt', 'r', encoding='cp1251') as f:
    keywords = f.read().splitlines()

key_200_list = []
key_200_str = ''
i = 1
with open('res', 'w') as f:
    for keyword in keywords:
        key_200_str=''
        print(f'Doing {i} of {len(keywords)}')
        if len(key_200_list)<200:
            key_200_list.append(keyword)
            i+=1
        else:
            f.write('syntax:(')
            for key200 in key_200_list:
                key_200_str+=f'{key200}|'
            key_200_str=key_200_str[:-1]
            f.write(f'{key_200_str}')
            f.write(')\n')
            key_200_list=[]
            i+=1
