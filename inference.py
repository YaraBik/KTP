import numpy
import scipy.stats          # makes use of scipy!
from matplotlib import pyplot

# Posterior = (likelihood * prior) / evidence --> denominator usually omitted


def mean():
    x = []  # answers will be put in here as data or "evidence"
    # sigma is the standard deviation - not really sure how to implement this in our application.
    # We probably would need ask Sieta for specific numbers?
    # standard deviation can't be 0, so we avoid having it as a candidate
    burnout_standard_deviation = 0.2
    sigma = 0.2
    initial_mu = 0

    # our mean (code): -2 for burnout, 0 stress, +2 healthy? 1000 iterations/tests
    mu_candidates = numpy.linspace(-2, 2, 1000)

    def mean_posterior(mu, sigma, x):
        mu_prior = scipy.stats.norm.logpdf(mu, initial_mu, burnout_standard_deviation * 2)
        return mu_prior + scipy.stats.norm.logpdf(x, mu, sigma).sum()

    def compute_mean_posteriors(mu_candidates, sigma, x):
        for mu in mu_candidates:
            yield mean_posterior(mu, sigma, x)

    mean_posteriors = list(compute_mean_posteriors(mu_candidates, sigma, x))

    print('Most likely disease code: %.2f' % mu_candidates[numpy.argmax(mean_posteriors)])

    pyplot.plot(mu_candidates, numpy.exp(mean_posteriors))
    pyplot.xlabel('Mean disease code')
    pyplot.ylabel('Probability')
    pyplot.title('Posterior of the mean of the disease code');

    return mu_candidates  # does this work like this? Only return one mean value?


# not sure if we really need to figure out our standard deviation through Bayes.
# Nevertheless, we can use the same methods
def standard_deviation():

    x = []  # answers will be put in here as data or "evidence"
    # range to figure out the proper standard deviation
    # standard deviation can't be 0, so we avoid having it as a candidate
    min_sigma = .01
    max_sigma = 5.
    mu = mean()

    # to figure out a fitting standard deviation value with 1000 iterations
    sigma_candidates = numpy.linspace(min_sigma, max_sigma, 1000)

    def sd_posterior(mu, sigma, x):
        # compute the prior with standard deviations
        # to avoid very small probabilities, use logs instead
        sigma_prior = scipy.stats.uniform.logpdf(sigma, min_sigma, max_sigma)
        return sigma_prior + scipy.stats.norm.logpdf(x, mu, sigma).sum()

    def compute_sd_posteriors(mu, sigma_candidates, x):
        # compute posterior
        for sigma in sigma_candidates:
            yield sd_posterior(mu, sigma, x)

    sd_posteriors = list(compute_sd_posteriors(mu, sigma_candidates, x))

    print('Most likely standard deviation for disease: %.2f' % sigma_candidates[numpy.argmax(sd_posteriors)])

    pyplot.plot(sigma_candidates, numpy.exp(sd_posteriors))
    pyplot.xlabel('disease standard deviation')
    pyplot.ylabel('Probability')
    pyplot.title('Posterior of the disease standard deviation');