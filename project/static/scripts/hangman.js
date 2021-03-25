var lives;
var word;
var guessedLetters = [];
var hidden;
var msgBox = document.getElementById('msg')
var img = document.getElementById('img')
function newGame(){

    var wordBin = ["hangman", "word", "king", "boat", "bill","finest","belt","due","minute","save",
    "task","control","moment","important","higher","trouble",
    "wash","farther","met","compass","rhyme","gate",
    "tie","have","sight","angle","letter","donkey",
    "place","political","orbit","dinner","last","pound",
    "horn","meant","belong","heading","education","comfortable",
    "natural","angle","sleep","joy","unhappy","dream",
    "popular","indeed","after","determine","chicken","happened",
    "student","model","worker","spite","flag","form","improve","income",
    "ask","should","service","additional","over","move",
    "surface","whispered","spite","wrong","threw","line",
    "rope","dance","principal","equator","train"];
    img.src = "../static/game/hangmanGame/hangman1.png"
    word = wordBin[Math.floor(Math.random() * wordBin.length)]
    hidden = word.split("")
    for (i = 0; i < hidden.length; i++) {
        hidden[i] = "_";
    }
    console.log(hidden)
    document.getElementById('hiddenWord').innerHTML = hidden.join(" ")
    guessedLetters = [];
    document.getElementById('guessedLetters').innerHTML = guessedLetters.join(" ")
    document.getElementById('msg').innerHTML = ""
    lives = 12;
    console.log(word)

}
document.querySelector('#letter').addEventListener('keyup', event =>{
    event.preventDefault();
    if (event.keyCode === 13){
        document.querySelector('#tryButton').click();
    }
})


document.querySelector('#tryButton').onclick = () => {
    var inptBox = document.getElementById('letter');
    var letter = inptBox.value;
    console.log(typeof letter)
    inptBox.value="";
    if (guessedLetters.includes(letter)) {
        msgBox.innerHTML = "You have already guessed the letter: "+letter
    }
    else if (letter.toLowerCase() == letter.toUpperCase()){
        msgBox.innerHTML = "You must enter a letter"
    }

    else {
        guessedLetters.push(letter);
        msgBox.innerHTML = ""
        if (word.includes(letter)){

            for (i = 0; i < word.length; i++) {
                if (word[i] == letter){
                    hidden[i] = letter;
                }
            }
            document.getElementById('hiddenWord').innerHTML = hidden.join(" ")
            if (hidden.includes('_') == false){
                msgBox.innerHTML = "Congratulations, you won the Game!"

            }
        }
        else{
            lives = lives - 1;
            var num = 13 - lives
            img.src = '../static/game/hangmanGame/hangman'+num+'.png'

            if (lives == 0){
                msgBox.innerHTML = "You lost. The word was: "+ word

            }
        }
        document.getElementById('guessedLetters').innerHTML = guessedLetters.join(" ");
    }
}


document.querySelector('#reset').onclick = () =>{
    console.log("game reset")
    newGame()
    console.log(hidden,guessedLetters,word)
}