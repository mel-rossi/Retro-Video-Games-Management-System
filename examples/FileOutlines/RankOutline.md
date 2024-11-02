# Rank.py File Algorithm Outline

- A Flask Blueprint File that performs sorting methods on .csv files that were converted to data frames 

## Imports 

### Python Libraries

- os 
- pandas 
- CORS
- flask (request, jsonify & Blueprint)  

### Foreign Functions 

#### From file `RentalStat.py`: 

- `rent_num(dataframe)`: Counts total number of rentals in provided data frame. 
- `avg_rental_time(dataframe)`: Calculates average rental time (total rental time / number of total rentals) in provided data frame. 
- `rental_filter(string)`: Filters Rentals by Rental ID (string provided) 

#### From file `GameRental.py`: 

- `game_filter(string)`: Filters Rentals by Video Game ID (string provided) 

#### From file `MemberRental.py`: 

- `member_filter(string)`: Filters Rentals by Member ID (string provided) 

### .csv Files Imported as Dataframes

* Accomplished through use of os and pandas 

#### `Rentals.csv` 
#### `Member.csv` 
#### `VideoGames.csv` 

## Blueprint Specifications 

#### Variable Name: `rank_bp`
#### Blueprint Name: `'Rank`
#### URL rule (endpoint): `'/rank'`
#### HTTP methods handled: `POST`

## Local Functions 

### `ranking(idName, filters, df, bias)`

#### Parameters 

- `idName` : a string 
- `filters` : a function 
- `df` : a data frame
- `bias` : a boolean

#### Sorts a data frame (`df`) based on Rental Time

- Uses imported functions `rent_num` and `avg_rental_time` to calculate a `'score'` (Rental Time) which will be assigned to `df`. Then local function `sort` with `'score'` will be called. Score is then dropped after being used. 
- Returns a sorted version of `df` 

### `limitOut(df, top)`

#### Parameters 

- `df` : a data frame 
- `top` : an integer

#### Limits the size of the dataframe (`df`)

- Returns limited version of `df` 

### `sort(df, valueID, bias)`

#### Parameters

- `df` : a data frame 
- `valueID` : a string 
- `bias` : a boolean 

#### Sorts through a dataframe (`df`) by a column (`valueID`), in the desired orientation

- Orientation is determined by `bias` 
- Returns sorted version of `df`

### Input/Variable Validation Functions 

- Returns a boolean (`True` if check is confirmed & `False` if it is not) 

#### `validRank(rank)`: Checks whether string (rank) is valid 
#### `validBase(base, rank)`: Checks whether string (base) is valid 
#### `validSort(rank, base, sort)`: Checks whether string (sort) is valid 
#### `validTop(top)`: Checks whether top is a digit string or an integer 

### `sortingMethod(rankType, sortBy, sortAdd, top, bias)`

- Parameters are defaulted to `None` and only of importance (used) if they are valid

#### Parameters 

- `rankType`
- `sortBy` 
- `sortAdd`
- `top`
- `bias`

#### Processes user input and performs sorting according to input

- Returns a sorted data frame as specified by user input 

### `rank_route()`

#### Route handler function

- Reads user input from POST request and calls processor function `sortingMethod`
- Returns `sortingMethod` return value as a json 

## File Interaction via User Input 

### User Input Fields (provided to `sortingMethod` in this order)

- `'rank'` : Determines what data frame is going to be sorted through 
- `'base'` : Determines values the sorting will be based on 
- `'sort'` : Determines and Considers a few additional sorting factors, if Valid changes `'base'` Case functionality 
- `'top'` : Determines the limit of the size of the data frame you want as an output 
- `'trend'` : Determines sorting orientation 

### Valid & Default User Inputs 

- Any User Input that is not Valid becomes Default
- All User Input is Case Insensitive
- If a field is dependent on another field, it means that the [validity/functionality] of certain inputs [requires/is affected by] the other field [to be/being] a specific Case 

#### Ultimate Default (when there is no User Input or all User Input is Invalid) 

***Rentals*** data frame (***`Rentals.csv`***) is **fully** sorted, based on 'Ranking', by *Highest to Lowest* Score 

#### `'rank'`

- `Default` : Sorting performed on ***Rentals*** data frame (***`Rentals.csv`***)
- `'Game'`: Sorting performed on ***Video Games*** data frame (***`VideoGames.csv`***)
- `'Member'`: Sorting performed on ***Members*** data frame (***`Members.csv`***)

#### `'base'` (dependent on `'rank'`)

- `Default` : Sorting is based on 'Ranking' which is the `'score'` calculated by the `ranking` function
- `'Id'` : Sorting is based on an 'ID' column
    - When `'rank'` = `Default` : Sorts ***Rentals*** based on 'Rental ID' 
    - When `'rank'` = `'Game'` : Sorts ***Video Games*** based on 'Video Game ID' 
    - When `'rank'` = `'Member'` : Sorts ***Members*** based on 'Member ID'
- `'Name'` : Sorting is based on a 'Name' column 
    - Pre-requirements: `'rank'` = `'Game'` OR `'Member'`
        - When `'rank'` = `'Game'` : Sorts ***Video Games*** based on 'Title' 
        - When `'rank'` = `'Member'` : Sorts ***Members*** based on 'First Name'
- `'Year'` : ***Video Games*** Sorted based on 'Year' column
    - Pre-requirements: `'rank'` = `'Game'`
- `'Genre'` : ***Video Games*** Sorted based on 'Genre' column 
    - Pre-requirements: `'rank'` = `'Game'`

#### `'sort'` (dependent on `'rank'` AND `'base'`) 

- `Default` : Input is ignored 
- `'Surname'` : Sorts ***Members*** based on 'Last Name'  
    - Pre-requirements: `'rank'` = `'Member'` AND `'base'` = `'Name'`
- `'Publisher'` : Sorts ***Video Games*** based on 'Publisher'
    - Pre-requirements: `'rank'` = `'Game'` AND `'base'` = `'Name'`
- `'Member'` : Sorts ***Rentals*** based on 'Member ID'
    - Pre-requirements: `'rank'` = `Default` AND `'base'` = `'Id'`
- `'Game'` : Sorts ***Rentals*** based on 'Video Game ID'
    - Pre-requirements: `'rank'` = `'Default` AND `'base'` = `'Id'` 

#### `'top'`

- `Default` : The **full** data frame is returned without size restrictions 
- `Any Digit String or Integer Number` : The data frame is size **restricted** by input number before being returned

#### `'trend'`

- Default : Sorted by descending (*Highest to Lowest*) order of values 
- `'Flip'`: Sorted by ascending (*Lowest to Highest*) order of values 


