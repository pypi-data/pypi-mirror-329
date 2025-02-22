def calculate_wall_sign_ratios(h, s, B):
    """
    Calculates the ratios of the vertical dimension to wall height (s/h)
    and the horizontal dimension to vertical dimension (B/s).

    :param h: The height of the wall.
    :param s: The vertical dimension.
    :param B: The horizontal dimension.
    :return: A dict with keys:
        - "clearance": s/h (rounded to 5 decimals)
        - "aspect": B/s (rounded to 5 decimals)
    """
    s_over_h = s / h
    b_over_s = B / s

    return {
        "clearance": round(s_over_h, 5),
        "aspect": round(b_over_s, 5),
    }

def calculate_reduction_factor(epsilon):
    """
    Calculates the reduction factor δ = 1 - (1 - ε)^(1.5).

    :param epsilon: A value between 0 and 1.
    :return: The reduction factor (rounded to 5 decimals).
    """
    if epsilon < 0 or epsilon > 1:
        raise ValueError("Epsilon (ε) must be between 0 and 1.")

    delta = 1 - (1 - epsilon) ** 1.5
    return round(delta, 5)

def interpolate_force_coefficient_for_ab(aspect_ratio, clearance_ratio, delta):
    """
    Performs a bilinear interpolation of force coefficients (C_f) based on:
      - aspect_ratio: (B/s)
      - clearance_ratio: (s/h)
      - delta: The reduction factor.

    Uses pre-defined tables of aspect_ratios, clearance_ratios, and force_coefficients.

    :param aspect_ratio: B/s
    :param clearance_ratio: s/h
    :param delta: reduction factor δ
    :return: A dict with keys:
        - "cfa": δ * interpolated_value (Case A)
        - "cfb": δ * interpolated_value (Case B)
    """
    aspect_ratios = [0.05, 0.1, 0.2, 0.5, 1, 2, 4, 5, 10, 20, 30, 45]
    clearance_ratios = [1, 0.9, 0.7, 0.5, 0.3, 0.2, 0.16]
    force_coefficients = [
        [1.80, 1.70, 1.65, 1.55, 1.45, 1.40, 1.35, 1.35, 1.30, 1.30, 1.30, 1.30],  # clearance = 1
        [1.85, 1.75, 1.70, 1.60, 1.55, 1.50, 1.45, 1.45, 1.40, 1.40, 1.40, 1.40],  # clearance = 0.9
        [1.90, 1.85, 1.75, 1.70, 1.65, 1.60, 1.55, 1.55, 1.55, 1.55, 1.55, 1.55],  # clearance = 0.7
        [1.95, 1.85, 1.80, 1.75, 1.75, 1.70, 1.70, 1.70, 1.70, 1.70, 1.70, 1.75],  # clearance = 0.5
        [1.95, 1.90, 1.85, 1.80, 1.80, 1.80, 1.80, 1.80, 1.80, 1.85, 1.85, 1.85],  # clearance = 0.3
        [1.95, 1.90, 1.85, 1.80, 1.80, 1.80, 1.80, 1.80, 1.85, 1.90, 1.90, 1.95],  # clearance = 0.2
        [1.95, 1.90, 1.85, 1.85, 1.80, 1.80, 1.85, 1.85, 1.85, 1.90, 1.90, 1.95],  # clearance = 0.16
    ]

    def find_indices(arr, value):
        """
        Finds the pair of indices in 'arr' between which 'value' lies.
        If value is outside the range, returns the last pair of indices.
        """
        for i in range(len(arr) - 1):
            if arr[i] <= value <= arr[i + 1]:
                return i, i + 1
        return len(arr) - 2, len(arr) - 1

    # Find indices for aspect ratio
    i1, i2 = find_indices(aspect_ratios, aspect_ratio)
    x1, x2 = aspect_ratios[i1], aspect_ratios[i2]

    # Find indices for clearance ratio
    j1, j2 = find_indices(clearance_ratios, clearance_ratio)
    y1, y2 = clearance_ratios[j1], clearance_ratios[j2]

    # Corner values for bilinear interpolation
    Q11 = force_coefficients[j1][i1]
    Q12 = force_coefficients[j1][i2]
    Q21 = force_coefficients[j2][i1]
    Q22 = force_coefficients[j2][i2]

    # Bilinear interpolation
    denominator = (x2 - x1) * (y2 - y1)
    # Prevent division by zero if input is outside table range in a degenerate way
    if abs(denominator) < 1e-12:
        interpolated_value = Q11  # fallback or handle it differently if needed
    else:
        interpolated_value = (
            Q11 * (x2 - aspect_ratio) * (y2 - clearance_ratio)
            + Q21 * (aspect_ratio - x1) * (y2 - clearance_ratio)
            + Q12 * (x2 - aspect_ratio) * (clearance_ratio - y1)
            + Q22 * (aspect_ratio - x1) * (clearance_ratio - y1)
        ) / denominator

    cfa = delta * interpolated_value
    cfb = delta * interpolated_value

    return {
        "cfa": cfa,
        "cfb": cfb,
    }

def calculate_wind_force(qh, G, CfA, As):
    """
    Calculates the design wind force on a pylon.

    :param qh: The velocity pressure at height h.
    :param G: The gust effect factor.
    :param CfA: The force coefficient (Cf) as obtained from tables, etc.
    :param As: The projected area of the structure.
    :param load_case_type: Either "A" or "B" (or a similar descriptor).
    :param B: Horizontal dimension (used if needed for eccentricity).
    :return: The design wind force (float).
    """
    # Design wind force
    force = qh * G * CfA * As

    # If needed for case "B", you could calculate eccentricity = 0.2 * B
    # but it does not affect the force itself in this function unless
    # you incorporate it in further calculations.

    return force
