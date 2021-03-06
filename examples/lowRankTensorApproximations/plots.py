import pickle
import matplotlib as mpl
import matplotlib.pyplot as plt

import os
from examples.lowRankTensorApproximations.fig_pars import set_labels, set_pars

os.nice(19)

def save_experiment_settings(kind_list, Ns, kinds, sol_rank_range_set, material_list,
                             data_folder='data_for_plot'):
    if not os.path.exists('{}'.format(data_folder)):
        os.makedirs('{}/'.format(data_folder))

    for dim in [2, 3]:
        for material in material_list:
            if not os.path.exists('{}/dim_{}/mat_{}/'.format(data_folder, dim, material)):
                os.makedirs('{}/dim_{}/mat_{}/'.format(data_folder, dim, material))

    pickle.dump(kind_list, open("{}/kind_list.p".format(data_folder), "wb"))
    pickle.dump(Ns, open("{}/Ns.p".format(data_folder), "wb"))
    pickle.dump(kinds, open("{}/kinds.p".format(data_folder), "wb"))
    pickle.dump(sol_rank_range_set, open("{}/sol_rank_range_set.p".format(data_folder), "wb"))
    pickle.dump(material_list, open("{}/material_list.p".format(data_folder), "wb"))

    return


def load_experiment_settings(data_folder='data_for_plot'):
    material_list = pickle.load(open("{}/material_list.p".format(data_folder), "rb"))
    sol_rank_range_set = pickle.load(open("{}/sol_rank_range_set.p".format(data_folder), "rb"))
    kinds = pickle.load(open("{}/kinds.p".format(data_folder), "rb"))
    Ns = pickle.load(open("{}/Ns.p".format(data_folder), "rb"))
    kind_list = pickle.load(open("{}/kind_list.p".format(data_folder), "rb"))
    solver = 'mr'

    return material_list, sol_rank_range_set, kinds, Ns, kind_list, solver


