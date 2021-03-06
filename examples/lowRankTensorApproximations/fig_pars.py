import matplotlib.pyplot as plt

def set_pars(mpl):
    mpl.rcParams['text.latex.preamble'] = [r"\usepackage{amsmath,bm,amsfonts}"]
    params={'text.usetex': True,
            'font.family': 'serif',
            'font.size': 12,
            'legend.fontsize': 10,
            }
    mpl.rcParams.update(params)
    fig_par={'dpi': 1000,
             'facecolor': 'w',
             'edgecolor': 'k',
             'figsize': (4, 3),
             'figsize3D': (4, 4),
             'pad_inches': 0.02,
             }

    return fig_par

def set_labels():
    lines={'Gafull': 'bo-',
           'GaNifull': '--',
           'Gacano': 'bx-',
           'Gatucker': 'ro-',
           'Gatt': 'kv-',

           'GaSparse': 'rx-',
           'GaSparse_2': 'ro-',
           'GaSparse_3': 'r<-',
           'GaSparse_4': 'r*-',
           'GaSparse_5': 'rd-',
           'GaSparse_6': 'rv-',
           'GaSparse_7': 'r^-',

           'full': '--',
           'mem_cano':   ['bx--','bo--','bx--','bv--','bo--','bx--','b<--'],
           'mem_tucker': ['rx--', 'ro--', 'rx--', 'rv--', 'ro--', 'rx--', 'r<--'],
           'mem_tt':     ['kx-', 'ko-', 'kx--', 'kv--', 'ko--', 'kx--', 'k<--'],

           'Ga_cano': ['bx-', 'bo-', 'bx-', 'bv-', 'bo-', 'bx-', 'b<-'],
           'Ga_tucker': ['rx-', 'ro-', 'rx-', 'rv-', 'ro-', 'rx-', 'r<-'],
           'Ga_tt': ['kx-', 'ko-','kx--', 'kv-', 'ko-', 'kx-', 'k<-'],

           'GaNi_cano': ['bx--', 'bo--', 'bx--', 'bv--', 'bo--', 'bx--', 'b<--'],
           'GaNi_tucker': ['rx--', 'ro--', 'rx--', 'rv--', 'ro--', 'rx--', 'r<--'],
           'GaNi_tt': ['kx--', 'ko--', 'kx--', 'kv--', 'ko--', 'kx--', 'k<--'],


           'Ga': ['-','x-','<-','|-','^-','x-','o-', '<-', 'v-','^-','d-',],
           'GaNi': ['--', 'x--', '<--', '|--', '^--', 'x--', 'o--', '<--', 'v--', '^--', 'd--'],

           }

    labels = {'full': 'Full',
              'tensorsLowRank': 'Sparse',
              'Gafull': 'Ga Full',
              'Gacano': 'Ga CP',
              'Gatucker': 'Ga Tucker',
              'Gatt': 'Ga TT',

              'Garank': 'Solution rank',
              'GaNirank': 'Solution rank',

              'GaNifull': 'GaNi Full',

              'GaNicano': 'GaNi CP',
              'GaNicanoN': 'Cano N=',

              'GaNitucker': 'GaNi Tucker',
              'GaNituckerN': 'Tucker N=',

              'GaNitt': 'GaNi TT',
              'GaNittN': 'TT N=',
              }
    return lines, labels

def copy_files(src, dest, files='all'):
    import os
    from shutil import copy
    src_files=os.listdir(src)
    for file_name in src_files:
        if files=='all' or file_name in files:
            full_file_name=os.path.join(src, file_name)
            if (os.path.isfile(full_file_name)):
                copy(full_file_name, dest)
        else:
            continue
    print('copy of files is finished')
    return
print((plt.style.available))
