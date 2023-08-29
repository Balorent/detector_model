import numpy as np
import scipy.special
import parameters

a = 0
s = 0
A = 0


def green(k, r):
    approx = False
    if approx:
        res = np.ones(np.shape(r), dtype=complex)
    else:
        res = -1/(2*np.pi) * scipy.special.kv(0, -1j*k*r)
    return res


def plane_wave(x, y, k, angle):
    return np.exp(1j*k*(x*np.cos(angle) + y*np.sin(angle)))


def I(k, r):
    if r != 0:
        res = -np.imag(green(k, r))
    else:
        res = 1/4
    return res


def inv_f(k, alpha):
    res = 0
    if parameters.model == "max":
        res = 1j/4
    elif parameters.model == "h-s":
        res = -I(k, 0) * green(k, alpha) / I(k, alpha)
    return res


def compute_a():
    N = parameters.N
    if N != 0:
        coordinates = []
        for i in range(N):
            coordinates.append(
                [parameters.coordinates[i][0], parameters.coordinates[i][1]])
        wave_type = parameters.wave_type
        k = parameters.k
        alpha = parameters.alpha
        x, y = np.array(coordinates)[:,0], np.array(coordinates)[:,1]
        dx = x[:, None] - x
        dy = y[:, None] - y
        r = np.sqrt(dx ** 2 + dy ** 2) + np.identity(N)
        matrix = inv_f(k, alpha) * np.identity(N, dtype=complex)
        matrix -= green(k, r) * (1-np.identity(N, dtype=complex))
        vec_phi = 0
        if wave_type == "sph":
            dist = np.sqrt(x * x + y * y)
            vec_phi = green(k, dist)
        elif wave_type == "pl":
            vec_phi = plane_wave(x, y, k, parameters.plane_wave_angle)
        res = np.linalg.solve(matrix, vec_phi)
    else:
        res = []
    return np.array(res)


def compute_s(a_):
    N = parameters.N
    k = parameters.k
    theta_res = parameters.theta_res
    theta = np.linspace(0, 2 * np.pi, theta_res)
    coordinates = []
    for i in range(N):
        coordinates.append(
            [parameters.coordinates[i][0], parameters.coordinates[i][1]])
    coordinates = np.array(coordinates).reshape((N, 2))
    r = np.array([np.cos(theta), np.sin(theta)]).transpose()
    return np.dot(np.exp(-1j * k * np.dot(r, coordinates.T)), np.array(a_).reshape((N, 1)))


def compute_A(s_):
    theta_res = parameters.theta_res
    integrand = np.abs(s_)**2 + 2*np.real(s_)
    return 2*np.pi / (2*np.pi + sum(integrand * 2*np.pi/theta_res))


def compute_psi(x, y, update):
    global a, s, A
    if update:
        update_math()
    k = parameters.k
    N = parameters.N
    coordinates = np.array(parameters.coordinates)
    wave_type = parameters.wave_type
    psi = 0
    if wave_type == "sph":
        dist = np.sqrt(x * x + y * y)
        psi = green(k, dist)
    elif wave_type == "pl":
        psi = plane_wave(x, y, k, parameters.plane_wave_angle)
    for i in range(N):
        dx = x - coordinates[i][0]
        dy = y - coordinates[i][1]
        r = np.sqrt(dx ** 2 + dy ** 2)
        psi += a[i] * green(k, r)
    return A*psi


def compute_cross_section(s_):
    return np.array(1 / parameters.k * np.abs(s_) ** 2).reshape(parameters.theta_res)


def compute_J_with_obstacles(s_, A_):
    integrand = np.abs(s_) ** 2 + 2 * np.real(s_)
    J = parameters.k * (A_ + A_ * integrand)
    return np.array(J).reshape(parameters.theta_res)


def update_math():
    global a, s, A
    a = compute_a()
    s = compute_s(a)
    A = compute_A(s)
