import math
import functools
from typing import NamedTuple, Union
import matplotlib.pyplot as plt


CODE_DISTANCE = 31
LOGICAL_QUBIT_AREA = 2 * (CODE_DISTANCE+1)**2  # physical qubits
FACTORY_DEPTH = 6.5 * 31  # microseconds
FACTORY_AREA = 12 * 6 * LOGICAL_QUBIT_AREA  # physical qubits
FACTORY_PRODUCTION_RATE = 1 / FACTORY_DEPTH  # MegaHertz
REACTION_TIME = 10  # microseconds
FACTORY_ROUTING_OVERHEAD = 0.5
FACTORY_VOLUME = FACTORY_DEPTH * FACTORY_AREA
SINGLE_THREADED_TOFFOLI_RATE = 1 / REACTION_TIME


class Cost(NamedTuple('BaseCost', [
    ('n', int),
    ('k', int),
    ('toffoli_count', int),
    ('ancilla_count', int),
    ('measure_depth', int),
    ('trace_distance', float),
])):
    @property
    def duration(self) -> int:  # microseconds
        return max(1, self.measure_depth * REACTION_TIME)

    @property
    def total_space(self) -> int:
        toffoli_rate = self.toffoli_count / self.duration  # MegaHertz
        factory_count = int(math.ceil(toffoli_rate / FACTORY_PRODUCTION_RATE))
        factory_area = FACTORY_AREA * factory_count
        routing_area = factory_area * FACTORY_ROUTING_OVERHEAD
        qubit_area = (self.ancilla_count + self.n) * LOGICAL_QUBIT_AREA
        return qubit_area + routing_area + factory_area

    @property
    def total_volume(self) -> int:
        return self.total_space * self.duration


def gidney_ripple_carry_adder_cost(n: int, k: int) -> Cost:
    return Cost(n=n,
                k=k,
                toffoli_count=k*max(0, n-1),
                ancilla_count=n - 1,
                measure_depth=k*max(0, 2*n-3),
                trace_distance=0)


def cuccaro_ripple_carry_adder_cost(n: int, k: int) -> Cost:
    """
    Args:
        n: Register size being operated on.
        k: Number of additions to perform.
    """
    return Cost(n=n,
                k=k,
                toffoli_count=k*max(0, 2*n-3),
                ancilla_count=0,
                measure_depth=k*max(0, 2*n-3),
                trace_distance=0)


def cuccaro_ripple_carry_modular_adder_cost(n: int, k: int) -> Cost:
    """
    Args:
        n: Register size being operated on.
        k: Number of additions to perform.
    """
    # a += b  [adder costs 2n]
    # c = a >= N  [comparison costs 2n]
    # if c: a -= N  [conditional adder costs 4n]
    # del c = a < N - b  [comparison costs 2n]
    return Cost(n=n,
                k=k,
                toffoli_count=k*10*n,
                ancilla_count=1,
                measure_depth=k*10*n,
                trace_distance=0)


def gidney_ripple_carry_modular_adder_cost(n: int, k: int) -> Cost:
    """
    Args:
        n: Register size being operated on.
        k: Number of additions to perform.
    """
    # a += b  [adder costs n]
    # c = a >= N  [comparison costs n]
    # if c: a -= N  [conditional adder costs 2n]
    # del c = a < N - b  [comparison costs n]
    return Cost(n=n,
                k=k,
                toffoli_count=k*5*n,
                ancilla_count=n+1,
                measure_depth=k*10*n,
                trace_distance=0)


def w(n: int) -> int:
    """Number of set bits in an integer. The Hamming weight. The pop count."""
    assert n >= 0
    t = 0
    while n:
        n &= n-1
        t += 1
    return t


def lg(n: Union[int, float]) -> int:
    """Ceiling of the base-2 logarithm, clamped to be at least 0."""
    if n <= 1:
        return 0
    return int(math.ceil(math.log2(n)))


def log_depth_adder_cost(n: int, k: int) -> Cost:
    """
    Args:
        n: Register size being operated on.
        k: Number of additions to perform.
    """
    tof = max(1, 10*n - 3 * w(n) - 3 * w(n-1)  - 3 * lg(n) - 3 * lg(n-1) - 7)
    dep = max(1, lg(n) + lg(n-1) + lg(n/3) + lg((n-1)/3) + 14 - 2 - 4)
    return Cost(n=n,
                k=k,
                toffoli_count=tof * k,
                ancilla_count=max(0, 2*n - w(n) - lg(n) - 1),
                measure_depth=dep * k,
                trace_distance=0)


def log_depth_modular_adder_cost(n: int, k: int) -> Cost:
    """
    Args:
        n: Register size being operated on.
        k: Number of additions to perform.
    """
    # a += b  [added ]
    # c = a >= N  [comparison using adder]
    # if c: a -= N  [conditional adder; +n tofs +lg(n) depth]
    # del c = a < N - b  [comparison using adder]
    non_mod = log_depth_adder_cost(n, k)
    return Cost(n=n,
                k=k,
                toffoli_count=non_mod.toffoli_count * 4 + n*k,
                ancilla_count=non_mod.ancilla_count + 1,
                measure_depth=non_mod.measure_depth * 4 + lg(n) * k,
                trace_distance=0)


