<!DOCTYPE html>
<html>
<head>
    <link href="http://www.artsmartiauxcombat.com/images/favicon.ico-16x16-i11.ico" rel="shortcut icon" type="image/x-icon" />
    <title>ИИТ</title>
    <style>
    body{
        background-color: aliceblue;
    }
    .main{
        margin: auto;
        width: 780px;
        text-align: center;
    }
    .user{
        display: inline-block;
        width: 100px;
        height: 120px;
        margin: 15px;
        margin-left: 10px;
        margin-right: 10px;
    }
    img{
        border-radius: 50%;
        height: 100px;
        width: 100px;
    }
    a{
        text-decoration: none;
        font-family: -apple-system,BlinkMacSystemFont,Roboto,Open Sans,Helvetica Neue,sans-serif;
        font-size: 14px;
        color: #2a5885;
    }
    a:hover{
        text-decoration: underline;
    }
</style>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.1.1/jquery.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery.lazyload/1.9.1/jquery.lazyload.js"></script>
</head>
<body>
    <div class="main">
        % for idx, user in enumerate(members):
        <div class="user">
            <a href="/id{{idx}}">


            <img class="lazy" data-original="{{user['photo_100']}}" width="100px" height="100px">

                <span class="name">{{user['first_name']}}<br>{{user['last_name']}}</span>
            </a>
        </div>
        % end
    </div>
<script>
    $("img.lazy").lazyload({
        threshold : 0
    });
</script>
</body>
</html>