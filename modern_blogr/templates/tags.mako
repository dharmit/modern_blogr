<%inherit file="layout.mako"/>

<div class="blog-post">
  <h2 class="blog-post-title" style="margin-bottom: 20px">Tags</h2>
  <ul class="list-inline">
  % for tag in tags:
    <li><a href="${request.route_url('tag', tag_name=tag[0])}" style="font-size: ${tag[2]}px">${tag[0]}</a>
  % endfor
  </ul>
</div>