def plot_error():
    data_folder = "data_for_plot/error"
    material_list, sol_rank_range_set, kinds, Ns, kind_list, solver = load_experiment_settings(
        data_folder=data_folder)
    ylimit = [10**-11, 10**0]
    xlabel = 'rank of solution'
    ylabel = 'relative error'

    for dim in [2]:
        N = max(Ns['{}'.format(dim)])
        xlimend = max(sol_rank_range_set['{}'.format(dim)])
        if not os.path.exists('figures'):
            os.makedirs('figures')

        ##### BEGIN: figure 1 resiguum(solution rank) ###########
        for material in material_list:
            parf = set_pars(mpl)
            lines, labels = set_labels()
            src = 'figures/'  # source folder\
            plt.figure(num=None, figsize=parf['figsize'], dpi=parf['dpi'])
            plt.ylabel('relative error')
            plt.xlabel('rank of solution')

            sol_rank_range = sol_rank_range_set['{}'.format(dim)]
            i = 0
            for kind in kinds['{}'.format(dim)]:
                sols_Ga = pickle.load(open("{}/dim_{}/mat_{}/sols_Ga_{}.p".format(data_folder, dim, material, N), "rb"))
                sols_GaNi = pickle.load(
                    open("{}/dim_{}/mat_{}/sols_GaNi_{}.p".format(data_folder, dim, material, N), "rb"))
                sols_Ga_Spar = pickle.load(
                    open("{}/dim_{}/mat_{}/sols_Ga_Spar_{}_{}_{}.p".format(data_folder, dim, material, kind, N, solver),
                         "rb"))
                sols_GaNi_Spar = pickle.load(
                    open("{}/dim_{}/mat_{}/sols_GaNi_Spar_{}_{}_{}.p".format(data_folder, dim, material, kind, N,
                                                                             solver),
                         "rb"))

                plt.semilogy(sol_rank_range,
                             [abs((sols_Ga_Spar[i]-sols_Ga[1])/sols_Ga[1]) for i in range(len(sols_Ga_Spar))],
                             lines['Ga_{}'.format(kind_list[kind])][i], label=labels['Ga{}'.format(kind_list[kind])],
                             markevery=1)
                plt.semilogy(sol_rank_range,
                             [abs((sols_GaNi_Spar[i]-sols_GaNi[1])/sols_GaNi[1]) for i in range(len(sols_GaNi_Spar))],
                             lines['GaNi_{}'.format(kind_list[kind])][i],
                             label=labels['GaNi{}'.format(kind_list[kind])], markevery=1, markersize=7,
                             markeredgewidth=1, markerfacecolor='None')
                i = i + 1

            ax = plt.gca()
            plt.xlabel(xlabel)
            ax.set_xlim([0, xlimend])
            ax.set_ylim(ylimit)

            plt.xticks(sol_rank_range)

            plt.ylabel(ylabel)

            plt.legend(loc='best')
            fname = src + 'Error_dim{}_mat{}_{}_N{}{}'.format(dim, material, solver, N, '.pdf')
            print(('create figure: {}'.format(fname)))
            plt.savefig(fname, dpi=parf['dpi'], pad_inches=parf['pad_inches'], bbox_inches='tight')
        print('END plot errors 2D')
        ##### END: figure 1 resiguum(solution rank) ###########

    for dim in [3]:
        N = max(Ns['{}'.format(dim)])
        xlimend = max(sol_rank_range_set['{}'.format(dim)])
        if not os.path.exists('figures'):
            os.makedirs('figures')

        ##### BEGIN: figure 1 resiguum(solution rank) ###########
        for material in material_list:
            parf = set_pars(mpl)
            lines, labels = set_labels()
            src = 'figures/'  # source folder\
            plt.figure(num=None, figsize=parf['figsize'], dpi=parf['dpi'])

            sol_rank_range = sol_rank_range_set['{}'.format(dim)]
            i = 0
            for kind in kinds['{}'.format(dim)]:
                sols_Ga = pickle.load(
                    open("data_for_plot/error/dim_{}/mat_{}/sols_Ga_{}.p".format(dim, material, N), "rb"))
                sols_GaNi = pickle.load(
                    open("{}/dim_{}/mat_{}/sols_GaNi_{}.p".format(data_folder, dim, material, N), "rb"))
                sols_Ga_Spar = pickle.load(
                    open("{}/dim_{}/mat_{}/sols_Ga_Spar_{}_{}_{}.p".format(data_folder, dim, material, kind, N, solver),
                         "rb"))
                sols_GaNi_Spar = pickle.load(
                    open("{}/dim_{}/mat_{}/sols_GaNi_Spar_{}_{}_{}.p".format(data_folder, dim, material, kind, N,
                                                                             solver),
                         "rb"))

                plt.semilogy(sol_rank_range,
                             [abs((sols_Ga_Spar[i]-sols_Ga[1])/sols_Ga[1]) for i in range(len(sols_Ga_Spar))],
                             lines['Ga_{}'.format(kind_list[kind])][i], label=labels['Ga{}'.format(kind_list[kind])],
                             markevery=1)
                plt.semilogy(sol_rank_range,
                             [abs((sols_GaNi_Spar[i]-sols_GaNi[1])/sols_GaNi[1]) for i in range(len(sols_Ga_Spar))],
                             lines['GaNi_{}'.format(kind_list[kind])][i],
                             label=labels['GaNi{}'.format(kind_list[kind])], markevery=1, markersize=7,
                             markeredgewidth=1, markerfacecolor='None')

            ax = plt.gca()
            plt.xlabel(xlabel)
            ax.set_xlim([0, xlimend])
            plt.xticks(sol_rank_range)
            ax.set_ylim(ylimit)
            plt.ylabel(ylabel)

            plt.legend(loc='best')
            fname=src+'Error_dim{}_mat{}_{}_N{}{}'.format(dim, material, solver, N, '.pdf')
            print(('create figure: {}'.format(fname)))
            plt.savefig(fname, dpi=parf['dpi'], pad_inches=parf['pad_inches'], bbox_inches='tight')
        print('END plot errors 3D')
        ##### END: figure 1 resiguum(solution rank) ###########


