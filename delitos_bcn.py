import matplotlib.pyplot as plt
import pandas as pd
from absl import app
from absl import flags
import pickle

FLAGS = flags.FLAGS
flags.DEFINE_string('action', 'create_data', 'One of {`create_data`, `plot`}.')
flags.DEFINE_string('codi', '-1', 'Codi to create figure with.')
flags.DEFINE_string('output', None, 'Path to the save the output.')

_YEARS = [2010, 2012, 2013, 2014, 2015, 2016, 2017, 2018]

def _create_data():
  """Saves a data in pickle format.

  The data is a `List`, one per year. Each year has a `Dict` of the code and
  the total number of cases seen in that year.
  """

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
  plt.xlabel('Any')
  plt.ylabel('Número de casos')
  plt.grid()
  plt.savefig('codi_{}.png'.format(FLAGS.codi), dpi=600)


def _find_worst():
  """Finds the one code that has the largest increase since 2010."""

  with open('data.pkl', 'rb') as f:
    data = pickle.load(f)

  out = {}
  data_2010 = data[0]
  data_last_year = data[-1]
  for code, count in data_2010.items():
    if not code in data_last_year:
      continue
    out[code] = data_last_year[code] - count

  with open(FLAGS.output, 'wt') as f:
    f.write('code,count\n')
    for key, count in out.items():
      f.write('{},{}\n'.format(key, count))


def main(argv):
  if FLAGS.action == 'create_data':
    _create_data()
  elif FLAGS.action == 'plot':
    _plot()
  elif FLAGS.action == 'find_worst':
    _find_worst()


if __name__ == '__main__':
  app.run(main)
