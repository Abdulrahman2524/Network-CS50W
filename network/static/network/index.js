document.addEventListener('DOMContentLoaded', function() {
    console.log("Clicked")

});
function edit_post(id){
    console.log(id)
    const text = document.getElementById(id).querySelector('#edit-text');
    text.style.display = 'none';
    const edit_area = document.getElementById(id).querySelector('#edit-area');
    const edit_button = document.getElementById(id).querySelector('#edit0');
    edit_area.style.display = 'block';
    edit_button.style.display = 'block';
    console.log(text.innerHTML)

    console.log(id, edit_area.innerHTML)
    edit_button.addEventListener('click', () => {
        
        if (edit_area.value == text.innerHTML){
            alert(`you haven't change any thing`)
        }else {
            update_post(id, edit_area.value)
            edit_area.style.display = 'none';
            edit_button.style.display = 'none';
            text.style.display = 'block';
            text.innerHTML = edit_area.value;
        }

    });
}

function clickedBtn(id) {
    console.log(id);
    like_post(id)
    fetch(`/postLikes/${id}`)
    .then((response) => {
        if(!response.ok) throw new Error(response.status);
        else return response.json();
      })
        .then(post => {
            // Print post   
            console.log(post.like);
            if (post.like == true){
                document.getElementById(id).querySelector('#heart').innerHTML = `<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="red" class="bi bi-heart" viewBox="0 0 16 16">
                <path d="m8 2.748-.717-.737C5.6.281 2.514.878 1.4 3.053c-.523 1.023-.641 2.5.314 4.385.92 1.815 2.834 3.989 6.286 6.357 3.452-2.368 5.365-4.542 6.286-6.357.955-1.886.838-3.362.314-4.385C13.486.878 10.4.28 8.717 2.01L8 2.748zM8 15C-7.333 4.868 3.279-3.04 7.824 1.143c.06.055.119.112.176.171a3.12 3.12 0 0 1 .176-.17C12.72-3.042 23.333 4.867 8 15z"/>
              </svg>`;
            }
        })
        .catch((error) => {
        console.log('error: ' + error);
        document.getElementById(id).querySelector('#heart').innerHTML = `<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-heart-fill" viewBox="0 0 16 16">
        <path fill-rule="evenodd" d="M8 1.314C12.438-3.248 23.534 4.735 8 15-7.534 4.736 3.562-3.248 8 1.314z"/>
      </svg>`;

      });


}

function like_post(post_id){
    fetch(`/postLikes/${post_id}`, {
        method: 'POST',
        body: JSON.stringify({
            post: post_id,
            like: true
        })
      })
}

function update_post(id, text){
    console.log(id, text)
    fetch(`/edit/${id}`, {
        method: 'PUT',
        body: JSON.stringify({
            id: id,
            text: text
        })
      })

}
