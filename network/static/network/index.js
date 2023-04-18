document.addEventListener('DOMContentLoaded', function() {

    const follow_btn = document.querySelector('#follow-btn');
    const follow_value = document.querySelector('#follow-btn').value;
    const user_id = document.querySelector('#username').value;
    console.log(user_id)
    
    fetch(`/followers/${user_id}`)
    .then(response => response.json())
    .then(user => {
        // Print user
        console.log(user);

        if (user.user == follow_value || user.follower == user_id){
            follow_btn.innerHTML = "Unfollow"
            follow_btn.addEventListener('click', () =>{
                unfollow_user(follow_value, user_id)
                follow_btn.innerHTML = "Follow"

            });
    
        } else {
            follow_btn.innerHTML = "Follow"
            follow_btn.addEventListener('click', () =>{
                follow_user(follow_value, user_id)
                follow_btn.innerHTML = "Unfollow"
        });
        }
    });
});

function follow_user(me, follower){
        fetch(`/followUser/${me}`, {
            method: 'POST',
            body: JSON.stringify({
                following_user_id: follower
            })
          })
}

function unfollow_user(me , follower){
    fetch(`/unFollow/${me}`, {
        method: 'POST',
        body: JSON.stringify({
            following_user_id: follower
        })
      })

}