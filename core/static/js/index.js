function changeTab(evt, tabName) {
    var i, tablinks;

    if (tabName === 'home') {
        document.location.href = "/home";
    } else if (tabName === 'donate') {
        document.location.href = "/donate";
    }
    
    tablinks = document.getElementsByClassName("tablinks");
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" active", "");
    }

    evt.currentTarget.className += " active";
}