# -*- coding: utf-8 -*-
import numpy as np
import csv
from collections import defaultdict

# https://blog.quakelogic.net/understanding-signal-to-noise-ratio-snr-and-its-importance-in-seismic-and-structural-health-monitoring/#:~:text=SNR%20=%2010%20%E2%8B%85%20log%20%E2%81%A1%20(%20P,Data%20is%20likely%20unusable%20without%20significant%20noise%20reduction.
def calculate_snr(filename):
    signal = 0
    noise = 0
    combinations = []

    violation_counts = defaultdict(int)


    with open(filename, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            combinations.append(row['items'])

    # check each combination to see if it complies with the rule
    for combo in combinations:
        categories = combo.split(', ')
        valid = True

        # Rule 1: Food types should not be repeated
        if len(categories) != len(set(categories)):
            violation_counts['Rule1'] += 1
            valid = False

        # Rule 2: Combination of Meat/Seafood + Vegetables (Fruit_Cup/Salad/Vegetable)
        meat_seafood = {'Meat', 'Seafood'}
        vegetables = {'Salad', 'Fruit_cup', 'Vegetable'}
        has_meat = any(c in meat_seafood for c in categories)
        has_veg = any(c in vegetables for c in categories)
        if (has_meat or has_veg):
            if not (has_meat and has_veg):
                violation_counts['Rule2'] += 1
                valid = False

        # Rule 3: No more than one staple food (Rice/Noodle)
        staple_count = sum(1 for c in categories if c in ['Rice', 'Noodle'])
        if staple_count > 1:
            violation_counts['Rule3'] += 1
            valid = False

        # Rule 4: No more than one drink in a combination
        drink_count = sum(1 for c in categories if c == 'Drink')
        if drink_count > 1:
            violation_counts['Rule4'] += 1
            valid = False

        # Rule 5: Sandwich and Warp should not appear in the same combination
        if 'Sandwich' in categories and 'Warp' in categories:
            violation_counts['Rule5'] += 1
            valid = False

        # # Rule 6? Meat and Seafood should not appear in the same combination
        # if 'Meat' in categories and 'Seafood' in categories:
        #     violation_counts['Rule6'] += 1
        #     valid = False

        if valid:
            signal += 1
        else:
            noise += 1

    # Calculate SNR
    snr = 10 * np.log10(signal/noise)

    print(f"Filename    : {filename}")
    print(f"Total Data  : {len(combinations)} ")
    print(f"Signal Data : {signal} ")
    print(f"Noise Data  : {noise} ")
    print(f"Signal to Noise Ratio: {snr:.2f} dB\n") # The higher the dB, the better
    print("Noise distribution:")
    for rule, count in violation_counts.items():
        print(f"{rule}: {count} ({count/len(combinations):.2%})")
    print("\nNoise Ratio: {:.2%}".format(1-(signal/len(combinations))))

if __name__ == "__main__":
    csv_file = "fine_food_combinations.csv"
    calculate_snr(csv_file)
