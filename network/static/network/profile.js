document.addEventListener('DOMContentLoaded', function() {
    const follow_btn = document.querySelector('#follow-btn');
    const follow_value = follow_btn.value;
    const user_id = document.querySelector('#username').value;
    user_profile(follow_btn, follow_value, user_id)
});
function user_profile(follow_btn, follow_value, user_id){
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
                    window.location.reload();
                });
        
            } else {
                follow_btn.innerHTML = "Follow"
                follow_btn.addEventListener('click', () =>{
                    follow_user(follow_value, user_id)
                    window.location.reload();
            });
            }
        });
    
    
    }
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
    
