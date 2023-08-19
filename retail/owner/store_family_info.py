import os
import sys
import csv
import matplotlib.pyplot as plt
import pandas as pd

# input: python3 store_family_info.py <store_name> <family_name>    
store = sys.argv[1]
family = sys.argv[2]

dataset_path = '/Users/abbasmammadov/Downloads/store-sales-time-series-forecasting/train.csv'

with open("recommendations.csv", "r") as f:
    reader = csv.reader(f)
    # skip header
    reader.__next__()
    for row in reader:
        if str(row[0]) == str(store) and str(row[1]) == str(family):
            recommendation = str(row[2])

# print(recommendation)
df = pd.read_csv(dataset_path)
# print(family)
# print(store)
# print(df)
df = df[df['family'] == str(family)]
df = df[df['store_nbr'] == int(store)]

# print(df)


def decisions(store_id, family):
    df = pd.read_csv(dataset_path)
    df = df[df['family'] == family]
    df = df[df['store_nbr'] == store_id]

    sma = df['sales'].mean()
    sd = df['sales'].std()
    lower = sma - 2.5 * sd
    middle = sma + sd
    upper = sma + 2.5 * sd
    discount = sma - 1.8 * sd
    
    upper = int(upper)
    discount = int(discount)
    lower = int(lower)
    
    return lower, middle, upper, discount

lw, _, up, diss = decisions(int(store), str(family))

with open("result.csv", "r") as f:
    reader = csv.reader(f)
    reader.__next__()
    for row in reader:
        if str(row[0]) == str(store) and str(row[1]) == str(family):
            new_prediction = int(row[2])


plt.hist(df['sales'], bins=200)
plt.axvline(x=lw, color='y', linestyle='dashed', linewidth=2, label="(re)move thershold)")
plt.axvline(x=diss, color='m', linestyle='dashed', linewidth=2, label ="discount recommmendation")
plt.axvline(x=up, color='g', linestyle='dashed', linewidth=2, label ="recommend to keep")

# add a point with star shape to show the location of predicted point with some different color
plt.axvline(x=new_prediction, color='r', linestyle='solid', linewidth=2, label = "predicted value")

plt.legend(loc='upper right')
plt.show()

# output is plt (figure for graph) and recommendation (corresponding decision suggegsted to owner/manager)
