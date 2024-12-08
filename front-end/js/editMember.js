const EDIT_MEMBER_CONTAINER = document.getElementById("edit-member-container");
const FORM = document.getElementById("edit-member-form");
const MEMBER_ID = document.getElementById("member-id");
const FIRST_NAME_INPUT = document.getElementById("first-name");
const LAST_NAME_INPUT = document.getElementById("last-name");
const PHONE_NUMBER_INPUT = document.getElementById("phone-number");
const EMAIL_INPUT = document.getElementById("email");
const REQUEST_BUTTON = document.getElementById("request-button");
const RESPONSE = document.getElementById("response");

// Modal elements
const MODAL = document.getElementById("custom-modal");
const MODAL_BODY = document.querySelector("#custom-modal .modal-body");
const MODAL_CONFIRM_BUTTON = document.querySelector("#custom-modal .confirm-button");
const MODAL_CANCEL_BUTTON = document.querySelector("#custom-modal .cancel-button");
const SUCCESS_MODAL = document.getElementById("success-modal");
const SUCCESS_MESSAGE = document.getElementById("success-message");
const CLOSE_SUCCESS_MODAL = document.getElementById("close-success-modal");

let originalData = {};
//autopopulat the form on window load
window.onload = autopopulateForm;
function autopopulateForm(){

    let memberID = EDIT_MEMBER_CONTAINER.getAttribute("data-member-id");
    let params = {
        MemberID: memberID
    };
    postRequestParams("edit_member", params, populateForm, (error) => {
        console.error("Failed to fetch member details:", error);
    });
}

// populate the form
function populateForm(data){
    if (!data || !data['Member Details Requested'] ||  data['Member Details Requested'].length === 0){
        console.error("No member details found in response.");
        return;
    }

    let memberDetails = data['Member Details Requested'][0];

    MEMBER_ID.value = memberDetails['MemberID']|| "";
    FIRST_NAME_INPUT.value = memberDetails['FirstName']|| "";
    LAST_NAME_INPUT.value = memberDetails['LastName']|| "";
    PHONE_NUMBER_INPUT.value = memberDetails['PhoneNumber']|| "";
    EMAIL_INPUT.value = memberDetails['Email']|| "";

    //Store original values
     originalData = {
        MemberID: memberDetails['MemberID'],
        FirstName: memberDetails['FirstName'],
        LastName: memberDetails['LastName'],
        PhoneNumber: memberDetails['PhoneNumber'],
        Email: memberDetails['Email']
    };
}

//request button confirm
REQUEST_BUTTON.addEventListener("click", openModal);
function openModal(event) {
    event.preventDefault(); // prevent form submission

    // compare the current form values with the original values
    const CHANGES = [];
    if(FIRST_NAME_INPUT.value.trim() !== originalData.FirstName){
        CHANGES.push(`First Name: ${FIRST_NAME_INPUT.value.trim() || "[No Change]"}`);
    } 
    if(LAST_NAME_INPUT.value.trim() !== originalData.LastName) {
        CHANGES.push(`Last Name: ${LAST_NAME_INPUT.value.trim()}`);
    }
    if(PHONE_NUMBER_INPUT.value.trim() !== originalData.PhoneNumber) {
        CHANGES.push(`Phone Number: ${PHONE_NUMBER_INPUT.value.trim()}`);
    }
    if(EMAIL_INPUT.value.trim() !== originalData.Email) {
        CHANGES.push(`Email: ${EMAIL_INPUT.value.trim()}`);
    }

    //if there are no changes, show the no changes message
    if (CHANGES.length === 0) {
        noChangeMessage();

    //change button labels to Go back and Cancel
    MODAL_CONFIRM_BUTTON.textContent = "Go Back";
    MODAL_CONFIRM_BUTTON.removeEventListener("click", handleSubmit);
    MODAL_CONFIRM_BUTTON.addEventListener("click", closeModal); // remove any old event listener
    }
    else {
        const CONFIRMATION_MESSAGE = `
        <p>Please confirm the following changes for member: <strong>${MEMBER_ID.value}</strong></p>
       
        <ul>
          ${CHANGES.map(change => `<li>${change}</li>`).join('')}
        </ul>`;

        MODAL_BODY.innerHTML = CONFIRMATION_MESSAGE;

        //change back button labels to Confirm and Cancel
        MODAL_CONFIRM_BUTTON.textContent = "Confirm";
        MODAL_CONFIRM_BUTTON.removeEventListener("click", closeModal);
        MODAL_CONFIRM_BUTTON.addEventListener("click", handleSubmit);
    }
    MODAL.style.display = "block";  

}
function closeModal(){
    MODAL.style.display = "none";
}

