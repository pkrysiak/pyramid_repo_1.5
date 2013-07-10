
<%inherit file="base.mako"/>

<%block name = "content">
    <div class="outer">
        <div class="main_box">
            <div class="gimme_some_space">
                <p class="name_list">History:</p>
                <ul class="i_want_some_space_too">
                    % for search in search_list:
                        <li> - ${search} </li>
                    % endfor
                </ul>

            </div>
        </div>
    </div>
</%block>