import numpy as np

from nose.tools import assert_raises, assert_true, assert_false, raises

from datarray.datarray import Axis, DataArray
from datarray.stuple import *

d_arr = DataArray(np.random.randn(3, 2, 4, 2),
                  labels=('x', 'y', 'u', 'v'))

def test_a_stuple_is_a_tuple():
    s = stuple( (1,2,3,4) )
    yield assert_true, s == (1,2,3,4)

@raises(StupleSlicingError)
def test_slicing_exception1():
    axes = d_arr.axes
    # s_anon is not registered with an index, and so
    # one should not be able to slice it
    s_anon = stuple( ( slice(None), )*len(axes), axes=axes )
    s_anon[0]

@raises(StupleSlicingError)
def test_slicing_exception2():
    axes = d_arr.axes
    s_anon = stuple( ( slice(None), )*len(axes), axes=axes )
    s_x = s_anon.x[::2]
    # now, the x-axis has already been sliced, and cannot be sliced again
    s_x.x[0]

def test_slice_shapes():
    axes = d_arr.axes
    s_all = stuple( ( slice(None), )*len(axes), axes=axes )

    sub_arr = d_arr[ s_all.u[0].v[1] ]
    yield assert_true, sub_arr.shape == (3,2)

    dt = d_arr.T
    # have to recreate stuple slicer with refs to new Axis objects..
    # this will obviously be part of the DataArray construction later
    s_all = stuple( ( slice(None), )*len(axes), axes=dt.axes )

    sub_arr = dt[ s_all.u[0].v[1] ]
    yield assert_true, sub_arr.shape == (2,3)

def test_slice_op():
    axes = d_arr.axes
    s_all = stuple( ( slice(None), )*len(axes), axes=axes )

    sub_arr = d_arr[ s_all.u[0].v[1] ]
    yield assert_true, (sub_arr == d_arr[:,:,0,1]).all()

    sub_arr = d_arr[ s_all.x[::2].u[::-1] ]
    yield assert_true, (sub_arr == d_arr[::2,:,::-1,:]).all()
    

def test_stuple_slices_ndarray():
    # THIS FAILS, BUT WHY??
    axes = d_arr.axes
    s_all = stuple( ( slice(None), )*len(axes), axes=axes )

    try:
        b = (np.asarray(d_arr)[s_all]==np.asarray(d_arr)).all()
        yield assert_true, b
    except:
        yield assert_true, False, 'stuple does not slice a vanilla ndarray'
           
           
          