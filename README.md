{% extends "layout.html" %}

{% block title %} Daniel and Amy's Art Website {% endblock %}

{% block main %}

<body>
<h1>How would you like to browse the museum today?</h1>
<p>Brought to you by my.Tour</p>

<form action="/curateexplore" method="post">
<div>
<button type="submit" name="action" class="button" value="curate">Get Help from a Curator!</button>
</div>
</form>
<form action="/realcustom" method="post">
<div>
<button type="submit" name ="action" class="button" value="custom">Design Your Own Tour!</button>
<input name="customround" type="hidden" value="first">
</div>
</form>

</body>
{% endblock %}

