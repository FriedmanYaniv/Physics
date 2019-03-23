import numpy as np
import matplotlib.pyplot as plt
from scipy.misc import derivative


def parabolic_potential(a0, a1, a2):
    fn = lambda t: a0 + a1*t + a2*(t**2)
    return fn


if __name__ == '__main__':
    potentials = []
    phi_vec = np.linspace(0, 1, num=1000)
    num_phases = int(input('How many phases? '))
    for phase in range(num_phases):
        print('choose a1 smaller than a2')
        coefs = [float(x) for x in
                 input('for phase number {}, please type coefficients a0, a1, a2'.format(phase+1)).split()]
        potentials.append(parabolic_potential(coefs[0], -coefs[1], coefs[2]))

    f1 = potentials[0]
    plt.plot(phi_vec, f1(phi_vec))
    plt.xlim((0, 1))
    np.argmin(derivative(f1, phi_vec))
