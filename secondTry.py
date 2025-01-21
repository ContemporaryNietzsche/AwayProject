import numpy as np
import matplotlib.pyplot as plt
import random

# Define parameters
num_trials = 8000
dot_range = (5, 25)
ratio_range = (1.2, 2.0)
learning_rate = 0.01
initial_ratio_range = (1.2, 2.0)  # Store initial ratio range for later use

# Initialize performance
performance = []

# Training loop
for trial in range(num_trials):
    # Generate two dot arrays with a random ratio
    num_dots1 = random.randint(*dot_range)
    ratio = random.uniform(*ratio_range)
    num_dots2 = int(num_dots1 * ratio)

    # Simulate user response (replace with actual user input)
    user_response = np.random.choice([0, 1]) 

    # Calculate feedback
    correct_response = 1 if num_dots1 < num_dots2 else 0
    feedback = 1 if user_response == correct_response else 0

    # Update performance
    performance.append(feedback)

    # Adjust difficulty (optional)
    if feedback == 1:
        ratio_range = (max(ratio_range[0] + learning_rate, 1.0), ratio_range[1] + learning_rate)
    else:
        ratio_range = (max(ratio_range[0] - learning_rate, 1.0), max(ratio_range[1] - learning_rate, initial_ratio_range[0]))

# Plot performance
plt.plot(performance)
plt.xlabel("Trial")
plt.ylabel("Performance (Accuracy)")
plt.title("ANS Training Performance")
plt.show()

# Generalization tests
# 1. Untrained locations (Simulate by randomly shifting dot array positions)
untrained_locations_performance = []
for trial in range(1000):  # Example: 1000 trials for generalization test
    # Generate dot arrays as before
    num_dots1 = random.randint(*dot_range)
    ratio = random.uniform(*initial_ratio_range)  # Use initial ratio range for generalization
    num_dots2 = int(num_dots1 * ratio)

    # Simulate presentation at a random location (simplified)
    location = np.random.randint(0, 4)  # 0: top-left, 1: top-right, 2: bottom-left, 3: bottom-right

    # Simulate user response
    user_response = np.random.choice([0, 1])

    # Calculate feedback
    correct_response = 1 if num_dots1 < num_dots2 else 0
    feedback = 1 if user_response == correct_response else 0

    untrained_locations_performance.append(feedback)

# 2. Enumeration task (Simulate by asking for the number of dots)
enumeration_performance = []
for trial in range(1000):
    # Generate dot array
    num_dots = random.randint(*dot_range)

    # Simulate user response
    user_enumeration = random.randint(num_dots - 2, num_dots + 2)  # Allow for some estimation error

    # Calculate feedback
    feedback = 1 if user_enumeration == num_dots else 0
    enumeration_performance.append(feedback)

# 3. Ratio comparison (Simulate with different ratio ranges)
ratio_comparison_performance = []
for trial in range(1000):
    # Generate dot arrays with a wider ratio range
    num_dots1 = random.randint(*dot_range)
    ratio = random.uniform(1.1, 2.5)  # Wider ratio range
    num_dots2 = int(num_dots1 * ratio)

    # Simulate user response
    user_response = np.random.choice([0, 1])

    # Calculate feedback
    correct_response = 1 if num_dots1 < num_dots2 else 0
    feedback = 1 if user_response == correct_response else 0

    ratio_comparison_performance.append(feedback)

# 4. Arithmetic (Simulate simple addition/subtraction)
arithmetic_performance = []
for trial in range(1000):
    # Generate simple arithmetic problem
    operand1 = random.randint(1, 10)
    operand2 = random.randint(1, 5)
    operator = random.choice(['+', '-'])

    if operator == '+':
        correct_answer = operand1 + operand2
    else:
        correct_answer = operand1 - operand2

    # Simulate user response
    user_answer = correct_answer + random.randint(-2, 2)  # Allow for some estimation error

    # Calculate feedback
    feedback = 1 if user_answer == correct_answer else 0
    arithmetic_performance.append(feedback)

# Analyze results
print("Mean training performance:", np.mean(performance))
print("Mean untrained locations performance:", np.mean(untrained_locations_performance))
print("Mean enumeration performance:", np.mean(enumeration_performance))
print("Mean ratio comparison performance:", np.mean(ratio_comparison_performance))
print("Mean arithmetic performance:", np.mean(arithmetic_performance))

# (Further analysis and statistical tests can be added here)