from typing import Callable, Union

import numpy as np
from numpy import exp, pi, cos, sin
from scipy.stats import norm

from cfinversion.cf_inverter.bohman.bohman_abstract import BohmanAbstract


# Straight on
class NaiveBohmanA(BohmanAbstract):
    def __init__(self, N: int, delta: float) -> None:
        super().__init__()
        self.phi = None
        self.N = int(N)
        self.delta = delta

    def fit(self, phi: Callable[[float], complex]) -> None:
        self.phi = phi

    def cdf(self, x: float) -> Union[float, np.ndarray]:
        if self.phi is None:
            raise ValueError("Characteristic function (phi) is not set. Call fit() first.")
        F = 0.5 + (self.delta * x) / (2 * pi)
        for v in range(1 - self.N, self.N):
            if v == 0:
                continue
            F -= (self.phi(self.delta * v) / (2 * pi * 1j * v)) * exp(-1j * self.delta * v * x)
        return F.real


# Battling the truncation error by deforming F
class NaiveBohmanB(BohmanAbstract):

    def __init__(self, N: int, delta: float) -> None:
        super().__init__()
        self.phi = None
        self.N = int(N)
        self.delta = delta

    def fit(self, phi: Callable[[float], complex]) -> None:
        self.phi = phi

    def __C(self, t: float):
        if t > 1:
            return 0
        if t < 0:
            return self.__C(-t)
        return (1 - t) * cos(pi * t) + sin(pi * t) / pi

    def cdf(self, x: float) -> Union[float, np.ndarray]:
        if self.phi is None:
            raise ValueError("Characteristic function (phi) is not set. Call fit() first.")
        F = 0.5 + (self.delta * x) / (2 * pi)
        for v in range(1 - self.N, self.N):
            if v == 0:
                continue
            F -= self.__C(v / self.N) * (self.phi(self.delta * v) / (2 * pi * 1j * v)) * exp(-1j * self.delta * v * x)
        return F.real


# Reducing importance of trigonometric series by considering difference between F and
class NaiveBohmanC(BohmanAbstract):
    def __init__(self, N: int, delta: float):
        super().__init__()
        self.phi = None
        self.N = int(N)
        self.delta = delta

    def fit(self, phi: Callable[[float], complex]) -> None:
        self.phi = phi

    def cdf(self, x: float) -> Union[float, np.ndarray]:
        if self.phi is None:
            raise ValueError("Characteristic function (phi) is not set. Call fit() first.")
        F = norm.cdf(x, loc=0, scale=1)
        for v in range(1 - self.N, self.N):
            if v == 0:
                continue
            p = self.delta * v
            F += ((exp(- (p ** 2) / 2) - self.phi(p)) / (2 * pi * 1j * v)) * exp(-1j * p * x)
        return F.real


# Reducing the aliasing error and reducing importance of trigonometric series
class NaiveBohmanD(BohmanAbstract):
    def __init__(self, N: int, delta: float, K: int):
        super().__init__()
        self.phi = None
        self.N = int(N)
        self.delta = delta
        self.K = K

    def fit(self, phi: Callable[[float], complex]) -> None:
        self.phi = phi

    def __H(self, x: float, delta: float) -> complex:
        H = 0
        for v in range(1 - self.N, self.N):
            if v == 0:
                continue
            p = delta * v
            H += ((exp(- (p ** 2) / 2) - self.phi(p)) / (2 * pi * 1j * v)) * exp(-1j * p * x)
        return H

    def cdf(self, x: float) -> Union[float, np.ndarray]:
        if self.phi is None:
            raise ValueError("Characteristic function (phi) is not set. Call fit() first.")
        F = norm.cdf(x, loc=0, scale=1) + self.__H(x, self.delta)
        d = (2 * pi) / (self.N * self.delta)
        for v in range(1, self.K):
            L = self.N // self.K
            delta_1 = self.delta / self.K
            d_1 = self.K * d
            F -= self.__H(x + v * L * d_1, delta_1)
        return F.real


# Reducing the aliasing error and Reducing importance of trigonometric
# series and Battling the truncation error by deforming F
class NaiveBohmanE(BohmanAbstract):
    def __init__(self,  N: int, delta: float, K: int):
        super().__init__()
        self.phi = None
        self.N = int(N)
        self.delta = delta
        self.K = K

    def fit(self, phi: Callable[[float], complex]) -> None:
        self.phi = phi

    def __C(self, t: float) -> float:
        if t > 1:
            return 0
        if t < 0:
            return self.__C(-t)
        return (1 - t) * cos(pi * t) + sin(pi * t) / pi

    def __G(self, x: float, delta: float) -> np.ndarray:
        G = 0
        for v in range(1 - self.N, self.N):
            if v == 0:
                continue
            p = delta * v
            G += self.__C(v / self.N) * ((exp(- (p ** 2) / 2) - self.phi(p)) / (2 * pi * 1j * v)) * exp(-1j * p * x)
        return G

    def cdf(self, x: float) -> Union[float, np.ndarray]:
        if self.phi is None:
            raise ValueError("Characteristic function (phi) is not set. Call fit() first.")
        F = norm.cdf(x, loc=0, scale=1) + self.__G(x, self.delta)
        d = (2 * pi) / (self.N * self.delta)
        L = self.N // self.K
        delta_1 = self.delta / self.K
        d_1 = self.K * d
        for v in range(1, self.K):
            F -= self.__G(x + v * L * d_1, delta_1)
        return F.real
