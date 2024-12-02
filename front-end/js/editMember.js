const EDIT_MEMBER_CONTAINER = document.getElementById("edit-member-container");
const FORM = document.getElementById("edit-member-form");
const MEMBER_ID = document.getElementById("member-id");
const FIRST_NAME_INPUT = document.getElementById("first-name");
const LAST_NAME_INPUT = document.getElementById("last-name");
const PHONE_NUMBER_INPUT = document.getElementById("phone-number");
const EMAIL_INPUT = document.getElementById("email");
const REQUEST_BUTTON = document.getElementById("request-button");
const CONFIRM_BUTTON = document.querySelector('#request-modal .confirm-button');
const RESPONSE = document.getElementById("response");

// Modal elements
const MODAL = document.getElementById("custom-modal");
const MODAL_BODY = document.querySelector("#custom-modal .modal-body");
const MODAL_CONFIRM_BUTTON = document.querySelector("#custom-modal .confirm-button");
const MODAL_CANCEL_BUTTON = document.querySelector("#custom-modal .cancel-button");

//autopopulat the form on window load
window.onload = autopopulateForm;
function autopopulateForm(){
    let memberID = EDIT_MEMBER_CONTAINER.getAttribute("data-member-id");
    let params = {
        MemberID: memberID
    };
    postRequestParams("edit_member", params, populateForm, () => {});
}
// populate the form
function populateForm(data){

    if (!data || !data['Member Details Requested'] ||  data['Member Details Requested'].length === 0){
        console.error("No member details found in response.");
        return;
    }

    let memberDetails = data['Member Details Requested'][0];

    MEMBER_ID.value = memberDetails['MemberID'];
    FIRST_NAME_INPUT.value = memberDetails['FirstName'];
    LAST_NAME_INPUT.value = memberDetails['LastName'];
    PHONE_NUMBER_INPUT.value = memberDetails['PhoneNumber'];
    EMAIL_INPUT.value = memberDetails['Email'];
}

//request button confirm
REQUEST_BUTTON.addEventListener("click", requestChanges);


function requestChanges() {

        const CONFIRMATION_MESSAGE = `
                            Please confirm the following changes for member ${MEMBER_ID.value}: \n\n
                            + First Name: ${FIRST_NAME_INPUT.value}\n
                            + Last Name: ${LAST_NAME_INPUT.value}\n
                            + Phone Number: ${PHONE_NUMBER_INPUT.value}\n
                            + Email: ${EMAIL_INPUT.value}\n`;

        MODAL_BODY.textContent = CONFIRMATION_MESSAGE;
        openModal();
}

function openModal() {
    MODAL.style.display = "block";
}
function closeModal(){
    MODAL.style.display = "none";
}

MODAL_CONFIRM_BUTTON.addEventListener("click", handleSubmit);
       
function handleSubmit() {

    let params = {
        MemberID: MEMBER_ID.value,
        Request: "verified",
        Confirm: "confirmed",
        FirstName: FIRST_NAME_INPUT.value.trim(),
        LastName: LAST_NAME_INPUT.value.trim(),
        PhoneNumber: PHONE_NUMBER_INPUT.value.trim(),
        Email: EMAIL_INPUT.value.trim()
    };

    // Validate user input
    if (!params.FirstName || !params.LastName || !params.PhoneNumber || !params.Email) {
        alert("Please fill in all fields");
        return;
    }

    postRequestParams("edit_member", params, handleResponse,() => {});
    closeModal(); //close modal after submitting
}

MODAL_CANCEL_BUTTON.addEventListener("click", closeModal);

function handleResponse(data){
    if (data && data.success){
        //update the UI to reflect the changes
        RESPONSE.textContent = "Member details updated successfully.";
        // update form fields to reflect the changes
        if (data.MemberID) MEMBER_ID.value = data.MemberID;
        if (data.FirstName) FIRST_NAME_INPUT.value = data.FirstName;
        if (data.LastName) LAST_NAME_INPUT.value = data.LastName;
        if (data.PhoneNumber) PHONE_NUMBER_INPUT.value = data.PhoneNumber;
        if (data.Email) EMAIL_INPUT.value = data.Email;
    } 
    else if (data && data.error) {
        //handle any errors that occured during the update process
        RESPONSE.textContent = "Error updating member details: " + data.error;
    }
    else {
        //handle any errors that occured during the update process
        RESPONSE.textContent = "Unknown error occurred.";
    }
    
}