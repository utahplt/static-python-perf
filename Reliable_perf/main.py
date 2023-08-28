import numpy as np

np.random.seed(42)
mean = 10
std_dev = 1
sample_size = 8
normal_sample = np.random.normal(mean, std_dev, sample_size)
uniform_sample = np.random.uniform(0, 20, sample_size)

def bootstrap_confidence_interval(data, alpha=0.95, num_resamples=10000):
    resamples = np.random.choice(data, size=(num_resamples, len(data)), replace=True)
    sample_means = np.mean(resamples, axis=1)
    lower_percentile = (1 - alpha) / 2
    upper_percentile = 1 - lower_percentile
    lower_bound = np.percentile(sample_means, lower_percentile * 100)
    upper_bound = np.percentile(sample_means, upper_percentile * 100)
    return lower_bound, upper_bound

# Normal
conf_interval_normal = bootstrap_confidence_interval(normal_sample)
sample_mean_normal = np.mean(normal_sample)
sample_mean_10_percent_interval_normal = [sample_mean_normal - 0.1 * sample_mean_normal, sample_mean_normal + 0.1 * sample_mean_normal]
ci_within_10_percent_interval_normal = sample_mean_10_percent_interval_normal[0] <= conf_interval_normal[0] and sample_mean_10_percent_interval_normal[1] >= conf_interval_normal[1]

# Uniform
conf_interval_uniform = bootstrap_confidence_interval(uniform_sample)
sample_mean_uniform = np.mean(uniform_sample)
sample_mean_10_percent_interval_uniform = [sample_mean_uniform - 0.1 * sample_mean_uniform, sample_mean_uniform + 0.1 * sample_mean_uniform]
ci_within_10_percent_interval_uniform = sample_mean_10_percent_interval_uniform[0] <= conf_interval_uniform[0] and sample_mean_10_percent_interval_uniform[1] >= conf_interval_uniform[1]

print("Normal Sample:", normal_sample)
print("Normal 95% Confidence Interval:", conf_interval_normal)
print("Normal Sample Mean:", sample_mean_normal)
print("Normal 10% Mean Interval:", sample_mean_10_percent_interval_normal)
print("Normal CI Interval within 10% Interval:", ci_within_10_percent_interval_normal)
print("")

print("Uniform Sample:", uniform_sample)
print("Uniform 95% Confidence Interval:", conf_interval_uniform)
print("Uniform Sample Mean:", sample_mean_uniform)
print("Uniform 10% Mean Interval:", sample_mean_10_percent_interval_uniform)
print("Uniform CI Interval within 10% Interval:", ci_within_10_percent_interval_uniform)
