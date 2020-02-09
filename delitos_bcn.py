import matplotlib.pyplot as plt
import pandas as pd
from absl import app
from absl import flags
import pickle

FLAGS = flags.FLAGS
flags.DEFINE_string('action', 'create_data', 'One of {`create_data`, `plot`, `find_worst`}.')
flags.DEFINE_string('code', '-1', 'Codi to create figure with.')
flags.DEFINE_string('output', None, 'Path to the save the output.')

_YEARS = [2010, 2012, 2013, 2014, 2015, 2016, 2017, 2018]

def _create_data():
  """Saves a data in pickle format.

  The data is a `List`, one per year. Each year has a `Dict` of the code and
  the total number of cases seen in that year.
  """

  data = []
  codes = {}
  for year in _YEARS:
    print(year)
    filename = '{}_incidents_gestionats_gub.csv'.format(year)
    one_year = pd.read_csv(filename)
    data_year = {}
    for _, entry in one_year.iterrows():
      if 'Codi Incident' in entry:
        code = entry['Codi Incident']
        if code not in codes:
          codes[code] = entry['Descripció Incident']
      elif 'Codi_Incident' in entry:
        code = entry['Codi_Incident']
        if code not in codes:
          codes[code] = entry['Descripcio_Incident']
      if code in data_year:
        data_year[code] += 1
      else:
        data_year[code] = 0
    data.append(data_year)
  with open('data.pkl', 'wb') as f:
    pickle.dump(data, f)
  with open('codes.pkl', 'wb') as f:
    pickle.dump(codes, f)


def _plot():
  with open('data.pkl', 'rb') as f:
    data = pickle.load(f)
  with open('codes.pkl', 'rb') as f:
    codes = pickle.load(f)

  colors = ['r', 'b', 'd', 'g', 'c']
  legend = []
  for i, code in enumerate(FLAGS.code.split(',')):
    items = []
    for entry in data:
      items.append(entry[code])
    plt.plot(_YEARS, items, '{}o-'.format(colors[i]))
    legend.append(codes[code].strip().replace(',', '.'))

  plt.xlabel('Any')
  plt.ylabel('Número de casos')
  if ',' not in FLAGS.code:
    plt.title(codes[code].strip().replace(',', '.'))
  else:
    plt.legend(legend)
  plt.grid()
  plt.savefig('code_{}.png'.format(FLAGS.code.replace(',', '_')), dpi=600)


def _find_worst():
  """Finds the one code that has the largest increase since 2010."""

  with open('data.pkl', 'rb') as f:
    data = pickle.load(f)
  with open('codes.pkl', 'rb') as f:
    codes = pickle.load(f)

  out = {}
  data_2010 = data[0]
  data_last_year = data[-1]
  for code, count in data_2010.items():
    if not code in data_last_year:
      continue
    out[code] = data_last_year[code] - count

  with open(FLAGS.output, 'wt') as f:
    f.write('code,description,count\n')
    for key, count in out.items():
      f.write('{},{},{}\n'.format(key, codes[key].strip().replace(',', '.'),
                                  count))


def main(argv):
  if FLAGS.action == 'create_data':
    _create_data()
  elif FLAGS.action == 'plot':
    _plot()
  elif FLAGS.action == 'find_worst':
    _find_worst()


if __name__ == '__main__':
  app.run(main)
