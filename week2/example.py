
# !1is & ==的差別
# == 比較的是兩個對象的值是否相等(不同記憶體位置不影響)
a = [1, 2, 3]
b = [1, 2, 3]
print(a == b)  # True，因為列表a和b的值相等
print(a is b)  # False，因為記憶體位置不同，所以較常用==

# is 比較的是兩個對象的引用是否相等(記憶體位置是否相同)
a = [1, 2, 3]
b = a  # 將b指向與a相同的對象
print(a is b)  # True，因為a和b引用相同的對象

# TODO：===

# !2取得 Key/Value Pairs
# 定義一個字典
my_dict = {'a': 1, 'b': 2, 'c': 3}

# 使用 items() 方法取得 Key/Value Pairs，並逐一印出它們
for key, value in my_dict.items():
    print("!2", f"Key: {key}, Value: {value}") #f-string


# !3提取字典中的所有键dictionary.keys()/.values()
keys_list = list(my_dict.keys())
values_list = list(my_dict.values())
print("!3", keys_list)  # 输出：['key1', 'key2', 'key3']
print("!3", values_list)

# !4提取字典中的所有值dictionary.items()
for k, v in my_dict.items(): #tuple 包著 key value的list？？
    print("!4", k, v)
print("!4", my_dict.items())

# !5基於列表生成字典
dic5={x:x*2 for x in [3,4,5]}
print('!5', dic5)

# !6