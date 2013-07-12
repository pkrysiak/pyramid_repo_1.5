
<%inherit file="base.mako"/>

<%block name = "content">
    <table cellpadding="0" celllspacing="0" border="0" class="list">
            %for uid, name, all_link, all_price, nok_link, nok_price, quantity in search_list:
                <tr>
                    <td class="thumb"><!-- <img src="http://image.ceneo.pl/data/products/19719012/f-asus-x501a-xx145h.jpg" alt="img_demo"/> --></td>
                    <td class="name_list">${name}</td>
                    <td class="price_list"><img src="${request.static_url('pyramid_app:static/img/all.jpg')}"/></td>
                    <td class="price_list">${all_price} zł</td>
                    <td class="price_list"><img src="${request.static_url('pyramid_app:static/img/nok.jpg')}"/></td>
                    <td class="price_list">${nok_price} zł</td>
                    <td class="more">
                              <a href="${all_link}" class="link_more btn">Zobacz Allegro</a>
                              <a href="${nok_link}" class="link_more btn">Zobacz Nokaut</a>
                    </td>
                </tr>
            %endfor
    </table>
</%block>