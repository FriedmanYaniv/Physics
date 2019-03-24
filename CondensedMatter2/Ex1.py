import numpy as np
import matplotlib.pyplot as plt
from scipy.misc import derivative


# def parabolic_potential(a0, a1, a2):
#     fn = lambda t: a0 + a1*t + a2*(t**2)
#     return fn

def parabolic_potential(xmin, bias, t=10):
    fn = lambda x: bias + (x-xmin)**2 + t
    return fn


if __name__ == '__main__':
    potentials = []
    phi_vec = np.linspace(0, 1, num=1000)
    num_phases = int(input('How many phases? '))
    for phase in range(num_phases):
        print('choose a1 smaller than a2')
        coefs = [float(x) for x in
                 input('for phase number {}, please type coefficients x_min, bias'.format(phase+1)).split()]
        # potentials.append(parabolic_potential(coefs[0], -coefs[1], coefs[2]))
        potentials.append(parabolic_potential(coefs[0], coefs[1]))

    for ind, f in enumerate(potentials):
        plt.plot(phi_vec, f(phi_vec), label='f_{}'.format(ind + 1))
        plt.xlim((0, 1))
    plt.legend()
    plt.grid()


    # find common tangent by finding phi for which the abs(derivative1 - derivative2) is minimum
    np.argmin(derivative(f, phi_vec))

