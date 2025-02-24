import math

import matplotlib.pyplot as plt
import numpy as np
import rbutils.rbnp as rbnp
import sympy as sp


def _plot_surface(X, Y, Z, **kwargs):
    if kwargs.get('ax') is None:
        ax = plt.axes(projection="3d")
    else:
        ax = kwargs.get('ax')
    ax.plot_surface(X, Y, Z, cmap="viridis", edgecolor="none")
    if kwargs.get('aspect') is not None:
        ax.set_aspect(kwargs.get('aspect'))
    plt.show()


def _plot3D(X, Y, Z, **kwargs):
    if kwargs.get('ax') is None:
        ax = plt.axes(projection="3d")
    else:
        ax = kwargs.get('ax')
    if kwargs.get('showDot', False) is True:
        ax.scatter3D(X, Y, Z)
    ax.plot3D(X, Y, Z, kwargs.get('color', 'red'))
    if kwargs.get('aspect') is not None:
        ax.set_aspect(kwargs.get('aspect'))
    # 显示图形
    if kwargs.get('isChain', False) is not True:
        plt.show()
    else:
        return ax


def _plot2D(X, Y, **kwargs):
    if kwargs.get('showDot', False) is True:
        plt.scatter(X, Y)
    plt.plot(X, Y, kwargs.get('color', 'red'))
    if kwargs.get('aspect') is not None:
        ax = plt.gca()
        ax.set_aspect(kwargs.get('aspect'))
    plt.show()


def plot_2d_curve_parametric(
        t_start, t_end, funX, funY, **kwargs
):
    T = np.linspace(t_start, t_end, kwargs.get('num', 1001))
    X = funX(T)
    Y = funY(T)
    _plot2D(X, Y, **kwargs)


def example_plot_2d_curve_parametric():
    plot_2d_curve_parametric(0, 6, lambda t: np.sin(t), lambda t: np.cos(t), aspect="equal")


def plot_3d_curve_parametric(
        t_start, t_end, funX, funY, funZ, **kwargs
):
    T = np.linspace(t_start, t_end, kwargs.get('num', 1001))
    X = funX(T)
    Y = funY(T)
    Z = funZ(T)
    _plot3D(X, Y, Z, **kwargs)


def example_plot_3d_curve_parametric():
    plot_3d_curve_parametric(
        0, 4, lambda t: t * t + 1, lambda t: 4 * t - 3, lambda t: 2 * t * t - 6 * t, aspect="equal"
    )


# 绘制3d参数曲线，和某个点的切线
def plot_3d_curve_parametric_with_tangent(t_start, t_end, funX, funY, funZ, t0, **kwargs):
    T = np.linspace(t_start, t_end, kwargs.get('num', 1001))
    X = funX(T)
    Y = funY(T)
    Z = funZ(T)

    t = sp.symbols('t')
    point = np.array([funX(t0), funY(t0), funZ(t0)])
    vector = np.array([float(sp.diff(funX(t), t).subs(t, t0)),
                       float(sp.diff(funY(t), t).subs(t, t0)),
                       float(sp.diff(funZ(t), t).subs(t, t0))])
    v = rbnp.reverse_vector(point, point + vector)
    print('切线向量：',vector)
    ax = _plot3D(*v, isChain=True, showDot=True)
    _plot3D(X, Y, Z, **kwargs, ax=ax)


def example_plot_3d_curve_parametric_with_tangent():
    plot_3d_curve_parametric_with_tangent(
        0, 4, lambda t: t * t + 1, lambda t: 4 * t - 3, lambda t: 2 * t * t - 6 * t, 2, aspect="equal"
    )


def plot_3d_plane_dot2normal(x_start, x_end, y_start, y_end, point, normal, **kwargs):
    X, Y = np.meshgrid(
        np.linspace(x_start, x_end, kwargs.get('num', 101)), np.linspace(y_start, y_end, kwargs.get('num', 101))
    )
    # 平面方程 a*x+b*y+c*z+d=0，可的d=-(ax+by+cz)
    d = -point.dot(normal)
    # a*x+b*y+c*z+d=0 可的 z = -(ax+by+d)/c
    Z = (-normal[0] * X - normal[1] * Y - d) * 1.0 / normal[2]
    vector = rbnp.reverse_vector(point, point + normal)
    ax = _plot3D(*vector, isChain=True, showDot=True)
    _plot_surface(X, Y, Z, ax=ax, **kwargs)


def example_plot_3d_plane_dot2normal():
    plot_3d_plane_dot2normal(-5, 5, -5, 5, np.array([1, 2, 3]), np.array([1, 1, 2]), aspect="equal")


def plot_3d_surface_z(x_start, x_end, y_start, y_end, funZ, **kwargs):
    X, Y = np.meshgrid(
        np.linspace(x_start, x_end, kwargs.get('num', 101)), np.linspace(y_start, y_end, kwargs.get('num', 101))
    )
    Z = funZ(X, Y)
    _plot_surface(X, Y, Z, **kwargs)


def example_plot_3d_surface_z():
    plot_3d_surface_z(-3, 3, -3, 3, lambda x, y: x ** 2 + y ** 2, aspect="equal")


def plot_3d_surface_z_with_curve(x_start, x_end, y_start, y_end, funZ, point1, point2, **kwargs):
    X, Y = np.meshgrid(np.linspace(x_start, x_end, kwargs.get('num', 101)),
                       np.linspace(y_start, y_end, kwargs.get('num', 101)))
    Z = funZ(X, Y)
    # 创建3d绘图区域
    X1 = np.linspace(point1[0], point2[0])
    Y1 = np.linspace(point1[1], point2[1])
    Z1 = funZ(X1, Y1)
    ax = _plot3D(X1, Y1, Z1, **kwargs, isChain=True)
    _plot_surface(X, Y, Z, ax=ax, **kwargs)


def example_plot_3d_surface_z_with_curve():
    plot_3d_surface_z_with_curve(0, 2, -1, 1, lambda x, y: x * math.e ** (2 * y), np.array([1, 0]), np.array([2, -1]),
                                 aspect="equal")


if __name__ == "__main__":
    # 本地测试使用
    # example_plot_2d_curve_parametric()
    # example_plot_3d_curve_parametric()
    example_plot_3d_curve_parametric_with_tangent()
    # example_plot_3d_surface_z()
    # example_plot_3d_plane_dot2normal()
    # example_plot_3d_surface_z_with_curve()
