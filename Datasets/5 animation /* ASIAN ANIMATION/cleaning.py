from imdbpie import Imdb
import pickle
import pandas


REMOVE_BOTH = ['BigFishAndBegonia', 'BoonieBears', 'HappyRunning', 'JiangZiya',
          'Kuiba', 'TheLegendOfHei', 'LingLongIncarnation', 'LittleBigPanda',
          'LittleDoorGods', 'MonkeyKingHeroIsBack', 'MonkeyKingReborn',
          'NewGodsNezhaReborn2021', 'NextGen', 'NeZha',
          'PleasantGoatAndBigBigWolf', 'WhiteSnake2019', 'GreenSnake2021',
          'RobotTaekwonV', 'SpaceTransformers', 'TurtleHero',
          'MyBeautifulGirlMari', 'SkyBlue', 'EmpressChung', 'AachiAndSsipak',
          'YobiTheFiveTailedFox', 'TheKingOfPigs', 'LeafieAHenIntoTheWild',
          'SpecklesTheTarbosaurus', 'Padak', 'MiniforceNewHeroesRise',
          'SeoulStation', 'TheUnderdog', 'RedShoesAndTheSevenDwarfs',
          'AliBabaAndTheGoldRaiders', 'ArjunTheWarriorPrince',
          'ArmenFilmAnimatedShorts', 'BhaagamBhaag', 'CreationOfTheWorld',
          'DayoSaMundoNgElementalia', 'GajuBhai', 'Hammerboy',
          'KrishnaAurKans', 'MalekKhorshid', 'NanaMoon', 'PrincessIronFan',
          'RPGMetanoia', 'RoadsideRomeo', 'ShittyTheCat', 'SpaceThunderKids',
          'TheReturnOfHanuman', 'Urduja', 'XiaoMingAndWangMao',
          'BeautyAndWarrior', 'CrazyCandies', 'DoggyPoo',
          'DziwnePrzygodyKoziolkaMatolka', 'FruityRobo',
          'HayopKaTheNimfaDimaanoStory', 'LegendOfBlue', 'MissDaizi', 'Mutya',
          'RomanceOfTheThreeKingdoms', 'TheDailyLifeOfTheImmortalKing',
          'TheNut1967']

REMOVE_IMDB = ['ArtOdyssey', 'FlowerFairy', 'GhostMessenger', 'HappyFamily',
               'InspectorChingum', 'Kodama', 'KuangKuang', 'LusTime', 'Mojospy',
               'NanoCore', 'OyeGolu', 'PangPond', 'SweetsFairy', 'Tobot',
               'ZellyGo', 'Akis', 'AstroPlan', 'ChhotaBheem', 'EjenAli',
               'MK22', 'Miniforce', 'Oddbods', 'RunningMan']

df = pandas.read_pickle('tv_tropes_asiananimation.pkl')
df = df[~df['title'].isin(REMOVE_BOTH)]

print(list(dict.fromkeys(df['title'])))
print('fish')

df.to_pickle('tv_tropes_asiananimation_cleaned.pkl')

# remove from imdb_data_dict.pkl
with open('imdb_data_dict.pkl', 'rb') as f:
    imdb_data_dict = pickle.load(f)

data_new = {}

for key, value in imdb_data_dict.items():
    if key not in REMOVE_IMDB and key not in REMOVE_BOTH:
        data_new[key] = value

with open('imdb_data_dict_manual.pkl', 'rb') as f:
    imdb_data_dict_manual = pickle.load(f)
    data_new.update(imdb_data_dict_manual)

print(data_new.keys())

with open('imdb_data_dict_compiled.pkl', 'wb') as f:
    pickle.dump(data_new, f)

with open('title_matches.pkl', 'rb') as f:
    title_matches = pickle.load(f)

for k in REMOVE_BOTH or k in REMOVE_IMDB:
    title_matches.pop(k, None)

with open('title_matches_manual.pkl', 'rb') as f:
    title_matches_manual = pickle.load(f)
    title_matches.update(title_matches_manual)

with open('title_matches_compiled.pkl', 'wb') as f:
    pickle.dump(title_matches, f)