MODAL_CANCEL_BUTTON.addEventListener("click", closeModal);
MODAL_CONFIRM_BUTTON.addEventListener("click", handleSubmit);       
function handleSubmit() {
    let currentData ={
        MemberID: MEMBER_ID.value,
        FirstName: FIRST_NAME_INPUT.value.trim(),
        LastName: LAST_NAME_INPUT.value.trim(),
        PhoneNumber: PHONE_NUMBER_INPUT.value.trim(),
        Email: EMAIL_INPUT.value.trim(),
    }; 

    //compare current data with original data
    const noChangesMade = Object.keys(currentData).every(key => currentData[key] === originalData[key]);

    if (noChangesMade) {
        noChangeMessage(); // display no change message
        return;
    }

    //proceed with submitting data since changes were made
    let params = {
        MemberID: MEMBER_ID.value,
        Request: "verified",
        FirstName: currentData.FirstName|| null,
        LastName: currentData.LastName|| null,
        PhoneNumber: currentData.PhoneNumber|| null,
        Email: currentData.Email|| null
    };

    postRequestParams("edit_member", params, handleResponse,(error) => {
        RESPONSE.textContent = `Error updating member details: ${error.Error || "Unknown error"}`;
        RESPONSE.className = "error";
    });

    closeModal(); // close modal after submitting
}

function noChangeMessage() {
    MODAL_BODY.innerHTML = `
        <p>No changes were made to the member's details.</p>
    `;
}
function showSuccessModal() {
    SUCCESS_MODAL.style.display = "block";
    SUCCESS_MESSAGE.textContent = "Member details updated successfully.";
}

CLOSE_SUCCESS_MODAL.addEventListener("click", () => {
    SUCCESS_MODAL.style.display = "none";
});

window,addEventListener("click", (event) => {
    if (event.target == SUCCESS_MODAL) {
        SUCCESS_MODAL.style.display = "none";
    }
});
function handleResponse(data){
    if (data && !data.error) {
        showSuccessModal();

        //update original data after successful submission
        originalData = {
            MemberID: data[0]?.MemberID || originalData.MemberID,
            FirstName: data[0]?.FirstName || originalData.FirstName,
            LastName: data[0]?.LastName || originalData.LastName,
            PhoneNumber: data[0]?.PhoneNumber || originalData.PhoneNumber,
            Email: data[0]?.Email || originalData.Email
        };

        // update form fields to reflect the changes
        MEMBER_ID.value = data[0]?.MemberID ||MEMBER_ID.value;
        FIRST_NAME_INPUT.value = data[0]?.FirstName || FIRST_NAME_INPUT.value;
        LAST_NAME_INPUT.value = data[0]?.LastName || LAST_NAME_INPUT.value;
        PHONE_NUMBER_INPUT.value = data[0]?.PhoneNumber || PHONE_NUMBER_INPUT.value;
        EMAIL_INPUT.value = data[0]?.Email || EMAIL_INPUT.value;

    } 
    else {
        RESPONSE.textContent = `Error: ${data.error}`;
        RESPONSE.className = "error";
    }
    
}
