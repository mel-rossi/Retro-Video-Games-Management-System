import pandas as pd

# Open Rentals.csv and Members.csv
df_Rentals = pd.read_csv('Inventory/Rentals.csv')
df_Members = pd.read_csv('Inventory/Members.csv')

# Member ID input
MemberID_input = input("Enter Member ID: ")

# Get member details and rental status by member ID
def get_member_info (MemberID_input):
    
    #search for member in Members.csv
    member_row = df_Members[df_Members['MemberID'] == MemberID_input]
    if member_row.empty:
        print(f"Member with ID {MemberID_input} not found.")
        return

    # Extract member details
    first_name = member_row['FirstName'].values[0]
    last_name = member_row['LastName'].values[0]
    phone_number = member_row['PhoneNumber'].values[0]
    email = member_row['Email'].values[0]

    # Search for rentals related to the member in Rentals.csv
    rental_records = df_Rentals[df_Rentals['MemberID'] == MemberID_input]

    # Count occurrences of 'Active'
    active_count = (rental_records['Status'] == 'Active').sum()

    # Determine Rental Status
    if active_count >= 5:
        rental_status = f"Maximum limit Reached! \n Number of video games rented: {active_count} "
    else:
        rental_status = f"Number of video games rented: {active_count}"
    
    # Print member details
    print(f"Member ID: {MemberID_input}")
    print(f"First Name: {first_name}")
    print(f"Last Name: {last_name}")
    print(f"Phone Number: {phone_number}")
    print(f"Email: {email}")
    print(f"Rental Status: {rental_status}")

#call the function
get_member_info(MemberID_input)

