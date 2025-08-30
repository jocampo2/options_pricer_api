import json
import random

# Function to generate a single random option
def generate_random_option():
    return {
        "spot": round(random.uniform(50, 150), 2),
        "strike": round(random.uniform(50, 150), 2),
        "maturity": round(random.uniform(0.1, 2.0), 2),        # in years
        "interest_rate": round(random.uniform(0.01, 0.1), 4),  # 1% - 10%
        "volatility": round(random.uniform(0.1, 0.5), 2)       # 10% - 50%
    }

# Generate a list of N random options
N = 100000
random_options = [generate_random_option() for _ in range(N)]

# Save to JSON file
with open("examples/random_options_100000.json", "w") as f:
    json.dump(random_options, f, indent=2)

print(f"Saved {N} random options to examples/random_options.json")
