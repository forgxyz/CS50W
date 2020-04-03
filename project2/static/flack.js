document.addEventListener('DOMContentLoaded', () => {
  // start by loading homepage
  load_page('home');
});

// render content of page in main view.
function load_page(name) {
  const request = new XMLHttpRequest();
  request.open('GET', `${name}`);
  request.onload = () => {
    const response = request.responseText;
    document.querySelector('#body').innerHTML = response;

    // push state to URL
    document.title = name;
    history.pushState({'title': name, 'text': response}, name, name);
  };
  request.send();
};
