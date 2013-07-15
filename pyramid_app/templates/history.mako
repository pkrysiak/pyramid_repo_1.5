
<%inherit file="base.mako"/>

<%block name = "content">
    <table cellpadding="0" celllspacing="0" border="0" class="list">
            %for hist in user_hist:
                <tr>
                    <td class="thumb"><!-- <img src="http://image.ceneo.pl/data/products/19719012/f-asus-x501a-xx145h.jpg" alt="img_demo"/> --></td>
                    <td class="name_list">${hist.search_content}</td>
                    <td class="price_list"><img src="${request.static_url('pyramid_app:static/img/all.jpg')}"/></td>
                    <td class="price_list">${hist.all_price} zł</td>
                    <td class="price_list"><img src="${request.static_url('pyramid_app:static/img/nok.jpg')}"/></td>
                    <td class="price_list">${hist.nok_price} zł</td>
                    <td class="more">
                              <a href="${hist.all_link}" class="link_more btn">Zobacz Allegro</a>
                              <a href="${hist.nok_link}" class="link_more btn">Zobacz Nokaut</a>
                    </td>
                </tr>
            %endfor
    </table>
</%block>