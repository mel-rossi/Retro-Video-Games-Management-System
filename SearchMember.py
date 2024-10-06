import pandas as pd

#Load the CSV file
file_path = 'Inventory/Members.csv'
members_df = pd.read_csv('Inventory/Members.csv')

def member_layout(row):
    """ Formats the member info for output"""

    member_id = row['MemberID']
    first_name = row['FirstName']
    last_name = row['LastName']
    phone_number = row['PhoneNumber']
    email = row['Email']
    rentals = row['CurRentals']

    # Member ID auto format
    #member_id = f"M{member_id}"

    # 10-digit phone number auto format ###-###-####
    #phone_number = f"{phone_number[:3]}-{phone_number[3:6]}-{phone_number[6:]}"

    #print member details
    print(f"Member ID: {member_id}")
    print(f"First Name: {first_name}")
    print(f"Last Name: {last_name}")
    print(f"Phone Number: {phone_number}")
    print(f"Email: {email}")
    print(f"Rental Count: {rentals}")

def search_member(user_input):
    """ Finds and returns a member based on the input (Member ID / Phone Number)"""

    if user_input.isdigit() and len(user_input) == 4:
        user_input = "M" + user_input #automatically add "M" before the number

    if user_input.startswith("M") and len(user_input) == 5:
        member = members_df[members_df['MemberID'] == user_input]
    else:
        updated_input = user_input.replace("-","").replace(" ","")
        member = members_df[members_df['PhoneNumber'].str.replace("-","").str.replace(" ","") == updated_input]
    
    #if member is found, print the information
    if not member.empty:
        member_layout(member.iloc[0])
    else:
        print("No member found with the provided ID or phone number.")

# Main loop 
while True:
    user_input = input("Enter Member ID (M####) or 10-Digit Phone Number, or type exit to quit: ").strip()
    if user_input.lower() == 'exit':
        print("Exiting the program.")
        break
    
    search_member(user_input)
