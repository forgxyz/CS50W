document.addEventListener('DOMContentLoaded', () => {
    // Start by loading first page.
    load_page('home');

    // Set links up to load new pages.
    document.querySelectorAll('.nav-link').forEach(link => {
        link.onclick = () => {
            const page = link.dataset.page;
            load_page(page);
            return false;
        };
    });
});

// store the display name to local storage
function store_displayname() {
    if (localStorage.displayname !== undefined) {
        alert('The display name is already set!');
        return false;
    }
    let displayname = document.querySelector('#displayname').value;
    localStorage.setItem('displayname', displayname);
    if (localStorage.displayname === undefined) {
        alert('ERROR: Unable to set display name.');
    } else {
        alert(`Hello, ${displayname}! Thanks for setting your display name.`);
    }
    load_page('home');
}


// Update text on popping state.
window.onpopstate = e => {
    const data = e.state;
    document.title = data.title;
    document.querySelector('#body').innerHTML = data.text;
};

// Renders contents of new page in main view.
function load_page(name) {
    if (localStorage.displayname === undefined) {
        // no user is stored
        // compile locally instead of on flask server
        const displaynametemplate = Handlebars.compile(document.querySelector('#displayname_form').innerHTML);
        const content = displaynametemplate();
        document.querySelector('#body').innerHTML = content;
    } else if (name === 'logout') {
        localStorage.clear();
        load_page('home');
      }
    else {
        const request = new XMLHttpRequest();
        request.open('GET', `/${name}`);
        request.onload = () => {
            const response = request.responseText;
            document.querySelector('#body').innerHTML = response;

            // Push state to URL.
            document.title = name;
            // history.pushState({'title': name, 'text': response}, name, name);
          };
        request.send();
  }
}
