def calculate_weighted_rating(ratings, weights):
    total_weight = sum(weights)
    weighted_sum = sum(rating * weight for rating, weight in zip(ratings, weights))
    return weighted_sum / total_weight

# Example ratings distribution
ratings = [5, 4, 3, 2, 1]
# Example number of ratings for each star
counts = [10002, 6020, 2505, 1040, 524]
# Example weights (could be based on recency, user reliability, etc.)
weights = [1.2, 1.1, 1.0, 0.9, 0.8]

weighted_ratings = [rating * count * weight for rating, count, weight in zip(ratings, counts, weights)]
total_weighted_count = sum(count * weight for count, weight in zip(counts, weights))

overall_rating = sum(weighted_ratings) / total_weighted_count

print(f"Overall rating: {overall_rating:.1f}")