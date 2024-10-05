from flask import Flask, request, jsonify
import pandas as pd

app = Flask(__name__)

# Open Rentals.csv and Members.csv
df_Rentals = pd.read_csv('Inventory/Rentals.csv')
df_Members = pd.read_csv('Inventory/Members.csv')


# Get member details and rental status by member ID
def get_member_info ():
   # Get Member ID and Phone Number from the POST request (sent from JavaScript)
    MemberID_input = request.json('MemberID')
    phone_number_input = request.json.get('PhoneNumber')
    
   # Search for member either by Member ID or Phone Number
    if MemberID_input:
        member_row = df_Members[df_Members['MemberID'] == MemberID_input]
    elif phone_number_input:
        member_row = df_Members[df_Members['PhoneNumber'] == phone_number_input]
    else:
        return jsonify({"error": "Please provide either Member ID or Phone Number."})
    
    # Check if member exists
    if member_row.empty:
        return jsonify({"error": "Member not found."})
    
        
    # Extract member details
    first_name = member_row['FirstName'].values[0]
    last_name = member_row['LastName'].values[0]
    phone_number = member_row['PhoneNumber'].values[0]
    email = member_row['Email'].values[0]
    #cur_rentals = member_row['CurRentals'].values[0]

    # Search for rentals related to the member in Rentals.csv
    rental_records = df_Rentals[df_Rentals['MemberID'] == member_row['MemberID'].values[0]]

    # Count occurrences of 'Active'
    active_count = (rental_records['Status'] == 'Active').sum()

    # Determine Rental Status
    if active_count >= 5:
        rental_status = f"Maximum limit Reached! \n Number of video games rented: {active_count} "
    else:
        rental_status = f"Number of video games rented: {active_count}"
    
    # Send member details and rental status as JSON response
    return jsonify({
        "MemberID": member_row['MemberID'].values[0],
        "FirstName": first_name,
        "LastName": last_name,
        "PhoneNumber": phone_number,
        "Email": email,
        "RentalStatus": rental_status
    })
   
   
if __name__ == '__main__':
    app.run(debug=True)



