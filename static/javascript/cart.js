const updateBtns = document.getElementsByClassName('update-cart')
const menu = document.getElementById('menu-icon')
let navlist = document.querySelector('.navlist')

menu.onclick = () => {
    menu.classList.toggle('bx-x');
    navlist.classList.toggle('active')
}

window.onscroll = () => {
    menu.classList.remove('bx-x');
    navlist.classList.remove('active');
}
//loop through each button and give them a function
for (let i = 0; i < updateBtns.length; i++) {
    updateBtns[i].addEventListener('click', function(){
        let product_Id = this.dataset.product
        let action = this.dataset.action
        console.log('p_ID:', product_Id, 'Action:', action)

        console.log('User:', user)
        
        if (user === 'AnonymousUser') {
            console.log('You are not authenticated')
        } else {
            updateUserOrder(product_Id,action)
        }
    })
}

function updateUserOrder(product_Id, action) {
    console.log('User is authenticated')

    let url = '/update_item/'
    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type':'application/json',
            'X-CSRFToken': csrftoken,
        },
        body:JSON.stringify({'p_Id':product_Id,'action':action})
        })
        .then((response) => {
            return response.json
        })
        .then((data) => {
            console.log(data) 
            location.reload()
        })
    
}






