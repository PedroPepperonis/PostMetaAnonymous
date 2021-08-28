// menu
function dropdown_menu() {
    console.log('Вы нажали на меню')
    document.getElementById("dropdown_menu__content").classList.toggle("show");
}

// Закройте выпадающее меню, если пользователь щелкает за его пределами
window.onclick = function(event) {
    if (!event.target.matches('.dropdown_menu__button')) {
        let dropdowns = document.getElementsByClassName("dropdown_menu__content");
        let i;
        for (i = 0; i < dropdowns.length; i++) {
            let openDropdown = dropdowns[i];
            if (openDropdown.classList.contains('show')) {
                openDropdown.classList.remove('show');
            }
        }
    }
}

$('.post_likes__like_btn').on('click', function () {
    let post_id = $(this).attr('id')
    let data = {
        post_id: post_id
    }
    $.ajax({
        data: data,
        dataType: 'json',
        method: 'GET',
        url: '/like_post/',
        success: function(data) {
            document.getElementById('likes-count').textContent = data.likes
            document.getElementById('dislikes-count').textContent = data.dislikes
        }
    })
})
$('.post_likes__dislike_btn').on('click', function () {
    let post_id = $(this).attr('id')
    let data = {
        post_id: post_id
    }
    $.ajax({
        data: data,
        dataType: 'json',
        method: 'GET',
        url: '/dislike_post/',
        success: function(data) {
            document.getElementById('likes-count').textContent = data.likes
            document.getElementById('dislikes-count').textContent = data.dislikes
        }
    })
})

$('.comments_item__delete').on('click', function () {
    let comment_id = $(this).attr('id')
    console.log(comment_id)
    let data = {
        comment_id: comment_id
    }
    $.ajax({
        method: 'GET',
        dataType: 'json',
        data: data,
        url: '/delete_comment/',
        success: function (data) {
            $(`div[id='${comment_id}']`).remove()
        }
    })
})

$('.delete_post').on('click', function (){
    let post_id = $(this).attr('id')
    let data = {
        post_id: post_id
    }
    $.ajax({
        method: 'GET',
        dataType: 'json',
        data: data,
        url: '/delete_post/' + post_id,
        success: function (data){
            $(`div[id='${post_id}']`).remove()
        }
    })
})

$('.send_friend_request').on('click', function () {
    let user_id = $(this).attr('id')
    console.log(user_id)
    let data = {
        user_id: user_id
    }
    $.ajax({
        method: 'GET',
        dataType: 'json',
        data: data,
        url: '/send_friend_request/',
        success: function (data){
            location.reload()
        }
    })
})
$('.delete_friend').on('click', function () {
    let user_id = $(this).attr('id')
    let data = {
        user_id: user_id
    }
    $.ajax({
        method: 'GET',
        dataType: 'json',
        data: data,
        url: '/delete_friend/',
        success: function (data){
            $(`div[id='${user_id}']`).remove()
        }
    })
})
$('.accept_friend_request').on('click', function () {
    let request_id = $(this).attr('id')
    let data = {
        request_id: request_id
    }
    $.ajax({
        method: 'GET',
        dataType: 'json',
        data: data,
        url: '/accept_friend_request/',
    success: function (data){
            location.reload()
        }
    })
})
$('.decline_friend_request').on('click', function () {
    let request_id = $(this).attr('id')
    let data = {
        request_id: request_id
    }
    $.ajax({
        method: 'GET',
        dataType: 'json',
        data: data,
        url: '/decline_friend_request',
        success: function (data){
            $(`div[id='${request_id}']`).remove()
        }
    })
})

let is_subscribed = document.getElementById('subscribe_button').getAttribute('is_subscribed')
if (is_subscribed === 'True') document.getElementById('subscribe_button').textContent = 'Отписаться'
else document.getElementById('subscribe_button').textContent = 'Подписаться'
$('.subscribe_button').on('click', function () {
    let is_subscribed = document.getElementById('subscribe_button').getAttribute('is_subscribed')
    let group_slug = $('.subscribe_button').attr('group_slug')
    console.log(group_slug)
    if (is_subscribed === 'True') {
        $.ajax({
            data: $(this).serialize(),
            type: $(this).attr('method'),
            url: '/group/unsubscribe/' + group_slug,
            success: function () {
                document.getElementById('subscribe_button').textContent = 'Подписаться'
                $('.subscribe_button').attr('is_subscribed', 'False')
                document.getElementById('followers').textContent = parseInt(document.getElementById('followers').textContent) - 1
                console.log('Вы отписались от сообщества')
            }
        })
    }
else {
    $.ajax({
        data: $(this).serialize(),
        type: $(this).attr('method'),
        url: '/group/subscribe/' + group_slug,
        success: function () {
            document.getElementById('subscribe_button').textContent = 'Отписаться'
            $('.subscribe_button').attr('is_subscribed', 'True')
            document.getElementById('followers').textContent = parseInt(document.getElementById('followers').textContent) + 1
            console.log('Вы подписались на сообщество')
        }
    })
}
})