def plot_memory():
    material_list, sol_rank_range_set, kinds, Ns, kind_list, solver = load_experiment_settings()
    xlabel = 'rank of solution'
    ylabel = 'memory efficiency'
    if not os.path.exists('figures'):
        os.makedirs('figures')
    for dim in [2]:
        sol_rank_range = sol_rank_range_set['{}'.format(dim)]
        N = max(Ns['{}'.format(dim)])
        xlimend = max(sol_rank_range_set['{}'.format(dim)])
        ##### BEGIN: figure 2 Memory efficiency ###########
        for material in material_list:

            parf = set_pars(mpl)
            lines, labels = set_labels()
            src = 'figures/'  # source folder\
            plt.figure(num=None, figsize=parf['figsize'], dpi=parf['dpi'])

            mem_GaNi = pickle.load(open("data_for_plot/dim_{}/mat_{}/mem_GaNi_{}.p".format(dim, material, N, ), "rb"))

            plt.semilogy(sol_rank_range, mem_GaNi, lines['full'],
                         label=labels['GaNi{}'.format(('full'))], markevery=1, markersize=7,
                         markeredgewidth=1, markerfacecolor='None')

            for N in Ns['{}'.format(dim)]:
                i = 0
                for kind in kinds['{}'.format(dim)]:
                    mem_GaNi_Spar = pickle.load(open(
                        "data_for_plot/dim_{}/mat_{}/mem_GaNi_Spar_{}_{}_{}.p".format(dim, material, kind, N, solver),
                        "rb"))
                    plt.semilogy(sol_rank_range, mem_GaNi_Spar, lines['mem_{}'.format(kind_list[kind])][i],
                                 label='{}{}'.format(labels['GaNi{}N'.format(kind_list[kind])], N),
                                 markevery=1, markersize=7, markeredgewidth=1,
                                 markerfacecolor='None')
                    i = i + 1

            ax = plt.gca()
            plt.xticks(sol_rank_range)
            plt.xlabel(xlabel)
            ax.set_xlim([0, xlimend])

            plt.ylabel(ylabel)

            plt.legend(loc='best')
            fname=src+'Memory_dim{}_mat{}{}'.format(dim, material, '.pdf')
            print(('create figure: {}'.format(fname)))
            plt.savefig(fname, dpi=parf['dpi'], pad_inches=parf['pad_inches'], bbox_inches='tight')
        print('END plot memory')
        ##### END: figure 2 memory ###########

    for dim in [3]:
        sol_rank_range = sol_rank_range_set['{}'.format(dim)]
        N = max(Ns['{}'.format(dim)])
        xlimend = max(sol_rank_range_set['{}'.format(dim)])
        ##### BEGIN: figure 2 Memory efficiency ###########
        for material in material_list:

            plt.figure(num=None, figsize=parf['figsize'], dpi=parf['dpi'])

            mem_GaNi=pickle.load(open("data_for_plot/dim_{}/mat_{}/mem_GaNi_{}.p".format(dim, material, N), "rb"))

            plt.semilogy(sol_rank_range, mem_GaNi, lines['full'],
                         label=labels['GaNi{}'.format(('full'))],
                         markevery=1, markersize=7, markeredgewidth=1, markerfacecolor='None')

            for kind in kinds['{}'.format(dim)]:
                i = 0
                for N in [max(Ns['{}'.format(dim)]), min(Ns['{}'.format(dim)])]:
                    mem_GaNi_Spar = pickle.load(open(
                        "data_for_plot/dim_{}/mat_{}/mem_GaNi_Spar_{}_{}_{}.p".format(dim, material, kind, N, solver),
                        "rb"))
                    plt.semilogy(sol_rank_range, mem_GaNi_Spar, lines['mem_{}'.format(kind_list[kind])][i],
                                 label='{}{}'.format(labels['GaNi{}N'.format(kind_list[kind])], N),
                                 markevery=1, markersize=7, markeredgewidth=1,
                                 markerfacecolor='None')
                    i = i + 1

            ax = plt.gca()
            plt.xticks(sol_rank_range)
            plt.xlabel(xlabel)
            ax.set_xlim([0, xlimend])

            plt.ylabel(ylabel)

            plt.legend(loc='best')
            fname = src + 'Memory_dim{}_mat{}{}'.format(dim, material, '.pdf')
            print(('create figure: {}'.format(fname)))
            plt.savefig(fname, dpi=parf['dpi'], pad_inches=parf['pad_inches'], bbox_inches='tight')
        print('END plot memory')
        ##### END: figure 2 memory ###########


