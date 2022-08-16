import numpy as np
from scipy.optimize import curve_fit

def sigmoid(x, L ,x0, k, b):
    y = L / (1 + np.exp(-k*(x-x0))) + b
    return (y)

def rip_norm(matrix):
    '''
    script for finding average square norm with periodic boundary conditions
    assumes 4x4 matrix
    '''
    matrix = np.array(matrix)
    print(matrix)
    indices = np.asarray(np.where(matrix==1.0)).T
    #goes from (1,8,2) to (8,8,2)
    x = indices[np.newaxis,:] #this basically meshgrids a new axis
    y = indices[:,np.newaxis]
    dist = x-y #subtract x and y to find distance
    dist = dist - (np.round(dist/4))*4 #if distance is more than 2, the other way is shorter

    norm = np.linalg.norm(dist, axis = 2)
    norm = norm**2 #square so small differences are more apparent
    res = np.sum(norm)/2 #matrix is symmetric, so upper triangle is just half of the sum
    ones_matrix = np.ones((len(norm[0]), len(norm[1]))) #number of elements in upper triangle
    res = res/((ones_matrix.sum() - np.trace(ones_matrix))/2)
    print(res)

    #sum over øvre triangel i annen, del på 8
    return res

def test_rip_norm():
    a = np.array(([[0,0,0,0,],[0,1,1,0],[0,0,0,0],[0,0,0,0]]))
    assert rip_norm(a) ==1

def fit_sigmoid(load_curve, fig, axs, c = False):
    '''
    https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.curve_fit.html
    https://stackoverflow.com/questions/55725139/fit-sigmoid-function-s-shape-curve-to-data-using-python
    '''
    time = load_curve[:,0]
    fx = load_curve[:,1]

    #fitting sigmoid to selected interval.
    polfit_start_indx = (np.abs(time - 0.7)).argmin()
    polfit_stop_indx = (np.abs(time - 1.3)).argmin()
    #translation so it has same shape as load_curve
    polfit_data = np.array((time[polfit_start_indx:polfit_stop_indx],
                           fx[polfit_start_indx:polfit_stop_indx])).T


    #curve fit doesn't like nan. removing theese for now
    non_nan_mask = ~np.isnan(polfit_data[:,1])

    #https://stackoverflow.com/questions/55725139/fit-sigmoid-function-s-shape-curve-to-data-using-python
    time_nnan = polfit_data[non_nan_mask,0]
    load_curve_nnan = polfit_data[non_nan_mask,1]
    #this was [max(time_nnan), etc and worked.. website says ydata first
    p0 = [max(time_nnan), np.median(time_nnan),1,min(load_curve_nnan)] # this is an mandatory initial guess


    popt, pcov = curve_fit(sigmoid, time_nnan, load_curve_nnan,p0, method='dogbox')

    #max_rise = np.max(np.gradient(sigmoid(time_nnan, *popt))) this gives wrong values. idk

    #repeating selection and polyfit but this time fitting linear func to sigmoid midriff
    midriff = np.array((popt[1] - 0.05, popt[1] + 0.05))

    midriff_start_indx = (np.abs(time_nnan - midriff[0])).argmin()
    midriff_stop_indx = (np.abs(time_nnan - midriff[1])).argmin()

    polfit_data2 = np.array((time_nnan[midriff_start_indx:midriff_stop_indx],
                            load_curve_nnan[midriff_start_indx:midriff_stop_indx])).T


    rise, intersect = np.polyfit(polfit_data2[:,0], polfit_data2[:,1], 1)

    max_sig = sigmoid(time_nnan, *popt)[-1]
    
    if c: #gotta add . any () to this
        axs.plot(time_nnan, sigmoid(time_nnan, *popt), c= c, linewidth = 2)
    else:
        axs.plot(time_nnan, sigmoid(time_nnan, *popt))

    return max_sig


