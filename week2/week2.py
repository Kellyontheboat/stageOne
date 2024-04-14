# 第一題
def find_and_print(messages, current_station):
    # Define station names
    station = ['Songshan', 'Nanjing Sanmin', 'Taipei Arena', 'Nanjing Fuxing', 'Songjiang Nanjing', 'Zhongshan', 'Beimen', 'Ximen', 'Xiaonanmen', 'Chiang Kai-Shek Memorial Hall', 'Guting', 'Taipower Building', 'Gongguan', 'Wanlong', 'Jingmei', 'Dapinglin', 'Qizhang', 'Xindian City Hall', 'Xindian']
    # Sanitize station names
    sanitized_station = [station_name.replace(' ', '').replace(',', '').replace('.', '') for station_name in station]

    # Sanitize current station
    sanitized_cur_stat = current_station.replace(' ', '').replace(',', '').replace('.', '')

    # Initialize variables
    min_difference = len(station)
    closest_friend = None

    for friend, message in messages.items():
        # Sanitize message
        sanitized_message = message.replace(' ', '').replace(',', '').replace('.', '')

        found_station = False

        # Check if friend is at Xiaobitan directly
        if 'Xiaobitan' in sanitized_message:
            qizhang_index = sanitized_station.index('Qizhang')
            satation2 = sanitized_station.copy()
            satation2.insert(qizhang_index + 1, 'Xiaobitan')

            difference = abs(satation2.index('Xiaobitan') - satation2.index(sanitized_cur_stat))

            if satation2.index(sanitized_cur_stat) > satation2.index('Xiaobitan'):
                difference += 1

            if difference < min_difference:
                min_difference = difference
                closest_friend = friend

            found_station = True

        else:
            # Iterate through sanitized stations
            for station_name in sanitized_station:
                if station_name in sanitized_message:
                    difference = abs(sanitized_station.index(sanitized_cur_stat) - sanitized_station.index(station_name))

                    if difference < min_difference:
                        min_difference = difference
                        closest_friend = friend

                    found_station = True
                    break

        if not found_station:
            continue

    print(closest_friend or 'No Service')

messages = {
    "Leslie": "I'm at home near Xiaobitan station.",
    "Bob": "I'm at Ximen MRT station.",
    "Mary": "I have a drink near Jingmei MRT station.",
    "Copper": "I just saw a concert at Taipei Arena.",
    "Vivian": "I'm at Xindian station waiting for you."
}

find_and_print(messages, "Wanlong")  # print Mary
find_and_print(messages, "Songshan")  # print Copper
find_and_print(messages, "Qizhang")   # print Leslie
find_and_print(messages, "Ximen")     # print Bob
find_and_print(messages, "Xindian City Hall")  # print Vivian


# 第二題
booked_times = {}

def initialize_booked_times(consultants):
    for consultant in consultants:
        booked_times[consultant["name"]] = [False] * 24

def book(consultants, hour, duration, criteria):
    def is_available(consultant, hour, duration):
        booked_slots = booked_times[consultant["name"]]
        for i in range(hour, hour + duration):
            if booked_slots[i]:
                return False
        return True

    available_consultants = [consultant for consultant in consultants if is_available(consultant, hour, duration)]

    if not available_consultants:
        print("No Service")
        return

    available_consultants.sort(key=lambda x: x[criteria], reverse=criteria == "rate")

    selected_consultant = available_consultants[0]
    print(selected_consultant["name"])

    booked_slots = booked_times[selected_consultant["name"]]
    for i in range(hour, hour + duration):
        booked_slots[i] = True


consultants = [
    {"name": "John", "rate": 4.5, "price": 1000},
    {"name": "Bob", "rate": 3, "price": 1200},
    {"name": "Jenny", "rate": 3.8, "price": 800}
]

initialize_booked_times(consultants)

book(consultants, 15, 1, "price")  # Jenny
book(consultants, 11, 2, "price")  # Jenny
book(consultants, 10, 2, "price")  # John
book(consultants, 20, 2, "rate")   # John
book(consultants, 11, 1, "rate")   # Bob
book(consultants, 11, 2, "rate")   # No Service
book(consultants, 14, 3, "price")  # John

# 第三題
def func(*data):
    def get_middle_name(name):
        parts = list(name)  # Splitting into list of characters
        if len(parts) == 2:
            return parts[1]
        elif len(parts) == 4:
            return parts[2]
        else:
            return parts[1]

    middle_names = list(map(get_middle_name, data))

    unique_middle_name = []
    # unique_indices = []

    for index, name in enumerate(middle_names):
        if name not in unique_middle_name:
            unique_middle_name.append(name)
            # unique_indices.append(index)
        elif name in unique_middle_name:
            unique_middle_name.remove(name)

    if unique_middle_name:
        name_has_unique_mid = next((name for name in data if unique_middle_name[0] in name), None)
        print(name_has_unique_mid)
    else:
        print("沒有")

func("彭大牆", "陳王明雅", "吳明") # print 彭大牆
func("郭靜雅", "王立強", "郭林靜宜", "郭立恆", "林花花") # print 林花花
func("郭宣雅", "林靜宜", "郭宣恆", "林靜花") # print 沒有
func("郭宣雅", "夏曼藍波安", "郭宣恆") # print 夏曼藍波安

# 第四題
def get_number(index):
  quotient = index // 3
  reminder = index % 3
  result = quotient * 7 + (reminder * 4)
  print(result)

get_number(1) # print 4
get_number(5) # print 15
get_number(10) # print 25
get_number(30) # print 70

# 第五題
def find(spaces, stat, n):
    min_spaces_car_index = -1
    min_spaces = float('inf')

    for i, x in enumerate(stat):
        x = spaces[i] if x != 0 else 0
        if x >= n:
            if x < min_spaces:
                min_spaces = x
                min_spaces_car_index = i

    print(min_spaces_car_index)

find([3, 1, 5, 4, 3, 2], [0, 1, 0, 1, 1, 1], 2)  # print 5
find([1, 0, 5, 1, 3], [0, 1, 0, 1, 1], 4)        # print -1
find([4, 6, 5, 8], [0, 1, 1, 1], 4)               # print 2
