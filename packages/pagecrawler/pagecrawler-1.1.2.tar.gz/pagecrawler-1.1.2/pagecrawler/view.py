from typing import List

colors = [
    "#FF6384",  # Rotes Rosa
    "#36A2EB",  # Blaues Türkis
    "#FFCE56",  # Gelb
    "#4BC0C0",  # Türkis
    "#9966FF",  # Lila
    "#FF8A80",  # Hellrot
    "#1E88E5",  # Dunkles Blau
    "#FFD54F",  # Orange
    "#4DB6AC",  # Grünblau
    "#7CB342",  # Grün
    "#F06292",  # Rosa
    "#9575CD",  # Hellviolett
    "#64B5F6",  # Himmelblau
    "#FFB74D",  # Orange
    "#81C784",  # Hellgrün
    "#7986CB",  # Blauviolett
    "#A1887F",  # Braungrau
    "#90A4AE",  # Blaugrau
]

basic_chart_html = '<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>'

def build_html(script1, body, script2):
    return f'<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><title>Title</title>{script1}</head><body>{body}<script>{script2}</script></body></html>'

def return_colors():
    times = -1
    while True:
        if times >= len(colors) - 1:
            times = -1
        times += 1
        yield colors[times]

def basic_config(name, type_):
    return  f" var config = {{type: '{type_}', data: data, options: {{ responsive: true, plugins: {{ legend: {{ position: 'top', }}, title: {{ display: true, text: '{name}' }} }} }}, }};"

def basic_dataset(data, color_generator):
    return f"{{label: '{data[0]}', data: {data[1:]}, backgroundColor: '{next(color_generator)}'}}"

def basic_html(name, height:list=(100, 100)):
    return f'<canvas id="{name}" width="{height[0]}" height="{height[1]}"></canvas>'

def basic_script(name, labels, dataset, config):
    return f'var labels = {labels}; var data = {{labels: labels, datasets: [{dataset}]}}; {config}; {name} = new Chart("{name}", config);'

def make_basic_chart(type, name, labels, datasets, high:list = (100, 100)):
    color_generator = return_colors()
    config = basic_config(name, type)
    dataset = list()
    for x in datasets:
        dataset.append(basic_dataset(x, color_generator))
    dataset = ', '.join(dataset)
    scripts =basic_script(name, labels, dataset, config)
    return basic_html(name, high), scripts

def generate_chart(type, name, labels, datasets, high:list = (100, 100), func_config=basic_config, func_dataset=basic_dataset, func_script=basic_script,  func_html=basic_html):
    color_generator = return_colors()
    config = func_config(name, type)
    dataset = list()
    for x in datasets:
        dataset.append(func_dataset(x, color_generator))
    dataset = ', '.join(dataset)
    scripts = func_script(name, labels, dataset, config)
    return func_html(name, high), scripts

def basic_display_info_dicit(info:dict, display):
    Return = list()
    keys = info.keys()
    for x in keys:
        Return.append(f'{info[display]} : ')
        Return.append(f'    {x} : {info[x]}')
    Return = '''
    '''.join(Return)
    return f'''<span>{Return}</span>'''