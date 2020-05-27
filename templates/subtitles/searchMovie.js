function search_movie() {
    let input = document.getElementById('movieName').value;
    input = input.toLowerCase();
    link_generator(input);
}

function link_generator(name) {
    let a = document.createElement('a');
    let link = document.createTextNode("DO IT");
    a.appendChild(link);
    a.title = "DO IT";
    name = name.replace(/\s+/g, '+');
    a.href = "https://www.google.com/search?q=" + name + "+subtitle";
    window.location.href = a.href;
    // document.body.appendChild(a);
}