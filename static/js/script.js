// initialize elements
let menu_btn = document.querySelector('#menu-btn');
let sidebar = document.querySelector('#sidebar');
let videos_section = document.querySelector('#videos_section');

// initialize event listener
menu_btn.addEventListener('click', openSidebar);

// initialize functions
function openSidebar(e) {
    if(sidebar.style.display === 'none') {
        sidebar.style.display = 'block';
        sidebar.style.zIndex = '10';
        sidebar.style.background = 'white';
        console.log('clicked on if');
    }else {
        sidebar.style.display = 'none';
        videos_section.style.width = '100%';
        console.log('clicked on else')
    }
}