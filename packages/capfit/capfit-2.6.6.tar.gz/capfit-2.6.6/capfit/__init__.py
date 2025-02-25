__version__ = "2.6.6"

from .capfit import capfit, lsq_box, lsq_lin, lsq_lin_cvxopt, cov_err, lsq_eq

__all__ = [
    "capfit",
    "lsq_box", 
    "lsq_lin", 
    "lsq_lin_cvxopt", 
    "cov_err", 
    "lsq_eq"
]

