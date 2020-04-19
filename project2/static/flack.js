document.addEventListener('DOMContentLoaded', () => {
    // Start by loading first page.
    if (localStorage.displayname === undefined) {
        // no user is stored
        // compile locally instead of on flask server
        const template = Handlebars.compile(document.querySelector('#displayname_form').innerHTML);
        const content = template();
        document.querySelector('#body').innerHTML = content;
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

});


// Update text on popping state.
window.onpopstate = e => {
    const data = e.state;
    document.title = data.title;
    document.querySelector('#body').innerHTML = data.text;
};


// create a new channel or return an error from the server
function createChannel () {
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
    localStorage.setItem('activeChannel', channel);
    const template = Handlebars.compile(`<a class='nav-link'>${channel}</a>`);
    document.querySelector('#active_channel').innerHTML = template();

    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);
    socket.emit('load_messages', {data: channel});
    socket.on('messages', (data) => {
        // receive messages in the channel from the server
        document.querySelector('#body').innerHTML = data;
    });
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


// store the display name to local storage
function storeDisplayname () {
    let displayname = document.querySelector('#displayname').value;
    localStorage.setItem('displayname', displayname);
    alert(`Hello, ${displayname}! Thanks for setting your display name.`);
    loadPage('home');
}
