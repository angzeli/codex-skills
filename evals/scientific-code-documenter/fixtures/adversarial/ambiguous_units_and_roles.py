def transform_series(a, b, scale=1e-9):
    adjusted = [value * scale for value in a]
    ratio = [left / right for left, right in zip(adjusted, b)]
    return adjusted, ratio