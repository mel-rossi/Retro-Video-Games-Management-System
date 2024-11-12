//TODO Design class better I think?
class AddRental{
    constructor(manageContainer){    
        this.memberTextBox = null;
        this.resultContainer = null;
        this.resultText = null;
        this.confirmRentalStatus = false;

        this.manageContainer = manageContainer;
    }

    //create add rental html
    createAddRental(){
        let fragment = document.createDocumentFragment();

        let title = document.createElement("h1");
        title.innerText = "Add Rental to Customer";

        let addInfoDiv = document.createElement("div");
        addInfoDiv.setAttribute("id", "addInfo");

        let memberTextBox = document.createElement("input");
        memberTextBox.setAttribute("type", "text");
        memberTextBox.setAttribute("id", "memberInput");
        memberTextBox.setAttribute("placeholder", "Phone number or email");
        memberTextBox.onkeydown = (event) => {
            if(event.key == 'Enter'){
                enterClick();
            }

            if(!confirmRentalStatus){
                resultTextChange("");
            }
        };

        this.memberTextBox = memberTextBox;
        addInfoDiv.appendChild(memberTextBox);

        let enterButton = document.createElement("button");
        enterButton.setAttribute("class", "enter-button");
        enterButton.onclick = this.enterClick;
        enterButton.innerText = "Enter";

        addInfoDiv.appendChild(enterButton);

        let resultDiv = document.createElement("div");
        resultDiv.setAttribute("id", "resultInfo");

        let resultText = document.createElement("p");

        this.resultText = resultText;
        this.resultContainer = resultDiv;
        resultDiv.appendChild(resultText);
        addInfoDiv.appendChild(resultDiv);

        fragment.appendChild(title);
        fragment.appendChild(addInfoDiv);

        this.manageContainer.appendChild(fragment);
    }

    enterClick(){
        //if we are confirming to create the rental
        if(this.confirmRentalStatus){
            this.confirmRental();
        }
        //if we are not confirming rental grab member info
        else{
            //handles valid customer input with given textbox
            this.searchCustomer(this.memberTextBox, this.validCustomer, this.errorHandling);
        }
    }

    //when customer data is valid make a request to add rental
    validCustomer(data){
        this.confirmRentalStatus = true;

        this.memberID = data['Member'][0]['MemberID'];    

        let params = {
            'VideoGameID': videoGameID,
            'MemberID': memberID
        };

        postRequestParams('open_rental', params, 
            () => this.resultTextChange("Confirm rental for " + data['Member'][0]['FirstName'] + " " +  data['Member'][0]['LastName']), 
            this.errorHandling);
    }

    //when a request was made that we can add rental, confirm the rental
    confirmRental(){
        this.confirmRentalStatus = false;

        let params = {
            'Confirm': 'confirmed',
            'VideoGameID': videoGameID,
            'MemberID': memberID
        };

        postRequestParams('open_rental', params, ()=> this.resultTextChange("Rental Complete!"), this.errorHandling);
    }

    //change the text for the result element
    resultTextChange(text){
        this.resultText = text;        
    }

    //display error message
    errorHandling(errorData){
        this.resultTextChange(errorData['Error']);
    }
}

class RemoveRental{
    constructor(){

    }


}