import pickle

# get the trope list from the pickle file
with open('trope_names.pkl', 'rb') as f:
    trope_names = pickle.load(f)

data_chunks = [trope_names[i:i+500] for i in range(0, len(trope_names), 500)]
print(len(data_chunks))

# save the chunks
for i in range(len(data_chunks)):
    filename = 'trope_name_chunk_' + str(i) + '.pkl'
    with open(filename, 'wb') as f:
        pickle.dump(data_chunks[i], f)

print('Chunks successfully saved')
