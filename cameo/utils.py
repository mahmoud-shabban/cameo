import cv2 
import numpy as np
import scipy.interpolate


def create_curve_func(points:list):
    '''return a function derived from control points.'''

    if points is None:
        return None
    
    num_points = len(points)

    if num_points < 2:
        return None
    
    xs, ys = zip(*points)

    if num_points < 3:
        kind = 'linear'
    elif num_points < 4:
        kind = 'quadratic'
    else:
        kind = 'cubic'
    
    return scipy.interpolate.interp1d(xs, ys, kind, bounds_error=False)

def create_lookup_array(func, length = 256):
    '''
        return a lookup for whole-number inputs to a function
        the lookup values are clamped to [0, lenght -1]
    '''
    if func is None:
        return None
    
    lookup_array = np.empty(length)
    
    i = 0
    while i < length:
        func_i = func(i)
        lookup_array[i] = min(max(0, func_i), length - 1)
        i += 1
    return lookup_array

def apply_lookup_array(lookup_array, src, dest):
    '''
    map a source to destination using a lookup
    '''

    if lookup_array is None:
        return
    dest[:] = lookup_array[src]


def create_composite_function(func_0, func_1):
    '''return a composite of two functions'''

    if func_0 is None:
        return func_1
    if func_1 is None:
        return func_0
    
    return lambda x: func_0(func_1(x))