import sqlite3
import csv
# opencv, pixellib
data = [{
    'lastname': 'Иванов',
    'firstname': 'Пётр',
    'class_number': 9,
    'class_letter': 'А'},
    {
    'lastname': 'Кузнецов',
    'firstname': 'Алексей',
    'class_number': 9,
    'class_letter': 'В'}]


con = sqlite3.connect('fjords.db')
cur = con.cursor()


def trip(s, country):
    result = cur.execute(f'''SELECT name,coast_length,depth,water_temperature, state
        FROM Fjords, States
        WHERE States.id = country_id and coast_length <= {s}
    ''').fetchall()
    result1 = []
    count = -1
    for i in result:
        if i[4] in country:
            count += 1
            result1.append([])
            result1[count].append(i[0])
            result1[count].append(i[1])
            result1[count].append(i[2])
            result1[count].append(i[3])
    result1.sort(key=lambda x: x[3], reverse=True)
    with open('ikea.csv', 'w', newline='') as csvfile:
        writer = csv.DictWriter(
            csvfile, fieldnames=list(data[0].keys()),
            delimiter=';', quoting=csv.QUOTE_NONNUMERIC)
        writer.writeheader()
        for d in data:
            print(data)
            writer.writerow(d)
    print(result1)
    # print(result)

# count = -1
# travel = []
# result.sort(key=lambda x: (x[2], x[1]))
# for i in result:
#     count += 1
#     travel.append([])
#     travel[count].append(i[0])
#     travel[count].append(i[1])
# con.close()

v = ["Norway"]
trip(60, v)