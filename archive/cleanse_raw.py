import unidecode
import pandas as pd
import ast

def _parse_bytes(bytes_repr):
    result = ast.literal_eval(bytes_repr)

    if not isinstance(result, bytes):
        raise ValueError("Malformed bytes repr")

    return result

def cleanse_string(text):
    
    try:
        byt_text = _parse_bytes(text)
        return unidecode.unidecode(byt_text.decode('utf-8'))
    except:
        try:
            byt_text = text.encode('utf-8')
            return unidecode.unidecode(byt_text.decode('utf-8'))
        except:
            return text
def to_text(text):
    print(type(text))
def cleanse_esc_scraped():
    df = pd.read_csv('esc_scrape_all.csv')
    df['Artist'] =  df['Performer'].apply(cleanse_string)
    df['Title'] =  df['Song'].apply(cleanse_string)
    df.to_csv('esc_scrape_cleansed.csv')
    winners = pd.read_csv('winners_enriched.csv')
    winners['song'] = winners['song'].apply(cleanse_string)
    winners['performer'] = winners['performer'].apply(cleanse_string)

    winners.to_csv('winners_cleansed.csv')

winners = pd.read_csv('winners_enriched.csv')
all_entries = pd.read_csv('esc_scrape_cleansed.csv')
winners_dict = winners.to_dict('records')
entries_dict = all_entries.to_dict('records')

for w in winners_dict:
    year = w.get('year')
    winning_country = w.get('winner')
    runner_up_country = w.get('runner_up')
    for e in entries_dict:
        if e.get("Year") == year and e.get("Country") == winning_country:
            if e['Place SF1'] != None:
                w['winner_sf_score'] = e['Place SF1']
                for rup in entries_dict:
                    
                    if rup['Year'] == year and rup['Place SF1'] == 2:
                        
                        try:
                            margin = int(rup['Points SF1']) - int(e['Points SF1'])
                            print(str(margin))
                            w['sf_margin'] = margin
                        except:
                            print("No")
            if e['Place SF2'] != None:
                w['winner_sf_score'] = e['Place SF2']
        if e.get("Year") == year and e.get("Country") == runner_up_country:
                if e['Place SF1'] != None:
                    w['runner_up_sf_score'] = e['Place SF1']
                if e['Place SF2'] != None:
                    w['runner_up_sf_score'] = e['Place SF2']


winners = pd.DataFrame(winners_dict)
winners.to_csv('winners_out.csv')
#all_data = pd.read_csv('esc_scrape_cleansed.csv')
