import matplotlib.pyplot as plt
import pandas as pd
import csv

dataset_path = '/Users/abbasmammadov/Downloads/store-sales-time-series-forecasting/train.csv'


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
    
    # plt.hist(df['sales'], bins=200)
    
    return lower, middle, upper, discount

stores = [6, 8]
families = ["POULTRY", "SEAFOOD"]
stock_information = {"6_POULTRY": 200, "6_SEAFOOD": 100, "8_POULTRY": 600, "8_SEAFOOD": 80}  # static for now but easily be fetched from data

predictions = {}
recommendations = {}
recommendations_detailed = {}
recommendation = ""

with open("result.csv", "r") as f:
    reader = csv.reader(f)
    # skip header
    reader.__next__()
    for row in reader:
        predictions["{}_{}".format(row[0], row[1])] = int(row[2])
        recommendations["{}_{}".format(row[0], row[1])] = 0
        recommendations_detailed["{}_{}".format(row[0], row[1])] = ""


for store in stores:
    for family in families:
        curr_lw, _, curr_up, curr_diss = decisions(store, family)
        if predictions["{}_{}".format(store, family)] < curr_lw:
            recommendations["{}_{}".format(store, family)] = -2
        elif predictions["{}_{}".format(store, family)] < curr_diss:
            recommendations["{}_{}".format(store, family)] = -1
        elif predictions["{}_{}".format(store, family)] > curr_up:
            recommendations["{}_{}".format(store, family)] = 1
        else:
            recommendations["{}_{}".format(store, family)] = 0
        

for family in families:
    curr_item_is_bad_for = []
    if recommendations["{}_{}".format(store, family)] == -2:
        curr_item_is_bad_for.append(store)    
    
for family in families:
    for store in stores:
        recommendation = ""
        if recommendations["{}_{}".format(store, family)] == 0:
            recommendation += "Hold The {}".format(family)
            if predictions["{}_{}".format(store, family)] < stock_information["{}_{}".format(store, family)]:
                recommendation += " and Order More"
                recommendation += " for Store {}".format(store)
                recommendation += " with an amount of at least {}".format(stock_information["{}_{}".format(store, family)] - predictions["{}_{}".format(store, family)])
            else:
                recommendation += " and Do Not Need to Order More"
                recommendation += " for Store {}".format(store)
                
        elif recommendations["{}_{}".format(store, family)] == -1:
            recommendation += "Discount The {}".format(family)
            recommendation += " for Store {}".format(store)
            
        elif recommendations["{}_{}".format(store, family)] == 1:
            recommendation += "Strongly Recommend to keep and Raise The {}".format(family)
            recommendation += " for Store {}".format(store)
            recommendation += " and Order at least {}".format(stock_information["{}_{}".format(store, family)] - predictions["{}_{}".format(store, family)])
            
        else:
            if  0 < len(curr_item_is_bad_for) < len(stores):
                recommendation += "Move the {}".format(family)
                recommendation += " to different stores with need of this item to balance the stock, since the stores {} are in need of this item".format(list(set(stores) - set(curr_item_is_bad_for)))
            else:
                recommendation += "Remove it from the all the stores!!!"
        
        recommendations_detailed["{}_{}".format(store, family)] = recommendation
        
    
for key in recommendations_detailed.keys():
    print(key, recommendations_detailed[key])
    print("\n")

# save as a csv file
with open("recommendations.csv", "w") as f:
    writer = csv.writer(f)
    writer.writerow(["store_nbr", "family", "recommendation"])
    for key in recommendations_detailed.keys():
        writer.writerow([key.split("_")[0], key.split("_")[1], recommendations_detailed[key]])