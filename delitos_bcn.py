import matplotlib.pyplot as plt
import pandas as pd
from absl import app
from absl import flags
import pickle

FLAGS = flags.FLAGS
flags.DEFINE_bool('create_data', True, 'True to create data.')
flags.DEFINE_string('codi', '-1', 'Codi to create figure with.')

_YEARS = [2010, 2012, 2013, 2014, 2015, 2016, 2017, 2018]

def _create_data():
  data = []
  for year in _YEARS:
    print(year)
    filename = '{}_incidents_gestionats_gub.csv'.format(year)
    one_year = pd.read_csv(filename)
    data_year = {}
    for _, entry in one_year.iterrows():
      if 'Codi Incident' in entry:
        codi = entry['Codi Incident']
      elif 'Codi_Incident' in entry:
        codi = entry['Codi_Incident']
      if codi in data_year:
        data_year[codi] += 1
      else:
        data_year[codi] = 0
    data.append(data_year)
  with open('data.pkl', 'wb') as f:
    pickle.dump(data, f)


def _plot():
  with open('data.pkl', 'rb') as f:
    data = pickle.load(f)

  items = []
  for entry in data:
    items.append(entry[FLAGS.codi])

  plt.plot(_YEARS, items, 'o-')
  plt.grid()
  plt.savefig('codi_{}.png'.format(FLAGS.codi))


def main(argv):
  if FLAGS.create_data:
    _create_data()
  else:
    _plot()


if __name__ == '__main__':
  app.run(main)
