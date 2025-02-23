from math import prod
from numpy import ceil, floor
import pandas as pd
from pkg_resources import resource_stream


def normalize_arities(arity=2, repeat=1, direction=1):
    assert isinstance(arity, (int, list)), "Parameter `arity` should be of type int | list[int]"
    assert isinstance(repeat, int) and repeat >= 0, "Parameter `repeat` should be of type int, and >=0"
    assert isinstance(direction, (int, list)), "Parameter `direction` be of type int | list[int]"

    arities = [arity] if isinstance(arity, int) else arity
    assert all(isinstance(a, int) and abs(a) >= 2 for a in arities), "Each arity should be an int | list[int] where every integer satisfies abs >= 2."
    arities *= repeat
    directions = [direction] if isinstance(direction, int) else direction
    assert all(isinstance(d, int) and abs(d) == 1 for d in directions), "Each direction should be an int of either +1 or -1"
    assert len(arities) % len(directions) == 0, "Incorrect length of directions."
    directions *= (len(arities) // len(directions))
    arities = [a * d for a, d in zip(arities, directions)]
    return arities

def normalize_correct_detect(correct=0, detect=0):
    assert isinstance(correct, int) and correct >= 0, "Parameter `correct` should be of type int, and >= 0"
    if detect is None:
        detect = correct
    assert isinstance(detect, int) and detect >= correct, "Parameter `detect` should be of type int, and >= correct"
    return correct, detect


def normalize_parameters(arity, repeat, direction, correct, detect):
    arities = normalize_arities(arity, repeat, direction)
    correct, detect = normalize_correct_detect(correct, detect)
    return arities, correct, detect


def normalize_result(lb, ub, inclusive="both", eps=1e-3):
    if inclusive in ["right", "neither"]:
        lb += eps
    if inclusive in ["left", "neither"]:
        ub -= eps
    lb = int(ceil(lb))
    ub = int(floor(ub))
    if lb == ub:
        return lb
    return range(lb, ub+1)
        

def trim(arities):
    while len(arities) > 0:
        if arities[0] < 0:
            arities.pop(0)
        else:
            break
    while len(arities) > 0:
        if arities[-1] < 0:
            arities.pop(-1)
        else:
            break
    return arities


def filter_direction(arities, direction=None):
    if direction:
        arities = [a for a in arities if a * direction > 0]
    return arities


def absolute(arities):
    abs_arities = [abs(a) for a in arities]
    return abs_arities


def lookuptable(table_name, **kwargs):
    stream = resource_stream(__name__, 'data/' + table_name + ".csv")
    df = pd.read_csv(stream)
    query = "&".join(("({}=={})".format(k, v) for k, v in kwargs.items()))
    df0 = df.query(query)
    if len(df0):
        data = df0.iloc[0].to_dict()
        lb, ub = data["lb"], data["ub"]
        return normalize_result(lb, ub)
    return None


def volume(dimensions, radius):
    return sum(prod(d) for d in combinations(dimensions, 2))
    

def max_size_forward(arities, distance=1):
    # require: arities list[int] all elements>=2
    # require: distance: int >=1
    arities = sorted(arities)
    n = len(arities)
    nd1 = n - distance + 1

    singleton_ub = prod(arities[:nd1])  # singleton bound
    if distance in [1, 2, n]:
        return singleton_ub

    min_arity = arities[0]
    max_arity = arities[-1]
    
    if min_arity == max_arity:
        result = lookuptable("qnd", arity=min_arity, repeat=n, distance=distance)
        if result is not None:
            return result
    
        if min_arity == 2 and 3 * distance > 2 * repeat:
            return 2
        
    if min_arity == 2 and max_arity == 3:
        repeat2 = arities.count(2)
        repeat3 = arities.count(3)
        result = lookuptable("23", repeat2=repeat2, repeat3=repeat3, distance=distance)
        if result is not None:
            return result

    # Hamming bound
    product = prod(arities)
    radius = (distance-1) // 2
    dimensions = [arity - 1 for arity in arities]
    hamming_ub = product / volume(dimensions, radius)

    # Plotkin bound
    inv_sum = sum(1. / arity for arity in arities)
    plotkin_ub = 1 / (1 - 1. / distance * (n - inv_sum))

    lb = 1  # trivial
    ub = min([singleton_ub, hamming_ub, plotkin_ub])
    return normalize_result(lb, ub)

    
def max_size_interactive(arities, correct=0, detect=0):
    # requires: arities[0]>=2, arities[-1]>=2, pos_count>d
    n = len(arities)
    if n == 3:  # +-+
        a, b, c = absolute(arities)
        return min([a, b * (c-1)])
    if n == 4:
        a, b, c, d = absolute(arities)
        if arities[1] < 0:  # +-++
            lb = min([a, b, max([c*(d-1), 2*d])])
            ub = min([a, b, pow(c, d)])
        else:  # ++-+
            lb = max([min([a, b*(c-1), d]), min([a, c, b*(d-1)]), min([a, b, (c-1)*(d-1)+1])])
            for k in range(2, min(c, d)):
                lb = max(lb, min([a, k*b, (c-k)*(d-k)]))
            ub = min([a, b*(c-1), b*(d-1)])
            for k in range(1, min(c, d)+1):
                ub = min(ub, max([(k-1)*b, (c-k)*(d-k)+k]))
        return normalize_result(lb, ub)
    return normalize_result(1, pos_prod)  # trivial


def max_size(arity=2, repeat=1, direction=1, correct=0, detect=None):
    """ Get the maximum size of the codes
    
    Parameters
    ----------
    arity: int | list[int]=2
    repeat: int=1
    direction: int | list[int]=1
    correct: int=0
    detect: Optional[int]=None
    
    Results
    ----
    size: int | range
    
    Examples
    --------
    from errcode import max_size
    print(max_size(arity=2, repeat=6, correct=4))
    print(max_size(arity=[5, -3, 4], detect=1))
    """
    arities, correct, detect = normalize_parameters(arity=arity, repeat=repeat, direction=direction, correct=correct, detect=detect)
    arities = trim(arities)
    pos_arities = filter_direction(arities, 1)
    n = len(arities)
    pos_n = len(pos_arities)
    d = correct + detect + 1
    pos_prod = prod(pos_arities)  # trivial upper bound
    if pos_n < d:
        return 1
    if d == 1:
        return pos_prod
    if n == pos_n: # forward
        result = max_size_forward(arities, distance=d)
    else: # interactive
        result = max_size_interactive(arities, correct=correct, detect=detect)
    if result is not None:
        return result
    return normalize_result(1, pos_prod)  # trivial
