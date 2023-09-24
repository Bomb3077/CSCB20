const searchUserForm = document.getElementById("searchUserForm");
const inviteForm = document.getElementById("inviteForm");
const messages = document.getElementById("messages");
const profileBox = document.getElementById("setProfile");
const renameForm = document.getElementById("renameForm");
const deleteForm = document.getElementById("deleteForm");

// show page elements depending on the command number
function showContent(command){
  switch(command){
    // show the form to search for a user
    case 0:
      messages.style.display = 'none';
      searchUserForm.style.display = 'block';
      inviteForm.style.display = 'none';
      profileBox.style.display = 'none';
      renameForm.style.display = 'none';
      deleteForm.style.display = 'none';
      break;
    // show the messages
    case 1:
      searchUserForm.style.display = 'none';
      messages.style.display = 'block';
      inviteForm.style.display = 'none';
      profileBox.style.display = 'none';
      renameForm.style.display = 'none';
      deleteForm.style.display = 'none';
      break;
    // show the messages and the invitation form
    case 2:
      searchUserForm.style.display = 'none';
      messages.style.display = 'block';
      inviteForm.style.display = 'block';
      profileBox.style.display = 'none';
      renameForm.style.display = 'none';
      deleteForm.style.display = 'none';
      break;
    // show the profile box
    case 3:
      searchUserForm.style.display = 'none';
      messages.style.display = 'none';
      inviteForm.style.display = 'none';
      profileBox.style.display = 'block';
      renameForm.style.display = 'none';
      deleteForm.style.display = 'none';
      break;
    // show the messages and the rename form
    case 4:
      searchUserForm.style.display = 'none';
      messages.style.display = 'block';
      inviteForm.style.display = 'none';
      profileBox.style.display = 'none';
      renameForm.style.display = 'block';
      deleteForm.style.display = 'none';
      break;
    // show the messages and the delete form
    case 5:
      searchUserForm.style.display = 'none';
      messages.style.display = 'block';
      inviteForm.style.display = 'none';
      profileBox.style.display = 'none';
      renameForm.style.display = 'none';
      deleteForm.style.display = 'block';
      break;
  }
}

const messageBox = document.getElementById("message_box");

// get messages from SQL and add them to messageBox
function getMessages(){
  fetch("/get_data")
    .then(function (response) {
      return response.text();
  }).then(function (text) {
      // no messages
      if(text === ""){
        messageBox.innerHTML = "There are no messages<br>Start the conversation below"
      // there are messages
      }else{
        messageBox.innerHTML = text;
      }
  });
}

// run getMessages on page load
getMessages();
// run getMessages every two seconds
setInterval(getMessages, 2000);

const functions = document.getElementById("functions");
// show/hide group functions
function showFunctions(more){
  if (functions.style.display == "none"){
      functions.style.display = "block";
  }else{
      functions.style.display = "none";
  }
}

// track to see whether the user scrolled the messages
let scrolled = false;
// update the scroll position to the bottom of the messages
function updateScroll(){
  if(!scrolled){
    messageBox.scrollTop = messageBox.scrollHeight;
  }
}

// run updateScroll every second
setInterval(updateScroll, 2000);

// delay two seconds
setTimeout(() => {
  // set scrolled to true if the messages have been scrolled
  messageBox.addEventListener("scroll", () => {
    scrolled = true;
  });
}
, 5000);