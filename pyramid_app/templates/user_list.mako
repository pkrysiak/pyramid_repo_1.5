<%inherit file="base.mako"/>

<%block name = "content">
    <table cellpadding="0" celllspacing="0" border="0" class="list">
            %for uid, uname, upass, ugroup in user_list:
                <tr>
                    <td class="thumb"><!-- <img src="http://image.ceneo.pl/data/products/19719012/f-asus-x501a-xx145h.jpg" alt="img_demo"/> --></td>
                    <td class="name_list">${uid}, ${uname}, ${upass}, ${ugroup}</td>
                    <td class="price_list"></td>
                    <!-- <td class="more"><a href="#" class="link_more btn"></a></td> -->
                </tr>
            %endfor
    </table>
</%block>