def required_padding(max_trace_distance: float, k: int, r: int):
    """
    Args:
        max_trace_distance: Error bound between 0 and 1.
        k: Number of additions that will be performed.
        r: Number of carry runways.
    """
    return lg(k*r / (max_trace_distance/2)**2)


def piecewise_adder_cost(n: int,
                         k: int,
                         s: int,
                         max_trace_distance: float
                         ) -> Cost:
    """
    Args:
        k: Number of additions that will be performed.
        n: Register size being operated on (not including runways).
        s: Spacing between runways in bits.
        max_trace_distance: Error bound between 0 and 1.
    """
    r = int(math.ceil(n / s)) - 1
    if r == 0:
        return cuccaro_ripple_carry_adder_cost(n, k)
    m = required_padding(max_trace_distance, k=k, r=r)
    padded = cuccaro_ripple_carry_adder_cost(n=s + m, k=k)
    end = cuccaro_ripple_carry_adder_cost(n=n - s * r, k=k)
    return Cost(n=n,
                k=k,
                toffoli_count=padded.toffoli_count * r + end.toffoli_count,
                measure_depth=max(padded.measure_depth, end.measure_depth),
                trace_distance=2 * math.sqrt(k * r * 2**-m),
                ancilla_count=r*m)


def piecewise_modular_adder_cost(n: int,
                                 k: int,
                                 s: int,
                                 max_trace_distance: float
                                 ) -> Cost:
    """
    Args:
        k: Number of additions that will be performed.
        n: Register size being operated on (not including runways).
        s: Spacing between runways in bits.
        max_trace_distance: Error bound between 0 and 1.
    """
    r = int(math.ceil(n / s)) - 1
    m = required_padding(max_trace_distance, k=k, r=r+1)
    if r == 0:
        return cuccaro_ripple_carry_adder_cost(n+m, k)
    padded = cuccaro_ripple_carry_adder_cost(n=s + m, k=k)
    end = cuccaro_ripple_carry_adder_cost(n=n - s * r + m, k=k)
    return Cost(n=n,
                k=k,
                toffoli_count=padded.toffoli_count * r + end.toffoli_count,
                measure_depth=max(padded.measure_depth, end.measure_depth),
                trace_distance=2 * math.sqrt(k * (r+1) * 2**-m),
                ancilla_count=(r+1)*m)


def plot_non_modular():
    ns = [int(math.floor(0.5+math.sqrt(2)**k)) for k in range(4*2, 20*2)]
    k_func = lambda n: n**2

    strategies = [
        ('Ripple-carry (Cuccaro)', cuccaro_ripple_carry_adder_cost, {'linewidth': 3}),
        ('Ripple-carry (Gidney)', gidney_ripple_carry_adder_cost, {}),
        ('Carry-lookahead (Draper et al)', log_depth_adder_cost, {'linewidth': 3}),
    ]
    for s in [64, 128, 256, 512, 1024, 2048]:
        f = functools.partial(piecewise_adder_cost, s=s, max_trace_distance=0.01)
        strategies.append(('Runway every {} bits'.format(s), f, {'linestyle': '--' if s != 256 else '-'}))

    costs = [[f(n, k_func(n)) for n in ns] for _, f, _ in strategies]

    depths = [[c.measure_depth for c in cs] for cs in costs]
    depths_per_add = [[v / k_func(n) for n, v in zip(ns, vs)] for vs in depths]

    tofs = [[c.toffoli_count for c in cs] for cs in costs]
    tofs_per_add = [[v / k_func(n) / n for n, v in zip(ns, vs)] for vs in tofs]

    vols = [[c.total_volume for n, c in zip(ns, cs)] for cs in costs]
    qubit_seconds = 10**6
    vols_per_add = [[v / k_func(n) / n / qubit_seconds for n, v in zip(ns, vs)] for vs in vols]

    spaces = [[c.total_space / LOGICAL_QUBIT_AREA for n, c in zip(ns, cs)] for cs in costs]
    spaces_per_add = [[s / n for n, s in zip(ns, ss)] for ss in spaces]

    plt.figure()
    plt.title('Depth per addition')
    for (k, _, s), v in zip(strategies, depths_per_add):
        plt.plot(ns, v, label=k, **s)
    plt.xscale('log')
    plt.yscale('log')
    plt.xlim(min(ns), max(ns))
    plt.xlabel('Register size (n)')
    plt.ylabel('Measurement depth per addition (V/k)')
    plt.legend()
    plt.savefig('plot-depth.png', figsize=(1024, 1024))

    plt.figure()
    plt.title('Toffolis per addition per register size')
    for (k, _, s), v in zip(strategies, tofs_per_add):
        plt.plot(ns, v, label=k, **s)
    plt.xscale('log')
    plt.xlim(min(ns), max(ns))
    plt.xlabel('Register size (n)')
    plt.ylabel('Toffolis per addition per register size (V/k/n)')
    plt.legend()
    plt.savefig('plot-toffoli.png', figsize=(1024, 1024))

    plt.figure()
    plt.title('Volume per addition per register size')
    for (k, _, s), v in zip(strategies, vols_per_add):
        plt.plot(ns, v, label=k, **s)
    plt.xscale('log')
    plt.yscale('log')
    plt.xlim(min(ns), max(ns))
    plt.xlabel('Register size (n)')
    plt.ylabel('Qubitseconds per addition per register qubit (V/k/n)')
    plt.legend()
    plt.savefig('plot-volume.png', figsize=(1024, 1024))

    plt.figure()
    plt.title('Average logical qubits during addition per register size')
    for (k, _, s), v in zip(strategies, spaces_per_add):
        plt.plot(ns, v, label=k, **s)
    plt.xscale('log')
    plt.yscale('log')
    plt.xlim(min(ns), max(ns))
    plt.xlabel('Register size (n)')
    plt.ylabel('Average logical space usage factor (S/n)')
    plt.legend()
    plt.savefig('plot-space.png', figsize=(1024, 1024))


