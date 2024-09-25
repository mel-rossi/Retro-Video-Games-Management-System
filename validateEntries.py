# Validation & Valid Generation methods 
import pandas as pd1
 
def generateRentalID():
    # Read CSV into DataFrame
    df = pd1.read_csv("Inventory/Rentals.csv")

    for rentalID in df['RentalID']:
        pass

    return rentalID + 1


# print(generateRentalID())
