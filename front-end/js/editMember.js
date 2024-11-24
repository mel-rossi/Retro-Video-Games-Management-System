const EDIT_MEMBER_CONTAINER = document.getElementById("edit-member-container");
const FORM = document.getElementById("edit-member-form");
const MEMBER_ID_INPUT = document.getElementById("member-id");
const FIRST_NAME_INPUT = document.getElementById("first-name");
const LAST_NAME_INPUT = document.getElementById("last-name");
const PHONE_NUMBER_INPUT = document.getElementById("phone-number");
const EMAIL_INPUT = document.getElementById("email");
const REQUEST_BUTTON = document.getElementById("request-button");
const CONFIRM_BUTTON = document.getElementById("confirm-button");
const RESPONSE = document.getElementById("response");

//autopopulat the form on window load
window.onload = autopopulateForm;
function autopopulateForm(){
    let memberID = EDIT_MEMBER_CONTAINER.getAttribute("data-member-id");
    let params = {
        MemberID: memberID
    };
    postRequestParams("edit_member", params, editForm, () => {});
}

function editForm(data){
    let memberDetails = data['Member Details Requested'][0];

    MEMBER_ID_INPUT.value = memberDetails['MemberID'];
    FIRST_NAME_INPUT.value = memberDetails['FirstName'];
    LAST_NAME_INPUT.value = memberDetails['LastName'];
    PHONE_NUMBER_INPUT.value = memberDetails['PhoneNumber'];
    EMAIL_INPUT.value = memberDetails['Email'];
}
function handleSubmit(event){

    event.preventDefault();

    let params = {
        Request: 'verified',
        MemberID: MEMBER_ID_INPUT.value,
        FirstName: FIRST_NAME_INPUT.value,
        LastName: LAST_NAME_INPUT.value,
        PhoneNumber: PHONE_NUMBER_INPUT.value,
        Email: EMAIL_INPUT.value
    };

    let confirmationMessage = `Please confirm the following changes for member ${MEMBER_ID_INPUT.value}: \n\n`
                            + `First Name: ${params.FirstName}\n`
                            + `Last Name: ${params.LastName}\n`
                            + `Phone Number: ${params.PhoneNumber}\n`
                            + `Email: ${params.Email}\n`;

    if (condirm(confirmantionMessage)){
    // Display modaal dialog
    $('#confirmationModal').modal('show');

    // Set the confirmation message
    $('#confirmationModal .modal-body').html(confirmationMessage);

    // Set modal dialog buttons
    $('#confirmationModal .modal-footer').html(`
        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
        <button type="button" class="btn btn-primary" onclick="confirmRequest()">Confirm</button>
        `);
    } else {
        // If the user clicks "Cancel on the modal dialog, do nothing"
        return;
    }
    postRequestParams("edit_member", params, handleResponse, () => {});
    }

    function confirmRequest(){
        let params ={
            Confirm: 'confirmed',
            MemberID: MEMBER_ID_INPUT.value,
            FirstName: FIRST_NAME_INPUT.value,
            LastName: LAST_NAME_INPUT.value,
            PhoneNumber: PHONE_NUMBER_INPUT.value,
            Email: EMAIL_INPUT.value
        }
    postRequestParams("edit_member", params, handleResponse, () => {});

    //Hide modal dialog
    $('#confirmationModal').modal('hide');
    }
    function handleResponse(data){
        RESPONSE.textContent = data.message || data.Message;
    }

    //Add event listener to form
    FORM.addEventListener('submit', handleSubmit);

    //Add event listener to request button
    REQUEST_BUTTON.addEventListener('click', handleSubmit);

