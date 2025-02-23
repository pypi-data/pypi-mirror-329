import numpy as np

taxBrackets = np.array(
   [ [9325, 37950, 91900, 191650, 416700, 418400, 9999999],
     [18650, 75900, 153100, 233350, 416700, 470700, 9999999],
   ])

# These are speculated.
taxBrackets2 = np.array(
    [
        [11850, 48200, 116700, 243400, 529200, 531400, 9999999],
        [23700, 96400, 194400, 296350, 529200, 596900, 9999999],
    ]
)
brackets = 1.3054 * taxBrackets
print(brackets)

stdDeduction = np.array([6350, 12700])
std = 1.3054 * stdDeduction
print(std)
