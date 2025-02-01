import pygame
import random
import sys
import numpy as np
import uuid
import scipy
import statsmodels.api as sm

# Initialize pygame
pygame.init()

# Set up display
width = pygame.display.Info().current_w
height = pygame.display.Info().current_h
radius_min, radius_max = 202, 300
num_trials = 14 # 32
GRAY = (169, 169, 169)

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Approximate Number System Game")

# Define colors
blue = (0, 0, 255)
yellow = (255, 255, 0)

# Function to check for collision
# new_dot = (color, x pos, y pos, radius)
# existing_dots = [dot, dot...]
def check_collide(new_dot, existing_dots):
    
    # checks for edge collision
    if new_dot[1] + new_dot[3] > width or new_dot[1] - new_dot[3] < 0:
        return True
    if new_dot[2] + new_dot[3] > height or new_dot[2] - new_dot[3] < 0:
        return True

    for _, x, y, radius in existing_dots:
        distance = ((new_dot[1] - x) ** 2 + (new_dot[2] - y) ** 2) ** .5
        # if the distance between the two circles is greater than the two radius + tolerance level
        if distance < radius + new_dot[3] + .1:
            return True
    return False

# Function to create ratio pools
# arrays are populated with tuples in the form of (yellow_dots, blue_dots)
# generates ratio sets and pull from b/y
# 50% yellow answers, 50% blue answers (non alternating using random.shuffle)
def generate_vals_from_ratio(array_size):
    blue_dot_favored_base = [(1, 1.2), (1, 1.3), (1, 1.5)]
    yellow_dot_favored_base = []
    out = []

    # appends inverse of blue_dot_favored
    for x, y in blue_dot_favored_base:
        yellow_dot_favored_base.append((y, x))
        
    blue_dot_favored = blue_dot_favored_base.copy()
    yellow_dot_favored = yellow_dot_favored_base.copy()
    
    for _ in range(0, array_size, 2):
        # https://stackoverflow.com/questions/1781970/multiplying-a-tuple-by-a-scalar
        # caution, can generate excess fat in floating point nums in tuple. unsure effect
        if len(blue_dot_favored) == 0:
            blue_dot_favored = blue_dot_favored_base.copy()
        if len(blue_dot_favored) == 1:
            temp = blue_dot_favored.pop(0)
        else:
            temp = blue_dot_favored.pop(random.randint(0, len(blue_dot_favored) - 1))
        
        
        rand_scalar = random.randint(10, 20)
        out.append(tuple(round(z * rand_scalar) for z in temp))

        if len(yellow_dot_favored) == 0:
            yellow_dot_favored = yellow_dot_favored_base.copy()
        if len(yellow_dot_favored) == 1:
            temp = yellow_dot_favored.pop(0)
        else:
            temp = yellow_dot_favored.pop(random.randint(0, len(yellow_dot_favored) - 1))
        
            
        rand_scalar = random.randint(10, 20)
        out.append(tuple(round(z * rand_scalar) for z in temp))

    random.shuffle(out)
    return out

# Function to create radius list
def generate_areas_from_ratio(array_size):
    out = []
    for _ in range(array_size):
        out.append(random.randint(radius_min, radius_max))
    return out

# x must be positive
# generates x numbers that sum to y
def generate_numbers(x, y, mean_radius=50, radius_deviation=10):
    # Generate radii following a normal distribution
    radii = np.random.normal(mean_radius, radius_deviation, x)

    # Clip radii to be non-negative
    radii = np.clip(radii, 0, None)

    # Normalize radii so that their sum is approximately y
    radii_sum = np.sum(radii)
    radii = (radii / radii_sum) * y

    # Round the radii to integers
    radii = np.round(radii).astype(int)

    # Ensure the sum is exactly y by adjusting the last radius
    radii[-1] += y - np.sum(radii)

    return radii.tolist()

# Function to generate random dots
# uses a normal distribution to cluster towards center of screen
def generate_dots(blue_dots, yellow_dots, dot_area_arr):
    dots = []
    count = 0
    for _ in range(blue_dots):
        x = int(np.random.normal(width / 2, width / 6))  # Mean = width/2, Std = width/6
        y = int(np.random.normal(height / 2, height / 6))  # Mean = height/2, Std = height/6
        new_dot = (blue, x, y, dot_area_arr[count])
        while check_collide(new_dot, dots):
            x = int(np.random.normal(width / 2, width / 6))
            y = int(np.random.normal(height / 2, height / 6))
            new_dot = (blue, x, y, dot_area_arr[count])
        dots.append(new_dot)
        count += 1

    for _ in range(yellow_dots):
        x = int(np.random.normal(width / 2, width / 6))
        y = int(np.random.normal(height / 2, height / 6))
        new_dot = (yellow, x, y, dot_area_arr[count])
        while check_collide(new_dot, dots):
            x = int(np.random.normal(width / 2, width / 6))
            y = int(np.random.normal(height / 2, height / 6))
            new_dot = (yellow, x, y, dot_area_arr[count])
        dots.append(new_dot)
        count += 1

    return dots