def plot_modular():
    ns = [int(math.floor(0.5 + math.sqrt(2)**k)) for k in
          range(4 * 2, 20 * 2)]
    k_func = lambda n: n**2

    strategies = [
        ('Via ripple-carry (Cuccaro)', cuccaro_ripple_carry_modular_adder_cost, {'linewidth': 3}),
        ('Via ripple-carry (Gidney)', gidney_ripple_carry_modular_adder_cost, {}),
        ('Via carry-lookahead (Draper et al)', log_depth_modular_adder_cost, {'linewidth': 3}),
    ]
    for s in [64, 128, 256, 512, 1024, 2048]:
        f = functools.partial(piecewise_adder_cost, s=s,
                              max_trace_distance=0.01)
        strategies.append(('Runway every {} bits'.format(s), f,
                           {'linestyle': '--' if s != 256 else '-'}))

    costs = [[f(n, k_func(n)) for n in ns] for _, f, _ in strategies]

    depths = [[c.measure_depth for c in cs] for cs in costs]
    depths_per_add = [[v / k_func(n) for n, v in zip(ns, vs)] for vs in
                      depths]

    tofs = [[c.toffoli_count for c in cs] for cs in costs]
    tofs_per_add = [[v / k_func(n) / n for n, v in zip(ns, vs)] for vs in
                    tofs]

    vols = [[c.total_volume for n, c in zip(ns, cs)] for cs in costs]
    qubit_seconds = 10**6
    vols_per_add = [
        [v / k_func(n) / n / qubit_seconds for n, v in zip(ns, vs)] for vs
        in vols]

    spaces = [[c.total_space / LOGICAL_QUBIT_AREA for n, c in zip(ns, cs)]
              for cs in costs]
    spaces_per_add = [[s / n for n, s in zip(ns, ss)] for ss in spaces]

    plt.figure()
    plt.title('Depth per modular addition')
    for (k, _, s), v in zip(strategies, depths_per_add):
        plt.plot(ns, v, label=k, **s)
    plt.xscale('log')
    plt.yscale('log')
    plt.xlim(min(ns), max(ns))
    plt.xlabel('Register size (n)')
    plt.ylabel('Measurement depth per modular addition (V/k)')
    plt.legend()
    plt.savefig('plot-depth-mod.png', figsize=(1024, 1024))

    plt.figure()
    plt.title('Toffolis per modular addition per register size')
    for (k, _, s), v in zip(strategies, tofs_per_add):
        plt.plot(ns, v, label=k, **s)
    plt.xscale('log')
    plt.xlim(min(ns), max(ns))
    plt.xlabel('Register size (n)')
    plt.ylabel('Toffolis per modular addition per register size (V/k/n)')
    plt.legend()
    plt.savefig('plot-toffoli-mod.png', figsize=(1024, 1024))

    plt.figure()
    plt.title('Volume per modular addition per register size')
    for (k, _, s), v in zip(strategies, vols_per_add):
        plt.plot(ns, v, label=k, **s)
    plt.xscale('log')
    plt.yscale('log')
    plt.xlim(min(ns), max(ns))
    plt.xlabel('Register size (n)')
    plt.ylabel('Qubitseconds per modular addition per register qubit (V/k/n)')
    plt.legend()
    plt.savefig('plot-volume-mod.png', figsize=(1024, 1024))

    plt.figure()
    plt.title('Average logical qubits during modular addition per register size')
    for (k, _, s), v in zip(strategies, spaces_per_add):
        plt.plot(ns, v, label=k, **s)
    plt.xscale('log')
    plt.yscale('log')
    plt.xlim(min(ns), max(ns))
    plt.xlabel('Register size (n)')
    plt.ylabel('Average logical space usage factor (S/n)')
    plt.legend()
    plt.savefig('plot-space-mod.png', figsize=(1024, 1024))


if __name__ == '__main__':
    plot_non_modular()
    plot_modular()
    plt.show()