from flask import Flask, jsonify, request
import pandas as pd

app = Flask(__name__)

# Load the .csv file
file_path = 'Inventory/Members.csv'
members_df = pd.read_csv(file_path)

# Format the member info for output
def member_layout(row):
    return {
        "MemberID": row['MemberID'],
        "FirstName": row['FirstName'],
        "LastName": row['LastName'],
        "PhoneNumber": row['PhoneNumber'],
        "Email": row['Email'],
        "CurRentals": row['CurRentals']
    }

# Search member based on input
def find_member(user_input):
    if user_input.isdigit() and len(user_input) == 4:
        user_input = "M" + user_input
    if user_input.startswith("M") and len(user_input) == 5:
        member = members_df[members_df['MemberID'] == user_input]
    else: 
        updated_input = user_input.replace("-","").replace(" ", "")
        member = members_df[members_df['PhoneNumber'].str.replace("-","").str.replace(" ","") == updated_input]

    if not member.empty:
        #return member_layout(member.iloc[0])
        return member.iloc[0].astype(object).to_dict()
    else:
        #return jsonify({"error": "No member found with the provided ID or phone number."}), 404
        return None

#Flask endpoint to search member

@app.route('/search_member', methods=['GET'])
def search_member_route():
    user_input = request.args.get('input')
    member = find_member(user_input)
    
    if member:
        return jsonify(member), 200
        #return jsonify(member.to_dict()), 200
    else:
        return jsonify ({"error": "No member found with the provided ID or phone number."}), 404
    
if __name__ == '__main__':
    app.run(debug=True)
