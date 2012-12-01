<h1>Server Path Root:</h1>
<p>{{ path_root }}</p>

<h1>Moments</h1>
<p>To browse a journal, a journal server must be loaded already.  Pose will connect to it using a RemoteJournal object.  The standard entry point is: </p>

<a href="/cloud/">/cloud</a>

<p>you could also supply a specific cloud: "/cloud/cloud_name"<br>
this will look in the cloud file relative to your path root</p>


<p>other Journal related options include:<br>
<ul>
<li>/cloud/ignore/[cloud_name]</li>
<li>/range/[start]/[end] (see links in header)</li>
<li>/tagged/[tag name]</li>
</ul>
</p>

<h1>Files</h1>

<p>It is also possible to browse files with pose, and customize the views as the situation requires:</p>

<ul>
<li><a href="/path/">/path/[relative path]</a></li>
<li><a href="/series/">/series/[relative path]</a></li>
<li><a href="/sort/">/sort/[moment log path]</a></li>
</ul>


<a href=""></a>
<p></p>
<blockquote></blockquote>

%rebase layout title="Pose Browser", active="home"
