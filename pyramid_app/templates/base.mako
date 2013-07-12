<!DOCTYPE HTML>
<html>
<head>
    <title></title>
    <meta charset="UTF-8" />
    <link rel="stylesheet" href="${request.static_url('pyramid_app:static/css/style.css')}">
</head>
<body>
    <div id="container">
        <div class="main_box">
            <div class="head">
                <div class="logo_img"><a href = "/"><img src="${request.static_url('pyramid_app:static/img/logo.png')}" alt="logo"/></a></div>
                <div class="logo_txt">
                    Compare products
                    <div class="logo_txt_small">We will help you find and compare products</div>
                </div>
                <div class="box_login">
                    % if not logged:
                        <a class="btn btn-success" href="/register">Register</a>
                        <a class="btn" href="/login">Login</a>
                    %else:
                        <a class="btn" href="/logout">Logout</a>
                    %endif
                </div>
            </div>
            <div class="middle">
                <%block name="search_box"> </%block>
                <%block name="login_form"> </%block>
                <%block name="content"> </%block>
            </div>
        </div>
        <div class="footer">
            <img src="${request.static_url('pyramid_app:static/img/logo_stx.png')}" alt="logo_stx"/>
        </div>
    </div>
    <script type="/js/jquery-1.8.3.min.js"></script>
    <script type="text/javascript">
    $(document).ready(function() {
        var btn_search = $('.search input');
        btn_search.focus(function() {
            $(this).attr('value','');
        });
    });
    </script>
</body>
</html>