<%inherit file="layout.mako"/>

% for entry in entries:
<div class="blog-post">
  <h2 class="blog-post-title">
  	<a href="${request.route_url('blog', id=entry.id, slug=entry.slug)}">${entry.title}</a>
  </h2>
  <p class="blog-post-meta">Created <strong title="${entry.created}">${entry.created_in_words}</strong> ago by ${entry.author.name}</p>
  ${entry.body | n}
</div>
% endfor

<%namespace file="pagination.mako" import="renderer_pagination"/>
% if pagination:
  ${renderer_pagination(pagination)}
% endif
