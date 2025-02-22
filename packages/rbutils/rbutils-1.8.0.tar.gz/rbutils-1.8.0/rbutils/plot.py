import math

import matplotlib.pyplot as plt
import numpy as np
import rbutils.rbnp as rbnp


def _plot_surface(X, Y, Z, **kwargs):
    ax = plt.axes(projection="3d")
    ax.plot_surface(X, Y, Z, cmap="viridis", edgecolor="none")
    if kwargs.get('aspect') is not None:
        ax.set_aspect(kwargs.get('aspect'))
    plt.show()


def _plot3D(X, Y, Z, **kwargs):
    ax = plt.axes(projection="3d")
    if kwargs.get('showDot', False) is True:
        ax.scatter3D(X, Y, Z)
    ax.plot3D(X, Y, Z, kwargs.get('color', 'red'))
    if kwargs.get('aspect') is not None:
        ax.set_aspect(kwargs.get('aspect'))
    # 显示图形
    plt.show()


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
        0, 1, lambda t: t * np.sin(20 * t), lambda t: t * np.cos(20 * t), lambda t: t
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
    ax = plt.axes(projection="3d")
    ax.scatter3D(*vector, "blue")
    ax.plot3D(*vector, "red")
    ax.plot_surface(X, Y, Z, cmap="viridis", edgecolor="none")
    if kwargs.get('aspect') is not None:
        ax.set_aspect(kwargs.get('aspect'))
    plt.show()


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


def plot_3d_surface_z_with_curve(x_start, x_end, y_start, y_end, funZ, x1, y1, x2, y2, **kwargs):
    X, Y = np.meshgrid(np.linspace(x_start, x_end, kwargs.get('num', 101)),
                       np.linspace(y_start, y_end, kwargs.get('num', 101)))
    Z = funZ(X, Y)
    # 创建3d绘图区域
    arr = rbnp.linspace_2d(x1, y1, x2, y2, kwargs.get('num', 101))
    X1 = arr[:, 0]
    Y1 = arr[:, 1]
    Z1 = funZ(X1, Y1)

    plt.xlabel("X")
    plt.ylabel("Y")
    ax = plt.axes(projection="3d")
    ax.plot_surface(X, Y, Z, cmap="viridis", alpha=0.9)
    ax.plot3D(X1, Y1, Z1, c="red")
    if kwargs.get('aspect') is not None:
        ax.set_aspect(kwargs.get('aspect'))
    plt.show()


def example_plot_3d_surface_z_with_curve():
    plot_3d_surface_z_with_curve(0, 3, -2, 1, lambda x, y: x * math.e ** (2 * y), 1, 0, 2, -1, aspect='equal')


if __name__ == "__main__":
    # 本地测试使用
    # example_plot_2d_curve_parametric()
    # example_plot_3d_curve_parametric()
    # example_plot_3d_surface_z()
    example_plot_3d_plane_dot2normal()
    # example_plot_3d_surface_z_with_curve()
