import numpy as np
import sys

def indices(n):
    """
    Finds a set of miller indices (hkl) which could satisfy n = h^2+k^2+l^2
    n : some integer which satisfies Legendre's three square theorem (accurate for the first 100 values)
    returns [h,k,l] for the given n
    """
    x = np.floor(n**(1/2))
    h = x
    k = x
    l = x
    while(h**2+k**2+l**2!=n):
        l-=1
        if(l<0):
           k-=1
           l=k
        if(k<0):
            h-=1
            k=h
            l=k
    return [int(h),int(k),int(l)]


def lattice_paramter(theta,wavelength,index):
    """
    determines the lattice parameter for some unknown material based on a given diffraction
    angles and corresponding miller index

    theta : half of the observed diffraction angle in degrees
    wavelength : at which the experiment was performed (angstrom)
    index : miller index of the corresponding peak

    returns the lattice parameter in angstroms
    """
    return wavelength/(2*np.sin(np.radians(theta)))*np.sum(np.power(index,2))**(1/2)


def main():
    #get the input diffraction values from command line
    try:
        thetas = [float(t) for t in sys.argv[1:]]
        thetas[0] #call to induce an index error if the list is empty
    except ValueError: #make sure the given values are only angles
        raise TypeError("Expected 2 Theta values as integers or floats")
    except IndexError: #in case no angles provided
        raise TypeError("Missing required diffraction angles")
    
    #convert to sin squared values
    sins = np.array([np.sin(np.radians(t/2))**2 for t in thetas])
    #use the ratios against the first sin squared to determine miller indices
    ratios = np.round(sins/sins[0])
    print("initial ratios:",ratios)

    #first 100 values which cannot be generated by the sum of three squares (Legendre's three square theorem)
    threesquares = [4**a*(8*b+7) for a in range(0,10) for b in range(0,10)]
    #check if any of the ratios are invalid and try higher order diffractions
    i = 1
    while (not set(ratios).isdisjoint(threesquares)):
        absence = list(set(ratios)&set(threesquares))
        index = np.where(ratios==absence[0])[0]
        i+=1
        ratios*=i
    inds = [indices(r) for r in ratios]

    #determine the lattice parameter and its uncertainty
    a = [lattice_paramter(thetas[i]/2,0.41,inds[i]) for i in range(0,len(inds))]
    #half the range
    uncertainty = round(np.ptp(a)/2,3)
    #average of all given vals
    a = round(np.mean(a),3)

    print("Final ratios:",ratios)
    print("Miller indices:",inds)
    print("Absences:",index+1)
    print(f"Lattice parameter (angstroms): {a}+/-{uncertainty}")
    
if __name__ == "__main__":
    main()



   
    
