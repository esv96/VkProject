<!DOCTYPE html>
<html>
<head>
    <title>{{user['first_name']}} {{user['last_name']}}</title>
    <style>
    body{
        background-color: aliceblue;
    }
    .main{
        margin: auto;
        width: 780px;
        text-align: center;
    }
    .post{
        padding: 10px;
        background-color: white;
        margin-top: 15px;
        margin-bottom: 15px;
    }

</style>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.1.1/jquery.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery.lazyload/1.9.1/jquery.lazyload.js"></script>
</head>
<body>
    <div class="main">
        % for post in posts:
        <div class="post">
            <a href="https://vk.com/wall{{post['owner_id']}}_{{post['id']}}">
                Пост {{post['owner_id']}}_{{post['id']}}
            </a>

                <p>{{post['text'][:200]+'...' if not post['text'] == '' else ''}}</p>

            % if 'attachments' in post and 'photo' in post['attachments'][0]:
                    <img class="lazy" data-original="{{post['attachments'][0]['photo']['photo_604']}}">
            % end
            % if 'copy_history' in post:
                <p>{{post['copy_history'][0]['text'][:100]+'...' if not post['copy_history'][0]['text'] == '' else ''}}</p>
            % end
        </div>
        % end
    </div>
<script>
    $("img.lazy").lazyload({
        threshold : 300
    });
</script>

</body>


</html>