import numpy as np

np.random.seed(420)

mean = 10
std_dev = 1
sample_size = 8

# calcualtes the bootstrap confidence interval by generaating values with replacement from the data, calculating means and percentiles
# and then calculating the lower and upper bounds of the confidence interval
def bootstrap_confidence_interval(data, alpha=0.95, num_resamples=10000):
    # Generate values with replacement from the data
    resamples = np.random.choice(data, size=(num_resamples, len(data)), replace=True)
    # Calculate the means
    sample_means = np.mean(resamples, axis=1)
    #  the lower and upper percentiles for the confidence interval
    lower_percentile = (1 - alpha) / 2
    upper_percentile = 1 - lower_percentile
    # Calculate the lower and upper bounds of the confidence interval
    lower_bound = np.percentile(sample_means, lower_percentile * 100)
    upper_bound = np.percentile(sample_means, upper_percentile * 100)
    # confidence interval
    return lower_bound, upper_bound


# this entire process was in the book I mentioned in the meeting.
"""The book is called Design of Observational Studies by Paul R. Rosenbaum."""
# the processes are explained step by step as from the book
def signed_rank_confidence_interval(data, alpha=0.95):
    # data in ascending order
    data = np.sort(data)
    # Calculate ranks (mentioned in the book)
    ranks = np.arange(1, len(data) + 1)
    # signed ranks based on the median
    signed_ranks = np.where(data > np.median(data), ranks, -ranks)
    # find the means
    sample_mean = np.mean(data)
    # sum up ranks
    sum_ranks = np.sum(signed_ranks)
    # error just in case
    se = np.sqrt((len(data) * (len(data) + 1) * (2 * len(data) + 1)) / 6)
    #  sample standard values
    z_alpha = np.abs(np.percentile(np.random.normal(0, 1, 10000), (1 - alpha / 2) * 100))
    # Calculate the upper and lower bound
    lower_bound = sample_mean - (z_alpha * se / np.sqrt(24))
    upper_bound = sample_mean + (z_alpha * se / np.sqrt(24))
    return lower_bound, upper_bound

# driver function
def driver(random_number_generator, max_iterations=20):
    for _ in range(max_iterations):
        data = random_number_generator()  # init data
        old_data = data.copy()  # Save the old data
        # Initialize
        converged = False
        iteration = 1
        while not converged:
            # Calculate a bootstrap interval
            conf_interval = bootstrap_confidence_interval(data)
            sample_mean = np.mean(data)
            # 10% interval around the mean
            sample_mean_10_percent_interval = [sample_mean - 0.1 * sample_mean, sample_mean + 0.1 * sample_mean]
            # Check if the bootstrap interval is within the 10% mean interval. Mentioned in meeting?
            ci_within_10_percent_interval = (
                    sample_mean_10_percent_interval[0] <= conf_interval[0]
                    and sample_mean_10_percent_interval[1] >= conf_interval[1]
            )
            # calc the signed rank interval
            signed_rank_conf_interval = signed_rank_confidence_interval(data)
            # If the bootstrap and signed rank intervals are within the 10% mean interval data converges
            if ci_within_10_percent_interval:
                converged = True
            else:
                # If not converged, increment the iteration count and add 8 more values to the old data
                iteration += 1
                additional_data = random_number_generator()  # Get 8 more values
                old_data = np.concatenate((old_data, additional_data))
                data = old_data  # Use the extended data

        print(f"Iteration {iteration}:")
        print("Sample:", data)
        print("Bootstrap 95% Confidence Interval (Normal):", conf_interval)
        print("Sample Mean (Normal):", sample_mean)
        print("10% Mean Interval (Normal):", sample_mean_10_percent_interval)
        print("CI Interval within 10% Interval (Normal):", ci_within_10_percent_interval)
        print("Signed Rank 95% Confidence Interval:", signed_rank_conf_interval)
        print("")

# random number generator functions for normal and uniform distributions
def random_number_generator_normal():
    return np.random.normal(mean, std_dev, sample_size)

def random_number_generator_uniform():
    return np.random.uniform(0, 20, sample_size)

# Call the driver function for both distributions
print("Results for Normal Distribution:")
driver(random_number_generator_normal)

print("Results for Uniform Distribution:")
driver(random_number_generator_uniform)