<script>
    import {url} from '../../static/site_url.js';
    let public_token;
    let private_token;
async function Create_team() {
    public_token = get_cookie('public_token');
    alert(public_token);
if (public_token === null) {
    const resp = await fetch(url + 'create/user', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({'platform_id': document.documentElement.clientWidth+' '+document.documentElement.clientHeight,
        'platform_name':'web', 'name':'', 'surname':''})
    });
    const json = await resp.json();
    alert(json['user']['name']);
    public_token = json['user']['public_token'];
    private_token = json['user']['private_token'];
    document.cookie = "public_token=" + escape(public_token) + "; expires=22/22/2022 00:00:00";
    document.cookie = "private_token=" + escape(private_token) + "; expires=22/22/2022 00:00:00";
} else {
    private_token = get_cookie('cookie_private');
}
    const resp = await fetch(url + 'create/team', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({'creator_token':private_token})
    });
    const json = await resp.json();
    alert(json['name']);
}
function get_cookie(cookie_name)
{
  let results = document.cookie.match('(^|;) ?' + cookie_name + '=([^;]*)(;|$)');

  if (results)
    return (unescape(results[2]));
  else
    return null;
}
</script>
<style>
.create_team {
    margin-top: 200px;
}
</style>
<button class="create_team" on:click={Create_team}>Создать команду</button>