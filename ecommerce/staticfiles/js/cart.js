
//creo un event listener al bottone "Add to cart" che al click mi aggiunge il prodotto al carrello


var addToCartButtons = document.getElementsByClassName("update-cart")

for (var i = 0; i < addToCartButtons.length; i++) {
    var button = addToCartButtons[i]
    button.addEventListener('click', function (){
        var itemId = this.dataset.product
        var action = this.dataset.action

        console.log('USER:', user)
        if(user === 'AnonymousUser'){
            console.log('Not logged in')
        }else{
            updateOrder(itemId, action)
        }
    })
}


function updateOrder(itemId, action){
    console.log('User is authenticated, sending data...')

    var url = '/update_item/'   //url a cui mandero i dati (post data)

    //dati da mandare
    fetch(url, {
        method: 'POST',
        headers:{
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({'itemId': itemId, 'action': action})
    })

    //risposta
    .then((response) =>{
        return response.json()
    })

    //data
    .then((data) =>{
        console.log('data:', data)
        location.reload()
    })
}