def plot_residuals():
    data_folder = "data_for_plot/residua"
    material_list, sol_rank_range_set, kinds, Ns, kind_list, solver=load_experiment_settings(
        data_folder=data_folder)

    xlabel = 'iteration'
    ylabel = 'norm of residuum'
    iter_rank_range_set = [1, 5, 10, 15, 20, 30, 40, 50]
    if not os.path.exists('figures'):
        os.makedirs('figures')

    for dim in [2]:
        xlimit = [0, 30]
        ylimit = [10**-7, 10**-1]
        for N in Ns['{}'.format(dim)]:

            ##### BEGIN: figure 5.1 Residuum for GA solution ###########
            for material in material_list:
                for kind in kinds['{}'.format(dim)]:
                    # plt.figure(1).clear()
                    parf = set_pars(mpl)
                    lines, labels = set_labels()
                    src = 'figures/'  # source folder\
                    sol_rank_range = sol_rank_range_set['{}'.format(dim)]
                    plt.figure(num=None, figsize=parf['figsize'], dpi=parf['dpi'])

                    res_Ga_Spar = pickle.load(open(
                        "{}/dim_{}/mat_{}/res_Ga_Spar_{}_{}_{}.p".format(data_folder, dim, material, kind, N, solver),
                        "rb"))

                    for sol_rank in range(0, len(sol_rank_range)):
                        plt.semilogy(list(range(len(res_Ga_Spar[sol_rank]))), res_Ga_Spar[sol_rank],
                                     lines['Ga'][sol_rank],
                                     label='{} {}'.format(labels['Garank'], sol_rank_range[sol_rank]),
                                     markevery=2)

                    ax = plt.gca()
                    plt.xticks(iter_rank_range_set)
                    plt.xlabel(xlabel)
                    ax.set_xlim(xlimit)
                    plt.ylabel(ylabel)
                    ax.set_ylim(ylimit)

                    plt.legend(loc='upper right')
                    fname = src + 'Residuum_dim{}_mat{}_kind_{}_Ga_{}_N{}{}'.format(dim, material, kind_list[kind],
                                                                                    solver, N, '.pdf')
                    print(('create figure: {}'.format(fname)))
                    plt.savefig(fname, dpi=parf['dpi'], pad_inches=parf['pad_inches'], bbox_inches='tight')
            print('END Ga 2D residuum N={}'.format(N))
            ##### END: figure 5.1 Residuum for Ga solution ###########

            ##### BEGIN: figure 5.2 Residuum for GaNi solution ###########
            for material in material_list:
                for kind in kinds['{}'.format(dim)]:

                    parf = set_pars(mpl)
                    lines, labels = set_labels()
                    src = 'figures/'  # source folder\
                    sol_rank_range = sol_rank_range_set['{}'.format(dim)]

                    plt.figure(num=None, figsize=parf['figsize'], dpi=parf['dpi'])

                    res_GaNi_Spar = pickle.load(
                        open("{}/dim_{}/mat_{}/res_GaNi_Spar_{}_{}_{}.p".format(data_folder, dim, material, kind, N,
                                                                                solver), "rb"))
                    plt.xticks(iter_rank_range_set)
                    for sol_rank in range(0, len(sol_rank_range)):
                        plt.semilogy(list(range(len(res_GaNi_Spar[sol_rank]))), res_GaNi_Spar[sol_rank],
                                     lines['GaNi'][sol_rank],
                                     label='{} {}'.format(labels['GaNirank'], sol_rank_range[sol_rank]),
                                     markevery=2, markersize=7,
                                     markeredgewidth=1, markerfacecolor='None')

                    ax = plt.gca()
                    plt.xticks(iter_rank_range_set)
                    plt.xlabel(xlabel)
                    ax.set_xlim(xlimit)

                    plt.ylabel(ylabel)
                    ax.set_ylim(ylimit)

                    plt.legend(loc='upper right')

                    fname = src + 'Residuum_dim{}_mat{}_kind_{}_GaNi_{}_N{}{}'.format(dim, material, kind_list[kind],
                                                                                      solver, N, '.pdf')
                    print(('create figure: {}'.format(fname)))
                    plt.savefig(fname, dpi=parf['dpi'], pad_inches=parf['pad_inches'],
                                bbox_inches='tight')
            print('END GaNi 2D residuum N={}'.format(N))
            ##### END: figure 5.2 Residuum for GaNi solution ###########

    for dim in [3]:
        xlimit = [0, 30]
        ylimit = [10**-7, 10**-1]
        for N in Ns['{}'.format(dim)]:
            ##### 0 material  ###########
            for material in material_list:
                for kind in kinds['{}'.format(dim)]:
                    parf = set_pars(mpl)
                    lines, labels = set_labels()
                    src = 'figures/'  # source folder\
                    sol_rank_range = sol_rank_range_set['{}'.format(dim)]

                    plt.figure(num=None, figsize=parf['figsize'], dpi=parf['dpi'])
                    res_Ga_Spar = pickle.load(
                        open(
                            "{}/dim_{}/mat_{}/res_Ga_Spar_{}_{}_{}.p".format(data_folder, dim, material, kind, N,
                                                                             solver),
                            "rb"))

                    for sol_rank in range(0, len(
                            sol_rank_range)):
                        plt.semilogy(list(range(len(res_Ga_Spar[sol_rank]))), res_Ga_Spar[sol_rank],
                                     lines['Ga'][sol_rank],
                                     label='{} {}'.format(labels['Garank'], sol_rank_range[sol_rank]),
                                     markevery=2)

                    ax = plt.gca()
                    plt.xticks(iter_rank_range_set)
                    plt.xlabel(xlabel)
                    ax.set_xlim(xlimit)

                    plt.ylabel(ylabel)
                    ax.set_ylim(ylimit)

                    plt.legend(loc='best')
                    fname = src + 'Residuum_dim{}_mat{}_kind_{}_Ga_{}_N{}{}'.format(dim, material, kind_list[kind],
                                                                                    solver, N, '.pdf')
                    print(('create figure: {}'.format(fname)))
                    plt.savefig(fname, dpi=parf['dpi'], pad_inches=parf['pad_inches'],
                                bbox_inches='tight')
            print('END Ga 3D residuum N={} mat {}'.format(N, material))
            ##### END: figure 5.1 Residuum for Ga solution ###########

            ##### BEGIN: figure 5.2 Residuum for GaNi solution ###########
            for material in material_list:
                for kind in kinds['{}'.format(dim)]:

                    parf = set_pars(mpl)
                    lines, labels = set_labels()
                    src = 'figures/'  # source folder\
                    sol_rank_range = sol_rank_range_set['{}'.format(dim)]

                    plt.figure(num=None, figsize=parf['figsize'], dpi=parf['dpi'])
                    #        plt.hold(True)

                    res_GaNi_Spar = pickle.load(
                        open("{}/dim_{}/mat_{}/res_GaNi_Spar_{}_{}_{}.p".format(data_folder, dim, material, kind, N,
                                                                                solver),
                             "rb"))

                    for sol_rank in range(0, len(sol_rank_range)):  # range(len(sol_rank_range)):
                        plt.semilogy(list(range(len(res_GaNi_Spar[sol_rank]))), res_GaNi_Spar[sol_rank],
                                     lines['GaNi'][sol_rank],
                                     label='{} {}'.format(labels['GaNirank'], sol_rank_range[sol_rank]),
                                     markevery=2, markersize=7,
                                     markeredgewidth=1, markerfacecolor='None')
                    ax = plt.gca()
                    plt.xticks(iter_rank_range_set)
                    plt.xlabel(xlabel)
                    ax.set_xlim(xlimit)

                    plt.ylabel(ylabel)
                    ax.set_ylim(ylimit)

                    lg=plt.legend(loc='upper right')
                    fname=src+'Residuum_dim{}_mat{}_kind_{}_GaNi_{}_N{}{}'.format(dim, material, kind_list[kind],
                                                                                      solver, N, '.pdf')
                    print(('create figure: {}'.format(fname)))
                    plt.savefig(fname, dpi=parf['dpi'], pad_inches=parf['pad_inches'], bbox_inches='tight')
            print('END GaNi 3D residuum N={} mat {}'.format(N, material))
            ##### END: figure 5.2 Residuum for GaNi solution ###########


