<%inherit file="layout.mako"/>

<div class="blog-post">
  <h2 class="blog-post-title" style="margin-bottom: 20px">Blog Archive for ${fullname}</h2>
  <ul>
  % for entry in entries:
  	<li><a href="${request.route_url('blog', id=entry.id, slug=entry.slug)}">${entry.title}</a><span class="text-muted">, written on ${entry.created.strftime("%B %d, %Y")}</span></li>
  % endfor
  </ul>
</div>