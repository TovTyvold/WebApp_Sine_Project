import matplotlib.pyplot as plt


def plot_array(t_vec, y, title, xlabel, ylabel, label_graph, color_graph, ls_graph, save, filename):
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.plot(t_vec, y, label= label_graph, color =color_graph, ls=ls_graph)
    plt.legend()
    if save == True:
        plt.savefig(f"{filename}")
    return None
