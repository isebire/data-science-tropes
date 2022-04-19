import pickle

for i in range(12):

    filename = 'manual_checks_' + str(i) + '.pkl'
    print('Reading ' + filename)
    with open(filename, 'rb') as f:
      manual_dict = pickle.load(f)

    remove_from_dataset = []
    replacements = {}

    for item in manual_dict.items():
        print(item)
        # ask if right or not, remove if not
        right = input('Is it right? (y/n):')
        if right == 'n':
            remove_from_dataset.append(item[0])
            replacement = input('Enter replacement or empty: ').strip()
            # imdb id
            if replacement != '':
                replacements[item[0]] = replacement

    filename = 'remove_' + str(i) + '.pkl'
    with open(filename, 'wb') as f:
        pickle.dump(remove_from_dataset, f)

    filename = 'replacements_' + str(i) + '.pkl'
    with open(filename, 'wb') as f:
        pickle.dump(replacements, f)
