const blindButton = document.getElementsByClassName('bad-vision')[0];

const HTML = document.getElementsByClassName('html')[0];

console.log(HTML);

let isBlind = localStorage.getItem('isBlind');
if (isBlind) {
  HTML.classList.add('body__blind')
  localStorage.setItem('isBlind', true)
}

blindButton.onclick = (e) => {
  let isBlind = localStorage.getItem('isBlind');
  if (!isBlind) {
    HTML.classList.add('body__blind')
    localStorage.setItem('isBlind', true)
  } else {
    HTML.classList.remove('body__blind')
    localStorage.removeItem('isBlind')
  }
}