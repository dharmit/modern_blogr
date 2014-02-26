<%inherit file="layout.mako"/>

<form action="${request.route_url('blog_action', action=action)}" method="post">
  %if action =='edit':
    ${form.id()}
  %endif
  
  % for error in form.title.errors:
    <div class="error">${error}</div>
  % endfor
  
  <div class="form-group">
  	${form.title.label}
  	${form.title(class_="form-control")}
  </div>
  
  % for error in form.body.errors:
    <div class="error">${error}</div>
  % endfor
  
  <div class="form-group">
  	${form.body.label}
  	${form.body(class_="form-control")}
  </div>
  
  % for error in form.tags.errors:
    <div class="error">${error}</div>
  % endfor
  
  <div class="form-group">
  	${form.tags.label}
  	${form.tags(class_="form-control")}
  </div>
  
  <div style="margin-bottom: 50px;">
    <button class="btn btn-primary" type="submit" value="Submit">Publish</button>
  </div>
</form>

<style type="text/css">
.error{
    font-weight: bold;
    color: red;
}
</style>