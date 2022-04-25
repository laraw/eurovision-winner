import pandas as pd

countries = pd.read_csv("country_code.csv",header=0)
countries.set_index("Name", drop=True,inplace=True)
clookup = countries.to_dict(orient="index")
# df=countries.applymap(str).groupby('Code')['Name'].apply(list).to_dict()

result_type = "final"
final = pd.read_csv("final2021.csv").to_dict('records')
output = []

for f in final:
    result = {}
    for k, v in f.items():
        result['year'] = '2021'
        result['round'] = result_type
        if str(k) == "Country":
            result['to_country'] = clookup[str(v)]


