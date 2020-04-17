document.addEventListener('DOMContentLoaded', () => {
    // Start by loading first page.
    load_page('home');
    display_channels();

    // Set links up to load new pages.
    document.querySelectorAll('.nav-link').forEach(link => {
        const page = link.dataset.page;
        if (page === undefined) {
          return false;
        } else {
            link.onclick = () => {
            load_page(page);
            return false;
          }
        };
    });

});


// Update text on popping state.
window.onpopstate = e => {
    const data = e.state;
    document.title = data.title;
    document.querySelector('#body').innerHTML = data.text;
};


// create a new channel or return an error from the server
function create_channel () {
    const request = new XMLHttpRequest();
    request.open('POST', '/channels');
    request.onload = () => {
        const result = request.responseText;
        alert(result);
    }

    // send form input
    const data = new FormData();
    data.append('name', document.querySelector('#channelname').value);
    request.send(data);
}


// display the channel List
function display_channels () {
    const request = new XMLHttpRequest();
    request.open('GET', '/get_channel_list');
    request.onload = () => {
        const data = JSON.parse(request.responseText);
        const template = Handlebars.compile(document.querySelector('#template_channel_list').innerHTML);
        const content = template({'channels': data});
        document.querySelector('#channel_list').innerHTML = content;
    }
    request.send();
}


// Retrieve the channel message data from the server and display on the page
// DELETE THIS AND CHANGE TO SOCKET
function load_channel (name) {
    const request = new XMLHttpRequest();
    request.open('GET', `/channel/${name}`);
    request.onload = () => {
        const contents = JSON.parse(request.responseText);
        contents.forEach((item, i) => {
            const template = Handlebars.compile(document.querySelector('#display_channel').innerHTML);
            const content = template({'content': item});
            document.querySelector('#body').innerHTML += content;
            return True
        });
      }
    request.send();
}


// Renders contents of new page in main view.
function load_page (name) {
    if (localStorage.displayname === undefined) {
        // no user is stored
        // compile locally instead of on flask server
        render_handlebars('displayname_form');
    } else if (name === 'logout') {
        localStorage.clear();
        load_page('home');
    } else if (name === 'create') {
        render_handlebars('create_channel_form');
    } else {
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


function render_handlebars (id, params = false) {
    const template = Handlebars.compile(document.querySelector(`#${id}`).innerHTML);
    const content = template(params);
    document.querySelector('#body').innerHTML = content;
}


// store the display name to local storage
function store_displayname () {
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
