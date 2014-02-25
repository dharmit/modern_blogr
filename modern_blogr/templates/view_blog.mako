<%inherit file="layout.mako"/>

<div class="blog-post">
  <h2 class="blog-post-title">${entry.title}</h2>
  <p class="blog-post-meta">
    Created <strong title="${entry.created}">${entry.created_in_words}</strong> ago by ${entry.author.name}
  </p>
  ${entry.body | n}
  <hr>
  Tags: 
  % for tag in entry.tags:
    <span class="label label-default">${tag.name}</span>
  % endfor
</div>

% if logged_in == entry.author.name:
  <div style="margin-bottom: 50px;">
    <a href="${request.route_url('blog_action', action='edit', _query=(('id', entry.id),))}" class="btn btn-default" role="button">Edit</a>
  </div>
% endif
