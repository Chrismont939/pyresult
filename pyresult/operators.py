# -*- coding: utf-8 -*-
'''Result operators'''

from toolz import curry

from pyresult.result import (
    OK,
    ERROR,
    VALUE_IDX,
    STATUS_IDX,
    ok,
    error,
    result,
    is_ok,
    is_error,
    value
)

@curry
def errmap(func, res):
    '''Transform error with `func`.

    errmap: (x -> y) -> Result a x -> Result a y
    '''
    return error(func(res[VALUE_IDX])) if is_error(res) else res


@curry
def rmap(func, res):
    '''Map `func` to result `res`

    rmap: (a -> value) -> Result a -> Result value
    '''
    return ok(func(res[VALUE_IDX])) if is_ok(res) else res


@curry
def and_then(func, res):
    '''Chain together a sequence of computations that may fail.

    and_then: (a -> Result b x) -> Result a x -> Result b x
    '''
    return result(func(res[VALUE_IDX])) if is_ok(res) else res


@curry
def and_else(func, res):
    '''When `res` is error, then call `func` with it

    and_else: (x -> Result b x) -> Result a x -> Result a x
    '''
    return result(func(res[VALUE_IDX])) if is_error(res) else res


@curry
def fold(res):
    ''' List results is decomposited into list of results values
    and list of result errors.

    fold: (List Result a x) -> Result (List a) (List x)
    '''
    len_res = len(res)
    val = [None]*len_res
    err = [None]*len_res

    for i, e in enumerate(res):
        if is_ok(e):
            val[i] = e[VALUE_IDX]
        else:
            err[i] = e[VALUE_IDX]

    if None in val:
        return error(err)
    else:
        return ok(val)


def resolve(res):
    '''Flatten nested results

    resolve: Result (Result a x) x -> Result a x
    '''
    return res if is_error(res) else result(res[VALUE_IDX])
