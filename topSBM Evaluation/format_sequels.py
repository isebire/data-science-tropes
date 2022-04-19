# Format sequels
import pickle

with open('vg_sequels.txt', 'r') as f:
    lines = f.readlines()

sequels_list = []
new_series = True

for line in lines:

    line = line.strip()

    if line != '':
        if new_series is True:
            sequels_list.append([line])
            new_series = False
        else:
            sequels_list[-1].append(line)

    else:
        new_series = True

with open('vg_sequels_list.pkl', 'wb') as f:
    pickle.dump(sequels_list, f)
