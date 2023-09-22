from model.plot_utils import *
from model.allocations import solve


def allocation_chart(x, solutions, ax=None, xlabel="", legend=True):
    if not ax:
        fig, ax = plt.subplots(1, 1, figsize=(5, 3))
    
    x = np.array(list(x))
    strategies = ["Eucalyptus 25", "Mahogany 100", "Mahogany 200", "Reserve"]

    allocation_changes = {}
    for strategy in strategies:
        allocation_changes[strategy] = np.array([s.allocations[strategy] for s in solutions])

    bottom = np.zeros(len(x))
    w = x[1] - x[0]
    for s in strategies:
        # assert x.shape == allocation_changes[s].shape, f"mismatch for {s}, {x.shape} vs {allocation_changes[s].shape}"
        ax.bar(x, allocation_changes[s], color=colors[s], label=s, bottom=bottom, width=w)
        bottom += allocation_changes[s]
    if legend:
        ax.legend(framealpha=1, fontsize="xx-small", loc="lower left")
    ax.margins(x=0, y=0)

    ax.set_xticklabels([int(i) for i in ax.get_xticks()], rotation = 45)
    ax.set_xlabel(xlabel)
    ax.set_ylabel('Allocations (Hectares)')

def plot_constrained_allocations():
    min_habs = range(0, 200)
    solutions_given_habs = []
    for min_hab in min_habs:
        solutions_given_habs.append(solve(set_min_habitats=min_hab))

    min_yield = range(100000, 200000, 1000)
    solutions_given_yield = []
    for min_y in min_yield:
        solutions_given_yield.append(solve(set_min_yield=min_y))

    fig, axes = plt.subplots(2, 2, figsize=(4.5, 5), width_ratios=[1, 0.25])

    fig.suptitle("Only Eucalyptus Satisfies Stricter Constraints")
    allocation_chart(min_habs, solutions_given_habs, ax=axes[0, 0], xlabel="Minimum Habitats", legend=False)
    allocation_chart(min_yield, solutions_given_yield, ax=axes[1, 0], xlabel="Minimum Yield", legend=False)
    axes[0, 1].axis('off')
    axes[1, 1].axis('off')
    axes[0, 1].legend(legend_content[:-2], legend_names[:-2], fontsize=8, frameon=False)
    plt.tight_layout()