import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from scipy.integrate import odeint


GRAPH_AXES = None
SLIDER_BETA = 0.2
SLIDER_GAMMA = 0.1
SLIDER_I0 = 0.01
SLIDER_T = 160.0


def onChangeValue(value):
    update_graph()


def SIR(N=1, I0=0.01, R0=0, beta=0.2, gamma=0.1, time=160):
    """ Функция данных графика """

    S0 = N - I0 - R0
    t = np.linspace(0, time, time)
    y0 = S0, I0, R0
    ret = odeint(deriv, y0, t, args=(N, beta, gamma))
    S, I, R = ret.T
    return S, I, R, N, t


def deriv(y, t, N, beta, gamma):
    """ Дифференциальные уравнения модели """

    S, I, R = y
    dSdt = -beta * S * I / N
    dIdt = beta * S * I / N - gamma * I
    dRdt = gamma * I
    return dSdt, dIdt, dRdt


def create_plot():
    """ Задает параметры графика """

    global GRAPH_AXES
    GRAPH_AXES.set_xlabel("Время [дней]")
    GRAPH_AXES.set_ylabel("Доля [людей]")
    GRAPH_AXES.set_ylim(-0.05, 1.05)


def show():
    """ Выводит график """

    global GRAPH_AXES
    global SLIDER_BETA
    global SLIDER_GAMMA
    global SLIDER_I0
    global SLIDER_T

    fig, GRAPH_AXES = plt.subplots()
    fig.canvas.set_window_title('SIR Model')
    fig.subplots_adjust(left=0.1, right=0.96, top=0.97, bottom=0.4)

    axes_slider_I0 = plt.axes([0.05, 0.09, 0.38, 0.04])
    SLIDER_I0 = Slider(axes_slider_I0, label='I0', valmin=0.0, valmax=1.0, valinit=0.01, valfmt='%1.2f', valstep=0.01)
    SLIDER_I0.on_changed(onChangeValue)

    axes_slider_T = plt.axes([0.54, 0.09, 0.38, 0.04])
    SLIDER_T = Slider(axes_slider_T, label='T', valmin=10, valmax=200, valinit=150, valstep=1)
    SLIDER_T.on_changed(onChangeValue)

    axes_slider_beta = plt.axes([0.05, 0.25, 0.87, 0.04])
    SLIDER_BETA = Slider(axes_slider_beta, label='β', valmin=0.01, valmax=1.0, valinit=0.35, valfmt='%1.2f', valstep=0.01)
    SLIDER_BETA.on_changed(onChangeValue)

    axes_slider_gamma = plt.axes([0.05, 0.17, 0.87, 0.04])
    SLIDER_GAMMA = Slider(axes_slider_gamma, label='γ', valmin=0.01, valmax=1.0, valinit=0.17, valfmt='%1.2f', valstep=0.01)
    SLIDER_GAMMA.on_changed(onChangeValue)

    update_graph()
    plt.show()


def update_graph():
    """ Обновляет данные графика """

    global GRAPH_AXES
    global SLIDER_BETA
    global SLIDER_GAMMA
    global SLIDER_I0
    global SLIDER_T

    beta = SLIDER_BETA.val
    gamma = SLIDER_GAMMA.val
    I0 = SLIDER_I0.val
    time = SLIDER_T.val
    S, I, R, N, t = SIR(beta=beta, gamma=gamma, I0=I0, time=time)

    GRAPH_AXES.clear()
    create_plot()
    GRAPH_AXES.plot(t, S, 'g', alpha=1, lw=2, label='Уязвимые')
    GRAPH_AXES.plot(t, I, 'r', alpha=1, lw=2, label='Инфицированные')
    GRAPH_AXES.plot(t, R, 'black', alpha=1, lw=2, label='Нулевые')
    plt.draw()
