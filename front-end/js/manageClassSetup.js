class BaseRental {
    constructor(manageContainer) {
        this.resultText = document.createElement("p");;

        this.manageContainer = manageContainer;
    }

    getResultText() {
        return this.resultText;
    }

    getManageContainer() {
        return this.manageContainer;
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

//TODO Design class better I think?
class AddRental extends BaseRental {
    constructor(manageContainer, videoGameID) {
        super(manageContainer);

        this.memberTextBox = null;
        this.resultContainer = null;
        this.confirmRentalStatus = false;

        this.memberID = NaN;
        this.videoGameID = videoGameID;
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

            //reset the textbox when we are not confirming a rental
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

        this.resultContainer = resultDiv;

        resultDiv.appendChild(super.getResultText());
        addInfoDiv.appendChild(resultDiv);

        fragment.appendChild(title);
        fragment.appendChild(addInfoDiv);

        super.getManageContainer().appendChild(fragment);
    }

    enterClick() {
        //if we are confirming to create the rental
        if (this.confirmRentalStatus) {
            this.confirmRental();
        }
        //if we are not confirming rental grab member info
        else {
            //handles valid customer input with given textbox
            searchCustomer(this.memberTextBox, this.validCustomer.bind(this), super.errorHandling.bind(this));
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
                super.resultTextChange("Confirm rental for " + data['Member'][0]['FirstName'] + " " + data['Member'][0]['LastName']);
            },
            super.errorHandling.bind(this));
    }

    //when a request was made that we can add rental, confirm the rental
    confirmRental() {
        this.confirmRentalStatus = false;

        let params = {
            'Confirm': 'confirmed',
            'VideoGameID': this.videoGameID,
            'MemberID': this.memberID
        };

        postRequestParams('open_rental', params, () => super.resultTextChange("Rental Complete!"), super.errorHandling.bind(this));
    }
}

class RemoveRental extends BaseRental {
    constructor(manageContainer, rentalID) {
        super(manageContainer);

        this.resultContainer = null;        
        this.confirmRentalStatus = false;

        this.rentalID = rentalID;
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
        endButton.onclick = () => this.endClick();
        endButton.innerText = "End Rental";

        closeInfoDiv.appendChild(endButton);

        //Result div to contain elements for result
        let resultDiv = document.createElement("div");
        resultDiv.setAttribute("id", "resultInfo");

        this.resultContainer = resultDiv;

        resultDiv.appendChild(super.getResultText());

        resultDiv.appendChild(resultText);
        closeInfoDiv.appendChild(resultDiv);

        fragment.appendChild(title);
        fragment.appendChild(closeInfoDiv);

        this.manageContainer.appendChild(fragment);
    }

    endClick() {
        if (this.confirmRentalStatus) {
            this.confirmRental();
        }
        else {
            this.validRental();
        }
    }

    validRental() {
        this.confirmRentalStatus = true;

        let params = {
            'RentalID': this.rentalID
        };

        postRequestParams("close_rental", params,
            (data) => {
                super.resultTextChange(data['Message'] + "\n" + data['Registered Member (Name)'] + " close " + data['Registered Video Game (Title)']);
            }, super.errorHandling.bind(this));
    }

    confirmRental() {
        this.confirmRentalStatus = false;

        let params = {
            'Confirm': 'confirmed',
            'RentalID': this.rentalID
        };

        postRequestParams("close_rental", params, () => super.resultTextChange("Rental has been closed"), super.errorHandling.bind(this));
    }
}