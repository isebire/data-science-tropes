import pickle

# get the trope list from the pickle file
with open('games_names.pkl', 'rb') as f:
    games_names = pickle.load(f)

data_chunks = [games_names[i:i+500] for i in range(0, len(games_names), 500)]
print(len(data_chunks))

# save the chunks
for i in range(len(data_chunks)):
    filename = 'game_name_chunk_' + str(i) + '.pkl'
    with open(filename, 'wb') as f:
        pickle.dump(data_chunks[i], f)

print('Chunks successfully saved')