def plot_time():
    data_folder = "data_for_plot/time"

    kind_list = ['cano', 'tucker', 'tt']
    kinds = {'2': 0,
             '3': 2, }

    for material in [0, 3]:
        for dim in [2, 3]:
            kind = kinds['{}'.format(dim)]
            xlabel = 'number of points - $ N $'
            ylabel = 'time cost [s]'
            if not os.path.exists('figures'):
                os.makedirs('figures')

            parf = set_pars(mpl)
            lines, labels=set_labels()
            src='figures/'

            plt.figure(num=None, figsize=parf['figsize'], dpi=parf['dpi'])

            N_list = pickle.load(
                open("{}/dim_{}/mat_{}/N_list_{}.p".format(data_folder, dim, material,
                                                           kind_list[kind]), "rb"))
            full_time_list = pickle.load(
                open("{}/dim_{}/mat_{}/full_time_list_{}.p".format(data_folder, dim, material,
                                                                   kind_list[kind]), "rb"))
            sparse_time_list = pickle.load(
                open("{}/dim_{}/mat_{}/sparse_time_list_{}.p".format(data_folder, dim, material,
                                                                     kind_list[kind]),
                     "rb"))

            plt.plot(N_list, full_time_list, lines['Gafull'], label='full', markevery=1,
                     markerfacecolor='None')
            plt.plot(N_list, sparse_time_list, lines['GaSparse'], label='low-rank', markevery=1)

            ax = plt.gca()
            plt.xlabel(xlabel)
            plt.ylabel(ylabel)
            xlimit = [0, N_list[-1] + N_list[-1]/20]
            ylimit = [0 - full_time_list[-1]*0.05, full_time_list[-1]*1.05]
            ax.set_xlim(xlimit)
            ax.set_ylim(ylimit)

            plt.legend(loc='upper left')
            fname=src+'time_efficiency_dim{}_mat{}_{}{}'.format(dim, material, kind_list[kind], '.pdf')
            print(('create figure: {}'.format(fname)))
            plt.savefig(fname, dpi=parf['dpi'], pad_inches=parf['pad_inches'], bbox_inches='tight')
            print('END Ga time efficiency')

    for material in [2, 4]:
        kind_list = ['cano', 'tucker', 'tt']
        kinds = {'2': 0,
                 '3': 2, }
        for dim in [2, 3]:
            kind = kinds['{}'.format(dim)]
            xlabel = 'number of points - $ N $'
            ylabel = 'time cost [s]'
            if not os.path.exists('figures'):
                os.makedirs('figures')

            parf = set_pars(mpl)
            lines, labels = set_labels()
            src = 'figures/'

            plt.figure(num=None, figsize=parf['figsize'], dpi=parf['dpi'])

            N_list = pickle.load(
                open("{}/dim_{}/mat_{}/N_list_{}.p".format(data_folder, dim, material, kind_list[kind]), "rb"))
            full_time_list = pickle.load(
                open("{}/dim_{}/mat_{}/full_time_list_{}.p".format(data_folder, dim, material, kind_list[kind]), "rb"))
            sparse_time_list_1 = pickle.load(
                open("{}/dim_{}/mat_{}/sparse_time_list_{}_1e-03.p".format(data_folder, dim, material, kind_list[kind]),
                     "rb"))

            sparse_time_list_4 = pickle.load(
                open("{}/dim_{}/mat_{}/sparse_time_list_{}_1e-06.p".format(data_folder, dim, material, kind_list[kind]),
                     "rb"))

            plt.plot(N_list, full_time_list, lines['Gafull'], label='full', markevery=1, markerfacecolor='None')
            plt.plot(N_list, sparse_time_list_1, lines['GaSparse'], label='low-rank, err $<$ 1e-3', markevery=1)
            plt.plot(N_list, sparse_time_list_4, lines['GaSparse_4'], label='low-rank, err $<$ 1e-6', markevery=1)

            ax = plt.gca()
            plt.xlabel(xlabel)
            plt.ylabel(ylabel)
            xlimit = [0, N_list[-1] + N_list[-1]/20]
            ylimit = [0 - full_time_list[-1]*0.05, full_time_list[-1]*1.05]
            ax.set_xlim(xlimit)
            ax.set_ylim(ylimit)

            lg=plt.legend(loc='upper left')
            fname=src+'time_efficiency_dim{}_mat{}_{}{}'.format(dim, material, kind_list[kind], '.pdf')
            print(('create figure: {}'.format(fname)))
            plt.savefig(fname, dpi=parf['dpi'], pad_inches=parf['pad_inches'], bbox_inches='tight')
            print('END Ga time efficiency')


