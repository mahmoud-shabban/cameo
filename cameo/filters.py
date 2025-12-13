import cv2 
import numpy as np
import utils


def stroke_edges(src, dest, blurKsize: int = 5, edgeKsize: int = 5):
    if blurKsize >= 3:
        blurredSrc = cv2.medianBlur(src, blurKsize)
        graySrc = cv2.cvtColor(blurredSrc, cv2.COLOR_BGR2GRAY)
    else:
        graySrc = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
        cv2.Laplacian(graySrc, cv2.CV_8U, graySrc, ksize=edgeKsize)
    
    normalized_inverse_alpha = (1.0 / 255) * (255 - graySrc)
    
    channels = cv2.split(src)
    for channel in channels:
        channel[:] = channel * normalized_inverse_alpha
        cv2.merge(channels, dest)

class VConvolutionFilter(object):
    '''A filter that applies a convolution to V (or all BGR).'''
    def __init__(self, kernel):
        self._kernel = kernel
    
    def apply(self, src, dest):
        '''apply the filter with a BGR or gray src/dest'''
        cv2.filter2D(src, -1, self._kernel, dest)
class SharpenFilter(VConvolutionFilter):
    '''A sharpen filter with a 1-pixel radius'''
    def __init__(self):
        kernel = np.array([
            [-1, -1, -1],
            [-1,9,-1],
            [-1,-1,-1]
        ])

        super().__init__(kernel)

class BlurFilter(VConvolutionFilter):
    '''A blurr filter with a 2-pixel radius'''
    def __init__(self):
        kernel = np.array([
            [.04,.04, .04, .04, .04],
            [.04,.04, .04, .04,.04],
            [.04,.04, .04, .04,.04],
            [.04,.04, .04, .04,.04],
            [.04,.04, .04, .04,.04]
        ])
        super().__init__(kernel)

class EmbossFilter(VConvolutionFilter):
    '''Ann emboss filter with a 1-pixel radius'''
    def __init__(self, kernel):
        kernel = np.array([
            [-2, -1,0],
            [-1,1,1],
            [0,1,2]
        ])
        super().__init__(kernel)

class VFuncFilter(object):
    '''a filter that applies a function to V(value) (or all of BGR)'''
    def __init__(self, v_func = None, dtype = np.uint8):
        length = np.iinfo(dtype).max + 1
        self._vLookup_array = utils.create_lookup_array(v_func, length)
    
    def apply(self, src, dest):
        '''apply the filter with a BGR or gray src/dest'''
        src_flat_view = np.ravel(src)
        dest_flat_view = np.ravel(dest)

        utils.apply_lookup_array(self._vLookup_array, src_flat_view, dest_flat_view)

class VCurveFilter(VFuncFilter):
    '''a filter that applies a curve to V (value) (or all of BGR)'''
    def __init__(self, vPoints, dtype=np.uint8):
        super().__init__(utils.create_curve_func(vPoints), dtype)

class BGRFuncFilter(object):
    '''a filter that applies different functions to each BGR'''
    def __init__(self,
                 vFunc = None,
                 bFunc = None,
                 gFunc = None,
                 rFunc = None,
                 dtype = np.uint8):
        length = np.iinfo(dtype).max + 1
        self._bLookup_array = utils.create_lookup_array(
            utils.create_composite_function(bFunc, vFunc),
            length
        )

        self._gLookup_array = utils.create_lookup_array(
            utils.create_composite_function(gFunc, vFunc),
            length
        )

        self._rLookup_array = utils.create_lookup_array(
            utils.create_composite_function(rFunc, vFunc),
            length
        )

    def apply(self, src, dest):
        '''apply the filter with a BGR src/dest'''
        b,g,r = cv2.split(src)

        utils.apply_lookup_array(self._bLookup_array, b, b)
        utils.apply_lookup_array(self._gLookup_array, g, g)
        utils.apply_lookup_array(self._rLookup_array, r,r)

        cv2.merge([b,g,r], dest)

class BGRCurveFilter(BGRFuncFilter):
    '''a filter that applies different curves to each BGR'''
    def __init__(self, vPoints=None, bPoints = None, gPoints=None, rPoints=None, dtype=np.uint8):
        super().__init__(
            utils.create_curve_func(vPoints),
            utils.create_curve_func(bPoints),
            utils.create_curve_func(gPoints),
            utils.create_curve_func(rPoints),
            dtype)
        
class BGRPortraCurveFilter(BGRCurveFilter):
    '''a filter that applies portra-like curves to BGR'''
    def __init__(self, dtype=np.uint8):

        super().__init__(
            vPoints=[(0,0), (23,20),(157,173),(255,255)],
            bPoints=[(0,0),(41,46),(231,228),(255,255)],
            gPoints=[(0,0),(52,47),(189,196),(255,255)],
            rPoints=[(0,0),(69,69),(213,218),(255,255)],
            dtype=dtype)
        
class BGRProviaFilter(BGRCurveFilter):
    '''a filter that applier Provia-like curves to BGR'''
    def __init__(self, dtype=np.uint8):
        super().__init__(
            bPoints=[(0,0),(35,25),(205,227),(255,255)],
            gPoints=[(0,0),(27,21),(196,207),(255,255)],
            rPoints=[(0,0),(59,54),(202,210),(255,255)],
            dtype=dtype)
        
class BGRVelviaCurveFilter(BGRCurveFilter):
    '''a filter that applies Velvia-like curve to BGR'''

    def __init__(self, dtype=np.uint8):
        super().__init__(
            vPoints=[(0,0),(128,118),(221,215),(255,255)],
            bPoints=[(0,0),(25,21),(122,153),(255,255)],
            gPoints=[(0,0),(25,21),(95,102),(255,255)],
            rPoints=[(0,0),(41,28),(183,209),(255,255)],
            dtype=dtype)
        
class BGRCrossProcessCurveFilter(BGRCurveFilter):
    '''a filter that applies cross-process-like curves to BGR'''
    def __init__(self,dtype=np.uint8):
        super().__init__(
            bPoints=[(0,20),(255,235)],
            gPoints=[(0,0),(56,39),(208,226),(255,255)],
            rPoints=[(0,0),(56,22),(211,255),(255,255)],
            dtype=dtype)