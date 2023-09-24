// This is the JS file for ALL pages

// save the current dark mode setting
let darkModeSetting = null;

// when the page loads
window.addEventListener("DOMContentLoaded", () => {
  // get the dark mode setting from the local storage
  darkModeSetting = window.localStorage.getItem("darkModeSetting");
  // if the setting is "on", toggle on dark mode
  if (darkModeSetting === "on"){
    changeColors();
  // if there is no setting, set the setting to "off"
  }else if(darkModeSetting === null){
    darkModeSetting = "off";
  }
});

// get the element
const darkModeBtn = document.getElementById("dark_mode_icon");
// when darkModeBtn is clicked, run toggleDarkMode
darkModeBtn.addEventListener("click", () => {
  changeColors();
  // modify the current dark mode setting variable
  if(darkModeSetting === "off"){
    darkModeSetting = "on";
  }else{
    darkModeSetting = "off";
  }
  // save the dark mode setting in the local storage
  window.localStorage.setItem("darkModeSetting", darkModeSetting);
});

function changeColors(){
  // get the element
  const page = document.body;
  // toggle the class
  page.classList.toggle("dark_mode");

  // if the element exists
  if(document.querySelector(".splash")){
    // get the element
    const splash = document.querySelector(".splash");
    // toggle the class
    splash.classList.toggle("color_dark_mode");
  }

  // if the element exists
  if(document.querySelector(".header")){
    // get the element
    const header = document.querySelector(".header");
    // toggle the class
    header.classList.toggle("color_dark_mode");
  }

  // if the element exists
  if(document.querySelector(".navigation_bar")){
    // get the element
    const navigationBar = document.querySelector(".navigation_bar");
    // toggle the class
    navigationBar.classList.toggle("navigation_bar_dark_mode");
  }

  // if the element exists
  if(document.querySelectorAll(".box")){
    // get the element
    const boxes = document.querySelectorAll(".box");
    for(const box of boxes){
      // toggle the class
      box.classList.toggle("dark_mode");
    }
  }

  // if the element exists
  if(document.querySelectorAll("input[type=text]")){
    // get the element
    const fields = document.querySelectorAll("input[type=text]");
    for(const field of fields){
      // toggle the class
      field.classList.toggle("dark_mode");
    }
  }

  // if the element exists
  if(document.querySelectorAll("input[type=password]")){
    // get the element
    const fields = document.querySelectorAll("input[type=password]");
    for(const field of fields){
      // toggle the class
      field.classList.toggle("dark_mode");
    }
  }
}