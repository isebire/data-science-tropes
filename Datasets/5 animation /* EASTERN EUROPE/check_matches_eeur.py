import pickle


with open('manual_checks_easterneur.pkl', 'rb') as f:
    manual = pickle.load(f)

for item in manual.items():
    input(item)
