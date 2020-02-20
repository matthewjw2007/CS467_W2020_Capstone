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
        document.body.style.backgroundColor = "#1b262c";
        darkModeButton.innerText = 'Light Mode';
    } else {
        document.body.style.backgroundColor = "#a3a3c2";
        darkModeButton.innerText = 'Dark Mode';
    }
});