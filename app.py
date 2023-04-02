import requests as req
from flask import Flask
import numpy as np
import pandas as pd
import re, nltk, string
from nltk.corpus import stopwords


data = pd.read_excel('carbon-footprint-data.xlsx')
labels = pd.read_excel('labels.xlsx')

names = data["Product name (and functional unit)"]
industries = data["Company's GICS Industry"]
carbons = data["Product's carbon footprint (PCF, kg CO2e)"]
weights = data["Product weight (kg)"]
industry_names = [
        'Food Products',
        'Not used for 2015 reporting',
        'Building Products',
        'Electronic Equipment, Instruments & Components',
        'Chemicals',
        'Construction Materials',
        'Textiles, Apparel & Luxury Goods',
        'Computers & Peripherals',
        'Household Durables',
        'Beverages',
        'Metals & Mining',
        'Semiconductors & Semiconductor Equipment',
        'Software',
        'Paper & Forest Products',
        'Commercial Services & Supplies',
        'Aerospace & Defense',
        'Communications Equipment',
        'Gas Utilities',
        'Wireless Telecommunication Services',
        'Office Electronics',
        'Electrical Equipment',
        'Containers & Packaging',
        'Specialty Retail',
        'Media',
        'Automobiles',
        'Auto Components',
        'Life Sciences Tools & Services',
        'Machinery',
        'Diversified Telecommunication Services',
        'Trading Companies & Distributors',
        'Oil, Gas & Consumable Fuels',
        'Food & Staples Retailing',
        'Tobacco',
        'Personal Products',
        'IT Services',
        ]


unique_industry = {
        'Food Products': [],
        'Not used for 2015 reporting': [],
        'Building Products': [],
        'Electronic Equipment, Instruments & Components': [],
        'Chemicals': [],
        'Construction Materials': [],
        'Textiles, Apparel & Luxury Goods': [],
        'Computers & Peripherals': [],
        'Household Durables': [],
        'Beverages': [],
        'Metals & Mining': [],
        'Semiconductors & Semiconductor Equipment': [],
        'Software': [],
        'Paper & Forest Products': [],
        'Commercial Services & Supplies': [],
        'Aerospace & Defense': [],
        'Communications Equipment': [],
        'Gas Utilities': [],
        'Wireless Telecommunication Services': [],
        'Office Electronics': [],
        'Electrical Equipment': [],
        'Containers & Packaging': [],
        'Specialty Retail': [],
        'Media': [],
        'Automobiles': [],
        'Auto Components': [],
        'Life Sciences Tools & Services': [],
        'Machinery': [],
        'Diversified Telecommunication Services': [],
        'Trading Companies & Distributors': [],
        'Oil, Gas & Consumable Fuels': [],
        'Food & Staples Retailing': [],
        'Tobacco': [],
        'Personal Products': [],
        'IT Services': [],
        }

for i, industry in industries.items():
    unique_industry[industry].append(i)


print(unique_industry)

avgs = []
temp_sum = 0
for industry in industry_names:
    for i in unique_industry[industry]:
        temp_sum += int(carbons[i])
    avgs.append(temp_sum / len(unique_industry[industry]))
    temp_sum = 0

avg_weights = []
for industry in industry_names:
    for i in unique_industry[industry]:
        temp_sum += int(weights[i])
    avg_weights.append(temp_sum / len(unique_industry[industry]))
    temp_sum = 0

print(avgs)
print(avg_weights)

app = Flask(__name__)
@app.route("/carbon/<string:category>/<int:weight>")
def carbon(category, weight):
    index = -1
    for i, industry in enumerate(industry_names):
        if category == industry:
            index = i
    footprint = avgs[i] /  avg_weights[i] * weight
    return f"{footprint}"

@app.route("/category/<string:label>")
def category(label):
    i, c = np.where(labels == label)
    return f"{labels.columns[c][0]}"



if __name__ == '__main__':
    app.run(debug=True)
