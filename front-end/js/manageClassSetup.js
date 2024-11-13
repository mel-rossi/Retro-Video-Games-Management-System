//TODO Design class better I think?
class AddRental {
    constructor(manageContainer, videoGameID) {
        this.memberTextBox = null;
        this.resultContainer = null;
        this.resultText = null;

        this.confirmRentalStatus = false;

        this.memberID = NaN;
        this.videoGameID = videoGameID;
        this.manageContainer = manageContainer;
    }

    //create add rental html
    createAddRental() {
        let fragment = document.createDocumentFragment();

        //Create title
        let title = document.createElement("h1");
        title.innerText = "Add Rental to Customer";

        //Div Container for elements
        let addInfoDiv = document.createElement("div");
        addInfoDiv.setAttribute("id", "addInfo");

        //Textbox element for member info
        let memberTextBox = document.createElement("input");
        memberTextBox.setAttribute("type", "text");
        memberTextBox.setAttribute("id", "memberInput");
        memberTextBox.setAttribute("placeholder", "Phone number or email");
        memberTextBox.onkeydown = (event) => {
            if (event.key == 'Enter') {
                this.enterClick();
            }

            if (!this.confirmRentalStatus) {
                this.resultTextChange("");
            }
        };

        this.memberTextBox = memberTextBox;
        addInfoDiv.appendChild(memberTextBox);

        //Button element to start rental
        let enterButton = document.createElement("button");
        enterButton.setAttribute("class", "enter-button");
        enterButton.onclick = () => this.enterClick();
        enterButton.innerText = "Enter";

        addInfoDiv.appendChild(enterButton);

        //Result div to contain elements for result
        let resultDiv = document.createElement("div");
        resultDiv.setAttribute("id", "resultInfo");

        //Result text
        let resultText = document.createElement("p");

        this.resultText = resultText;
        this.resultContainer = resultDiv;
        resultDiv.appendChild(resultText);
        addInfoDiv.appendChild(resultDiv);

        fragment.appendChild(title);
        fragment.appendChild(addInfoDiv);

        this.manageContainer.appendChild(fragment);
    }

    //BUG: When doing this. in button event it thinks this. is the button element FUN
    enterClick() {
         //if we are confirming to create the rental
         if (this.confirmRentalStatus) {
            this.confirmRental();
        }
        //if we are not confirming rental grab member info
        else {
            //handles valid customer input with given textbox
            searchCustomer(this.memberTextBox, this.validCustomer.bind(this), this.errorHandling.bind(this));
        }
    }

    //when customer data is valid make a request to add rental
    validCustomer(data) {        

        this.memberID = data['Member'][0]['MemberID'];

        let params = {
            'VideoGameID': this.videoGameID,
            'MemberID': this.memberID
        };

        postRequestParams('open_rental', params,
            () => {
                this.confirmRentalStatus = true;
                this.resultTextChange("Confirm rental for " + data['Member'][0]['FirstName'] + " " + data['Member'][0]['LastName']);
            },
            this.errorHandling);
    }

    //when a request was made that we can add rental, confirm the rental
    confirmRental() {
        this.confirmRentalStatus = false;

        let params = {
            'Confirm': 'confirmed',
            'VideoGameID': this.videoGameID,
            'MemberID': this.memberID
        };

        postRequestParams('open_rental', params, () => this.resultTextChange("Rental Complete!"), this.errorHandling);
    }

    //change the text for the result element
    resultTextChange(text) {
        this.resultText.innerText = text;
    }

    //display error message
    errorHandling(errorData) {
        this.resultTextChange(errorData['Error']);
    }
}

class RemoveRental {
    constructor(manageContainer, rentalID) {
        this.resultContainer = null;
        this.resultText = null;
        this.confirmRentalStatus = false;

        this.rentalID = rentalID;
        this.manageContainer = manageContainer;
    }

    createRemoveRental() {
        let fragment = document.createDocumentFragment();

        //Create Title
        let title = document.createElement("h1");
        title.innerText = "Close Rental";

        //Div Container for elements
        let closeInfoDiv = document.createElement("div");
        closeInfoDiv.setAttribute("id", "closeInfo");

        //Button element to end rental
        let endButton = document.createElement("button");
        endButton.setAttribute("class", "enter-button");
        endButton.onclick = () => this.endClick;
        endButton.innerText = "End Rental";
        
        closeInfoDiv.appendChild(endButton);

        //Result div to contain elements for result
        let resultDiv = document.createElement("div");
        resultDiv.setAttribute("id", "resultInfo");

        //Result text
        let resultText = document.createElement("p");

        this.resultText = resultText;
        this.resultContainer = resultDiv;
        resultDiv.appendChild(resultText);
        closeInfoDiv.appendChild(resultDiv);

        fragment.appendChild(title);
        fragment.appendChild(closeInfoDiv);

        this.manageContainer.appendChild(fragment);
    }

    endClick() {
        if(this.confirmRentalStatus){

        }
        else{
            this.validRental();
        }        
    }

    validRental(){
        this.confirmRentalStatus = true;

        let params = {
            'RentalID': this.rentalID
        };

        postRequestParams("close_rental", params, () => { }, () => { });
    }

    //change the text for the result element
    resultTextChange(text) {
        this.resultText = text;
    }

    //display error message
    errorHandling(errorData) {
        this.resultTextChange(errorData['Error']);
    }
}