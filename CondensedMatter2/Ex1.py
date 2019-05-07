import numpy as np
import matplotlib.pyplot as plt
from scipy.misc import derivative
from scipy.optimize import fsolve


def add_liquid_phase(potentials):
    minimums = [f[1][1] for f in potentials]
    liquid_min = min(minimums) - 0.5
    liquid_coefs = [np.random.rand(), liquid_min]
    liquid_phase = parabolic_potential(liquid_coefs[0], liquid_coefs[1])
    potentials.append([liquid_phase, liquid_coefs])
    return potentials


def parabolic_potential(xmin, bias, t=10):
    fn = lambda x: bias + (x-xmin)**2 + t
    return fn


if __name__ == '__main__':
    auto_ans = True
    potentials = []
    phi_vec = np.linspace(0, 1, num=1000)
    if auto_ans:
        num_phases = 1
    else:
        num_phases = int(input('How many phases? '))

    for phase in range(num_phases):
        print('choose a1 smaller than a2')
        if auto_ans:
            coefs = [np.random.rand(), 1]
        else:
            coefs = [float(x) for x in
                     input('for phase number {}, please type coefficients x_min, bias'.format(phase + 1)).split()]

        # potentials.append(parabolic_potential(coefs[0], -coefs[1], coefs[2]))
        potentials.append([parabolic_potential(coefs[0], coefs[1]), coefs])

    potentials = add_liquid_phase(potentials)
    for ind, f in enumerate(potentials):
        plt.plot(phi_vec, f[0](phi_vec), label='f_{}'.format(ind + 1))
        plt.xlim((0, 1))
    plt.legend()
    plt.grid()


    # find common tangent by finding phi for which the abs(derivative1 - derivative2) is minimum
    T_0 = 0
    dist = min([f[1][1] for f in potentials[:-1]]) - potentials[-1][1][1]
    T_c = f[-1]

    np.argmin(abs(derivative(f[0], phi_vec)))
