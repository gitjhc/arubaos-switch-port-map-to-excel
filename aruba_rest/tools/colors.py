def get_color(index):
    colors = [
        '#F4CCCC', '#CFE2F3', '#FCE5CD', '#D9D2E9',
        '#B6D7A8', '#A4C2F4', '#FFD966', '#EA9999', '#A2C4C9',
        '#B4A7D6', '#FFF2CC', '#EAD1DC', '#D0E0E3', '#F9CB9C',
        '#C9DAF8', '#FDE9D9', '#D9D2E9', '#B7B7B7', '#A2C4C9', '#B4A7D6', '#FFF2CC', '#EAD1DC', '#D0E0E3',
        '#F9CB9C', '#C9DAF8',
    ]
    return colors[index % len(colors)]
