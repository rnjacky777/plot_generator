df = None #dataframe
title_list = None 
colors = ["#B64C2E", "#BC6B49", "#CB8F6F", "#DCAE92","#E8C9B6"]

def get_database_url(sheet_id:str):
    return f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv"
