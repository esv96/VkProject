<!DOCTYPE html>
<html>
<head>
    <title>{{user.first_name}} {{user.last_name}}</title>
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
            <a href="https://vk.com/wall{{post.owner.id_}}_{{post.id_}}">
                Пост {{post.owner.id_}}_{{post.id_}}
            </a>

                <p>{{post.text[:200]+'...' if not post.text == '' else ''}}</p>

            % if post.attachments:
                    %for att in post.attachments:
                        %if att['type'] == 'photo':
                            <div><img class="lazy" data-original="{{att['url']}}"></div>
                        %elif att['type'] == 'audio' and att['url'] != '':
                            <audio controls>
                                <source src="{{att['url']}}">
                            </audio>
                        %elif att['type'] == 'link':
                            <div><a href="{{att['url']}}">{{att['title']}}</a></div>
                        %end
                    %end
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