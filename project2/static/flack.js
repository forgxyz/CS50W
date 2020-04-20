document.addEventListener('DOMContentLoaded', () => {
    // Start by loading first page.
    if (localStorage.displayname === undefined) {
        redirectLogin();
    } else if (localStorage.active !== undefined) {
        loadChannel(localStorage.active);
    } else {
        loadPage('home');
    }
    displayChannels();

    // Set links up to load new pages, if needed
    document.querySelectorAll('.nav-link').forEach(link => {
        const page = link.dataset.page;
        if (page === undefined) {
            return false;
        } else {
            link.onclick = () => {
            loadPage(page);
            return false;
          }
        };
    });

    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

    socket.on('new message', (data) => {
        // receive messages in the channel from the server
        if (data.channel === localStorage.active) {
            const template = Handlebars.compile(document.querySelector('#template_message').innerHTML);
            const message = template({'message': data.message});
            document.querySelector('#body').innerHTML += message;
        }
    });

});


// Update text on popping state.
window.onpopstate = e => {
    const data = e.state;
    document.title = data.title;
    document.querySelector('#body').innerHTML = data.text;
};


// create a new channel or return an error from the server
function createChannel () {
    if (localStorage.displayname === undefined) {
        redirectLogin();
    } else {
    const request = new XMLHttpRequest();
    request.open('POST', '/channels');
    request.onload = () => {
        const result = request.responseText;
        alert(result);
        displayChannels();
    }

    // send form input
    const data = new FormData();
    data.append('name', document.querySelector('#channelname').value);
    request.send(data);
    document.querySelector('#channelname').value = '';
  }
}


// display the channel List
function displayChannels () {
    const request = new XMLHttpRequest();
    request.open('GET', '/channels');
    request.onload = () => {
        const data = JSON.parse(request.responseText);
        const template = Handlebars.compile(document.querySelector('#template_channel_list').innerHTML);
        const content = template({'channels': data});
        document.querySelector('#channel_list').innerHTML = content;
    }
    request.send();
}


// load the messages from a channel
function loadChannel (channel) {
    if (localStorage.displayname === undefined) {
        redirectLogin();
    } else {

    // store active channel in localStorage for use in sending new messages
    localStorage.active = channel;

    // clear the body
    document.querySelector('#body').innerHTML = '';

    // display the existing messages
    const request = new XMLHttpRequest();
    request.open('GET', `/channels/${channel}`);

    request.onload = () => {
        // list of message dicts returned
        const data = JSON.parse(request.responseText);
        for (let i = 0; i < data.length;  ++i) {
            const template = Handlebars.compile(document.querySelector('#template_message').innerHTML);
            const messages = template({'message': data[i]});
            document.querySelector('#body').innerHTML += messages;
        }
    }
    // add the new post form
    const template_form = Handlebars.compile(document.querySelector('#template_new_message').innerHTML);
    const newPost = template_form();
    document.querySelector('#active').innerHTML = channel;
    document.querySelector('#body_lower').innerHTML = newPost;

    request.send();
  }
}


// Renders contents of new page in main view.
function loadPage (name) {
    const request = new XMLHttpRequest();
    request.open('GET', `/${name}`);
    request.onload = () => {
        const response = request.responseText;
        document.querySelector('#body').innerHTML = response;
        // Push state to URL.
        // document.title = name;
        // history.pushState({'title': name, 'text': response}, name, name);
      };
    request.send();
}


// post a new message
function postMessage () {
    // send user & channel from localStorage and content from form
    const message_data = {'channel': localStorage.active, 'user': localStorage.displayname, 'content': document.querySelector('#new_message').value};
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);
    socket.emit('post message', {'data': message_data});
    document.querySelector('#new_message').value = '';
}


// "login"
function redirectLogin () {
    // no user is stored
    // compile locally instead of on flask server
    const template = Handlebars.compile(document.querySelector('#displayname_form').innerHTML);
    const content = template();
    document.querySelector('#body').innerHTML = content;
}


// store the display name to local storage
function storeDisplayname () {
    let displayname = document.querySelector('#displayname').value;
    localStorage.setItem('displayname', displayname);
    alert(`Hello, ${displayname}! Thanks for setting your display name.`);
    loadPage('home');
}
