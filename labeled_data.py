from queryspec import Intent

def get_training_data():
    with open('query.txt', 'r') as querys:
        output = {}

        for line in querys:
            line_split = line.rstrip().split('|')
            if line_split[0] == 'B4':
                output[line_split[1]] = Intent[line_split[3]]
    return output
