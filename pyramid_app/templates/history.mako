
<%inherit file="base.mako"/>

<%block name = "content">
    <table cellpadding="0" celllspacing="0" border="0" class="list">
            %for name, price, link in search_list:
                <tr>
                    <td class="thumb"><!-- <img src="http://image.ceneo.pl/data/products/19719012/f-asus-x501a-xx145h.jpg" alt="img_demo"/> --></td>
                    <td class="name_list">${name}</td>
                    <td class="price_list">${price} zł</td>
                    <td class="more"><a href="${link}" class="link_more btn">Zobacz</a></td>
                </tr>
            %endfor
    </table>
</%block>