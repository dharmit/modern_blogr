<%def name="renderer_pagination(pagination)">
  <ul class="pager">
  % if pagination.has_prev:
    % if pagination.page == 2:
      <li><a href="${request.route_url('home')}">
    % else:
      <li><a href="${request.route_url('home:page', page=pagination.page - 1)}">
    % endif
  % else:
    <li class="disabled"><a href="#">
  % endif
  Previous</a></li>

  % if pagination.has_next:
    <li><a href="${request.route_url('home:page', page=pagination.page + 1)}">
  % else:
    <li class="disabled"><a href="#">
  % endif
  Next</a></li>
  </ul>
</%def>