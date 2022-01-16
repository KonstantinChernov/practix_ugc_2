import random
import uuid

import pymongo
from timeit import Timer


client = pymongo.MongoClient(host="localhost", port=27017)
db = client['ugc']
marks = db.marks


def gen_mark():
    return {
        'mark': random.random(),
        'film_id': str(uuid.uuid4()),
        'uid': str(uuid.uuid4()),
    }


def marks_count(count=1):
    marks = []

    for item in range(count):
        marks.append(gen_mark())

    return marks


mark1 = gen_mark()
marks10 = marks_count(10)


def insert_one_mark():
    marks.insert_one(mark1)


def insert_marks(count):
    records = marks_count(count)
    marks.insert_many(records)


def show_one_mark():
    marks.find_one(mark1)


def insert_10_marks():
    insert_marks(10)


def insert_100_marks():
    insert_marks(100)


def insert_1000_marks():
    insert_marks(1000)


def insert_10000_marks():
    insert_marks(10000)


t_one = Timer("insert_one_mark()", "from __main__ import insert_one_mark")
t_show_one = Timer("show_one_mark()", "from __main__ import show_one_mark")
t_insert_10 = Timer("insert_10_marks()", "from __main__ import insert_10_marks")
t_insert_100 = Timer("insert_100_marks()", "from __main__ import insert_100_marks")
t_insert_1000 = Timer("insert_1000_marks()", "from __main__ import insert_1000_marks")
t_insert_10000 = Timer("insert_10000_marks()", "from __main__ import insert_10000_marks")


print("Insert one record: ", t_one.timeit(1))
print("Show record: ", t_show_one.timeit(1))
print("Insert 10 records: ", t_insert_10.timeit(1))
print("Show record: ", t_show_one.timeit(1))
print("Insert 100 records: ", t_insert_100.timeit(1))
print("Show record: ", t_show_one.timeit(1))
print("Insert 1000 records: ", t_insert_1000.timeit(1))
print("Show record: ", t_show_one.timeit(1))
print("Insert 10000 records: ", t_insert_10000.timeit(1))
print("Show record: ", t_show_one.timeit(1))
