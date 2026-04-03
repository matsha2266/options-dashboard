import numpy as np
from scipy.stats import norm

def d1(S,K,T,r,sigma):
    return (np.log(S/K)+(r+0.5*sigma**2)*T)/(sigma*np.sqrt(T))

def d2(S,K,T,r,sigma):
    return d1(S,K,T,r,sigma) - sigma*np.sqrt(T)

def call_price(S,K,T,r,sigma):
    return S*norm.cdf(d1(S,K,T,r,sigma)) - K*np.exp(-r*T)*norm.cdf(d2(S,K,T,r,sigma))

def delta(S,K,T,r,sigma):
    return norm.cdf(d1(S,K,T,r,sigma))

def gamma(S,K,T,r,sigma):
    return norm.pdf(d1(S,K,T,r,sigma))/(S*sigma*np.sqrt(T))

def vega(S,K,T,r,sigma):
    return S*norm.pdf(d1(S,K,T,r,sigma))*np.sqrt(T)
