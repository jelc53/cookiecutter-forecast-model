import math


def scaled_normal_pdf(x, para_1, para_2):
    """."""
    # Note, max f(x)=1, no longer true for area under curve
    mu = para_1
    sigma = para_2
    return math.exp(-pow((x - mu), 2) / (2 * pow(sigma, 2)))


def linear(x, para_1, para_2=1):
    """."""
    gradient = para_1
    y_int = para_2
    return gradient * x + y_int


def neg_linear(x, para_1, para_2=1):
    """."""
    gradient = para_1
    y_int = para_2
    return -gradient * x + y_int


def parabola(x, para_1, para_2, para_3=1):
    """."""
    apex_y = para_1
    apex_x = para_2
    gradient = para_3
    return gradient * (-apex_y / (apex_x**2)) * (x - apex_x) ** 2 + apex_y


def logistic_curve(x, para_1, para_2):
    """."""
    # Note, extra parameter allows more freedom than exponential decay
    growth_rate = para_1
    sigmoid_midpoint = para_2
    return 1 / (1 + math.exp(-growth_rate * (x - sigmoid_midpoint)))


def diminishing_returns(x, para_1):
    """."""
    # Passes through center, asymptotes at f(x)=1
    sensitivity = para_1
    return 1 - math.exp(-sensitivity * x)


def exponential_decay(x, para_1, para_2):
    """."""
    # Starts at 1 (height term), decays exponentially
    translation = para_1
    steepness = para_2
    return 1 - math.exp(steepness * x - translation)
