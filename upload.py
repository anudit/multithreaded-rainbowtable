import csv
import datetime

import deeplake
from dotenv import load_dotenv
from tqdm import tqdm

load_dotenv()

# ds = deeplake.load('hub://anudit/rainbow-table-2', reset=True)

ds = deeplake.empty('hub://anudit/rainbow-table-3')
phonenumber = ds.create_tensor('phonenumber', htype='text')
sha256hash = ds.create_tensor('sha256hash', htype='text')

ds.commit()

import csv
from itertools import islice

chunk_size = 100_000
total = 0

# loader = CSVLoader(file_path='rainbow_table.csv')

with open('rainbow_table.csv', 'r') as file:
    reader = csv.reader(file, delimiter=',')
    
    while True:
        chunk = list(islice(reader, chunk_size))
        if not chunk:  # Break the loop if no more lines are left
            break

        tempP = []
        tempH = []
        for row in chunk:
            tempP.append(row[0])
            tempH.append(row[1])

        ds.extend({
            'phonenumber': tempP,
            'sha256hash': tempH,
        })

        ds.commit()

        total+=chunk_size
        print('done', total, datetime.datetime.now())

