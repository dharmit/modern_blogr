<%inherit file="layout.mako"/>

<form class="form-inline" role="form" accept-charset="UTF-8" action="${url}" method="post">
  <input type="hidden" name="came_from" value="${came_from}">
  <div class="form-group">
    <label class="sr-only" for="login">Login</label>
    <input type="text" class="form-control" id="login" name="login" placeholder="Login">
  </div>
  <div class="form-group">
    <label class="sr-only" for="password">Password</label>
    <input type="password" class="form-control" id="password" name="password" placeholder="Password">
  </div>
  <div class="checkbox">
    <label>
      <input type="checkbox"> Remember me
    </label>
  </div>
  <button type="submit" class="btn btn-primary" name="form.submitted">Sign in</button>
</form>