# Function to draw dots on the screen
def draw_dots(dots):
    for color, x, y, radius in dots:
        pygame.draw.circle(screen, color, (x, y), radius)

# sum in position
def sum_in_position(array):
    out = []
    for x, y in array:
        out.append(x + y)
    return out

# Function to draw cross to the middle of the screen
def draw_cross():
    cross_horizontal = pygame.Rect(0, 0, 3, 25)
    cross_horizontal.center = (width / 2, height / 2)

    cross_vertical = pygame.Rect(0, 0, 25, 3)
    cross_vertical.center = (width / 2, height / 2)

    pygame.draw.rect(screen, (0, 0, 0), cross_vertical)
    pygame.draw.rect(screen, (0, 0, 0), cross_horizontal)

# Main game loop
def main():
    clock = pygame.time.Clock()

    # telemetry here:
    # https://stackoverflow.com/questions/2961509/python-how-to-create-a-unique-file-name
    # could replace with datetime, or name specifier

    
    # COMMENTED TO NOT CREATE NEW FILE ******************************************************************************************************************************************
    # filename = uuid.uuid4().hex + ".txt"
    # f = open(filename, "x")
    # ***************************************************************************************************************************************************************************


    correct_guesses = []
    actual_ratio = []

    trial = generate_vals_from_ratio(num_trials)
    areas = sum_in_position(trial)
    radii = generate_areas_from_ratio(num_trials)
    res = scipy.stats.pearsonr(areas, radii)
    print(res)
    while res[1] < .1 or abs(res[0]) > .1:
        trial = generate_vals_from_ratio(num_trials)
        radii = generate_areas_from_ratio(num_trials)
        areas = sum_in_position(trial)
        res = scipy.stats.pearsonr(areas, radii)
        print(res)

    # number of iterations is numtrials, +1 if x is odd (to even it)
    for yellow_blue, total_radius in zip(trial, radii):
        # sorts yellow_blue to reverse ascending order (larger value first)
        Sort = sorted(yellow_blue, reverse=True)
        print(Sort)
        actual_ratio.append(Sort[0] / Sort[1])

        # palate cleanse??? focus
        screen.fill(GRAY)
        draw_cross()
        pygame.display.update()
        pygame.time.wait(1000)

        # generate dots 
        screen.fill(GRAY)
        
        # changeable here for total colored area
        # total_radius = random.randint(radius_min, radius_max)
        dot_area_arr = generate_numbers(yellow_blue[1], total_radius)
        dot_area_arr += generate_numbers(yellow_blue[0], total_radius)

        dots = generate_dots(yellow_blue[1], yellow_blue[0], dot_area_arr)
        print("yellow" + str(yellow_blue[0]))
        print("blue" + str(yellow_blue[1]))

        # apply dots
        draw_dots(dots)
        pygame.display.flip()
        pygame.time.wait(1000)

        # clean
        screen.fill(GRAY)
        pygame.display.flip()

        # Wait for user input
        waiting_for_input = True
        while waiting_for_input:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_b or event.key == pygame.K_y:
                        # Valid key press
                        if event.key == pygame.K_b:
                            print("blue selected")
                            if yellow_blue[1] > yellow_blue[0]:
                                print("correct")
                                correct_guesses.append(1)
                            else:
                                correct_guesses.append(0)
                        elif event.key == pygame.K_y:
                            print("yellow selected")
                            if yellow_blue[1] < yellow_blue[0]:
                                print("correct")
                                correct_guesses.append(1)
                            else:
                                correct_guesses.append(0)
                        
                        waiting_for_input = False
                    else:
                        # Invalid key press
                        print("Invalid key. Please press 'b' for blue or 'y' for yellow.")

        clock.tick(30)

    # COMMENTED TO NOT CREATE NEW FILE ******************************************************************************************************************************************
    # f.write("Correct Guesses: " + str(sum(correct_guesses)) + "\nTotal Guesses: " + str(num_trials))
    # ***************************************************************************************************************************************************************************
    
    # Fit logistic function to performance
    x = actual_ratio[:len(correct_guesses)]
    y = correct_guesses
    x = sm.add_constant(x)  # Add a constant to the predictor
    model = sm.GLM(y, x, family=sm.families.Binomial())
    result = model.fit()

    # Predict values up to two times tested values
    predictX2 = np.arange(1, max(actual_ratio) * 2, 0.001)
    x_predict = sm.add_constant(predictX2)
    yfit3 = result.predict(x_predict)

    # Convert predicted probabilities to percentages
    percent2 = np.round(yfit3 * 100)

    # Concatenate x and y values
    x2_y2 = np.column_stack((predictX2, percent2))

    # Calculate the threshold for 79%
    p_thresh79 = np.mean(x2_y2[x2_y2[:, 1] == 79], axis=0)

    print("79% Ratio" + str(p_thresh79))

    # COMMENTED TO NOT CREATE NEW FILE ******************************************************************************************************************************************
    # f.write("79% Threshold: " + str(p_thresh79))
    # ***************************************************************************************************************************************************************************


if __name__ == "__main__":
    main()

# enumeration task