def display_data():
    kind_list = ['cano', 'tucker', 'tt']
    kinds = {'2': 0,
             '3': 2, }

    for material in [0, 3]:
        for dim in [2, 3]:
            kind = kinds['{}'.format(dim)]

            N_list = pickle.load(
                open("data_for_plot/time/dim_{}/mat_{}/N_list_{}.p".format(dim, material, kind_list[kind]), "rb"))
            rank_list = pickle.load(
                open("data_for_plot/time/dim_{}/mat_{}/rank_list_{}.p".format(dim, material, kind_list[kind]), "rb"))
            full_time_list = pickle.load(
                open("data_for_plot/time/dim_{}/mat_{}/full_time_list_{}.p".format(dim, material, kind_list[kind]), "rb"))
            sparse_time_list = pickle.load(
                open("data_for_plot/time/dim_{}/mat_{}/sparse_time_list_{}.p".format(dim, material, kind_list[kind]), "rb"))

            print("dim={}, material={}, kind={} ".format(dim, material, kind_list[kind]))
            print("N list {} ".format(N_list))
            print("rank list {} ".format(rank_list))
            print("tensorsLowRank time list {} ".format(sparse_time_list))
            print("full time list {} ".format(full_time_list))
            print()

    for material in [2, 4]:
        for dim in [2, 3]:
            kind = kinds['{}'.format(dim)]

            N_list = pickle.load(
                open("data_for_plot/time/dim_{}/mat_{}/N_list_{}.p".format(dim, material, kind_list[kind]), "rb"))
            rank_list_1 = pickle.load(
                open("data_for_plot/time/dim_{}/mat_{}/rank_list_{}_1e-03.p".format(dim, material, kind_list[kind]), "rb"))

            print("dim={}, material={}, kind={}, err_tol=1e-03 ".format(dim, material, kind_list[kind]))
            print("N list {} ".format(N_list))
            print("rank list {} ".format(rank_list_1))
            print()

            rank_list_2 = pickle.load(
                open("data_for_plot/time/dim_{}/mat_{}/rank_list_{}_1e-06.p".format(dim, material, kind_list[kind]), "rb"))

            print("dim={}, material={}, kind={}, err_tol=1e-06 ".format(dim, material, kind_list[kind]))
            print("N list {} ".format(N_list))
            print("rank list {} ".format(rank_list_2))
            print()

    for material in [0,3, 2, 4]:
        for dim in [2, 3]:
            kind = kinds['{}'.format(dim)]

            N_list = pickle.load(
                open("data_for_plot/time/dim_{}/mat_{}/N_list_{}.p".format(dim, material, kind_list[kind]), "rb"))
            rank_list = pickle.load(
                open("data_for_plot/time/dim_{}/mat_{}/full_solution_rank_list_{}.p".format(dim, material, kind_list[kind]), "rb"))

            print("dim={}, material={}, kind={} ".format(dim, material, kind_list[kind]))
            print("N list {} ".format(N_list))
            print("full solution rank list {} ".format(rank_list))

            print()
if __name__ == '__main__':
#     data used in plot_time have to be genereted first by experiment_time_efficiency.py
#     plot_time()

#     data used in plot_error, plot_memory() and plot_residuals() have to be genereted first by diffusion_comparison.py
#     plot_error()
#     plot_memory()
#     plot_residuals()
    display_data()
