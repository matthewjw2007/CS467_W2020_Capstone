// Saving recipe to user's database
// function addRecipe() {
//     console.log('button clicked');
//     let recipeName = document.getElementById('recipe-title');
//     let recipeURL = document.getElementsByClassName('recipe-url');
//     console.log(recipeName.textContent);
//     console.log(recipeURL[0].value);
// }

// document.getElementById('save-recipe-btn').addEventListener("click", function () {
//    console.log('button pressed');
//    let recipeName = document.getElementById('save-recipe-btn').parentElement.parentElement.firstElementChild;
//    console.log(recipeName.textContent);
//    let recipeURL = document.getElementById('save-recipe-btn').parentElement.parentElement.firstElementChild.nextElementSibling.nextElementSibling.nextElementSibling.firstElementChild;
//    console.log(recipeURL.href);
// });

let buttonClass = document.getElementsByClassName('save-recipe-btn');

for(let i=0; i<buttonClass.length; i++){
    buttonClass[i].addEventListener("click", function () {
        let recipeName = buttonClass[i].parentElement.parentElement.firstElementChild;
        console.log(recipeName.textContent);
        let recipeURL = buttonClass[i].parentElement.parentElement.firstElementChild.nextElementSibling.nextElementSibling.nextElementSibling.firstElementChild;
        console.log(recipeURL.href);
    });
}

// Dark Mode
let darkModeButton = document.getElementById('dark-mode-btn');

darkModeButton.addEventListener('click', function () {
    if(darkModeButton.innerText === 'Dark Mode'){
        sessionStorage.setItem('darkModeKey', 'on');
        document.body.style.backgroundColor = "#1b262c";
        document.getElementById('main-container').style.backgroundColor = "#3282b8";
        document.getElementById('main-navbar').classList.remove('navbar-light');
        document.getElementById('main-navbar').classList.add('bg-dark');
        document.getElementById('main-navbar').classList.add('navbar-dark');
        let links = document.links;
        for(let i=0; i<links.length; i++){
            links[i].style.color = "#FFFFFF";
        }
        darkModeButton.innerText = 'Light Mode';
    } else {
        sessionStorage.setItem('darkModeKey', 'off');
        document.body.style.backgroundColor = "#a3a3c2";
        document.getElementById('main-container').style.backgroundColor = "#ccf2ff";
        document.getElementById('main-navbar').classList.remove('bg-dark');
        document.getElementById('main-navbar').classList.remove('navbar-dark');
        document.getElementById('main-navbar').classList.add('navbar-light');
        let links = document.links;
        for(let i=0; i<links.length; i++){
            links[i].style.color = "#000000";
        }
        darkModeButton.innerText = 'Dark Mode';
    }
});

if(sessionStorage.getItem('darkModeKey') === 'on'){
    document.body.style.backgroundColor = "#1b262c";
    document.getElementById('main-container').style.backgroundColor = "#3282b8";
    document.getElementById('main-navbar').classList.remove('navbar-light');
    document.getElementById('main-navbar').classList.add('bg-dark');
    document.getElementById('main-navbar').classList.add('navbar-dark');
    let links = document.links;
    for(let i=0; i<links.length; i++){
        links[i].style.color = "#FFFFFF";
    }
    darkModeButton.innerText = 'Light Mode';
} else {
    document.body.style.backgroundColor = "#a3a3c2";
    document.getElementById('main-container').style.backgroundColor = "#ccf2ff";
    document.getElementById('main-navbar').classList.remove('bg-dark');
    document.getElementById('main-navbar').classList.remove('navbar-dark');
    document.getElementById('main-navbar').classList.add('navbar-light');
    let links = document.links;
    for(let i=0; i<links.length; i++){
        links[i].style.color = "#000000";
    }
    darkModeButton.innerText = 'Dark Mode';
}

document.getElementById("my-tasks").addEventListener("click", openMenu);

function openMenu() {
    document.getElementById("dropdown").classList.toggle("active");
    document.getElementById("my-tasks-span").classList.toggle("active");
}