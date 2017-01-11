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
        <div class="post">
            <a href="?order_by=date">По дате</a>
            <a href="?order_by=likes">По лайкам</a>
            <a href="?order_by=reposts">По репостам</a>
            <a href="?order_by=comments">По комментам</a>
            <a href="?order_by=share">По шерам</a>
        </div>
        % for post in posts:
        <div class="post">
            <h3>{{post.owner.first_name}} {{post.owner.last_name}}</h3>

                <p>{{post.text[:200]+'...' if not post.text == '' else ''}}</p>

            % if post.attachments:
                    %for att in post.attachments:
                        %if att['type'] == 'photo':
                            <div><img class="lazy" data-original="{{att['url']}}"></div>
                        %elif att['type'] == 'link':
                            <div><a href="{{att['url']}}">{{att['title']}}</a></div>
                        %end
                    %end
            % end
            % if post.original_post_id:
                <div class="repost" data-postid="{{post.original_post_id}}">
                    <a href="https://vk.com/wall{{post.original_post_id}}">оригинал поста</a>
                </div>
            % end
            <p>Лайки: {{post.likes}} Репосты: {{post.reposts}} Комменты: {{post.comments}}</p>
        </div>
        % end
        <div>
            % if page != 1:
                <a href="?order_by={{order_by}}&page={{page-1}}">назад</a>
            % end
            % if page != page_count:
                <a href="?order_by={{order_by}}&page={{page+1}}">вперед</a>
            % end
        </div>
    </div>
<script>
    $("img.lazy").lazyload({
        threshold : 300
    });
    /*$( ".repost" ).each(function() {
        postid = $( this ).attr('data-postid');
        console.log(postid);
        //$(this).html('kekchic');
        var req="https://api.vk.com/method/wall.getById?v=5.57&posts="+postid;
        $.ajax({
            url : req,
            type : "GET",
            dataType : "jsonp",
            context : this,
            success : function(data){
                post = data.response[0];
                if (post)
                    $(this).html(post.text.slice(0, 100));
            }
        });
    });*/
</script>

</body>


</html>