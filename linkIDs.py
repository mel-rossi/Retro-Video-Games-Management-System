# Methods that link and work with columns in different tables that are dependent on each other 

# Read VideoGames 
df1 = pd.read_csv('Inventory/VideoGames.csv')

# Read Members
df2 = pd.read_csv('Inventory/Members.csv')

def rentOut(VideoGameInput): 
    # Find the value of VideoGameID and change Availability to Unavailable 
    df1.loc[df1['VideoGameID' == VideoGameInput, 'Availability'] = 'Unavailable'

    # Save update DataFrame back to CSV file 
    df1.to_csv('Inventory/VideoGames.csv', index=False)
# rentOut

def returnGame(VideoGameInput): 
    # Find the value of VideoGameID and change Availability to Available    
    df1.loc[df1['VideoGameID' == VideoGameInput, 'Availability'] = 'Available'

    # Save updated DataFrame back to CSV file
    df1.to_csv('Inventory/VideoGames.csv', index=False)
# returnGame

def incRentals(MemberInput): 
    # Increments number of active rentals a Member has 
    df2.loc[df2['MemberID' == MemberInput, 'curRentals'] += 1

    # Save updated DataFrame back to CSV file
    df2.to_csv('Inventory/Members.csv', index=False)

def decRentals(MemberInput): 
    # Decrements number of active rentals a Member has 
    df2.loc[df2['MemberID' == MemberInput, 'curRentals'] -= 1

    # Save updated DataFrame back to CSV file
    df2.to_csv('Inventory/Members.csv', index=False)
