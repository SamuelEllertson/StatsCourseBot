from queryspec import Intent
import random as r
r.seed(16)
from operator import itemgetter

def get_training_data(test):
    with open('query.txt', 'r') as querys:
        output = {}

        for line in querys:
            line_split = line.rstrip().split('|')
            if line_split[0] == 'B4':
                output[line_split[1]] = Intent[line_split[3]]

    new_output = {}
    n = len(output) // 6            
    outputkeys = output.keys()
    sampled_keys = r.sample(outputkeys, n)
    if test:
        for key in sampled_keys:
            new_output[key] = output[key]
        return new_output
    else:
        for key in outputkeys:
            if key not in sampled_keys:
                new_output[key] = output[key]
        return new_output
        
    # for key in sampled_keys:
    #     new_output[key] = output[key]	

    
