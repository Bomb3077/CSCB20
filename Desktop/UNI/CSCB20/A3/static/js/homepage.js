// switch between sign in and sign up
const switch_button1 = document.querySelector("#switchbtn1");
const switch_button2 = document.querySelector("#switchbtn2");
switch_button1.addEventListner("click", swi_sign_up());
switch_button2.addEventListner("click", swi_sign_in());

//if log in form is displayed, toggle to sign up form
function swi_sign_up() {
  var login_container = document.getElementById("login_container");
  var signup_container = document.getElementById("signup_container");
  var switch1 = document.getElementById("switch_1");
  var switch2 = document.getElementById("switch_2");

  if ((login_container.style.display != "none" ) || (signup_container.style.display === "none")){
    login_container.style.display = "none";
    signup_container.style.display = "block";
    switch1.style.display = "none";
    switch2.style.display = "block";
  } 
}

//if sign up form is displayed, toggle to log in form
function swi_sign_in() {
  var login_container = document.getElementById("login_container");
  var signup_container = document.getElementById("signup_container");
  var switch1 = document.getElementById("switch_1");
  var switch2 = document.getElementById("switch_2");

  if ((login_container.style.display === "none" ) || (signup_container.style.display != "none")){
    login_container.style.display = "block";
    signup_container.style.display = "none";
    switch1.style.display = "block";
    switch2.style.display = "none";
  } 
}
